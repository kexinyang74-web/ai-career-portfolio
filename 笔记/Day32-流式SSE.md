# Day 32 流式输出 SSE（第 5 周第 4 天）

> 今天把 Day 30 的 `stream: false` 改成 `true`。回复不再是一整份 JSON，而是一行行 `data:`。代码在 `projects/python-practice/day32/`。对照项目一 `main.py` 的 `_consume_stream`（约 86–103 行）。

## 一、两处必须一起改

| | 非流式（Day 30） | 流式（今天） |
|---|---|---|
| body | `"stream": false` | `"stream": true` |
| requests | `requests.post(...)` | **还要** `stream=True`（让响应不要一次读完） |
| 取字 | `data["choices"][0]["message"]["content"]` | 每一片 `delta.content`，拼到 `[DONE]` |

只改 JSON 里的 `stream`、忘了 `requests.post(..., stream=True)`，有的环境下会卡住或看起来像没输出。

## 二、一行长什么样

```
data: {"choices":[{"delta":{"content":"你"}}]}
data: {"choices":[{"delta":{"content":"好"}}]}
data: [DONE]
```

完整回复 = 把每片 `content` 拼起来。`print(piece, end="", flush=True)` 才能边到边显示。

空行、不是 `data:` 开头的行直接跳过。`delta` 里可能没有 `content`（例如只有 role），用 `.get("content", "")`。

## 三、步骤

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\python-practice\day32
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item ..\day31\.env .env
python 01_stream.py
```

验收：字是一个个蹦出来的（不是等很久突然一整段）；最后有一行「完整回复: ……」。SSL 仍用 `$env:HTTPS_PROXY = "http://127.0.0.1:7897"`。

## 四、做完

答 `笔记/Day32-自测5题.md`，填学习日志。不要贴密钥。
