# Day 57 Chroma 持久化（第 9 周第 1 天）

> 把第 8 周的 `embeddings.json` **搬进 Chroma 磁盘目录**。Embedding 仍用百炼，不调 Chat。不上 LangChain（后天）。密钥继续 `day52/.env`。

对照：上周向量库 = 一个 JSON 文件，每次自己 `json.loads` 再手写余弦。今天 = Chroma 替你存向量、按相似度查。**写入时直接用已经算好的向量**，不必把 10 块再 Embed 一遍。问句仍要 Embed 一次。

## 今天必须能讲清

|           | `embeddings.json` | Chroma                  |
| --------- | ----------------- | ----------------------- |
| 存在哪       | 一个文件              | `chroma_db/` 目录（一堆内部文件） |
| 关掉 Python | 文件还在              | 目录还在，**再打开还能 query**    |
| 检索        | 你自己 for 循环 + 余弦   | `collection.query`      |
| 来源        | 字段 `source`       | `metadatas` 里的 `source` |

持久化 = 数据写在磁盘上，进程结束不丢。内存列表关掉就没了；JSON/Chroma 都算持久，Chroma 多了索引和以后的过滤。

## 今天你做

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\python-practice\day57
pip install -r requirements.txt
python 01_chroma.py
python 01_chroma.py
```

第二次应打印「已有数据，跳过写入」，条数仍是 10。问句默认转行晚不晚，top-1 仍应接近 `02.md`。

重写库：`python 01_chroma.py --rebuild`

`chroma_db/` 不要提交。代理：`$env:HTTPS_PROXY = 'http://127.0.0.1:7897'`

装包若报 Python 3.13 不兼容，把报错贴过来（不要贴密钥）。

## 明确不做

- 不调 Chat、不上 LangChain、不做 FAISS、不建项目二目录（Day 61）
- 不把 `.env` 提交

## 做完

答 [[Day57-自测5题]]。日志收尾时代填。说「收尾」再批。
