# 项目二：行业知识库 RAG 问答（命令行 MVP）

> 面向 **B站创作者** 的 AI 应用 —— 爆款案例库问答

用你第 8–9 周那约 10 篇拆解笔记做检索，回答时打印来源文件名（如 `02.md`）。
第 10 周再凑文档、写 30 条评测；今天不做网页、不做 FAISS。

## 它干什么

提问 → 向量库检索（Chroma）→ 片段塞进本轮 `user` → DeepSeek Chat → 打印来源。

默认**不重新 Embedding**，直接读 `python-practice/day57/chroma_db/`。密钥可沿用项目一 / `day52/.env`，也可复制 `.env.example` 为本目录 `.env`。不要把 `.env` 推到 GitHub。

## 运行

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\project-2-rag
pip install -r requirements.txt
$env:HTTPS_PROXY = "http://127.0.0.1:7897"
python main.py
python main.py "30岁转行学编程晚不晚？根据笔记回答并写上来源。"
python main.py "只根据转行那篇回答" --source 02.md
python main.py "30岁转行学编程晚不晚？" --no-rag
```

没有库时先：`cd ..\python-practice\day57` 然后 `python 01_chroma.py`。

## 和练习脚本的关系

`day60/01_vectorstore_qa.py` 是对照课。本目录是给简历用的项目入口：同一条流水线，改成可传问句、可 `--source`、可 `--no-rag`。
