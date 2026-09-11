"""Local-only HTTP interface for the eight creation helpers."""
from datetime import date, timedelta
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, Response

from models import Profile
from store import encode, now, uid
from studio_exports import markdown, storyboard, task_csv
from studio_models import (
    ArtifactInput, ConfirmInput, GenerateInput, IdeaInput, MaterialInput, PeriodInput,
    PositioningInput, PositioningOutput, PublicationInput, RequestInput, ScheduleInput,
    SopInput, TaskPatch, VariantInput, VariantPatch, WorkInput, WorkUpdate, Document,
)
from studio_service import TEMPLATES, artifact_record, checked_generate, generate_artifact, period_groups, sop_tasks, work_context
from studio_store import StudioStore


def install_studio(app, legacy, ai, writing):
    db = StudioStore(legacy)
    app.state.studio = db
    router = APIRouter(prefix='/api/studio')

    def perform(scope, model, action):
        body = model.model_dump(mode='json')
        if not body.get('request_id'):
            raise HTTPException(422, '缺少操作编号，请重新发起操作。')
        with writing():
            prior = db.prior(scope, body)
            if prior is not None:
                return prior
            records, result = action(body)
            return db.commit(records, scope, body, result)

    def check_materials(ids):
        for mid in ids:
            db.get('material', mid)

    def check_variant(wid, vid):
        db.get('work', wid)
        v = db.get('variant', vid)
        if v['work_id'] != wid:
            raise HTTPException(422, '内容版本不属于这份作品。')
        return v

    @router.get('/bootstrap')
    def bootstrap():
        return dict(profile=db.profile(), profile_versions=db.all('profile'),
                    materials=[db.material(m['id']) for m in db.all('material')], works=db.works(),
                    reviews=reviews(), weekly=db.weekly(), templates=TEMPLATES)

    @router.put('/profile')
    def save_profile(body: Profile):
        with writing():
            return db.save_profile(body.model_dump())

    @router.get('/positioning')
    def positioning_history():
        return [a for a in db.all('artifact') if a['kind'] == 'positioning']

    @router.post('/positioning')
    def positioning(body: PositioningInput):
        def action(data):
            context = dict(profile=db.profile(), interview=data['interview'])
            result = checked_generate(ai, 'positioning', context, PositioningOutput)
            artifact = artifact_record(db, 'positioning', result, context)
            return [('artifact', artifact, None)], artifact
        return perform('positioning', body, action)

    @router.get('/materials')
    def materials():
        return [db.material(m['id']) for m in db.all('material')]

    @router.post('/materials')
    def create_material(body: MaterialInput):
        with writing():
            m = dict(body.model_dump(), id=uid(), created_at=now(), updated_at=now(), images=[])
            return db.save('material', m)

    @router.put('/materials/{mid}')
    def update_material(mid: str, body: MaterialInput):
        with writing():
            m = db.get('material', mid)
            m.update(body.model_dump(), updated_at=now())
            return db.save('material', m)

    @router.post('/materials/{mid}/analyze')
    def analyze_material(mid: str, body: RequestInput):
        def action(data):
            m = db.get('material', mid)
            context = dict(material={k: v for k, v in m.items() if k != 'images'}, profile=db.profile())
            output = checked_generate(ai, 'case', context, Document)
            a = artifact_record(db, 'case', output, context, mid)
            return [('artifact', a, mid)], a
        return perform('case:' + mid, body, action)

    @router.post('/materials/{mid}/image')
    async def upload_image(mid: str, request: Request):
        db.get('material', mid)
        mime = request.headers.get('content-type', '').split(';')[0]
        extensions = {'image/png': '.png', 'image/jpeg': '.jpg', 'image/webp': '.webp'}
        if mime not in extensions:
            raise HTTPException(422, '仅支持 PNG、JPEG 或 WebP 图片。')
        payload = bytearray()
        async for chunk in request.stream():
            payload.extend(chunk)
            if len(payload) > 8 * 1024 * 1024:
                raise HTTPException(413, '图片请控制在 8 MB 以内。')
        valid = ((mime == 'image/png' and payload.startswith(b'\x89PNG\r\n\x1a\n')) or
                 (mime == 'image/jpeg' and payload.startswith(b'\xff\xd8\xff')) or
                 (mime == 'image/webp' and payload.startswith(b'RIFF') and payload[8:12] == b'WEBP'))
        if not valid:
            raise HTTPException(422, '图片内容与格式不符，请选择图片文件。')
        with writing():
            m = db.get('material', mid)
            image_id = uid()
            filename = image_id + extensions[mime]
            directory = db.path.parent / 'studio-images'
            directory.mkdir(exist_ok=True)
            path = directory / filename
            path.write_bytes(payload)
            record = dict(id=image_id, material_id=mid, name=filename, mime=mime, url='/api/studio/images/' + image_id)
            m['images'].append({k: record[k] for k in ('id', 'url', 'name')})
            m['updated_at'] = now()
            try:
                with legacy.connection() as conn:
                    db._put(conn, 'image', record, mid)
                    db._put(conn, 'material', m)
            except Exception:
                path.unlink(missing_ok=True)
                raise
            return m

    @router.get('/images/{image_id}')
    def image(image_id: str):
        record = db.get('image', image_id)
        path = db.path.parent / 'studio-images' / record['name']
        if not path.is_file():
            raise HTTPException(404, '图片文件不存在，请恢复备份中的 studio-images 文件夹。')
        return FileResponse(path, media_type=record['mime'])

    @router.get('/works')
    def works():
        return db.works()

    @router.post('/works')
    def create_work(body: WorkInput):
        def action(data):
            check_materials(data['material_ids'])
            if data['topic_id'] and not legacy.topic(data['topic_id']):
                raise HTTPException(404, '没有找到这个选题。')
            w = dict(id=uid(), title=data['title'], topic_id=data['topic_id'], material_ids=list(dict.fromkeys(data['material_ids'])),
                     profile_snapshot=db.profile(), created_at=now(), updated_at=now())
            return [('work', w, None)], dict(w, artifacts=[], variants=[], tasks=[])
        return perform('works', body, action)

    @router.get('/works/{wid}')
    def get_work(wid: str):
        return db.work(wid)

    @router.put('/works/{wid}')
    def update_work(wid: str, body: WorkUpdate):
        with writing():
            w = db.get('work', wid)
            check_materials(body.material_ids)
            w.update(body.model_dump(), updated_at=now())
            db.save('work', w)
            return db.work(wid)

    @router.post('/works/{wid}/variants')
    def create_variant(wid: str, body: VariantInput):
        def action(data):
            db.get('work', wid)
            v = dict(id=uid(), work_id=wid, form=data['form'], platform=data['platform'], status='待策划', created_at=now())
            return [('variant', v, wid)], dict(v, artifacts=[], publications=[])
        return perform('variants:' + wid, body, action)

    @router.patch('/variants/{vid}')
    def update_variant(vid: str, body: VariantPatch):
        with writing():
            v = db.get('variant', vid)
            v.update(body.model_dump(exclude_none=True))
            db.save('variant', v, v['work_id'])
            return db.variant(vid)

    @router.post('/works/{wid}/generate')
    def generate(wid: str, body: GenerateInput):
        return perform('generate:' + wid, body, lambda data: generate_artifact(db, ai, wid, data))

    @router.post('/works/{wid}/artifacts')
    def manual_artifact(wid: str, body: ArtifactInput):
        def action(data):
            context = work_context(db, wid, data)
            variant = context['variant']
            if data['kind'] in {'draft', 'package', 'review'} and not variant:
                raise HTTPException(422, '请先选择内容版本。')
            if context['source'] and context['source']['kind'] != data['kind']:
                raise HTTPException(422, '新版本与源稿件的类型不一致。')
            if context['source'] and context['source'].get('variant_id') != data['variant_id']:
                raise HTTPException(422, '请在原稿所属内容版本保存修改。')
            parent = variant['id'] if variant and data['kind'] != 'brief' else wid
            a = artifact_record(db, data['kind'], data['data'], context, parent, wid, variant['id'] if parent != wid else None)
            return [('artifact', a, parent)], a
        return perform('manual:' + wid, body, action)

    @router.patch('/artifacts/{aid}')
    def confirm_artifact(aid: str, body: ConfirmInput):
        with writing():
            a = db.get('artifact', aid)
            a['confirmed'] = body.confirmed
            return db.save('artifact', a, a.get('parent_id'))

    @router.get('/artifacts/{aid}/export')
    def export_artifact(aid: str, format: str = 'md'):
        a = db.get('artifact', aid)
        if format not in {'md', 'csv'}:
            raise HTTPException(422, '请选择 Markdown 或 CSV。')
        if format == 'csv' and 'sections' not in a['data']:
            raise HTTPException(422, '只有包含分镜或逐页结构的稿件支持 CSV 导出。')
        content = storyboard(a) if format == 'csv' else markdown(a)
        return Response(content, media_type='text/csv' if format == 'csv' else 'text/markdown',
                        headers={'Content-Disposition': f'attachment; filename="{a["kind"]}-{aid[:8]}-v{a["version"]}.{format}"'})

    @router.post('/works/{wid}/sop')
    def sop(wid: str, body: SopInput):
        return perform('sop:' + wid, body, lambda data: sop_tasks(db, wid, check_variant(wid, data['variant_id'])))

    @router.patch('/tasks/{tid}')
    def update_task(tid: str, body: TaskPatch):
        with writing():
            t = db.get('task', tid)
            data = body.model_dump(mode='json', exclude_unset=True)
            if any(k in data and data[k] is None for k in ('done', 'estimated_hours')):
                raise HTTPException(422, '完成状态和预计时间不能留空。')
            t.update(data)
            return db.save('task', t, t['variant_id'])

    @router.get('/works/{wid}/tasks/export')
    def export_tasks(wid: str):
        return Response(task_csv(db.work(wid)['tasks']), media_type='text/csv', headers={'Content-Disposition': 'attachment; filename="creation-tasks.csv"'})

    @router.get('/weekly')
    def weekly(week_start: date | None = None):
        return db.weekly(week_start.isoformat() if week_start else None)

    @router.post('/schedule')
    def schedule(body: ScheduleInput):
        with writing():
            week = db.weekly(body.week_start)
            capacity = max(0, week['budget_hours'] - week['planned_hours'])
            day_hours = {i: 0.0 for i in range(7)}
            start = date.fromisoformat(body.week_start)
            for t in week['tasks']:
                day_hours[(date.fromisoformat(t['due_date']) - start).days] += t['estimated_hours']
            earliest = {}
            blocked = set()
            all_tasks = db.all('task')
            unscheduled_ids = {t['id'] for t in week['unscheduled']}
            with legacy.connection() as conn:
                for index, task in enumerate(all_tasks):
                    vid = task['variant_id']
                    if task['done']:
                        continue
                    if task['due_date']:
                        earliest[vid] = max(earliest.get(vid, 0), (date.fromisoformat(task['due_date']) - start).days)
                        continue
                    if task['id'] not in unscheduled_ids or vid in blocked:
                        continue
                    later_dates = [(date.fromisoformat(t['due_date']) - start).days for t in all_tasks[index + 1:]
                                   if t['variant_id'] == vid and not t['done'] and t['due_date']]
                    last_day = min([6, *later_dates])
                    days = list(range(max(0, earliest.get(vid, 0)), last_day + 1))
                    if task['estimated_hours'] <= capacity + 1e-9 and days:
                        # Keep SOP order while spreading work inside the weekly budget.
                        preferred = [d for d in days if day_hours[d] + task['estimated_hours'] <= week['budget_hours'] / 7]
                        day = preferred[0] if preferred else min(days, key=day_hours.get)
                        task['due_date'] = (start + timedelta(days=day)).isoformat()
                        capacity -= task['estimated_hours']
                        day_hours[day] += task['estimated_hours']
                        earliest[vid] = day
                        db._put(conn, 'task', task, task['variant_id'])
                    else:
                        blocked.add(vid)
            return db.weekly(body.week_start)

    @router.post('/variants/{vid}/publications')
    def create_publication(vid: str, body: PublicationInput):
        def action(data):
            v = db.get('variant', vid)
            p = {k: value for k, value in data.items() if k != 'request_id'}
            p.update(id=uid(), variant_id=vid, work_id=v['work_id'], created_at=now(), updated_at=now())
            v['status'] = '已发布'
            return [('publication', p, vid), ('variant', v, v['work_id'])], p
        return perform('publication:' + vid, body, action)

    @router.put('/publications/{pid}')
    def update_publication(pid: str, body: PublicationInput):
        with writing():
            p = db.get('publication', pid)
            p.update(body.model_dump(mode='json', exclude={'request_id'}), updated_at=now())
            return db.save('publication', p, p['variant_id'])

    @router.get('/reviews')
    def reviews():
        return [a for a in db.all('artifact') if a['kind'] in {'review', 'period_review'}]

    @router.post('/reviews/period')
    def period_review(body: PeriodInput):
        def action(data):
            groups = period_groups(db, data['start_date'], data['end_date'])
            if not groups:
                raise HTTPException(422, '这个日期范围还没有发布记录，请先登记。')
            context = dict(profile=db.profile(), start_date=data['start_date'], end_date=data['end_date'], groups=groups)
            output = checked_generate(ai, 'period_review', context, Document)
            a = artifact_record(db, 'period_review', output, context)
            return [('artifact', a, None)], a
        return perform('period-review', body, action)

    @router.post('/reviews/{aid}/ideas')
    def adopt_idea(aid: str, body: IdeaInput):
        # Atomic across legacy topic tables and studio idempotency receipt.
        with writing():
            data = body.model_dump()
            prior = db.prior('idea:' + aid, data)
            if prior is not None:
                return prior
            a = db.get('artifact', aid)
            if a['kind'] not in {'review', 'period_review'}:
                raise HTTPException(422, '请选择一条复盘建议。')
            sid, tid = uid(), uid()
            session = dict(id=sid, title='复盘延伸：' + data['title'][:30], created_at=now(), updated_at=now(), batch=1, notice='',
                           messages=[dict(id=uid(), role='assistant', content='这条选题来自你采纳的复盘建议，结论仍待验证。', created_at=now())])
            topic = dict(id=tid, session_id=sid, batch=1, title=data['title'], category=next(iter(db.profile()['weights'])),
                         pain_point='由创作复盘提出的新问题', angle=data['title'], reason='用户采纳的下一轮实验',
                         estimated_hours=db.profile()['time_budget_hours'], to_test=['记录新一轮实际结果再比较'], missing_info=['补充本次实验素材'],
                         external_claims=[], platforms=[db.profile()['primary_platform']], favorite=True, status='待创作', feedback='', feedback_note='',
                         plan=None, sources=[], verification='构思，待亲测', created_at=now(), review_id=aid)
            with legacy.connection() as conn:
                conn.execute('INSERT INTO sessions VALUES (?,?)', (sid, encode(session)))
                conn.execute('INSERT INTO topics VALUES (?,?,?)', (tid, sid, encode(topic)))
                conn.execute('INSERT INTO studio_requests VALUES (?,?,?,?)', ('idea:' + aid, data['request_id'], db.fingerprint(data), encode(topic)))
            return topic

    app.include_router(router)
    return db
