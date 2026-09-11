"""Versioned studio records alongside the original topic tables.

Short transactions only; providers are never called while holding a DB transaction.
"""
import hashlib
import json
import sqlite3
from datetime import date, timedelta

from fastapi import HTTPException

from models import Profile
from store import encode, now, uid


class StudioStore:
    def __init__(self, legacy):
        self.legacy = legacy
        self.path = legacy.path
        self.migrate()

    def migrate(self):
        with self.legacy.connection() as db:
            version = db.execute('PRAGMA user_version').fetchone()[0]
            if version > 1:
                raise RuntimeError('数据库版本高于当前程序，请使用新版程序。')
            if version == 1:
                return
            backup_path = self.path.with_name(self.path.stem + '.pre-studio-1.db')
            if backup_path.exists():
                backup_path = self.path.with_name(self.path.stem + '.pre-studio-1-' + uid()[:8] + '.db')
            temporary = backup_path.with_suffix('.tmp')
            backup = sqlite3.connect(temporary)
            try:
                db.backup(backup)
            finally:
                backup.close()
            temporary.replace(backup_path)
            db.execute('BEGIN IMMEDIATE')
            self._create_schema(db)
            profile = Profile.model_validate(self.legacy.profile()).model_dump()
            profile['confirmed'] = False
            record = dict(profile, id=uid(), version=1, created_at=now())
            self._put(db, 'profile', record)
            db.execute('UPDATE settings SET data=? WHERE id=1', (encode(profile),))
            db.execute('PRAGMA user_version=1')

    @staticmethod
    def _create_schema(db):
        db.execute('CREATE TABLE studio_entities (id TEXT PRIMARY KEY, kind TEXT NOT NULL, parent_id TEXT REFERENCES studio_entities(id), data TEXT NOT NULL)')
        db.execute('CREATE INDEX studio_kind_parent ON studio_entities(kind,parent_id)')
        db.execute('CREATE TABLE studio_requests (scope TEXT NOT NULL, request_id TEXT NOT NULL, fingerprint TEXT NOT NULL, result TEXT NOT NULL, PRIMARY KEY(scope,request_id))')

    @staticmethod
    def _put(db, kind, record, parent=None):
        db.execute('INSERT INTO studio_entities VALUES (?,?,?,?) ON CONFLICT(id) DO UPDATE SET data=excluded.data',
                   (record['id'], kind, parent, encode(record)))

    def all(self, kind, parent=None):
        with self.legacy.connection() as db:
            if parent is None:
                rows = db.execute('SELECT data FROM studio_entities WHERE kind=? ORDER BY rowid', (kind,))
            else:
                rows = db.execute('SELECT data FROM studio_entities WHERE kind=? AND parent_id=? ORDER BY rowid', (kind, parent))
            return [json.loads(row[0]) for row in rows]

    def get(self, kind, rid):
        with self.legacy.connection() as db:
            row = db.execute('SELECT data FROM studio_entities WHERE id=? AND kind=?', (rid, kind)).fetchone()
        if row is None:
            raise HTTPException(404, '没有找到这条记录。')
        return json.loads(row[0])

    def save(self, kind, record, parent=None):
        with self.legacy.connection() as db:
            self._put(db, kind, record, parent)
        return record

    def commit(self, records, scope, body, result):
        """Commit all outputs and the deduplication receipt atomically."""
        with self.legacy.connection() as db:
            for kind, record, parent in records:
                self._put(db, kind, record, parent)
            db.execute('INSERT INTO studio_requests VALUES (?,?,?,?)', (scope, body['request_id'], self.fingerprint(body), encode(result)))
        return result

    @staticmethod
    def fingerprint(body):
        return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

    def prior(self, scope, body):
        with self.legacy.connection() as db:
            row = db.execute('SELECT fingerprint,result FROM studio_requests WHERE scope=? AND request_id=?', (scope, body['request_id'])).fetchone()
        if row:
            if row[0] != self.fingerprint(body):
                raise HTTPException(409, '这次重试的内容已变化，请重新发起操作。')
            return json.loads(row[1])
        return None

    def profile(self):
        return self.all('profile')[-1]

    def save_profile(self, profile):
        record = dict(profile, id=uid(), version=self.profile()['version'] + 1, created_at=now())
        with self.legacy.connection() as db:
            self._put(db, 'profile', record)
            db.execute('UPDATE settings SET data=? WHERE id=1', (encode(profile),))
        return record

    def material(self, mid):
        record = self.get('material', mid)
        record['analyses'] = self.all('artifact', mid)
        return record

    def variant(self, vid):
        record = self.get('variant', vid)
        record['artifacts'] = self.all('artifact', vid)
        record['publications'] = self.all('publication', vid)
        return record

    def work(self, wid):
        record = self.get('work', wid)
        record['artifacts'] = self.all('artifact', wid)
        record['variants'] = [self.variant(v['id']) for v in self.all('variant', wid)]
        record['tasks'] = [t for t in self.all('task') if t['work_id'] == wid]
        return record

    def works(self):
        return [self.work(w['id']) for w in self.all('work')]

    def weekly(self, week_start=None):
        start = date.fromisoformat(week_start) if week_start else date.today() - timedelta(days=date.today().weekday())
        end = start + timedelta(days=7)
        tasks = self.all('task')
        active = {v['id'] for v in self.all('variant') if v['status'] not in {'暂停', '放弃', '已复盘'}}
        tasks = [t for t in tasks if t['variant_id'] in active or t['done']]
        scheduled = [t for t in tasks if t['due_date'] and start <= date.fromisoformat(t['due_date']) < end]
        return dict(week_start=start.isoformat(), budget_hours=self.profile()['weekly_hours'],
                    planned_hours=round(sum(t['estimated_hours'] for t in scheduled), 2),
                    actual_hours=round(sum(t['actual_hours'] or 0 for t in scheduled), 2), tasks=scheduled,
                    unscheduled=[t for t in tasks if not t['due_date'] and not t['done']])


def public_artifact(artifact):
    """Keep source text and IDs, without recursively copying historical contexts."""
    return {k: v for k, v in artifact.items() if k != 'context'}
