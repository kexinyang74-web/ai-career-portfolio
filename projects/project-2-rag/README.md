# 项目二：行业知识库 RAG 问答（命令行 MVP）

> 面向 **B站创作者** 的 AI 应用 —— 爆款案例库问答

用约 10 篇爆款拆解笔记做检索，回答时写出来源文件名（如 `02.md`）。本仓库入口是 CLI；网页、FAISS 默认库、GraphRAG 都不在本项目里。

## 它干什么

提问 → Chroma 取 top-k 片段 → 塞进**本轮 `user`** → DeepSeek Chat → 打印来源。

默认**不重新 Embedding**，直接读 `projects/python-practice/day57/chroma_db/`（集合 `bilibili_notes`）。密钥可沿用项目一 / `day52/.env`，也可复制 `.env.example` 为本目录 `.env`。

**不要推到 GitHub：** `.env`、`chroma_db/`（本目录 `.gitignore` 已写；练习目录里的向量库也不要提交）。

## 架构

切分和入库在练习脚本里做完；本目录只做检索 + 问答。

1. **Load / Split**：`day51/docs` 约 10 篇 markdown → 按块切分（Day 57 写入时的切分）
2. **Embed**：阿里云百炼 `text-embedding-v3`（问句检索时也会 embed；**不要把 Chat 的 Key / 模型填进 Embedding**）
3. **VectorStore**：Chroma 持久化，`collection = bilibili_notes`
4. **Retrieve**：相似度 top-k（CLI 默认 **k=5**）；`--source 02.md` 时先按 metadata 过滤再排名
5. **Stuff**：命中片段拼进本轮 `HumanMessage`；人设和「资料不足就说不足」在 **system**，不把整库塞进 system
6. **Chat**：DeepSeek `deepseek-chat`；终端打印回答和来源文件名

`--no-rag` 跳过 4–5，只把问句发给 Chat，用来对比「没有笔记时会不会编」。

```text
问句 ──► Embed ──► Chroma top-k ──► 拼进 user ──► DeepSeek
              ▲
              └── day57/chroma_db（已写入，CLI 默认不重建）
```

## 运行

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\project-2-rag
pip install -r requirements.txt
$env:HTTPS_PROXY = "http://127.0.0.1:7897"
python main.py
python main.py "30岁转行学编程晚不晚？根据笔记回答并写上来源。"
python main.py "只根据转行那篇回答" --source 02.md
python main.py "30岁转行学编程晚不晚？" --no-rag
python main.py "……" -k 3
```

没有 `chroma_db` 时先：

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\python-practice\day57
python 01_chroma.py
```

**两个默认 k 不一样：**

| 入口 | 默认 k | 原因 |
| --- | --- | --- |
| `main.py`（日常问答） | **5** | 评测第 24 条在 k=3 时漏了 `02.md`，k=5 召回；第 1 条主答仍黏在 `02.md` |
| `eval_run.py`（评测脚本） | **3** | 保住 k=3 基线文件 `eval/运行记录.md`，避免随手 `--all` 覆盖 |

只要某一篇仍用 `--source`，不要靠把 k 加很大。对照基线请显式 `-k 3`。

## 使用示例

有 RAG（检索到 `02.md` 等，回答依据笔记并写文件名）：

```text
问：30岁转行学编程晚不晚？根据笔记回答并写上来源。
答：依据 02.md ……笔记没有替视频下「晚/不晚」的最终结论……
来源：02.md
```

`--no-rag`：同一问句不读库，模型只靠参数知识，**不能**当作拆解笔记里的结论。

## 评测

表：`eval/评测集.md`（30 条）。两个指标分开记：

- **可接受**：内容依据笔记、不胡编标题/钩子；资料不足时明确说不足也算
- **引用命中**：回答里的来源对得上「预期来源」；预期为「无」时不要编造 `xx.md`

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\project-2-rag
$env:HTTPS_PROXY = "http://127.0.0.1:7897"
python eval_run.py --all -k 3 --out eval/运行记录.md
python eval_run.py --all -k 5 --out eval/运行记录-k5.md
python eval_run.py --ids 24 -k 5 --out eval/运行记录-k5-q24.md
```

调 k 时必须另存 `--out`，**不要覆盖** `eval/运行记录.md`（k=3 基线）。脚本默认 `-k 3`、默认写出路径就是这份基线。

### 已跑数字（2026-09-18，约 10 篇库）

| | k=3（`eval/运行记录.md`） | k=5（`eval/运行记录-k5.md`） |
| --- | --- | --- |
| 可接受（人工） | **29/30 = 97%**（否：第 24 条） | 第 24 条召回 `02.md`；第 1 条主答未被带跑。未逐条重勾全部可接受 |
| 引用命中（人工 / k=3） | **29/30 = 97%**（否：第 24 条） | — |
| 引用命中（脚本自动） | 27/30 | **28/30**（第 24 条变为是；28、29 脚本仍因回答里出现检索到的文件名打否） |

第 24 条 k=3 检索：`10.md` / `05.md` / `01.md`（漏 `02.md`）。k=5：`10` / `05` / `01` / **`02`** / `04`。

可接受目标 ≥ 70%（规格书）；当前 k=3 人工已高于该线。

## 密钥

两套，不要对调：

- Chat：`DEEPSEEK_API_KEY`（`CHAT_BASE_URL` / `CHAT_MODEL`）
- Embedding：`DASHSCOPE_API_KEY` 或 `EMBEDDING_API_KEY`（`EMBEDDING_BASE_URL` / `EMBEDDING_MODEL=text-embedding-v3`）

模板见 `.env.example`。需要代理时设置 `HTTPS_PROXY`（上面示例是本机端口，按你的客户端改）。

## 目录

```text
project-2-rag/
├─ main.py              ← CLI 问答
├─ eval_run.py          ← 按评测表跑批次（默认 k=3）
├─ eval/
│  ├─ 评测集.md
│  ├─ 运行记录.md       ← k=3 基线，勿随手覆盖
│  └─ 运行记录-k5.md
├─ requirements.txt
├─ .env.example
└─ .gitignore           ← .env、chroma_db/
```

向量库实际在 `../python-practice/day57/chroma_db/`。对照课：`day60/01_vectorstore_qa.py`（同一条流水线，本目录加上可传问句、`--source`、`--no-rag`）。

## 明确不做（本周）

不上网页、不把默认库换成 FAISS、不建 GraphRAG / 知识图谱。切分策略能讲清即可；小库不必为了调参强行重 embed。
