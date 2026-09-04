# Day 31 多轮 messages（第 5 周第 3 天）

> 今天只改一件事：模型**没有跨请求的记忆**。能「接着聊」，是因为你把上一轮的 `assistant` 又塞回 `messages` 再 POST。代码在 `projects/python-practice/day31/`。密钥仍只在 `.env`。

## 一、单轮 vs 多轮

```
Day 30 一次 POST：
  [system, user]  →  回复 A

Day 31 两次 POST：
  第 1 次  [system, user1]                    → 回复 A
  你本地： messages.append(assistant=A)
           messages.append(user2)
  第 2 次  [system, user1, assistant A, user2] → 回复 B（能用到 A 和 user1）
```

项目一 `chat_repl` 就是这个列表：`history.append(user)` → `call_llm(history)` → `history.append(assistant)`。`/new` 把列表打回只剩 system。

## 二、今天要亲眼看见的两件事

1. **第二次问「我叫什么」时，模型能答出第一次你报的名字**（证明历史在 messages 里）。
2. **第二次的 `prompt_tokens` 比第一次大**（历史越长越贵，对应上下文窗口）。

对比实验（可选）：把 `append` 助手那两行注释掉再跑——第二次会像失忆。不要提交这个残废版，看完改回来。

## 三、步骤

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\python-practice\day31
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item ..\day30\.env .env
python 01_multi_turn.py
```

SSL 仍先：`$env:HTTPS_PROXY = "http://127.0.0.1:7897"`。

对照：`projects/project-1-ai-assistant/main.py` 里 `chat_repl` 的 `history.append`（约 149–154 行）。

## 四、做完

答 `笔记/Day31-自测5题.md`，填 `学习日志/2026-09-04-Day31-学习日志.md`。不要贴密钥。
