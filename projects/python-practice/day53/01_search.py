"""Day 53：读 Day 52 的 embeddings.json，问句走同一套 Embedding，手写余弦取 top-k。

不调 Chat。密钥仍用 day52/.env（不要复制进本目录再贴到聊天）。
"""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
DAY52 = HERE.parent / "day52"
load_dotenv(DAY52 / ".env")
load_dotenv(HERE / ".env")

EMB_PATH = DAY52 / "embeddings.json"
DEFAULT_QUERY = "30岁转行学编程晚不晚？"
DEFAULT_K = 3

API_KEY = (
    os.getenv("EMBEDDING_API_KEY")
    or os.getenv("DASHSCOPE_API_KEY")
    or os.getenv("DEEPSEEK_API_KEY")
    or ""
).strip()
BASE_URL = os.getenv("EMBEDDING_BASE_URL", "").strip().rstrip("/")
MODEL = os.getenv("EMBEDDING_MODEL", "").strip()


def cosine(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError(f"维度不一致：{len(a)} vs {len(b)}")
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def embed_one(text: str) -> list[float]:
    url = f"{BASE_URL}/embeddings"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"model": MODEL, "input": text}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=120)
        r.raise_for_status()
    except requests.Timeout:
        print("超时。代理可先: $env:HTTPS_PROXY = 'http://127.0.0.1:7897'")
        sys.exit(1)
    except requests.HTTPError:
        print("HTTP 错误:", r.status_code)
        print(r.text[:800])
        sys.exit(1)
    except requests.RequestException as exc:
        print("请求失败:", exc)
        sys.exit(1)

    vec = r.json()["data"][0]["embedding"]
    if not isinstance(vec, list) or not vec:
        print("问句没有拿到 embedding。")
        sys.exit(1)
    return vec


def main() -> None:
    query = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUERY
    k = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_K

    if not API_KEY or not BASE_URL or not MODEL:
        print("读不到 Embedding 配置。确认 day52/.env 还在，或在本目录另放一份 .env。")
        sys.exit(1)
    if not EMB_PATH.exists():
        print(f"没有 {EMB_PATH}。先到 day52 跑 python 01_embed.py。")
        sys.exit(1)

    records = json.loads(EMB_PATH.read_text(encoding="utf-8"))
    qvec = embed_one(query)
    print(f"问句: {query}")
    print(f"问句维度 {len(qvec)}，库里 {len(records)} 块，取 top-{k}")
    print("余弦 = 点积 / (问句模长 × 切块模长)，越大越同向")
    print("---")

    scored = []
    for row in records:
        score = cosine(qvec, row["embedding"])
        scored.append((score, row))
    scored.sort(key=lambda x: x[0], reverse=True)

    for rank, (score, row) in enumerate(scored[:k], start=1):
        preview = row["text"].replace("\n", " ")[:80]
        print(f"{rank}. {row['source']}#{row['index']}  余弦 {score:.4f}")
        print(f"   {preview}...")
        print()

    print("今天到此：能指出第几篇即可。不要调 Chat。")


if __name__ == "__main__":
    main()
