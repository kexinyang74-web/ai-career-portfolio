import json

import pytest
from fastapi.testclient import TestClient

from app import create_app
from provider import ProviderError


class FakeProvider:
    configured = True
    search_status = "not_checked"
    fail = None
    contexts = []

    def generate(self, kind, context, schema):
        self.contexts.append((kind, context))
        if self.fail:
            raise self.fail
        if kind == "question":
            return {"question": "这件事里，你已经亲自尝试过哪一步？"}
        if kind == "plan":
            return {"core_question": "能否减少整理时间？", "hypotheses": ["待验证：可能节省时间"],
                    "test_steps": ["记录手动耗时", "试用工具并对比"], "materials": ["脱敏记录"],
                    "boundaries": ["只报告实际测试结果"]}
        return {"topics": [dict(title=f"整理学习笔记的第{i}种切入点", category="AI工具",
                pain_point="下班后整理笔记费时", angle=f"用一个真实任务验证方法{i}", reason="贴近毕业生问题",
                estimated_hours=4, to_test=["用脱敏材料亲测"], missing_info=["待补充工具名称"],
                external_claims=["工具是否支持导出"], platforms=["小红书"]) for i in range(6)]}

    def research(self, topics):
        return {}, "联网工具未返回可验证的搜索结果，相关事实未核实。"


@pytest.fixture
def setup(tmp_path):
    provider = FakeProvider()
    provider.contexts = []
    path = tmp_path / "test.db"
    app = create_app(path, provider)
    with TestClient(app) as client:
        yield client, provider, path


def new_session(client):
    r = client.post("/api/sessions")
    assert r.status_code == 200
    return r.json()["id"]


def test_complete_flow_and_restart(setup):
    c, provider, path = setup
    sid = new_session(c)
    r = c.post(f"/api/sessions/{sid}/messages", json={"text": "我想整理学习笔记，还没试过AI", "request_id": "one"})
    assert r.status_code == 200
    r = c.post(f"/api/sessions/{sid}/generate")
    assert r.status_code == 200
    topics = r.json()["topics"]
    assert len(topics) == 6
    assert all(t["verification"] == "未核实" and not t["sources"] for t in topics)
    tid = topics[0]["id"]
    assert c.post(f"/api/topics/{tid}/plan").json()["plan"]["test_steps"]
    assert c.patch(f"/api/topics/{tid}", json={"favorite": True}).json()["status"] == "待创作"
    c.patch(f"/api/topics/{tid}", json={"status": "已发布"})
    with TestClient(create_app(path, provider)) as reopened:
        saved = reopened.get("/api/favorites?status=已发布").json()
        assert saved[0]["id"] == tid
        assert saved[0]["plan"]
        assert len(reopened.get(f"/api/sessions/{sid}").json()["messages"]) == 3


def test_failed_message_is_saved_and_retry_is_idempotent(setup):
    c, p, _ = setup
    sid = new_session(c)
    p.fail = ProviderError("timeout", "连接超时，请重试。", 504)
    body = {"text": "我试过做周报", "request_id": "same"}
    assert c.post(f"/api/sessions/{sid}/messages", json=body).status_code == 504
    assert c.get(f"/api/sessions/{sid}").json()["messages"][-1]["content"] == body["text"]
    p.fail = None
    assert c.post(f"/api/sessions/{sid}/messages", json=body).status_code == 200
    assert c.post(f"/api/sessions/{sid}/messages", json=body).status_code == 200
    assert len(c.get(f"/api/sessions/{sid}").json()["messages"]) == 3


def test_invalid_model_output_does_not_replace_existing_topics(setup):
    c, p, _ = setup
    sid = new_session(c)
    original = c.post(f"/api/sessions/{sid}/generate").json()["topics"]
    p.generate = lambda *args: {"topics": [{"title": "缺字段"}]}
    assert c.post(f"/api/sessions/{sid}/generate").status_code == 502
    assert c.get(f"/api/sessions/{sid}").json()["topics"] == original


def test_feedback_excludes_rejected_title_and_keeps_history(setup):
    c, p, _ = setup
    sid = new_session(c)
    topics = c.post(f"/api/sessions/{sid}/generate").json()["topics"]
    c.patch(f"/api/topics/{topics[0]['id']}", json={"feedback": "不适合", "feedback_note": "没有这种经历"})
    generated = c.post(f"/api/sessions/{sid}/generate").json()["topics"]
    assert len(generated) == 5
    assert topics[0]["title"] not in [t["title"] for t in generated]
    assert "没有这种经历" in json.dumps(p.contexts[-1], ensure_ascii=False)


def test_profile_validation_and_missing_resource(setup):
    c, _, _ = setup
    profile = c.get("/api/profile").json()
    profile["weights"] = {"AI工具": 60, "学习成长": 30, "生活管理": 10}
    assert c.put("/api/profile", json=profile).status_code == 200
    profile["weights"]["AI工具"] = -1
    assert c.put("/api/profile", json=profile).status_code == 422
    assert c.get("/api/sessions/missing").status_code == 404


def test_four_turns_stop_questioning(setup):
    c, p, _ = setup
    sid = new_session(c)
    for i in range(4):
        assert c.post(f"/api/sessions/{sid}/messages", json={"text": "补充经历", "request_id": str(i)}).status_code == 200
    detail = c.get(f"/api/sessions/{sid}").json()
    assert detail["ready"]
    assert "生成" in detail["messages"][-1]["content"]
    assert len([x for x in p.contexts if x[0] == "question"]) == 3


def test_local_origin_protection(setup):
    c, _, _ = setup
    assert c.post("/api/sessions", headers={"Origin": "https://evil.example"}).status_code == 403
    assert c.get("/api/profile", headers={"Host": "evil.example"}).status_code == 400
