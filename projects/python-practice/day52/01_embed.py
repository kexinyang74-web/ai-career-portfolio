"""Day 52：把 Day 51 的切块调 Embedding API，打印维度和前几个数。

工作目录建议为本文件夹。不要 print 密钥。不上检索、不调 Chat。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

HERE = Path(__file__).resolve().parent
load_dotenv(HERE / ".env")

DOCS = HERE.parent / "day51" / "docs"
MIN_CHARS = 40
OUT = HERE / "embeddings.json"

API_KEY = (
    os.getenv("EMBEDDING_API_KEY")
    or os.getenv("DASHSCOPE_API_KEY")
    or os.getenv("DEEPSEEK_API_KEY")
    or ""
).strip()
BASE_URL = os.getenv("EMBEDDING_BASE_URL", "").strip().rstrip("/")
MODEL = os.getenv("EMBEDDING_MODEL", "").strip()


def split_by_paragraph(text: str) -> list[str]:
    parts = [p.strip() for p in text.split("\n\n")]
    return [p for p in parts if p]


def load_chunks() -> list[dict]:
    files = sorted(p for p in DOCS.glob("*.md") if not p.name.startswith("_"))
    rows: list[dict] = []
    skipped = 0
    for path in files:
        for i, chunk in enumerate(split_by_paragraph(path.read_text(encoding="utf-8"))):
            if len(chunk) < MIN_CHARS:
                skipped += 1
                continue
            rows.append({"source": path.name, "index": i, "text": chunk})
    print(f"文档目录: {DOCS}")
    print(f"可用切块 {len(rows)}（跳过短于 {MIN_CHARS} 字的 {skipped} 块，多半是标题）")
    return rows


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
        print("超时。检查网络；代理可先: $env:HTTPS_PROXY = 'http://127.0.0.1:7897'")
        sys.exit(1)
    except requests.HTTPError:
        print("HTTP 错误:", r.status_code)
        print(r.text[:800])
        print("确认 EMBEDDING_BASE_URL 指向 /embeddings 所在服务，模型名不是 deepseek-chat。")
        sys.exit(1)
    except requests.RequestException as exc:
        print("请求失败:", exc)
        sys.exit(1)

    data = r.json()
    vec = data["data"][0]["embedding"]
    if not isinstance(vec, list) or not vec:
        print("响应里没有 embedding 列表。完整 JSON 前 800 字:")
        print(json.dumps(data, ensure_ascii=False)[:800])
        sys.exit(1)
    return vec


def main() -> None:
    if not API_KEY or not BASE_URL or not MODEL:
        print("请复制 .env.example 为 .env，填 EMBEDDING_BASE_URL、EMBEDDING_MODEL 和密钥。")
        print("不要用项目一的 Chat 地址硬套（通常没有 /embeddings）。")
        sys.exit(1)

    chunks = load_chunks()
    if not chunks:
        print("没有切块。先确认 Day 51 的 docs 还在。")
        sys.exit(1)

    records = []
    for i, row in enumerate(chunks, start=1):
        vec = embed_one(row["text"])
        preview = [round(x, 5) for x in vec[:5]]
        print(f"{i}. {row['source']}#{row['index']}  维度 {len(vec)}  前5个数 {preview}")
        records.append(
            {
                "source": row["source"],
                "index": row["index"],
                "dim": len(vec),
                "text": row["text"],
                "embedding": vec,
            }
        )

    OUT.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
    print(f"已写入 {OUT.name}（已 gitignore，不要把密钥写进去）")
    print("今天到此：有向量即可。不要调 Chat、不要手写检索。")


if __name__ == "__main__":
    main()
