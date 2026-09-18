# Day 61 项目二 MVP CLI（第 9 周第 5 天）

> 把 Day 60 那条链放进 `projects/project-2-rag/`。仍用现有约 10 篇和 `day57/chroma_db`。不凑 40 篇、不写 30 条评测、不上网页、不上 FAISS（明天）。

## 今天目的

**一条命令能问、能答、能打印来源文件名。** 这就是项目二 CLI 雏形。不是新发明一套 RAG。

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\project-2-rag
pip install -r requirements.txt
$env:HTTPS_PROXY = "http://127.0.0.1:7897"
python main.py "30岁转行学编程晚不晚？根据笔记回答并写上来源。"
```

对照再跑一次无检索：

```powershell
python main.py "30岁转行学编程晚不晚？" --no-rag
```

只要某一篇（Day 58 的过滤）：

```powershell
python main.py "只根据转行那篇回答" --source 02.md
```

看：有 RAG 时来源里有没有 `02.md`；`--no-rag` 时给不给得出文件名。

## 四个词还在这条命令里

Loader / Splitter 已经发生在 day51–59；今天 CLI 主要跑 **VectorStore + 拼 user + Chat**（旧名 RetrievalQA）。

## 明确不做

- 不写 30 条评测、不改项目一人设、不部署、不 push `.env` / `chroma_db`

## 做完

答 [[Day61-自测5题]]。说「收尾」再批。Day 60 若还没正式收尾，也可以之后补一句「Day 60 收尾」。
