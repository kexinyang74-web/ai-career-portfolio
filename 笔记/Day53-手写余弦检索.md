# Day 53 手写余弦检索（第 8 周第 4 天）

> 问句也变成向量，和 Day 52 的切块比余弦，取出最像的 k 块。不调 Chat、不上 LangChain/Chroma。密钥继续用 `day52/.env`，不要贴到对话里。

库文件：`projects/python-practice/day52/embeddings.json`（没有就先回 Day 52 重跑 `01_embed.py`）  
代码：`projects/python-practice/day53/01_search.py`

## 今天必须能讲清

问句和文档必须走**同一家 Embedding、同一个模型**，否则维度可能对不上，方向也不可比。

余弦相似度（本周手写，不要用框架）：

\[
\cos\theta = \frac{a\cdot b}{|a|\,|b|}
\]

点积除以两个模长。越接近 1 越同向（越相关），不是「向量里的数越大越相关」。这就是 Day 50 说的「先查」：查的是切块，不是把 JSON 丢给 Chat。

top-k：按余弦从高到低取前 k 名。k=1 只留最像的一块，可能漏掉并列相关的篇；k 太大又接近把库全塞回去。今天用 k=3 即可。

本周的「向量库」就是这份 JSON 列表：存了 `source`、`text`、`embedding`。Chroma 是第 9 周的事。

## 今天你做

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\python-practice\day53
python 01_search.py
python 01_search.py "大体重膝盖不好怎么跟练减肥" 3
```

默认问句是转行相关，预期应看到 `02.md`（或 `10.md`）排在前面。第二条减肥，预期 `08.md` 之类。日志记下：问了什么、top-3 分别是哪几篇、分数大概多少（四位小数即可）。

代理：`$env:HTTPS_PROXY = 'http://127.0.0.1:7897'`

## 明确不做

- 不调 `/chat/completions`，不把片段拼进 prompt（明天）
- 不引入 numpy / sklearn / chromadb 当黑盒过关（手写 `cosine` 那几行）
- 不提交 `.env`

## 做完

填 [[2026-09-10-Day53-学习日志]] + [[Day53-自测5题]]。说「收尾」再批。
