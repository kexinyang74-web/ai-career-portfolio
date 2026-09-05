"""Day 38：json_object + messages 里明确要求 JSON。

工作目录必须是本文件夹。不要 print 密钥。
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
    print("没有读到 DEEPSEEK_API_KEY。请把项目一的 .env 复制到本目录。")
    sys.exit(1)

url = f"{BASE_URL}/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}
payload = {
    "model": MODEL,
    "messages": [
        {
            "role": "system",
            "content": "你只输出 JSON，不要 Markdown，不要解释。",
        },
        {
            "role": "user",
            "content": (
                "输出一个 JSON 对象，键 items 是数组，恰好 2 个元素。"
                "每个元素键必须是 title、hook、fit（均为字符串）。"
                "赛道：转行学编程。fit 用一句话说为何像生活记录。"
            ),
        },
    ],
    "temperature": 0.7,
    "stream": False,
    "response_format": {"type": "json_object"},
}

try:
    r = requests.post(url, json=payload, headers=headers, timeout=120)
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

text = r.json()["choices"][0]["message"]["content"]
print("原始 content:")
print(text)
print("---")
try:
    obj = json.loads(text)
except json.JSONDecodeError as exc:
    print("解析失败:", exc)
    sys.exit(1)
print("解析成功，类型:", type(obj).__name__)
print("顶层键:", list(obj) if isinstance(obj, dict) else "(不是对象)")
print(json.dumps(obj, ensure_ascii=False, indent=2))
