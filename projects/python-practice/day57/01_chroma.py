"""Day 57：把 Day 52 的切块+向量写入 Chroma 持久化目录，再查询 top-k。

不调 Chat。密钥读 day52/.env。chroma_db/ 已 gitignore。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import chromadb
import requests
from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
DAY52 = HERE.parent / "day52"
load_dotenv(DAY52 / ".env")
load_dotenv(HERE / ".env")

EMB_PATH = DAY52 / "embeddings.json"
CHROMA_DIR = HERE / "chroma_db"
COLLECTION = "bilibili_notes"
DEFAULT_QUERY = "30岁转行学编程晚不晚？"
DEFAULT_K = 3

API_KEY = (
    os.getenv("EMBEDDING_API_KEY")
    or os.getenv("DASHSCOPE_API_KEY")
    or ""
).strip()
BASE_URL = os.getenv("EMBEDDING_BASE_URL", "").strip().rstrip("/")
MODEL = os.getenv("EMBEDDING_MODEL", "").strip()


def embed_one(text: str) -> list[float]:
    url = f"{BASE_URL}/embeddings"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    r = requests.post(url, json={"model": MODEL, "input": text}, headers=headers, timeout=120)
    try:
        r.raise_for_status()
    except requests.HTTPError:
        print("HTTP 错误:", r.status_code)
        print(r.text[:800])
        sys.exit(1)
    return r.json()["data"][0]["embedding"]


def main() -> None:
    rebuild = "--rebuild" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--rebuild"]
    query = args[0] if args else DEFAULT_QUERY
    k = int(args[1]) if len(args) > 1 else DEFAULT_K

    if not API_KEY or not BASE_URL or not MODEL:
        print("缺少 Embedding 配置。确认 day52/.env。")
        sys.exit(1)
    if not EMB_PATH.exists():
        print(f"没有 {EMB_PATH}。先跑 day52 的 01_embed.py。")
        sys.exit(1)

    records = json.loads(EMB_PATH.read_text(encoding="utf-8"))
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    col = client.get_or_create_collection(
        name=COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )
    n = col.count()
    print(f"持久化目录: {CHROMA_DIR}")
    print(f"当前集合条数: {n}")

    if n == 0 or rebuild:
        if rebuild and n:
            client.delete_collection(COLLECTION)
            col = client.get_or_create_collection(
                name=COLLECTION,
                metadata={"hnsw:space": "cosine"},
            )
        ids = [f"{row['source']}#{row['index']}" for row in records]
        col.add(
            ids=ids,
            documents=[row["text"] for row in records],
            embeddings=[row["embedding"] for row in records],
            metadatas=[{"source": row["source"], "index": row["index"]} for row in records],
        )
        print(f"已写入 {col.count()} 条（来自 embeddings.json，未再调 Embedding 切块）")
    else:
        print("已有数据，跳过写入。要重写请加 --rebuild")

    qvec = embed_one(query)
    got = col.query(
        query_embeddings=[qvec],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    print(f"问句: {query}")
    print("Chroma 的 distance 越小越近（cosine 空间里约等于 1-余弦）")
    print("---")
    docs = got["documents"][0]
    metas = got["metadatas"][0]
    dists = got["distances"][0]
    for i, (doc, meta, dist) in enumerate(zip(docs, metas, dists), start=1):
        preview = doc.replace("\n", " ")[:80]
        print(f"{i}. {meta.get('source')}  distance {dist:.4f}")
        print(f"   {preview}...")
        print()
    print("关终端再跑同一条命令：条数应仍 > 0，这就是持久化。不要调 Chat。")


if __name__ == "__main__":
    main()
