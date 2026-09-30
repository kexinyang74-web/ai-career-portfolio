"""Day 73：把 messages 里每一条的 role 印成中文标签。

循环沿用 Day 72 已跑通的那一版。你只补 print_roles 里还没写的三种标签。
说明见 笔记/Day73-ReAct对照消息角色.md。不要 print 密钥，不要用 LangGraph。
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
    print("没有读到 DEEPSEEK_API_KEY。请把 day72 或项目一的 .env 复制到本目录后再跑。")
    sys.exit(1)

FAKE_HOTSPOTS = {
    "科技": "「我用同一套提示词跑了 30 天」拆解：标题钩子是反差，不是工具清单。",
    "知识": "「30 岁转行学编程」评论区最高赞在问时间，不在问语言。",
    "生活": "「租房第一次验收」清单视频：完播靠的是逐项打勾，不是情绪。",
}


def lookup_hotspot(track: str) -> str:
    return FAKE_HOTSPOTS.get(track, f"没有「{track}」这条赛道的假数据。请换科技、知识或生活。")


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_hotspot",
            "description": "按赛道查一条写死的 B 站选题热点。只接受：科技、知识、生活。",
            "parameters": {
                "type": "object",
                "properties": {
                    "track": {
                        "type": "string",
                        "description": "赛道名，只能是 科技、知识、生活 之一",
                    }
                },
                "required": ["track"],
            },
        },
    }
]


def post_chat(messages: list) -> dict:
    url = f"{BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS,
        "temperature": 0,
        "stream": False,
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=120)
        response.raise_for_status()
    except requests.Timeout:
        print("超时。可先执行: $env:HTTPS_PROXY = 'http://127.0.0.1:7897'")
        sys.exit(1)
    except requests.HTTPError:
        print("HTTP 错误:", response.status_code)
        print(response.text[:800])
        sys.exit(1)
    except requests.RequestException as exc:
        print("请求失败:", exc)
        print("若是 SSL/连接问题，先设 HTTPS_PROXY=http://127.0.0.1:7897")
        sys.exit(1)

    data = response.json()
    return data["choices"][0]["message"]


def print_roles(messages: list) -> None:
    """从上到下打印：序号、role、中文标签。

    五种标签：规矩、用户的话、行动、观察、给用户的回答。
    assistant 有 tool_calls → 行动；没有 → 给用户的回答。
    """
    i = 0
    while i < len(messages):
        item = messages[i]
        role = item["role"]
        if role == "system":
            label = "规矩"
        elif role == "user":
            label = "用户的话"
        elif role == "tool":
            label = "观察"
        elif role == "assistant":
            if item.get("tool_calls"):
                label = "行动"
            else:
                label = "给用户的回答"
        print(i, role, label)
        i = i + 1


def main() -> None:
    messages = [
        {
            "role": "system",
            "content": "你是 B 站选题助手。需要赛道热点时必须调用 lookup_hotspot，不要凭空编选题。",
        },
        {"role": "user", "content": "今天科技赛道有什么值得写的选题？"},
    ]

    for step in range(1, 5):
        message = post_chat(messages)
        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            messages.append(message)
            print("--- 结束时的清单 ---")
            print_roles(messages)
            print("最终回答:", message.get("content"))
            return

        print(f"第 {step} 轮点名:", tool_calls[0]["function"]["name"], tool_calls[0]["function"]["arguments"])
        messages.append(message)
        raw = tool_calls[0]["function"]["arguments"]
        fields = json.loads(raw)
        track = fields["track"]
        tool_name = tool_calls[0]["function"]["name"]
        if tool_name == "lookup_hotspot":
            content = lookup_hotspot(track)
        else:
            content = "未知工具"
        messages.append(
            {"role": "tool", "tool_call_id": tool_calls[0]["id"], "content": content}
        )
        print(f"--- 第 {step} 轮工具交回之后的清单 ---")
        print_roles(messages)

    print("步数用尽，停。")


if __name__ == "__main__":
    main()
