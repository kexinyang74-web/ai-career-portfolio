"""Day 72：一个工具的 Function Calling 循环。

骨架负责：读 .env、带上 tools 发 POST、打印模型点名。
for 循环里四步由你写，写完删掉 NotImplementedError。
说明见 笔记/Day72-一个工具的调用循环.md。不要 print 密钥，不要用 LangGraph。
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

FAKE_HOTSPOTS = {
    "科技": "「我用同一套提示词跑了 30 天」拆解：标题钩子是反差，不是工具清单。",
    "知识": "「30 岁转行学编程」评论区最高赞在问时间，不在问语言。",
    "生活": "「租房第一次验收」清单视频：完播靠的是逐项打勾，不是情绪。",
}


def lookup_hotspot(track: str) -> str:
    """本地假数据。未知赛道也要返回一段文字，交给模型，不要在这里假装成功。"""
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
    """发一次 /chat/completions，返回 choices[0].message 这个字典。"""
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
        print(f"第 {step} 轮 message 的键:", list(message.keys()))
        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            print("最终回答:", message.get("content"))
            return

        print("模型点名:", json.dumps(tool_calls, ensure_ascii=False, indent=2))

        # 删掉下一行，按笔记补四步：
        # 1. messages 追加这条 assistant（message 原样放进去）
        # 2. json.loads(tool_calls[0]["function"]["arguments"])，取出 track
        # 3. 名字是 lookup_hotspot 才调用；否则 content 写「未知工具」
        # 4. messages 追加 role=tool，带 tool_call_id 和函数返回的字符串
        raise NotImplementedError("先完成笔记里的四步，再删掉这一行")

    print("步数用尽，停。最后一条 content:", messages[-1].get("content"))


if __name__ == "__main__":
    main()
