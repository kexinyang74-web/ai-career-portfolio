# Day 33 项目一骨架跑通（第 5 周第 5 天）

> 今天**不改人设**（那是 Day 34）。目标：用现成骨架 `projects/project-1-ai-assistant/main.py` 真正对话一次。Day 30-32 你手写的 POST / 多轮 / 流式，都已经装在这个文件里。

## 一、骨架和这三天的对应

| 你写过的 | 在 `main.py` 里 |
|---|---|
| Day 30 单轮 POST | `call_llm` + `ask_once`（`python main.py "一句话"`） |
| Day 31 `messages` 追加 | `chat_repl` 的 `history.append` |
| Day 32 SSE | `_consume_stream`；命令 `/stream` |
| `/new` | `history = [system]` |

人设文件是 `system_prompt.md`，今天先读一眼，**先别改**。

## 二、怎么跑（项目一目录）

你这边 venv 和 `.env` 多半已经有了。若没有，按 README 建。然后：

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\project-1-ai-assistant
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py "给我 1 个适合 B站 的转行编程选题，一句话。"
```

单次提问能打出一段中文 = 骨架通了。

再进交互（不带参数）：

```powershell
python main.py
```

试这几条（每条看终端提示）：

1. 随便问一句（人设还是模板里的 XX 行业，答得不像选题助手也正常）
2. `/stream` 再问一句（应变成交替蹦字）
3. `/save`（应出现 `chat_history.json`，这个文件已被 gitignore）
4. `/new` 再问「我刚才说了什么」——应接不上旧话题
5. `/exit` 退出

SSL 连不上仍先：`$env:HTTPS_PROXY = "http://127.0.0.1:7897"`。

README 里的路径 `outputs/projects/...` 是旧的，以你现在的 `projects\project-1-ai-assistant` 为准。

## 三、今天不要做

- 不要把密钥写进日志或发给我
- 不要大改 `main.py`（能跑就行；Day 34 才改 `system_prompt.md` 和 README 第一行）

## 四、做完

答 `笔记/Day33-自测5题.md`，填学习日志。把你试过的命令（`/stream` `/new` 等）写进「今天做了什么」。
