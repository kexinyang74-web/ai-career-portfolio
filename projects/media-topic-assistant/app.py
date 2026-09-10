import re
import threading
from contextlib import contextmanager
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from starlette.middleware.trustedhost import TrustedHostMiddleware

from models import MessageInput, Plan, Profile, Question, TopicBatch, TopicPatch
from provider import DeepSeekProvider, ProviderError
from store import Store, now, uid


ROOT = Path(__file__).resolve().parent


def normalized(title):
    return re.sub(r"[\W_]", "", title).casefold()


def create_app(db_path=None, provider=None):
    load_dotenv(ROOT / ".env")
    db = Store(db_path or ROOT / "data" / "assistant.db")
    ai = provider or DeepSeekProvider()
    app = FastAPI(title="灵感小记 · 自媒体选题助手", docs_url=None, redoc_url=None)
    app.state.store, app.state.provider = db, ai
    # Single local user: one generation at a time prevents double clicks from
    # overwriting feedback or creating two batches. Reads stay available.
    mutation_lock = threading.Lock()
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost", "[::1]", "testserver"])

    @app.middleware("http")
    async def local_only(request: Request, call_next):
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            origin = request.headers.get("origin")
            if origin and origin != str(request.base_url).rstrip("/"):
                return JSONResponse({"detail": "仅允许从本机应用页面执行操作。"}, status_code=403)
            if request.headers.get("sec-fetch-site") == "cross-site":
                return JSONResponse({"detail": "不接受跨站请求。"}, status_code=403)
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'"
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
        return response

    @app.exception_handler(ProviderError)
    async def provider_error(request, exc):
        return JSONResponse({"detail": exc.message, "code": exc.code}, status_code=exc.status)

    @app.exception_handler(RequestValidationError)
    async def input_error(request, exc):
        return JSONResponse({"detail": "输入不符合要求，请检查必填项、字数和比例（合计100）。"}, status_code=422)

    @contextmanager
    def writing():
        if not mutation_lock.acquire(blocking=False):
            raise HTTPException(409, "正在处理上一项操作，请等待完成后再试。")
        try:
            yield
        finally:
            mutation_lock.release()

    def session_or_404(sid):
        session = db.session(sid)
        if not session:
            raise HTTPException(404, "没有找到这段对话。")
        return session

    def topic_or_404(tid):
        topic = db.topic(tid)
        if not topic:
            raise HTTPException(404, "没有找到这个选题。")
        return topic

    def detail(sid):
        session = session_or_404(sid)
        all_topics = db.topics(sid)
        session["topics"] = [t for t in all_topics if t["batch"] == session["batch"]]
        session["previous_topics"] = [t for t in all_topics if t["batch"] != session["batch"]]
        session["ready"] = sum(m["role"] == "user" for m in session["messages"]) >= 2
        return session

    def context(sid):
        session = session_or_404(sid)
        return {"profile": db.profile(), "messages": session["messages"], "feedback": [
            {"title": t["title"], "angle": t["angle"], "feedback": t["feedback"], "note": t["feedback_note"]}
            for t in db.topics(sid) if t["feedback"]
        ]}

    def generate_valid(kind, data, schema):
        try:
            return schema.model_validate(ai.generate(kind, data, schema.model_json_schema()))
        except (ValidationError, ValueError, TypeError):
            raise ProviderError("invalid_output", "模型返回的内容缺少必要字段或格式不合格，已有结果已保留，请重试。") from None

    def apply_research(topics):
        references, notice = ai.research(topics)
        for topic in topics:
            incoming = references.get(topic["id"], [])
            if incoming:
                topic["sources"] = [dict(id=uuid5(NAMESPACE_URL, topic["id"] + ref["url"]).hex,
                                         topic_id=topic["id"], checked_at=now(), **ref) for ref in incoming]
            else:
                topic.setdefault("sources", [])  # failed refresh must retain past evidence
            topic["verification"] = "有参考来源，待核实" if topic["sources"] else ("未核实" if topic["external_claims"] else "构思，待亲测")
        return notice

    @app.get("/api/health")
    def health():
        return {"configured": ai.configured, "search_status": ai.search_status, "model": getattr(ai, "model", "test")}

    @app.get("/api/profile")
    def get_profile():
        return db.profile()

    @app.put("/api/profile")
    def update_profile(profile: Profile):
        with writing():
            return db.save_profile(profile.model_dump())

    @app.get("/api/sessions")
    def sessions():
        return [{k: s[k] for k in ("id", "title", "created_at", "updated_at", "batch")} for s in db.sessions()]

    @app.post("/api/sessions")
    def new_session():
        with writing():
            session = db.create_session()
            return detail(session["id"])

    @app.get("/api/sessions/{sid}")
    def session_detail(sid: str):
        return detail(sid)

    @app.post("/api/sessions/{sid}/messages")
    def message(sid: str, body: MessageInput):
        with writing():
            session = session_or_404(sid)
            existing = next((m for m in session["messages"] if m.get("request_id") == body.request_id), None)
            if existing and existing["content"] != body.text:
                raise HTTPException(409, "重试内容与原消息不同，请恢复原文或重新开始对话。")
            if any(m.get("reply_to") == body.request_id for m in session["messages"]):
                return detail(sid)
            pending = session["messages"][-1]
            if not existing and pending["role"] == "user":
                raise HTTPException(409, "上一条消息尚未完成，请先重试。")
            if not existing:
                session["messages"].append(dict(id=uid(), role="user", content=body.text, request_id=body.request_id, created_at=now()))
                if session["title"] == "新的选题对话":
                    session["title"] = body.text[:36]
                db.save_session(session)  # persist the user's work before any network call
            turns = sum(m["role"] == "user" for m in session["messages"])
            if turns >= 4:
                answer = "这些信息已经可以开始策划。点击「现在生成」，我会给你一组选题；尚未确认的部分会列为待补充。"
            else:
                answer = generate_valid("question", context(sid), Question).question
                # Keep the interview to one question even if a model adds extras.
                answer = re.split(r"[？?]", answer)[0].strip() + "？"
            session["messages"].append(dict(id=uid(), role="assistant", content=answer, reply_to=body.request_id, created_at=now()))
            db.save_session(session)
            return detail(sid)

    @app.post("/api/sessions/{sid}/generate")
    def generate(sid: str):
        with writing():
            session = session_or_404(sid)
            batch = generate_valid("topics", context(sid), TopicBatch)
            rejected = {normalized(t["title"]) for t in db.topics(sid) if t["feedback"] == "不适合"}
            seen = set(rejected)
            drafts = []
            for draft in batch.topics:
                key = normalized(draft.title)
                if key not in seen:
                    seen.add(key)
                    drafts.append(draft)
            if len(drafts) < 5:
                raise ProviderError("repeated_topics", "这次推荐与已否定选题重复过多，原结果已保留。请补充反馈后重试。")
            new_batch = session["batch"] + 1
            topics = [dict(**draft.model_dump(), id=uid(), session_id=sid, batch=new_batch, created_at=now(),
                           favorite=False, status="待创作", feedback="", feedback_note="", plan=None, sources=[], verification="未核实") for draft in drafts]
            session["notice"] = apply_research(topics)
            session["batch"] = new_batch
            db.save_batch(session, topics)
            return detail(sid)

    @app.get("/api/topics/{tid}")
    def topic(tid: str):
        return topic_or_404(tid)

    @app.patch("/api/topics/{tid}")
    def patch_topic(tid: str, body: TopicPatch):
        with writing():
            topic = topic_or_404(tid)
            updates = body.model_dump(exclude_none=True)
            if updates.get("favorite") and not topic["favorite"]:
                topic["status"] = "待创作"
            topic.update(updates)
            return db.save_topic(topic)

    @app.post("/api/topics/{tid}/plan")
    def expand(tid: str):
        with writing():
            topic = topic_or_404(tid)
            if not topic["plan"]:
                data = context(topic["session_id"])
                data["selected_topic"] = topic
                topic["plan"] = generate_valid("plan", data, Plan).model_dump()
                db.save_topic(topic)
            return topic

    @app.post("/api/topics/{tid}/research")
    def research(tid: str):
        with writing():
            topic = topic_or_404(tid)
            ai.search_status = "not_checked"
            notice = apply_research([topic])
            db.save_topic(topic)
            return {"topic": topic, "notice": notice}

    @app.get("/api/favorites")
    def favorites(status: str | None = None):
        return sorted([t for t in db.topics() if t["favorite"] and (not status or t["status"] == status)], key=lambda t: t["created_at"], reverse=True)

    @app.get("/")
    def home():
        return FileResponse(ROOT / "static" / "index.html")

    app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
    return app
