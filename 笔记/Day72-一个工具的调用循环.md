# Day 72 一个工具的调用循环（第 11 周第 2 天）

> 昨天只画了四步。今天用 `requests` 把这一圈跑通：**1 个本地假工具**，不用 LangGraph，不接真网页。
> 代码在 `projects/python-practice/day72/01_one_tool.py`。密钥沿用项目一，只放在本目录 `.env`，不要 print、不要发给我。

## 今天多出来的那一块

Day 30 的 POST 你已经会：`model` + `messages` → `choices[0].message.content`。

今天的 body 多一个字段 `tools`（工具清单）。模型回的 `message` 就有两种结局：

| 这一轮看到什么 | 你做什么 |
|---|---|
| 有 `tool_calls` | 还没结束。你执行函数，把结果塞回 `messages`，再 POST |
| 没有 `tool_calls`，有 `content` | 这才是给用户看的回答，循环停 |

`tool_calls` 是**列表**。今天只取第 0 个。`function.arguments` 是 **JSON 字符串**，要用 `json.loads` 变成字典，再传给 Python 函数。

## 假工具（数据写死，方便你核对）

函数名 `lookup_hotspot`，只收一个参数 `track`。字典里只有三条：

- 科技 → 句子里有「反差」
- 知识 → 句子里有「时间」
- 生活 → 句子里有「打勾」

用户问「今天科技赛道有什么值得写的选题？」跑通之后，最终回答里应出现「反差」。出现了，说明它用的是你交回去的观察；没出现、也没打印过 `tool_calls`，就是它没调工具、自己编的。

## 你要补的四步（都在 `for` 循环里）

骨架已经能发出带 `tools` 的请求，并打印模型点名。`raise NotImplementedError` 那一行删掉，换成：

1. **追加 assistant**：把这一轮的 `message` 原样放进 `messages`（里面带着 `tool_calls`）。
2. **解析参数**：`tool_calls[0]["function"]["arguments"]` 做 `json.loads`，取出 `track`。
3. **你执行**：只有名字是 `lookup_hotspot` 才调用函数。未知赛道函数会返回「没有这条赛道……」，这段文字也要交回去。
4. **追加 tool 结果**：

```text
{"role": "tool", "tool_call_id": "<刚才那个 id>", "content": "<函数返回的字符串>"}
```

`tool_call_id` 必须对上 `tool_calls[0]["id"]`。然后循环回到 `post_chat`。最多 4 轮，防止它一直点名。

## 命令

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\python-practice\day72
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item ..\..\project-1-ai-assistant\.env .env
$env:HTTPS_PROXY = "http://127.0.0.1:7897"
python 01_one_tool.py
```

终端里应先后看到：一轮 `tool_calls`（名字 `lookup_hotspot`，参数里有科技），然后一行「最终回答」，正文里有「反差」。

## 明确不做

- 不装、不写 `langgraph`
- 不接真热点网页（假字典就是今天的工具）
- 不改项目一、项目二
- 不把 `.env` 写进日志、不提交密钥

## 做完

用自己的话填 [[2026-09-29-Day72-学习日志]] 三栏，再答 [[Day72-自测5题]]。说「收尾」再批。
