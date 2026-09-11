"""Evidence-aware generation and deterministic SOP; no HTTP concerns here."""
from copy import deepcopy

from fastapi import HTTPException
from pydantic import ValidationError

from provider import ProviderError
from store import now, uid
from studio_models import Document, Draft, Section
from studio_store import public_artifact


TEMPLATES = {
    '图文': ['实操教程', '清单总结', '对比测评', '经历复盘'],
    '口播': ['问题引入', '观点展开', '案例说明', '行动建议'],
    '录屏教程': ['完整操作演示', '常见问题排查'],
    '生活记录': ['行动与变化', '一天的记录'],
    '混合视频': ['生活引入＋口播＋录屏'],
}


def checked_generate(ai, kind, context, schema):
    try:
        return schema.model_validate(ai.generate('studio.' + kind, context, schema.model_json_schema())).model_dump(mode='json')
    except (ValidationError, ValueError, TypeError):
        raise ProviderError('invalid_output', '生成结果格式不完整，已有稿件已保留，请重试。') from None


def artifact_record(db, kind, data, context, parent=None, work_id=None, variant_id=None):
    previous = [a for a in db.all('artifact') if a['kind'] == kind and a.get('parent_id') == parent]
    return dict(id=uid(), kind=kind, parent_id=parent, work_id=work_id, variant_id=variant_id,
                version=len(previous) + 1, created_at=now(), confirmed=False, data=data, context=context)


def work_context(db, wid, body):
    work = db.get('work', wid)
    variant = db.get('variant', body['variant_id']) if body.get('variant_id') else None
    if variant and variant['work_id'] != wid:
        raise HTTPException(422, '内容版本不属于这份作品。')
    source = db.get('artifact', body['source_id']) if body.get('source_id') else None
    if source and source.get('work_id') != wid:
        raise HTTPException(422, '引用稿件不属于这份作品。')
    materials = [{k: v for k, v in db.get('material', mid).items() if k not in {'images'}} for mid in work['material_ids']]
    briefs = [a for a in db.all('artifact', wid) if a['kind'] == 'brief']
    brief = next((a for a in reversed(briefs) if a['confirmed']), briefs[-1] if briefs else None)
    return dict(work=work, profile=work['profile_snapshot'], materials=materials,
                selected_topic=db.legacy.topic(work['topic_id']) if work.get('topic_id') else None,
                brief=public_artifact(brief) if brief else None, variant=variant,
                source=public_artifact(source) if source else None, settings=body,
                publications=db.all('publication', variant['id']) if variant else [])


def generate_artifact(db, ai, wid, body):
    context = work_context(db, wid, body)
    kind, variant, source = body['kind'], context['variant'], context['source']
    if kind in {'draft', 'revise', 'package', 'review'} and not variant:
        raise HTTPException(422, '请先选择图文或视频版本。')
    if kind in {'revise', 'package'}:
        if not source or source['kind'] != 'draft' or source['variant_id'] != variant['id']:
            raise HTTPException(422, '请选择该内容版本的一份稿件。')
    if kind == 'review' and not context['publications']:
        raise HTTPException(422, '请先登记发布信息；指标可以留空。')
    if kind == 'review':
        context['groups'] = period_groups(db, '0001-01-01', '9999-12-31', variant['id'])
    if kind == 'revise':
        sections = source['data'].get('sections', [])
        index = body.get('section_index')
        if index is None or not 0 <= index < len(sections):
            raise HTTPException(422, '请选择一个有效段落；纯文本稿件可手动修改并保存新版本。')
        if not body['instruction'].strip():
            raise HTTPException(422, '请说明这一段要如何修改。')
        context['selected_section'] = sections[index]
        replacement = checked_generate(ai, kind, context, Section)
        data = deepcopy(source['data'])
        data['sections'][index] = replacement
        kind = 'draft'
    else:
        data = checked_generate(ai, kind, context, Draft if kind == 'draft' else Document)
        if kind == 'draft' and variant['form'] == '图文' and len(data['sections']) != body['page_count']:
            raise ProviderError('invalid_output', '生成页数与设定不一致，原稿已保留，请重试。')
        if kind == 'draft' and variant['form'] != '图文':
            total_seconds = sum(s['seconds'] for s in data['sections'])
            if abs(total_seconds - body['duration_seconds']) > max(3, body['duration_seconds'] * .1):
                raise ProviderError('invalid_output', '脚本预计时长偏离目标超过10%，原稿已保留，请重试或调整目标。')
    parent = variant['id'] if variant and kind != 'brief' else wid
    a = artifact_record(db, kind, data, context, parent, wid, variant['id'] if parent != wid else None)
    records = [('artifact', a, parent)]
    work = context['work']
    work['updated_at'] = now()
    records.append(('work', work, None))
    return records, a


def sop_tasks(db, wid, variant):
    vid = variant['id']
    existing = db.all('task', vid)
    if existing:
        return [], existing
    middle = {
        '图文': ['逐页设计与配图', '排版与阅读检查'],
        '口播': ['口播排练与拍摄', '剪辑与字幕检查'],
        '录屏教程': ['脱敏与逐步录屏', '配音、剪辑与操作检查'],
        '生活记录': ['生活镜头与同期声采集', '旁白、剪辑与故事检查'],
        '混合视频': ['拍摄生活片段、口播与录屏', '转场、剪辑与字幕检查'],
    }[variant['form']]
    titles = ['确认核心问题与定位', '补齐亲测素材与来源', '策划与初稿', '核实观点并确认稿件', *middle, '整理标题封面与发布包', '手动发布并登记数据', '观察数据与复盘']
    proportions = [.05, .15, .2, .1, .2, .15, .05, .05, .05]
    budget = db.get('work', wid)['profile_snapshot']['time_budget_hours']
    tasks = [dict(id=uid(), work_id=wid, variant_id=vid, title=title, done=False, due_date=None,
                  estimated_hours=round(budget * fraction, 2), actual_hours=None, created_at=now()) for title, fraction in zip(titles, proportions)]
    return [('task', t, vid) for t in tasks], tasks


def period_groups(db, start, end, variant_id=None):
    groups = {}
    for publication in db.all('publication'):
        if variant_id and publication['variant_id'] != variant_id:
            continue
        if not start <= publication['published_at'] <= end:
            continue
        variant = db.get('variant', publication['variant_id'])
        key = (publication['platform'], variant['form'], publication['observation_days'])
        groups.setdefault(key, []).append(publication)
    result = []
    for (platform, form, days), records in groups.items():
        metric_names = ['views', 'likes', 'comments', 'saves', 'completion_rate']
        metrics = {}
        for name in metric_names:
            values = [p['metrics'][name] for p in records if p['metrics'].get(name) is not None]
            metrics[name] = dict(available_count=len(values), mean=sum(values) / len(values) if values else None)
        result.append(dict(platform=platform, form=form, observation_days=days, sample_size=len({p['variant_id'] for p in records}),
                           metrics=metrics, publications=records, note='仅描述现有样本，差异不等于因果；小样本只提出待验证假设。'))
    return result
