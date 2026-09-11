import json

import httpx
import pytest
from pydantic import ValidationError

from models import Profile
from provider import DeepSeekProvider


@pytest.mark.parametrize("kind", ["positioning", "case", "brief", "draft", "revise", "package", "review", "period_review"])
def test_studio_generation_dispatches_without_legacy_body_prohibition(kind):
    captured = []
    schema = {"type": "object", "properties": {"heading" if kind == "revise" else "markdown": {"type": "string"}}}
    context = {"form": "口播", "duration_seconds": 180, "page_count": 6}

    def handler(request):
        captured.append(json.loads(request.content))
        return httpx.Response(200, json={"status": "completed", "output": [{"type": "message", "content": [{"type": "output_text", "text": '{"result":"ok"}'}]}]})

    provider = DeepSeekProvider(api_key="test", transport=httpx.MockTransport(handler))
    assert provider.generate(f"studio.{kind}", context, schema) == {"result": "ok"}
    payload = captured[0]
    assert "不生成完整正文、脚本" not in payload["instructions"]
    assert "只返回JSON" in payload["instructions"]
    assert json.loads(payload["input"]) == {"context": context, "required_json_schema": schema}
    if kind == "revise":
        assert "Section" in payload["instructions"]
        assert "只返回一个" in payload["instructions"]
    if kind in {"review", "period_review"}:
        for group in ["平台", "形式", "观察", "null", "假设"]:
            assert group in payload["instructions"]


def test_profile_accepts_custom_directions_and_defaults_for_existing_records():
    profile = Profile(weights={"职场": 60, "读书": 40})
    assert profile.weights == {"职场": 60, "读书": 40}
    assert profile.weekly_hours == 8
    assert profile.content_forms == ["图文", "口播", "录屏教程", "生活记录", "混合视频"]
    assert profile.confirmed is False


@pytest.mark.parametrize("weights", [{"   ": 100}, {"方向": -1, "其他": 101}, {"方向": 99}, {}])
def test_profile_rejects_invalid_direction_weights(weights):
    with pytest.raises(ValidationError):
        Profile(weights=weights)


def test_draft_and_section_schema_support_long_scripts_and_enforce_structure():
    from studio_models import Draft, Section
    section = {"heading": "步骤", "text": "正文" * 4000, "visual": "操作画面", "seconds": 90, "subtitle": "字幕", "transition": "切到结果"}
    draft = {"titles": ["实用标题", "问题标题", "经历标题"], "cover": "封面", "intro": "开头", "sections": [section], "closing": "结尾", "publish_text": "发布文案", "missing": []}
    assert len(Draft.model_validate(draft).sections[0].text) == 8000
    for change in [{"titles": ["一个标题"]}, {"sections": []}]:
        with pytest.raises(ValidationError):
            Draft.model_validate({**draft, **change})
    with pytest.raises(ValidationError):
        Section.model_validate({**section, "seconds": -1})


@pytest.mark.parametrize("url", ["javascript:alert(1)", "file:///tmp/a", "https://user:password@example.com", "https://", "https://example.com\\@evil.example", "https://example.com\n/path"])
def test_material_rejects_unsafe_links(url):
    from studio_models import MaterialInput
    with pytest.raises(ValidationError):
        MaterialInput(title="参考", kind="外部参考", text="待核实", verification="未核实", missing=[], url=url)


def test_publication_preserves_unknown_metrics_and_rejects_invalid_values():
    from studio_models import Metrics, PublicationInput
    publication = PublicationInput(platform="B站", published_at="2026-09-11", observation_days=7, url="https://example.com/video", metrics={}, comments_text="", reflection="")
    assert publication.metrics.model_dump() == {"views": None, "likes": None, "comments": None, "saves": None, "completion_rate": None}
    assert publication.model_dump(mode="json")["published_at"] == "2026-09-11"
    for invalid in [{"views": -1}, {"completion_rate": 101}, {"likes": 1.5}]:
        with pytest.raises(ValidationError):
            Metrics(**invalid)


def test_generation_settings_and_date_ranges_are_validated():
    from studio_models import GenerateInput, PeriodInput, TaskPatch
    request = GenerateInput(kind="draft", variant_id="v1", request_id="g1")
    assert request.page_count == 6 and request.duration_seconds == 180
    for invalid in [{"page_count": 31}, {"duration_seconds": 14}, {"section_index": -1}]:
        with pytest.raises(ValidationError):
            GenerateInput(kind="draft", request_id="g1", **invalid)
    with pytest.raises(ValidationError):
        PeriodInput(start_date="2026-09-12", end_date="2026-09-11", request_id="r1")
    with pytest.raises(ValidationError):
        TaskPatch(due_date="2026-02-30")
    assert TaskPatch(due_date=None).model_dump(exclude_unset=True) == {"due_date": None}


@pytest.mark.parametrize("field", ["done", "estimated_hours", "actual_hours"])
def test_task_patch_only_allows_clearing_due_date(field):
    from studio_models import TaskPatch
    with pytest.raises(ValidationError):
        TaskPatch.model_validate({field: None})
