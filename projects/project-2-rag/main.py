"""项目二 MVP：爆款案例库 RAG 问答（CLI）。

提问 → Chroma 检索 → 片段进本轮 user → Chat → 打印来源。
默认读 day57 已写入的 chroma_db（约 10 篇），不重 embed。
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import chromadb
import requests
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PRACTICE = ROOT / "projects" / "python-practice"
DAY52 = PRACTICE / "day52"
DAY57 = PRACTICE / "day57"
PROJECT1 = ROOT / "projects" / "project-1-ai-assistant"

load_dotenv(PROJECT1 / ".env")
load_dotenv(DAY52 / ".env")
load_dotenv(HERE / ".env")

CHROMA_DIR = DAY57 / "chroma_db"
COLLECTION = "bilibili_notes"

EMBED_KEY = (
    os.getenv("EMBEDDING_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or ""
).strip()
EMBED_BASE = os.getenv("EMBEDDING_BASE_URL", "").strip().rstrip("/")
EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "").strip()

CHAT_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
CHAT_BASE = (
    os.getenv("CHAT_BASE_URL") or os.getenv("BASE_URL") or "https://api.deepseek.com"
).strip().rstrip("/")
CHAT_MODEL = os.getenv("CHAT_MODEL") or os.getenv("MODEL") or "deepseek-chat"
if "embedding" in CHAT_MODEL.lower():
    CHAT_MODEL = "deepseek-chat"
if "compatible-mode" in CHAT_BASE or "dashscope" in CHAT_BASE:
    CHAT_BASE = "https://api.deepseek.com"

SYSTEM = (
    "你是面向 B站创作者的爆款案例库助手。"
    "有资料时只根据资料回答，并写上来源文件名（如 02.md）。"
    "资料不足就说不足，不要编造笔记里没有的标题或钩子。"
)


def embed_one(text: str) -> list[float]:
    r = requests.post(
        f"{EMBED_BASE}/embeddings",
        headers={
            "Authorization": f"Bearer {EMBED_KEY}",
            "Content-Type": "application/json",
        },
        json={"model": EMBED_MODEL, "input": text},
        timeout=120,
    )
    try:
        r.raise_for_status()
    except requests.HTTPError:
        print("Embedding HTTP 错误:", r.status_code)
        print(r.text[:800])
        sys.exit(1)
    return r.json()["data"][0]["embedding"]


class DashScopeEmbeddings(Embeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [embed_one(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return embed_one(text)


def source_name(meta: dict) -> str:
    raw = (meta or {}).get("source") or ""
    return Path(str(raw)).name or str(raw)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="爆款案例库 RAG 问答")
    p.add_argument("query", nargs="?", default="30岁转行学编程晚不晚？根据笔记回答并写上来源文件名。")
    p.add_argument("-k", type=int, default=5, help="检索条数，默认 5（评测第 24 条 k=3 漏召回 02.md）")
    p.add_argument(
        "--source",
        default="",
        help="只要某一篇，例如 02.md（Chroma where 过滤）",
    )
    p.add_argument("--no-rag", action="store_true", help="不检索，只把问句发给 Chat")
    return p.parse_args()


def retrieve(query: str, k: int, source: str):
    if not CHROMA_DIR.exists():
        print(f"没有 {CHROMA_DIR}。先跑 day57/01_chroma.py。")
        sys.exit(1)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    n = client.get_or_create_collection(name=COLLECTION).count()
    if n == 0:
        print("集合是空的。先跑 day57/01_chroma.py。")
        sys.exit(1)
    store = Chroma(
        client=client,
        collection_name=COLLECTION,
        embedding_function=DashScopeEmbeddings(),
        create_collection_if_not_exists=False,
    )
    kwargs: dict = {"k": k}
    if source.strip():
        kwargs["filter"] = {"source": source.strip()}
    return store.similarity_search_with_score(query, **kwargs)


def chat(user_text: str) -> str:
    llm = ChatOpenAI(
        model=CHAT_MODEL,
        api_key=CHAT_KEY,
        base_url=CHAT_BASE,
        temperature=0.3,
    )
    out = llm.invoke(
        [SystemMessage(content=SYSTEM), HumanMessage(content=user_text)]
    )
    return str(out.content)


def main() -> None:
    args = parse_args()
    if not CHAT_KEY:
        print("缺少 DEEPSEEK_API_KEY。可放本目录 .env，或沿用项目一 / day52。")
        sys.exit(1)

    print("问句:", args.query)
    if args.no_rag:
        print("模式: 无检索")
        print()
        print(chat(args.query))
        return

    if not EMBED_KEY or not EMBED_BASE or not EMBED_MODEL:
        print("缺少 Embedding 配置（day52/.env 或本目录 .env）。")
        sys.exit(1)

    hits = retrieve(args.query, args.k, args.source)
    print("模式: RAG")
    if args.source:
        print(f"过滤: source={args.source}")
    if not hits:
        print("没有检索到片段。")
        print(chat("资料不足。问题：" + args.query))
        return

    names = []
    parts = ["资料（检索得到，请优先依据这些内容，并在回答里写上来源文件名）："]
    for i, (doc, score) in enumerate(hits, start=1):
        name = source_name(doc.metadata)
        names.append(name)
        print(f"  {i}. {name}  score {score:.4f}")
        parts.append(f"\n[{i}] 来源 {name}  score {score:.4f}\n{doc.page_content}")
    parts.append(f"\n问题：{args.query}")
    print("来源:", "、".join(dict.fromkeys(names)))
    print()
    print(chat("\n".join(parts)))


if __name__ == "__main__":
    main()
