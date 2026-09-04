"""Day 31：两次 POST，第二次带上第一轮的 assistant。

工作目录必须是本文件夹。不要 print 密钥。
"""
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
BASE_URL = os.getenv("BASE_URL", "https://api.deepseek.com").rstrip("/")
MODEL = os.getenv("MODEL", "deepseek-chat")

if not API_KEY:
    print("没有读到 DEEPSEEK_API_KEY。请把 day30 的 .env 复制到本目录后再跑。")
    sys.exit(1)

url = f"{BASE_URL}/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def 发一轮(messages: list[dict]) -> tuple[str, dict]:
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "stream": False,
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
    data = r.json()
    text = data["choices"][0]["message"]["content"]
    usage = data.get("usage") or {}
    return text, usage


messages = [
    {"role": "system", "content": "你是简洁的中文助手。用户报过名字就要记住。"},
    {"role": "user", "content": "我的名字是小周。请回复一个字：好"},
]

print("=== 第 1 次 POST，messages 条数:", len(messages), "===")
reply1, usage1 = 发一轮(messages)
print("回复1:", reply1)
print("prompt_tokens:", usage1.get("prompt_tokens"),
      "completion_tokens:", usage1.get("completion_tokens"))

# 多轮的关键两行（注释掉再跑 = 第二次会像失忆）
messages.append({"role": "assistant", "content": reply1})
messages.append({"role": "user", "content": "我叫什么名字？只回答名字。"})

print("\n=== 第 2 次 POST，messages 条数:", len(messages), "===")
print("当前 roles:", [m["role"] for m in messages])
reply2, usage2 = 发一轮(messages)
print("回复2:", reply2)
print("prompt_tokens:", usage2.get("prompt_tokens"),
      "completion_tokens:", usage2.get("completion_tokens"))
