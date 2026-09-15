# Day 60 VectorStore / RetrievalQA（第 9 周第 4 天）

> 昨天 Loader / Splitter 只到切块。今天接上后两步：查库、再问答。仍用 `day57/chroma_db/`，不重切、不重 embed 那 10 篇。不建 `project-2-rag/`（那是 Day 61）。

## 今天目的（先看这里）

**把四个词收齐**，对上你已经手写过的流水线。不是新做一个 RAG。

| LangChain 名字 | 你已经写过的 | 哪天 |
|---|---|---|
| Loader | `glob` + `read_text` | Day 51 / 59 |
| TextSplitter | 按空行 / 定长切 | Day 51 / 59 |
| **VectorStore** | `01_search.py` 余弦 / Day 57 Chroma `query` | **今天 1/2** |
| **RetrievalQA** | `01_rag_chat.py`：片段塞进 `user` 再 Chat | **今天 2/2** |

`RetrievalQA` 是旧教材里的**一键链**名字。新版 LangChain 不推荐再抄 `RetrievalQA.from_chain_type`。它干的事拆开就是三步：**检索 → 拼进本轮 user → Chat**。今天脚本把这三步写在明处，你才能讲，而不是只会一个函数名。

VectorStore 负责「问句变向量，按距离取 top-k」。Chat 仍然看不见磁盘上的 `chroma_db`，除非你把片段放进 `messages`。

## 脚本在干什么

1. 打开昨天用过的集合 `bilibili_notes`（约 10 条）。
2. `similarity_search_with_score`：对照手写 top-k。Chroma 的 **score 越小越近**。
3. 把命中片段写进 **本轮 `HumanMessage`（就是 user）**，再 `ChatOpenAI` 调 DeepSeek。规则仍在 system。

Embedding 仍是百炼（`DashScopeEmbeddings` 只是包了一层你 Day 52 的 `/embeddings`）。Chat 仍是 DeepSeek，两套 Key 不要混。

## 今天你做

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\python-practice\day60
pip install -r requirements.txt
python 01_vectorstore_qa.py
```

代理需要则设 `HTTPS_PROXY`。若提示没有 chroma_db，先回 day57 跑 `python 01_chroma.py`。

看两件事：1/2 有没有 `02.md`；2/2 回答有没有引用文件名、有没有用你的钩子。

## 明确不做

- 不重跑 10 篇 Embedding、不写 rerank、不加 `where`（除非你自己加着玩）
- 不建项目二目录、不提交 `.env` / `chroma_db`

## 做完

答 [[Day60-自测5题]]。说「收尾」再批。
