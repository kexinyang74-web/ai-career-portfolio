"""Day 29：先看清明天要 POST 的 JSON 长什么样（不发网络）。

粗算 token：中文约 1 字 ≈ 1 token，英文约 4 字符 ≈ 1 token。
这只是直觉，不是官方分词器；明天看响应里的 usage 才是准的。
"""
import json

messages = [
    {
        "role": "system",
        "content": "你是面向 B站 创作者的选题与脚本助手。用中文。先给结论。",
    },
    {"role": "user", "content": "给我 3 个「转行学编程」的视频选题。"},
]


def 粗算token(text: str) -> int:
    n = 0
    buf = []
    for ch in text:
        if "\u4e00" <= ch <= "\u9fff":
            if buf:
                n += max(1, len("".join(buf)) // 4)
                buf = []
            n += 1
        else:
            buf.append(ch)
    if buf:
        n += max(1, len("".join(buf)) // 4)
    return n


payload = {
    "model": "deepseek-chat",
    "messages": messages,
    "temperature": 0.7,
    "stream": False,
}

print("明天 POST 的 body 大概是：")
print(json.dumps(payload, ensure_ascii=False, indent=2))

全部文字 = "".join(m["content"] for m in messages)
print("\n粗算 prompt token ≈", 粗算token(全部文字))
print("（真实值看 API 返回的 usage.prompt_tokens）")
