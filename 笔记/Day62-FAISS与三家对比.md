# Day 62 FAISS 与三家对比（第 9 周第 6 天）

> 同一批 `day52/embeddings.json` 用 FAISS 再检索一次。不调 Chat，不部署 Milvus，不改项目二默认仓库（仍用 Chroma）。

## 今天目的

**能跑通 FAISS top-k，并能用自己的话说清三家各适合什么。** 不是把项目二换成 FAISS。

|      | Chroma（你 Day 57–61）    | FAISS（今天）          | Milvus（只讲）  |
| ---- | ---------------------- | ------------------ | ----------- |
| 它是什么 | 带元数据的向量数据库             | 近邻检索库（索引）          | 面向集群的向量数据库  |
| 你怎么用 | 持久化目录 + `where source` | `IndexFlatIP` 穷举内积 | 不装          |
| 适合   | 本机 RAG、要过滤、要存文档        | 只要算得快、元数据自己管       | 百万级以上、多机、运维 |
| 分数   | distance **越小**越近      | 今天归一化后内积 **越大**越近  | 看配置         |

Chroma 把「向量 + 正文 + source」放在一起。FAISS 默认只吃矩阵；`02.md` 是 Python 列表里对齐下标带出来的。所以 FAISS **没有**现成的 `where source=02.md`，要过滤得自己先筛行再搜，或搜完再丢。

`IndexFlatIP`：不压缩、把问句和每一条都做内积。10 条完全够。更大的库才会用 IVF / HNSW 等近似索引（今天不写）。

## 今天你做

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\python-practice\day62
pip install -r requirements.txt
$env:HTTPS_PROXY = "http://127.0.0.1:7897"
python 01_faiss.py
```

没有 `embeddings.json` 就先跑 `day52/01_embed.py`。看 top-1 是不是还接近 `02.md`。装 `faiss-cpu` 报错时把完整报错贴出来（Python 3.13 偶发没有轮子）。

## 明确不做

- 不调 Chat、不部署 Milvus、不把项目二默认改成 FAISS
- 不写 30 条评测

## 做完

答 [[Day62-自测5题]]。说「收尾」再批。明天 Day 63 检查点 + 周复盘。
