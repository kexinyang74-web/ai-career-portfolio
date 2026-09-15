"""Day 60：LangChain VectorStore 检索 + 手写拼 user 再 Chat。

对照 day53/01_search.py、day54/01_rag_chat.py。
读 day57 的 chroma_db，不重新切块、不重跑 10 篇 Embedding。
RetrievalQA 这个旧名字 = 下面「检索 → 拼进 user → Chat」三步；新版库已不推荐一键链，今天拆开写。
"""

from __future__ import annotations

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
PRACTICE = HERE.parent
DAY52 = PRACTICE / "day52"
DAY57 = PRACTICE / "day57"
PROJECT1 = PRACTICE.parent / "project-1-ai-assistant"

load_dotenv(PROJECT1 / ".env")
load_dotenv(DAY52 / ".env")

CHROMA_DIR = DAY57 / "chroma_db"
COLLECTION = "bilibili_notes"
DEFAULT_QUERY = "30岁转行学编程晚不晚？根据我的爆款拆解笔记回答，并写上来源文件名。"
DEFAULT_K = 3

EMBED_KEY = (
    os.getenv("EMBEDDING_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or ""
).strip()
EMBED_BASE = os.getenv("EMBEDDING_BASE_URL", "").strip().rstrip("/")
EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "").strip()

CHAT_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
CHAT_BASE = (
    os.getenv("CHAT_BASE_URL") or os.getenv("BASE_URL") or "https://api.deepseek.com"
).strip().rstrip("/")
CHAT_MODEL = os.getenv("CHAT_MODEL") or "deepseek-chat"
if "embedding" in CHAT_MODEL.lower():
    CHAT_MODEL = "deepseek-chat"
if "compatible-mode" in CHAT_BASE or "dashscope" in CHAT_BASE:
    CHAT_BASE = "https://api.deepseek.com"


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
    """给 LangChain VectorStore 用的包装：里面仍是你 Day 52 那次 /embeddings。"""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [embed_one(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return embed_one(text)


def source_name(meta: dict) -> str:
    raw = (meta or {}).get("source") or ""
    return Path(str(raw)).name or str(raw)


def main() -> None:
    query = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUERY
    k = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_K

    if not EMBED_KEY or not EMBED_BASE or not EMBED_MODEL:
        print("缺少 Embedding 配置（day52/.env）。")
        sys.exit(1)
    if not CHAT_KEY:
        print("缺少 DEEPSEEK_API_KEY（项目一或 day52/.env）。")
        sys.exit(1)
    if not CHROMA_DIR.exists():
        print(f"没有 {CHROMA_DIR}。先到 day57 跑 python 01_chroma.py。")
        sys.exit(1)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    n = client.get_or_create_collection(name=COLLECTION).count()
    if n == 0:
        print("集合是空的。先跑 day57/01_chroma.py。")
        sys.exit(1)

    # —— VectorStore：对照 01_search.py / day57 query ——
    store = Chroma(
        client=client,
        collection_name=COLLECTION,
        embedding_function=DashScopeEmbeddings(),
        create_collection_if_not_exists=False,
    )
    hits = store.similarity_search_with_score(query, k=k)

    print(f"问句: {query}")
    print(f"集合 {n} 条（day57 chroma_db）。score 越小越近。")
    print()
    print(f"== 1/2 VectorStore：similarity_search top-{k} ==")
    if not hits:
        print("没有结果。")
        sys.exit(1)
    for i, (doc, score) in enumerate(hits, start=1):
        preview = (doc.page_content or "").replace("\n", " ")[:72]
        print(f"  {i}. {source_name(doc.metadata)}  score {score:.4f}")
        print(f"     {preview}...")
    print()

    # —— 旧名 RetrievalQA = 检索 + 拼进 user + Chat（对照 01_rag_chat.py）——
    parts = ["资料（检索得到，请优先依据这些内容，并在回答里写上来源文件名）："]
    for i, (doc, score) in enumerate(hits, start=1):
        parts.append(
            f"\n[{i}] 来源 {source_name(doc.metadata)}  score {score:.4f}\n{doc.page_content}"
        )
    parts.append(f"\n问题：{query}")
    user_text = "\n".join(parts)

    llm = ChatOpenAI(
        model=CHAT_MODEL,
        api_key=CHAT_KEY,
        base_url=CHAT_BASE,
        temperature=0.3,
    )
    system = (
        "你是助手。有资料时只根据资料回答，并写上来源文件名（如 02.md）。"
        "资料不足就说不足，不要编造笔记里没有的标题或钩子。"
    )
    print("== 2/2 QA：片段在本轮 user，再 Chat ==")
    print(f"Chat: {CHAT_BASE}  模型 {CHAT_MODEL}")
    out = llm.invoke(
        [SystemMessage(content=system), HumanMessage(content=user_text)]
    )
    print(out.content)
    print()
    print("四词收齐：Loader / Splitter 昨天；VectorStore 是 1/2；RetrievalQA 是 2/2 这三步。")
    print("今天没有 where 过滤，没有新建项目二目录。")


if __name__ == "__main__":
    main()
