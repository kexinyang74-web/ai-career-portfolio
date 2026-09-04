"""Day 30：单轮非流式 Chat Completions（先跑通，再改 user 那句话）。

工作目录必须是本文件夹，这样 load_dotenv() 才能读到这里的 .env。
不要 print 密钥。
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
    print("没有读到 DEEPSEEK_API_KEY。请把项目一的 .env 复制到本目录后再跑。")
    sys.exit(1)

url = f"{BASE_URL}/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}
payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "你是简洁的中文助手，用两三句话回答。"},
        {"role": "user", "content": "用一句话说什么是 token。"},
    ],
    "temperature": 0.7,
    "stream": False,
}

try:
    r = requests.post(url, json=payload, headers=headers, timeout=120)
    r.raise_for_status()
except requests.Timeout:
    print("超时。检查网络；代理环境可先执行: $env:HTTPS_PROXY = 'http://127.0.0.1:7897'")
    sys.exit(1)
except requests.HTTPError:
    print("HTTP 错误:", r.status_code)
    print(r.text[:800])
    sys.exit(1)
except requests.RequestException as exc:
    print("请求失败:", exc)
    print("若是 SSL/连接问题，先设 HTTPS_PROXY=http://127.0.0.1:7897")
    sys.exit(1)

data = r.json()
print("状态码:", r.status_code)
print("完整 JSON:")
print(json.dumps(data, ensure_ascii=False, indent=2))
print("---")
print("回复:", data["choices"][0]["message"]["content"])
usage = data.get("usage") or {}
print("prompt_tokens:", usage.get("prompt_tokens"))
print("completion_tokens:", usage.get("completion_tokens"))
print("total_tokens:", usage.get("total_tokens"))
