"""Day 58：同一问句，不过滤 vs 只查 source=02.md。

读 Day 57 的 chroma_db。不调 Chat。不上 LangChain。密钥 day52/.env。
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import chromadb
import requests
from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
DAY52 = HERE.parent / "day52"
DAY57 = HERE.parent / "day57"
load_dotenv(DAY52 / ".env")

CHROMA_DIR = DAY57 / "chroma_db"
COLLECTION = "bilibili_notes"
DEFAULT_QUERY = "30岁转行学编程晚不晚？"
DEFAULT_K = 3

API_KEY = (
    os.getenv("EMBEDDING_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or ""
).strip()
BASE_URL = os.getenv("EMBEDDING_BASE_URL", "").strip().rstrip("/")
MODEL = os.getenv("EMBEDDING_MODEL", "").strip()


def embed_one(text: str) -> list[float]:
    r = requests.post(
        f"{BASE_URL}/embeddings",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={"model": MODEL, "input": text},
        timeout=120,
    )
    try:
        r.raise_for_status()
    except requests.HTTPError:
        print("HTTP 错误:", r.status_code)
        print(r.text[:800])
        sys.exit(1)
    return r.json()["data"][0]["embedding"]


def show(title: str, got: dict) -> None:
    print(title)
    docs = (got.get("documents") or [[]])[0]
    metas = (got.get("metadatas") or [[]])[0]
    dists = (got.get("distances") or [[]])[0]
    if not docs:
        print("  （没有结果）")
        print()
        return
    for i, (doc, meta, dist) in enumerate(zip(docs, metas, dists), start=1):
        preview = (doc or "").replace("\n", " ")[:72]
        print(f"  {i}. {meta.get('source')}  distance {dist:.4f}")
        print(f"     {preview}...")
    print()


def main() -> None:
    query = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUERY
    k = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_K
    if not API_KEY or not BASE_URL or not MODEL:
        print("缺少 Embedding 配置。")
        sys.exit(1)
    if not CHROMA_DIR.exists():
        print(f"没有 {CHROMA_DIR}。先到 day57 跑 python 01_chroma.py。")
        sys.exit(1)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    col = client.get_or_create_collection(name=COLLECTION)
    if col.count() == 0:
        print("集合是空的。先跑 day57/01_chroma.py。")
        sys.exit(1)

    qvec = embed_one(query)
    print(f"问句: {query}")
    print(f"集合 {col.count()} 条。distance 越小越近。")
    print()
    show(
        f"== 1/2 不过滤，top-{k} ==",
        col.query(
            query_embeddings=[qvec],
            n_results=k,
            include=["documents", "metadatas", "distances"],
        ),
    )
    show(
        f"== 2/2 只要 source=02.md，top-{k} ==",
        col.query(
            query_embeddings=[qvec],
            n_results=k,
            where={"source": "02.md"},
            include=["documents", "metadatas", "distances"],
        ),
    )
    print("过滤是硬条件：不是 02.md 的块根本不参与排序。rerank 是先广搜再重排，今天只记概念。")


if __name__ == "__main__":
    main()
