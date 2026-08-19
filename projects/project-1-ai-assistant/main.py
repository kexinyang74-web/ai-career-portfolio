"""项目一：行业场景 AI 助手（命令行版）

基于大模型 API 的多轮对话助手，支持流式输出、行业人设、对话保存。
默认对接 DeepSeek API（可切换任意 OpenAI 兼容接口）。
"""

import argparse
import json
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://api.deepseek.com").rstrip("/")
MODEL = os.getenv("MODEL", "deepseek-chat")
API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEFAULT_TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYSTEM_PROMPT_FILE = os.path.join(BASE_DIR, "system_prompt.md")
HISTORY_FILE = os.path.join(BASE_DIR, "chat_history.json")


def load_system_prompt() -> str:
    """读取 system_prompt.md；不存在时使用默认人设。"""
    if os.path.exists(SYSTEM_PROMPT_FILE):
        with open(SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return content
    return "你是一个乐于助人的 AI 助手，请用中文回答问题。"


def call_llm(
    messages: list[dict],
    temperature: float = DEFAULT_TEMPERATURE,
    stream: bool = False,
) -> str:
    """调用 OpenAI 兼容的 /chat/completions 接口，返回模型回复文本。"""
    if not API_KEY:
        print(
            "[错误] 未配置 DEEPSEEK_API_KEY。"
            "请复制 .env.example 为 .env 并填入密钥。",
            file=sys.stderr,
        )
        sys.exit(1)

    url = f"{BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "stream": stream,
    }

    try:
        response = requests.post(
            url, json=payload, headers=headers, timeout=120, stream=stream
        )
        response.raise_for_status()
    except requests.Timeout:
        print("[错误] 请求超时，请检查网络后重试。", file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as exc:
        print(f"[错误] API 请求失败：{exc}", file=sys.stderr)
        sys.exit(1)

    if stream:
        return _consume_stream(response)

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        print(f"[错误] 响应解析失败：{data}", file=sys.stderr)
        sys.exit(1)


def _consume_stream(response) -> str:
    """读取流式响应并实时打印，返回完整内容。"""
    chunks: list[str] = []
    for line in response.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data:"):
            continue
        data = line[len("data:"):].strip()
        if data == "[DONE]":
            break
        try:
            piece = json.loads(data)["choices"][0]["delta"].get("content", "")
        except (json.JSONDecodeError, KeyError, IndexError):
            continue
        if piece:
            chunks.append(piece)
            print(piece, end="", flush=True)
    print()
    return "".join(chunks)


def save_history(messages: list[dict]) -> None:
    """把当前对话历史保存为 JSON 文件。"""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


def chat_repl() -> None:
    """交互模式：多轮对话。"""
    system = {"role": "system", "content": load_system_prompt()}
    history: list[dict] = [system]
    stream = False

    print("=" * 52)
    print("行业场景 AI 助手")
    print(f"模型：{MODEL} ｜ 流式：{'开' if stream else '关'}")
    print("命令：/new 清空对话 ｜ /stream 切换流式 ｜ /save 保存 ｜ /exit 退出")
    print("=" * 52)

    while True:
        try:
            user_input = input("\n你 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not user_input:
            continue
        if user_input in ("/exit", "/quit"):
            print("再见！")
            break
        if user_input == "/new":
            history = [system]
            print("[已清空对话历史]")
            continue
        if user_input == "/stream":
            stream = not stream
            print(f"[流式输出 {'开' if stream else '关'}]")
            continue
        if user_input == "/save":
            save_history(history)
            print(f"[对话已保存到 {HISTORY_FILE}]")
            continue

        history.append({"role": "user", "content": user_input})
        print("AI > ", end="", flush=True)
        reply = call_llm(history, stream=stream)
        if not stream:
            print(reply)
        history.append({"role": "assistant", "content": reply})


def ask_once(prompt: str) -> None:
    """单次问答模式：python main.py \"你的问题\"。"""
    messages = [
        {"role": "system", "content": load_system_prompt()},
        {"role": "user", "content": prompt},
    ]
    print(call_llm(messages, stream=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="行业场景 AI 助手")
    parser.add_argument("prompt", nargs="?", help="单次提问内容；不填则进入交互模式")
    args = parser.parse_args()

    if args.prompt:
        ask_once(args.prompt)
    else:
        chat_repl()


if __name__ == "__main__":
    main()

