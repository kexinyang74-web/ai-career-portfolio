"""Day 62：同一批 embeddings.json 用 FAISS 做 top-k。不调 Chat，不部署 Milvus。"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import faiss
import numpy as np
import requests
from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
DAY52 = HERE.parent / "day52"
load_dotenv(DAY52 / ".env")

EMB_PATH = DAY52 / "embeddings.json"
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


def main() -> None:
    query = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUERY
    k = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_K
    if not API_KEY or not BASE_URL or not MODEL:
        print("缺少 Embedding 配置（day52/.env）。")
        sys.exit(1)
    if not EMB_PATH.exists():
        print(f"没有 {EMB_PATH}。先跑 day52/01_embed.py。")
        sys.exit(1)

    rows = json.loads(EMB_PATH.read_text(encoding="utf-8"))
    mat = np.array([row["embedding"] for row in rows], dtype="float32")
    faiss.normalize_L2(mat)
    index = faiss.IndexFlatIP(mat.shape[1])
    index.add(mat)

    q = np.array([embed_one(query)], dtype="float32")
    faiss.normalize_L2(q)
    scores, ids = index.search(q, k)

    print(f"问句: {query}")
    print(f"FAISS IndexFlatIP，{index.ntotal} 条。分数越大越近（内积≈余弦）。")
    print("和 Chroma 的 distance（越小越近）方向相反。")
    print()
    print(f"== FAISS top-{k} ==")
    for rank, (idx, score) in enumerate(zip(ids[0], scores[0]), start=1):
        row = rows[int(idx)]
        preview = (row.get("text") or "").replace("\n", " ")[:72]
        print(f"  {rank}. {row['source']}  分数 {float(score):.4f}")
        print(f"     {preview}...")
    print()
    print("FAISS 只管向量远近；source 是我们自己列表里带着的。没有 Chroma 那种 where。")
    print("Milvus 今天不装：适合集群、海量向量，本机 10 条用不上。")


if __name__ == "__main__":
    main()
