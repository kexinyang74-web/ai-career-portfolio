# Day 59 LangChain Loader / TextSplitter（第 9 周第 3 天）

> 对照 `day51/01_split.py`。今天只到「读文件 + 切块」。不调 Embedding、不写 Chroma、不调 Chat。VectorStore / RetrievalQA 是 Day 60。

## 四个词对上手写（先记前两个）

| LangChain        | 你已经写过的                                              |
| ---------------- | --------------------------------------------------- |
| **Loader**       | `Path.read_text` + `glob("*.md")`，跳过 `_template.md` |
| **TextSplitter** | `split_by_paragraph`（按空行）                           |
| VectorStore（明天）  | `embeddings.json` / Chroma `query`                  |
| RetrievalQA（明天）  | `01_rag_chat.py`：检索片段塞进本轮 `user` 再 Chat             |

Loader 吐出的是 `Document`：`page_content` 是正文，`metadata["source"]` 是文件路径（标签，不是向量）。这就是你 Day 58 的 `source: 02.md` 从哪来的那一类东西。

## 三种切分（检查点要能讲）

| 策略 | 今天怎么看见 | 对检索的影响 |
|---|---|---|
| **按段落** | 手写空行切；LC 用 `CharacterTextSplitter(separator="\\n\\n")` | 一块 ≈ 一个意思；一段特别长仍会超块 |
| **固定长度** | `RecursiveCharacterTextSplitter(chunk_size=80, overlap=20)` | 块变多、可能从句子中间切断；overlap 让答案少卡在切缝上 |
| **语义** | **今天不写代码** | 按句先 Embed，意思近的再合成一块；要调 Embedding，比前两种贵 |

切太碎：检索到半句，Chat 缺上下文。切太大：一块里混进不相关句，等于变相塞全文。你的 10 篇很短，按段大约 20 块；定长 80 字会明显更多。

## 今天你做

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\python-practice\day59
pip install -r requirements.txt
python 01_split_lc.py
```

看三件事：Loader 是不是 10 个 Document；按段块数是否接近手写；定长是不是更多、预览是否可能从中间断。

默认 `DirectoryLoader` 会走 Unstructured（还要额外包）。脚本已指定 `TextLoader` + `encoding=utf-8`，不要改回去。

## 明确不做

- 不调 Chat、不写向量、不建项目二目录
- 不提交 `.env` / `chroma_db`

## 做完

答 [[Day59-自测5题]]。说「收尾」再批。
