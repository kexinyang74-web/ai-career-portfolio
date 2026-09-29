# Day 73 给每一条消息起名字（第 11 周第 3 天）

> 昨天脚本已经跑通：第 1 轮点了 `lookup_hotspot`、参数是「科技」，第 2 轮回答里有「反差」。
> 今天不增加工具，不写 LangGraph。只做一件事：看着 `messages` 这条列表，给每一行起中文名。
> 代码在 `projects/python-practice/day73/01_print_roles.py`。密钥复制 day72 或项目一的 `.env`，不要 print、不要写进日志。

## 先把这几个词分开

昨天卡住的词，就这几对。每一对都是两样东西。

| 词 | 它是什么 | 你文件里的例子 |
|---|---|---|
| 列表 | 按顺序排的一串，用序号取。序号从 **0** 开始 | `tool_calls[0]` 是这一轮的第 1 条调用 |
| 字典 | 按名字存放的一张表，用名字取 | `b["track"]` 里的 `"track"` 是名字，不是第几个 |
| `append` | 在列表**末尾加一条**。不是命令行命令 | `messages.append(...)` |
| `tools` | 你事先交给模型的**菜单** | 文件里那个大写的 `TOOLS`，里面有名字、用途、参数 |
| `tool_calls` | 模型这一轮开出的**调用单**。没有这张单，就还没点菜 | 终端第 1 轮打印出来的那一段 JSON |
| `role` | 这一条是谁说的 | `system` / `user` / `assistant` / `tool` |
| `content` | 这一条的正文 | 给用户看的话，或工具返回的那句热点 |
| `arguments` | 调用单上的参数。拿下来时是**字符串** | `"{\"track\": \"科技\"}"` |
| `json.loads` | 把那段字符串变成字典，之后才能 `["track"]` | 你昨天写的那一行 |

`role` 和 `content` 长在 `messages` 的每一条上。它们不在 `tools` 菜单里。菜单里那三样是：`name`（名字）、`description`（用途）、`parameters`（参数长什么样）。

## 你这次运行，列表里实际有什么

用户那句是：「今天科技赛道有什么值得写的选题？」

**第 1 轮发去的时候**，列表里只有 2 条：

| 序号 | role | 中文名 |
|---|---|---|
| 0 | `system` | 规矩（必须调用工具，不要编） |
| 1 | `user` | 用户的话 |

模型交回来一份带 `tool_calls` 的消息。你的代码做了两件追加：

| 序号 | role | 中文名 | 里面有什么 |
|---|---|---|---|
| 2 | `assistant` | 行动 | 调用单：名字 `lookup_hotspot`，参数「科技」 |
| 3 | `tool` | 观察 | 假字典返回的那句，里面有「反差」 |

**第 2 轮**把这 4 条再发给模型。它这次没有 `tool_calls`，只有给用户看的正文。这条也要 `append` 进列表，否则清单停在「观察」，少了最后一句人话。

| 序号 | role | 中文名 |
|---|---|---|
| 4 | `assistant` | 给用户的回答 |

有 `tool_calls` 的那一轮，就算同时有 `content` 这个键，也先执行工具。没有 `tool_calls` 才算结束。

## ReAct 三个词，对上表里的三行

教材把这一圈叫 ReAct。三个英文词就是上面三行的别名：

| 教材里的词 | 意思 | 对上你的列表 |
|---|---|---|
| Thought（想） | 还要不要调工具 | 接口里**没有**单独一格叫 Thought。你能看见的决定就是：这一轮有没有 `tool_calls` |
| Action（行动） | 点了哪个工具、参数是什么 | 序号 2，`role=assistant` 且带着 `tool_calls` |
| Observation（观察） | 工具实际返回的文字 | 序号 3，`role=tool` 的 `content` |

想完再行动，行动完把观察交回去，再想一次。第 2 轮它不再行动，直接把序号 4 交给用户。

## 今天你写的那一个函数

`01_print_roles.py` 里的循环是昨天那份。你只补 `print_roles`：从上到下看 `messages`，每条打印「序号、role、中文标签」。

五种标签固定用这些词：规矩、用户的话、行动、观察、给用户的回答。

`system` 和 `user` 两种已经写好，照着写另外三种。`assistant` 要再看一眼这条里有没有 `tool_calls`：有就是「行动」，没有就是「给用户的回答」。

跑通后，终端里应能看到两段清单：

- 第 1 轮工具交回之后：0 规矩、1 用户的话、2 行动、3 观察
- 结束时：上面四条还在，多一条 4 给用户的回答

## 命令

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\python-practice\day73
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item ..\day72\.env .env
$env:HTTPS_PROXY = "http://127.0.0.1:7897"
python 01_print_roles.py
```

## 明确不做

- 不加第二个工具（那是明天以后）
- 不写 LangGraph
- 不改项目一、项目二
- 不把密钥写进日志

## 做完

用自己的话填 [[2026-09-30-Day73-学习日志]] 三栏，再答 [[Day73-自测5题]]。说「收尾」再批。
