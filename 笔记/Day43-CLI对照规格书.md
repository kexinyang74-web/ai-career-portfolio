# Day 43 项目一 CLI 对照规格书（第 7 周第 1 天）

> 第 6 周管 prompt。这周管 **交得出去**。今天只点名功能，**不改 README、不写 STAR、不录视频**。Day 42 休息跳过。

对照 [[03-项目三件套规格书]] 项目一「必须功能」。代码在 `projects/project-1-ai-assistant/main.py`。

## 规格 vs 现状（供你亲手验证，不要只看这张表打勾）

| 必须功能 | 代码里大概在哪 | 你今天要做的 |
|---|---|---|
| 多轮对话 | `chat_repl` 把 user/assistant 追加进 `history` | `python main.py` 连问两句，第二句应接得上第一句 |
| 流式开关 | `/stream` | 开一次，看字是否逐段出来 |
| 行业人设 | `system_prompt.md` → `load_system_prompt` | 糊一句「帮我想选题」，应仍是 B站/转行人设，不是电商 |
| 清空 / 保存 | `/new`、`/save` | `/new` 后再问，不应再提上一轮细节；`/save` 生成 `chat_history.json`（此文件不进 git） |
| 错误处理 | 无密钥 `sys.exit`；超时 / `RequestException` | 今天不必故意删密钥；知道报错会退出即可 |

**缺口：** 规格简历句写了「错误重试」。现在超时/失败是打印后 **退出**，不会自动再 POST 一次。今天验收后在日志里写一句：本周要不要加有限次重试（例如超时重试 1 次）。要加再说，我按你的验收改，不提前改 `main.py`。

## 操作（项目一目录、venv 已激活）

```powershell
python main.py
```

建议顺序：一句选题 → 追问改条数 → `/stream` → 再问一句 → `/save` → `/new` → 再问一句看是否清空 → `/exit`。

PowerShell 单行提问仍避免 user 里套英文 `"`（Day 39）。交互模式粘贴更稳。

## 明确不做

- 不改 README 定位句、不写 STAR、不上 RAG
- 不提交 `.env`、不把密钥贴进聊天或日志

## 做完

答 `笔记/Day43-自测5题.md`；日志写下：哪些命令实际跑过、要不要加重试。
