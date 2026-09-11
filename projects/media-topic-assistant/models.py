from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


Text = Annotated[str, Field(min_length=1, max_length=3000)]
Items = Annotated[list[Text], Field(min_length=1, max_length=12)]
Category = Text


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Profile(StrictModel):
    audience: Text = "22—26岁，毕业0—3年的年轻人"
    positioning: Text = "分享AI工具如何帮助年轻人适应职场、持续学习和管理生活。真实有用，容易实践。"
    primary_platform: Text = "小红书图文"
    secondary_platforms: list[Text] = ["抖音/视频号", "B站/公众号"]
    weights: dict[Category, int] = {"AI工具": 70, "学习成长": 20, "生活管理": 10}
    time_budget_hours: float = Field(default=4, gt=0, le=72)
    goal: str = Field(default="", max_length=10000)
    voice: str = Field(default="", max_length=10000)
    boundaries: str = Field(default="", max_length=10000)
    columns: list[Text] = Field(default_factory=list, max_length=100)
    content_forms: list[Literal["图文", "口播", "录屏教程", "生活记录", "混合视频"]] = Field(default_factory=lambda: ["图文", "口播", "录屏教程", "生活记录", "混合视频"], min_length=1, max_length=5)
    on_camera: Text = "可出镜或不出镜"
    weekly_hours: float = Field(default=8, ge=0, le=168, allow_inf_nan=False)
    interview: str = Field(default="", max_length=100000)
    confirmed: bool = False

    @model_validator(mode="after")
    def validate_weights(self):
        if not self.weights or any(v < 0 for v in self.weights.values()) or sum(self.weights.values()) != 100:
            raise ValueError("内容方向的比例必须非负，合计100。")
        return self


class MessageInput(StrictModel):
    text: Text
    request_id: str = Field(min_length=1, max_length=100)


class Question(StrictModel):
    question: str = Field(min_length=3, max_length=240)


class TopicDraft(StrictModel):
    title: str = Field(min_length=3, max_length=100)
    category: Category
    pain_point: Text
    angle: Text
    reason: Text
    estimated_hours: float = Field(gt=0, le=72)
    to_test: Items
    missing_info: list[Text] = Field(max_length=12)
    external_claims: list[Text] = Field(max_length=8)
    platforms: list[Text] = Field(min_length=1, max_length=5)


class TopicBatch(StrictModel):
    topics: list[TopicDraft] = Field(min_length=5, max_length=10)


class Plan(StrictModel):
    core_question: Text
    hypotheses: Items
    test_steps: Items
    materials: Items
    boundaries: Items


class TopicPatch(StrictModel):
    favorite: bool | None = None
    status: Literal["待创作", "已发布", "放弃"] | None = None
    feedback: Literal["感兴趣", "不适合", ""] | None = None
    feedback_note: str | None = Field(default=None, max_length=500)
