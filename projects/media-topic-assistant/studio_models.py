"""Validated input and model-output contracts for the local creative studio."""

from datetime import date
from typing import Annotated, Literal, get_args
from urllib.parse import urlsplit

from pydantic import AfterValidator, BeforeValidator, Field, model_validator

from models import StrictModel, Text


Form = Literal["图文", "口播", "录屏教程", "生活记录", "混合视频"]
Status = Literal["待策划", "待补素材", "写稿中", "待制作", "待发布", "已发布", "已复盘", "暂停", "放弃"]
FORMS = get_args(Form)
STATUSES = get_args(Status)
LongText = Annotated[str, Field(max_length=100000)]
RequiredLongText = Annotated[str, Field(min_length=1, max_length=100000)]
Identifier = Annotated[str, Field(min_length=1, max_length=100)]
Hours = Annotated[float, Field(ge=0, allow_inf_nan=False)]


def validate_url(value):
    if not isinstance(value, str):
        raise ValueError("链接必须是文本。")
    if any(ord(char) < 32 or ord(char) == 127 for char in value) or "\\" in value:
        raise ValueError("链接不能包含控制字符或反斜杠。")
    value = value.strip()
    if not value:
        return ""
    try:
        parsed = urlsplit(value)
        valid = parsed.scheme in {"http", "https"} and parsed.hostname and not any(char.isspace() for char in value)
        if not valid or parsed.username is not None or parsed.password is not None:
            raise ValueError("只允许不含账号密码的 http(s) 链接。")
        parsed.port  # Reject malformed port numbers as well as malformed hosts.
    except ValueError:
        raise ValueError("只允许有效且不含账号密码的 http(s) 链接。") from None
    return value


SafeURL = Annotated[str, Field(max_length=4000), BeforeValidator(validate_url)]


def validate_date(value):
    date.fromisoformat(value)
    return value


ISODate = Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}$"), AfterValidator(validate_date)]


class RequestInput(StrictModel):
    request_id: Identifier


class MaterialInput(StrictModel):
    title: Text
    kind: Literal["亲身经历", "外部参考", "待验证想法"]
    text: RequiredLongText
    url: SafeURL = ""
    verification: Literal["未核实", "有参考来源，待核实", "用户已亲测"] = "未核实"
    missing: list[Text] = Field(default_factory=list, max_length=100)


class WorkInput(RequestInput):
    title: Text
    topic_id: Identifier | None = None
    material_ids: list[Identifier] = Field(default_factory=list, max_length=100)


class WorkUpdate(StrictModel):
    title: Text
    material_ids: list[Identifier] = Field(max_length=100)


class VariantInput(RequestInput):
    form: Form
    platform: Text


class VariantPatch(StrictModel):
    status: Status | None = None
    platform: Text | None = None


class GenerateInput(RequestInput):
    kind: Literal["brief", "draft", "revise", "package", "review"]
    variant_id: Identifier | None = None
    source_id: Identifier | None = None
    instruction: LongText = ""
    section_index: int | None = Field(default=None, ge=0, le=99)
    page_count: int = Field(default=6, ge=1, le=30)
    duration_seconds: int = Field(default=180, ge=15, le=3600)
    template: LongText = ""


class Document(StrictModel):
    markdown: RequiredLongText
    missing: list[Text] = Field(default_factory=list, max_length=100)


class Section(StrictModel):
    heading: Text
    text: LongText
    visual: LongText
    seconds: float = Field(ge=0, allow_inf_nan=False)
    subtitle: LongText
    transition: LongText


class Draft(StrictModel):
    titles: list[Text] = Field(min_length=3, max_length=3)
    cover: LongText
    intro: LongText
    sections: list[Section] = Field(min_length=1, max_length=100)
    closing: LongText
    publish_text: LongText
    missing: list[Text] = Field(default_factory=list, max_length=100)


class PositioningInput(RequestInput):
    interview: RequiredLongText


class PositioningCandidate(StrictModel):
    positioning: Text
    audience: Text
    pillars: list[Text] = Field(min_length=1, max_length=20)
    difference: Text
    voice: Text
    boundaries: Text
    columns: list[Text] = Field(min_length=1, max_length=20)
    tradeoff: Text


class PositioningOutput(StrictModel):
    candidates: list[PositioningCandidate] = Field(min_length=3, max_length=3)


class ArtifactInput(RequestInput):
    kind: Literal["brief", "draft", "package", "review"]
    variant_id: Identifier | None = None
    source_id: Identifier | None = None
    data: Document | Draft


class ConfirmInput(StrictModel):
    confirmed: bool


class SopInput(RequestInput):
    variant_id: Identifier


class TaskPatch(StrictModel):
    done: bool | None = None
    due_date: ISODate | None = None
    estimated_hours: Hours | None = None
    actual_hours: Hours | None = None

    @model_validator(mode="after")
    def validate_explicit_values(self):
        for field in ("done", "estimated_hours", "actual_hours"):
            if field in self.model_fields_set and getattr(self, field) is None:
                raise ValueError("只有截止日期允许清空；完成状态和工时必须填写有效值。")
        return self


class ScheduleInput(StrictModel):
    week_start: ISODate


class Metrics(StrictModel):
    views: int | None = Field(default=None, ge=0)
    likes: int | None = Field(default=None, ge=0)
    comments: int | None = Field(default=None, ge=0)
    saves: int | None = Field(default=None, ge=0)
    completion_rate: float | None = Field(default=None, ge=0, le=100, allow_inf_nan=False)


class PublicationInput(StrictModel):
    platform: Text
    published_at: ISODate
    observation_days: int = Field(default=7, ge=1, le=365)
    url: SafeURL = ""
    metrics: Metrics = Field(default_factory=Metrics)
    comments_text: LongText = ""
    reflection: LongText = ""
    actual_hours: Hours | None = None
    request_id: str = Field(default="", max_length=100)


class PeriodInput(RequestInput):
    start_date: ISODate
    end_date: ISODate

    @model_validator(mode="after")
    def validate_range(self):
        if self.end_date < self.start_date:
            raise ValueError("结束日期不能早于开始日期。")
        return self


class IdeaInput(RequestInput):
    title: Text
