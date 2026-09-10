import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from models import Profile


def uid():
    return uuid4().hex


def now():
    return datetime.now(timezone.utc).isoformat()


def encode(value):
    return json.dumps(value, ensure_ascii=False)


class Store:
    """Short SQLite transactions; network calls always happen outside them."""

    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.executescript("""
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY, data TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, data TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS topics (
                    id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id), data TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS topics_session ON topics(session_id);
            """)
            db.execute("INSERT OR IGNORE INTO settings VALUES (1, ?)", (encode(Profile().model_dump()),))

    @contextmanager
    def connection(self):
        with sqlite3.connect(self.path, timeout=10) as db:
            db.execute("PRAGMA foreign_keys=ON")
            yield db

    def profile(self):
        with self.connection() as db:
            return json.loads(db.execute("SELECT data FROM settings WHERE id=1").fetchone()[0])

    def save_profile(self, profile):
        with self.connection() as db:
            db.execute("UPDATE settings SET data=? WHERE id=1", (encode(profile),))
        return profile

    def create_session(self):
        session = dict(id=uid(), title="新的选题对话", created_at=now(), updated_at=now(), messages=[
            dict(id=uid(), role="assistant", content="最近在工作、学习或生活中，有哪件事让你觉得费时、困惑，或者想分享给同龄人？", created_at=now())
        ], batch=0, notice="")
        self.save_session(session)
        return session

    def save_session(self, session):
        session["updated_at"] = now()
        with self.connection() as db:
            db.execute("INSERT INTO sessions VALUES (?,?) ON CONFLICT(id) DO UPDATE SET data=excluded.data", (session["id"], encode(session)))

    def session(self, sid):
        with self.connection() as db:
            row = db.execute("SELECT data FROM sessions WHERE id=?", (sid,)).fetchone()
        return json.loads(row[0]) if row else None

    def sessions(self):
        with self.connection() as db:
            rows = [json.loads(r[0]) for r in db.execute("SELECT data FROM sessions")]
        return sorted(rows, key=lambda s: s["updated_at"], reverse=True)

    def topics(self, sid=None):
        with self.connection() as db:
            rows = db.execute("SELECT data FROM topics WHERE session_id=?", (sid,)) if sid else db.execute("SELECT data FROM topics")
            return [json.loads(r[0]) for r in rows]

    def topic(self, tid):
        with self.connection() as db:
            row = db.execute("SELECT data FROM topics WHERE id=?", (tid,)).fetchone()
        return json.loads(row[0]) if row else None

    def save_topic(self, topic):
        with self.connection() as db:
            db.execute("UPDATE topics SET data=? WHERE id=?", (encode(topic), topic["id"]))
        return topic

    def save_batch(self, session, topics):
        session["updated_at"] = now()
        with self.connection() as db:
            for topic in topics:
                db.execute("INSERT INTO topics VALUES (?,?,?)", (topic["id"], session["id"], encode(topic)))
            db.execute("UPDATE sessions SET data=? WHERE id=?", (encode(session), session["id"]))
