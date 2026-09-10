"""Day 54：同一问句，无检索 vs 检索后拼进 user 再调 Chat。

Embedding 用百炼（day52/.env），Chat 用 DeepSeek（项目一或 day52 里的 DEEPSEEK_API_KEY）。
不上 LangChain。不要 print 密钥。
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
PRACTICE = HERE.parent
DAY52 = PRACTICE / "day52"
PROJECT1 = PRACTICE.parent / "project-1-ai-assistant"

load_dotenv(PROJECT1 / ".env")
load_dotenv(DAY52 / ".env")
load_dotenv(HERE / ".env")

EMB_PATH = DAY52 / "embeddings.json"
DEFAULT_QUERY = "30岁转行学编程晚不晚？根据我的爆款拆解笔记回答，并写上来源文件名。"
DEFAULT_K = 3

EMBED_KEY = (
    os.getenv("EMBEDDING_API_KEY")
    or os.getenv("DASHSCOPE_API_KEY")
    or ""
).strip()
EMBED_BASE = os.getenv("EMBEDDING_BASE_URL", "").strip().rstrip("/")
EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "").strip()

CHAT_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
CHAT_BASE = (os.getenv("CHAT_BASE_URL") or os.getenv("BASE_URL") or "https://api.deepseek.com").strip().rstrip("/")
CHAT_MODEL = os.getenv("CHAT_MODEL") or "deepseek-chat"
if "embedding" in CHAT_MODEL.lower():
    CHAT_MODEL = "deepseek-chat"
if "compatible-mode" in CHAT_BASE or "dashscope" in CHAT_BASE:
    CHAT_BASE = "https://api.deepseek.com"


def cosine(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError(f"维度不一致：{len(a)} vs {len(b)}")
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def http_json(url: str, api_key: str, payload: dict) -> dict:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=120)
        r.raise_for_status()
    except requests.Timeout:
        print("超时。代理可先: $env:HTTPS_PROXY = 'http://127.0.0.1:7897'")
        sys.exit(1)
    except requests.HTTPError:
        print("HTTP 错误:", r.status_code, url)
        print(r.text[:800])
        sys.exit(1)
    except requests.RequestException as exc:
        print("请求失败:", exc)
        sys.exit(1)
    return r.json()


def embed_one(text: str) -> list[float]:
    data = http_json(
        f"{EMBED_BASE}/embeddings",
        EMBED_KEY,
        {"model": EMBED_MODEL, "input": text},
    )
    return data["data"][0]["embedding"]


def chat(messages: list[dict]) -> str:
    data = http_json(
        f"{CHAT_BASE}/chat/completions",
        CHAT_KEY,
        {
            "model": CHAT_MODEL,
            "messages": messages,
            "temperature": 0.3,
            "stream": False,
        },
    )
    return data["choices"][0]["message"]["content"]


def top_k(query: str, k: int) -> list[dict]:
    records = json.loads(EMB_PATH.read_text(encoding="utf-8"))
    qvec = embed_one(query)
    scored = [(cosine(qvec, row["embedding"]), row) for row in records]
    scored.sort(key=lambda x: x[0], reverse=True)
    out = []
    for score, row in scored[:k]:
        item = dict(row)
        item["score"] = score
        out.append(item)
    return out


def build_user_with_rag(query: str, hits: list[dict]) -> str:
    parts = ["资料（检索得到，请优先依据这些内容，并在回答里写上来源文件名）："]
    for i, row in enumerate(hits, start=1):
        parts.append(f"\n[{i}] 来源 {row['source']}  余弦 {row['score']:.4f}\n{row['text']}")
    parts.append(f"\n问题：{query}")
    return "\n".join(parts)


def main() -> None:
    query = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUERY
    k = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_K

    if not EMBED_KEY or not EMBED_BASE or not EMBED_MODEL:
        print("缺少 Embedding 配置。确认 day52/.env 里有 DASHSCOPE_API_KEY / EMBEDDING_BASE_URL / EMBEDDING_MODEL。")
        sys.exit(1)
    if not CHAT_KEY:
        print("缺少 DEEPSEEK_API_KEY。可放在项目一 .env 或 day52/.env。")
        sys.exit(1)
    if not EMB_PATH.exists():
        print(f"没有 {EMB_PATH}。先跑 day52 的 01_embed.py。")
        sys.exit(1)

    system = (
        "你是助手。有资料时只根据资料回答，并写上来源文件名（如 02.md）。"
        "资料不足就说不足，不要编造笔记里没有的标题或钩子。"
    )

    print("问句:", query)
    print(f"Chat: {CHAT_BASE}  模型 {CHAT_MODEL}")
    print("== 1/2 无检索（不把文档放进 user）==")
    no_rag = chat(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": query},
        ]
    )
    print(no_rag)
    print()

    hits = top_k(query, k)
    print(f"== 检索 top-{k} ==")
    for i, row in enumerate(hits, start=1):
        print(f"{i}. {row['source']}  余弦 {row['score']:.4f}")
    print()

    print("== 2/2 有检索（片段在本轮 user）==")
    yes_rag = chat(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": build_user_with_rag(query, hits)},
        ]
    )
    print(yes_rag)
    print()
    print("对比写进日志：有没有胡编、有没有点到 02.md / 你的钩子。不要贴密钥。")


if __name__ == "__main__":
    main()
