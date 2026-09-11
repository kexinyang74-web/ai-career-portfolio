import json
import sqlite3

import pytest
from fastapi.testclient import TestClient

from app import create_app
from provider import ProviderError
from store import Store


class StudioFake:
    configured = True
    search_status = 'not_checked'

    def __init__(self):
        self.calls = []
        self.fail = False
        self.invalid = False

    def generate(self, kind, context, schema):
        self.calls.append((kind, context))
        if self.fail:
            raise ProviderError('timeout', '超时，草稿已保留', 504)
        if self.invalid:
            return {'bad': 'output'}
        section = dict(heading='观察问题', text='我发现整理笔记费时；效果待亲测。', visual='展示脱敏笔记', seconds=30, subtitle='待亲测', transition='切换录屏')
        if kind == 'studio.positioning':
            return {'candidates': [dict(positioning=f'真实记录方向{i}', audience='初学者', pillars=['真实记录'], difference='亲测', voice='自然', boundaries='不编造', columns=['每周实践'], tradeoff='需要素材') for i in range(3)]}
        if kind == 'studio.draft':
            count = context['settings']['page_count'] if context['variant']['form'] == '图文' else 3
            seconds = 0 if context['variant']['form'] == '图文' else context['settings']['duration_seconds'] / count
            return dict(titles=['实用标题', '问题标题', '经历标题'], cover='亲测记录', intro='从一个问题出发', sections=[dict(section, heading=f'第{i+1}段', seconds=seconds) for i in range(count)], closing='试一试', publish_text='分享真实过程', missing=['待补结果截图'])
        if kind == 'studio.revise':
            return dict(section, text='修改后的这一段，仍待亲测。')
        return {'markdown': '# 创作建议\n\n已有材料来自用户；缺少结果，先验证。', 'missing': ['待补亲测结果']}


@pytest.fixture
def studio(tmp_path):
    p = StudioFake()
    path = tmp_path / 'assistant.db'
    with TestClient(create_app(path, p)) as c:
        yield c, p, path


def post(c, path, data):
    r = c.post('/api/studio' + path, json=data)
    assert r.status_code == 200, r.text
    return r.json()


def work(c, key='work'):
    return post(c, '/works', {'title': '我的真实笔记实验', 'request_id': key})


def variant(c, w, form='图文', key='variant'):
    return post(c, f'/works/{w["id"]}/variants', {'form': form, 'platform': '小红书' if form == '图文' else 'B站', 'request_id': key})


def generate(c, w, v, key='draft', **extra):
    return post(c, f'/works/{w["id"]}/generate', dict(kind='draft', variant_id=v['id'], request_id=key, **extra))


def test_bootstrap_migration_preserves_old_and_versions(tmp_path):
    path = tmp_path / 'old.db'
    old = Store(path)
    sid = old.create_session()['id']
    before = old.profile()
    with TestClient(create_app(path, StudioFake())) as c:
        boot = c.get('/api/studio/bootstrap')
        assert boot.status_code == 200
        assert boot.json()['profile']['confirmed'] is False
        assert c.get('/api/profile').json()['positioning'] == before['positioning']
        assert c.get(f'/api/sessions/{sid}').status_code == 200
        assert len(boot.json()['profile_versions']) == 1
    backups = list(tmp_path.glob('*.pre-studio-*.db'))
    assert len(backups) == 1
    with sqlite3.connect(backups[0]) as db:
        assert db.execute('SELECT count(*) FROM sessions').fetchone()[0] == 1
    with TestClient(create_app(path, StudioFake())) as c:
        assert len(c.get('/api/studio/bootstrap').json()['profile_versions']) == 1
    assert len(list(tmp_path.glob('*.pre-studio-*.db'))) == 1


def test_profile_snapshot_and_custom_pillars(studio):
    c, _, _ = studio
    w = work(c)
    profile = c.get('/api/profile').json()
    profile.update(weights={'实践记录': 60, '阅读': 40}, voice='像朋友聊天', confirmed=True)
    r = c.put('/api/studio/profile', json=profile)
    assert r.status_code == 200, r.text
    assert r.json()['version'] == 2
    assert c.get(f'/api/studio/works/{w["id"]}').json()['profile_snapshot']['version'] == 1
    assert work(c, 'next')['profile_snapshot']['voice'] == '像朋友聊天'


def test_idempotent_creation_and_foreign_relations(studio):
    c, _, _ = studio
    w = work(c)
    assert work(c)['id'] == w['id']
    assert c.post('/api/studio/works', json={'title': '不同内容', 'request_id': 'work'}).status_code == 409
    assert c.post('/api/studio/works', json={'title': '不存在选题', 'topic_id': 'missing', 'request_id': 'bad'}).status_code == 404
    assert c.post('/api/studio/works', json={'title': '不存在素材', 'material_ids': ['missing'], 'request_id': 'bad-material'}).status_code == 404
    v = variant(c, w)
    other = work(c, 'other')
    assert c.post(f'/api/studio/works/{other["id"]}/generate', json={'kind': 'draft', 'variant_id': v['id'], 'request_id': 'bad-draft'}).status_code == 422


@pytest.mark.parametrize('form', ['图文', '口播', '录屏教程', '生活记录', '混合视频'])
def test_forms_revision_failure_restart_and_export(studio, form):
    c, p, path = studio
    w = work(c)
    v = variant(c, w, form)
    a = generate(c, w, v)
    assert generate(c, w, v)['id'] == a['id']
    assert len(p.calls) == 1
    assert c.patch(f'/api/studio/artifacts/{a["id"]}', json={'confirmed': True}).status_code == 200
    revised = post(c, f'/works/{w["id"]}/generate', {'kind': 'revise', 'variant_id': v['id'], 'source_id': a['id'], 'section_index': 0, 'instruction': '自然一点', 'request_id': 'revision'})
    assert revised['data']['sections'][0]['text'] != a['data']['sections'][0]['text']
    assert revised['data']['sections'][1:] == a['data']['sections'][1:]
    assert revised['version'] == 2
    assert revised['context']['source']['id'] == a['id']
    p.fail = True
    r = c.post(f'/api/studio/works/{w["id"]}/generate', json={'kind': 'draft', 'variant_id': v['id'], 'request_id': 'retry'})
    assert r.status_code == 504
    p.fail, p.invalid = False, True
    assert c.post(f'/api/studio/works/{w["id"]}/generate', json={'kind': 'draft', 'variant_id': v['id'], 'request_id': 'retry'}).status_code == 502
    with TestClient(create_app(path, p)) as reopened:
        saved = reopened.get(f'/api/studio/works/{w["id"]}').json()
        assert len(saved['variants'][0]['artifacts']) == 2
        assert saved['variants'][0]['artifacts'][0]['confirmed'] is True
        assert reopened.get(f'/api/studio/artifacts/{a["id"]}/export?format=md').status_code == 200
        assert 'visual' not in reopened.get(f'/api/studio/artifacts/{a["id"]}/export?format=csv').text


def test_manual_draft_without_model_and_independent_status(studio):
    c, p, _ = studio
    p.fail = True
    w = work(c)
    a, b = variant(c, w), variant(c, w, '口播', 'v2')
    draft = post(c, f'/works/{w["id"]}/artifacts', {'kind': 'draft', 'variant_id': a['id'], 'data': {'markdown': '这是自己写的稿件', 'missing': []}, 'request_id': 'manual'})
    assert draft['data']['markdown'] == '这是自己写的稿件'
    c.patch(f'/api/studio/variants/{a["id"]}', json={'status': '待发布'})
    saved = c.get(f'/api/studio/works/{w["id"]}').json()
    assert [v['status'] for v in saved['variants']] == ['待发布', '待策划']
    assert not p.calls


def test_material_evidence_snapshot_images_and_case(studio):
    import base64
    c, p, _ = studio
    m = post(c, '/materials', {'title': '亲测', 'kind': '亲身经历', 'text': '只做过一次', 'verification': '用户已亲测'})
    w = post(c, '/works', {'title': '实验', 'material_ids': [m['id']], 'request_id': 'matwork'})
    v = variant(c, w)
    a = generate(c, w, v)
    assert a['context']['materials'][0]['text'] == '只做过一次'
    c.put(f'/api/studio/materials/{m["id"]}', json={'title': '新结果', 'kind': '亲身经历', 'text': '做了两次', 'verification': '用户已亲测'})
    saved = c.get(f'/api/studio/works/{w["id"]}').json()
    assert saved['variants'][0]['artifacts'][0]['context']['materials'][0]['text'] == '只做过一次'
    png = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=')
    r = c.post(f'/api/studio/materials/{m["id"]}/image', content=png, headers={'Content-Type': 'image/png'})
    assert r.status_code == 200, r.text
    assert c.get(r.json()['images'][0]['url']).content == png
    assert c.post(f'/api/studio/materials/{m["id"]}/image', content=b'<svg/>', headers={'Content-Type': 'image/svg+xml'}).status_code == 422
    assert post(c, f'/materials/{m["id"]}/analyze', {'request_id': 'case'})['kind'] == 'case'


def test_sop_schedule_budget_publications_and_reviews(studio):
    c, p, _ = studio
    w = work(c)
    v = variant(c, w)
    tasks = post(c, f'/works/{w["id"]}/sop', {'variant_id': v['id'], 'request_id': 'sop'})
    assert len(tasks) >= 6
    assert post(c, f'/works/{w["id"]}/sop', {'variant_id': v['id'], 'request_id': 'sop2'}) == tasks
    assert c.patch(f'/api/studio/tasks/{tasks[0]["id"]}', json={'actual_hours': 0.5, 'done': True}).status_code == 200
    week = post(c, '/schedule', {'week_start': '2026-09-07'})
    assert week['planned_hours'] <= week['budget_hours']
    assert c.get(f'/api/studio/works/{w["id"]}/tasks/export').status_code == 200
    pub = post(c, f'/variants/{v["id"]}/publications', {'platform': '小红书', 'published_at': '2026-09-10', 'metrics': {'views': 100, 'likes': 5}, 'request_id': 'pub'})
    assert pub['metrics']['saves'] is None
    review = post(c, f'/works/{w["id"]}/generate', {'kind': 'review', 'variant_id': v['id'], 'request_id': 'review'})
    assert p.calls[-1][1]['publications'][0]['metrics']['saves'] is None
    period = post(c, '/reviews/period', {'start_date': '2026-09-01', 'end_date': '2026-09-30', 'request_id': 'period'})
    assert p.calls[-1][1]['groups'][0]['sample_size'] == 1
    idea = post(c, f'/reviews/{review["id"]}/ideas', {'title': '下次验证不同开头', 'request_id': 'idea'})
    assert c.get(f'/api/topics/{idea["id"]}').status_code == 200
    assert idea['verification'] == '构思，待亲测'
    assert len(c.get('/api/studio/reviews').json()) == 2


def test_positioning_is_suggestion_until_explicit_save(studio):
    c, _, _ = studio
    initial = c.get('/api/studio/bootstrap').json()['profile']
    a = post(c, '/positioning', {'interview': '我正在学开发，每周能投入八小时，愿意录屏。', 'request_id': 'position'})
    assert len(a['data']['candidates']) == 3
    assert c.get('/api/studio/bootstrap').json()['profile'] == initial
    assert len(c.get('/api/studio/positioning').json()) == 1


def test_migration_failure_rolls_back_schema_and_profile(tmp_path, monkeypatch):
    from studio_store import StudioStore
    path = tmp_path / 'rollback.db'
    old = Store(path)
    before = old.profile()
    def broken(db):
        db.execute('CREATE TABLE studio_entities (id TEXT)')
        db.execute('UPDATE settings SET data=? WHERE id=1', ('{}',))
        raise RuntimeError('simulated failure')
    monkeypatch.setattr(StudioStore, '_create_schema', staticmethod(broken))
    with pytest.raises(RuntimeError, match='simulated'):
        StudioStore(old)
    assert old.profile() == before
    with sqlite3.connect(path) as db:
        assert db.execute('PRAGMA user_version').fetchone()[0] == 0
        assert not db.execute("SELECT name FROM sqlite_master WHERE name='studio_entities'").fetchall()


def test_period_groups_keep_platform_form_observation_separate(studio):
    c, p, _ = studio
    w = work(c)
    for i, (form, platform, days) in enumerate([('图文', '小红书', 7), ('口播', '小红书', 7), ('图文', 'B站', 7), ('图文', '小红书', 1)]):
        v = variant(c, w, form, f'v{i}')
        post(c, f'/variants/{v["id"]}/publications', {'platform': platform, 'published_at': '2026-09-10', 'observation_days': days, 'metrics': {}, 'request_id': f'p{i}'})
    post(c, '/reviews/period', {'start_date': '2026-09-01', 'end_date': '2026-09-30', 'request_id': 'groups'})
    groups = p.calls[-1][1]['groups']
    assert len(groups) == 4
    assert all(g['metrics']['views']['mean'] is None for g in groups)


def test_schedule_respects_sop_sequence(studio):
    c, _, _ = studio
    w = work(c)
    v = variant(c, w)
    tasks = post(c, f'/works/{w["id"]}/sop', {'variant_id': v['id'], 'request_id': 'sop'})
    post(c, '/schedule', {'week_start': '2026-09-07'})
    saved = c.get(f'/api/studio/works/{w["id"]}').json()['tasks']
    dates = [t['due_date'] for t in saved if t['due_date']]
    assert dates == sorted(dates), '自动安排不得把发布/复盘放到策划前面'


def test_source_foreign_variant_invalid_section_and_csv_formula(studio):
    c, p, _ = studio
    w = work(c)
    a, b = variant(c, w), variant(c, w, '口播', 'b')
    draft = generate(c, w, a)
    r = c.post(f'/api/studio/works/{w["id"]}/generate', json={'kind': 'package', 'variant_id': b['id'], 'source_id': draft['id'], 'request_id': 'bad'})
    assert r.status_code == 422
    r = c.post(f'/api/studio/works/{w["id"]}/generate', json={'kind': 'revise', 'variant_id': a['id'], 'source_id': draft['id'], 'section_index': 99, 'request_id': 'out'})
    assert r.status_code == 422
    assert len(p.calls) == 1
    draft['data']['sections'][0]['text'] = '=HYPERLINK("http://example.com")'
    manual = post(c, f'/works/{w["id"]}/artifacts', {'kind': 'draft', 'variant_id': a['id'], 'data': draft['data'], 'request_id': 'csv'})
    assert "'=HYPERLINK" in c.get(f'/api/studio/artifacts/{manual["id"]}/export?format=csv').text


def test_legacy_profile_save_preserves_extended_values(studio):
    c, _, _ = studio
    initial = c.get('/api/profile').json()
    profile = dict(initial, voice='真实自然', weekly_hours=15, columns=['实验日志'], confirmed=True)
    assert c.put('/api/studio/profile', json=profile).status_code == 200
    legacy_payload = {k: v for k, v in initial.items() if k in {'audience', 'positioning', 'primary_platform', 'secondary_platforms', 'weights', 'time_budget_hours'}}
    legacy_payload['audience'] = '新的读者'
    result = c.put('/api/profile', json=legacy_payload)
    assert result.status_code == 200
    assert result.json()['voice'] == '真实自然'
    assert result.json()['weekly_hours'] == 15
    assert result.json()['confirmed'] is True


def test_migration_retry_takes_fresh_backup(tmp_path, monkeypatch):
    from studio_store import StudioStore
    path = tmp_path / 'fresh.db'
    old = Store(path)
    original = StudioStore._create_schema
    def broken(db):
        raise RuntimeError('migration failed')
    monkeypatch.setattr(StudioStore, '_create_schema', staticmethod(broken))
    with pytest.raises(RuntimeError):
        StudioStore(old)
    old.create_session()
    monkeypatch.setattr(StudioStore, '_create_schema', staticmethod(original))
    StudioStore(old)
    counts = []
    for backup in tmp_path.glob('*.pre-studio-*.db'):
        with sqlite3.connect(backup) as conn:
            counts.append(conn.execute('SELECT count(*) FROM sessions').fetchone()[0])
    assert max(counts) == 1, '重试迁移的备份必须包含这次升级前的最新记录'


def test_video_duration_mismatch_preserves_existing_draft(studio, monkeypatch):
    c, p, _ = studio
    w = work(c)
    v = variant(c, w, '口播')
    generate(c, w, v)
    original = p.generate
    def wrong_duration(kind, context, schema):
        output = original(kind, context, schema)
        for s in output['sections']:
            s['seconds'] = 1
        return output
    monkeypatch.setattr(p, 'generate', wrong_duration)
    result = c.post(f'/api/studio/works/{w["id"]}/generate', json={'kind': 'draft', 'variant_id': v['id'], 'request_id': 'too-short'})
    assert result.status_code == 502
    assert len(c.get(f'/api/studio/works/{w["id"]}').json()['variants'][0]['artifacts']) == 1


def test_schedule_does_not_skip_unfittable_predecessor(studio):
    c, _, _ = studio
    w, w2 = work(c), work(c, 'other')
    v, v2 = variant(c, w), variant(c, w2, key='other-v')
    t = post(c, f'/works/{w["id"]}/sop', {'variant_id': v['id'], 'request_id': 'sop'})
    post(c, f'/works/{w2["id"]}/sop', {'variant_id': v2['id'], 'request_id': 'sop-other'})
    c.patch(f'/api/studio/tasks/{t[0]["id"]}', json={'estimated_hours': 20})
    post(c, '/schedule', {'week_start': '2026-09-07'})
    assert not any(t['due_date'] for t in c.get(f'/api/studio/works/{w["id"]}').json()['tasks'])
    assert any(t['due_date'] for t in c.get(f'/api/studio/works/{w2["id"]}').json()['tasks'])


def test_single_review_groups_multiple_publication_platforms(studio):
    c, p, _ = studio
    w = work(c)
    v = variant(c, w, '口播')
    for i, platform in enumerate(['B站', '视频号']):
        post(c, f'/variants/{v["id"]}/publications', {'platform': platform, 'published_at': '2026-09-10', 'metrics': {'views': i * 100}, 'request_id': f'pub{i}'})
    post(c, f'/works/{w["id"]}/generate', {'kind': 'review', 'variant_id': v['id'], 'request_id': 'review'})
    groups = p.calls[-1][1]['groups']
    assert len(groups) == 2
    assert groups[0]['metrics']['views']['mean'] == 0
    assert groups[0]['metrics']['saves']['mean'] is None
