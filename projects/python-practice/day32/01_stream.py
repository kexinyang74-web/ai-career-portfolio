"""Day 32：流式 POST，按行读 data:，拼 delta.content。

工作目录必须是本文件夹。不要 print 密钥。
对照项目一 main.py 的 _consume_stream。
"""
import json
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
BASE_URL = os.getenv("BASE_URL", "https://api.deepseek.com").rstrip("/")
MODEL = os.getenv("MODEL", "deepseek-chat")

if not API_KEY:
    print("没有读到 DEEPSEEK_API_KEY。请把 day31 的 .env 复制到本目录后再跑。")
    sys.exit(1)

url = f"{BASE_URL}/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}
payload = {
    "model": MODEL,
    "messages": [
        {"role": "user", "content": "用四句短句介绍什么是流式输出。"},
    ],
    "temperature": 0.7,
    "stream": True,
}

try:
    r = requests.post(url, json=payload, headers=headers, timeout=120, stream=True)
    r.raise_for_status()
except requests.Timeout:
    print("超时。可先: $env:HTTPS_PROXY = 'http://127.0.0.1:7897'")
    sys.exit(1)
except requests.HTTPError:
    print("HTTP 错误:", r.status_code)
    print(r.text[:800])
    sys.exit(1)
except requests.RequestException as exc:
    print("请求失败:", exc)
    sys.exit(1)

print("AI > ", end="", flush=True)
chunks: list[str] = []
for line in r.iter_lines(decode_unicode=True):
    if not line or not line.startswith("data:"):
        continue
    data = line[len("data:"):].strip()
    if data == "[DONE]":
        break
    try:
        piece = json.loads(data)["choices"][0]["delta"].get("content") or ""
    except (json.JSONDecodeError, KeyError, IndexError):
        continue
    if piece:
        chunks.append(piece)
        print(piece, end="", flush=True)

print()
print("---")
print("完整回复:", "".join(chunks))
