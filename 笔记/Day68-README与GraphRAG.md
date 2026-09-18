# Day 68 README 与 GraphRAG（第 10 周第 5 天）

> 任务 3：把项目二 README 补到「外人能按步骤跑 CLI、能看见评测数字」。GraphRAG **只讲概念，不写代码、不建图谱**。

## 今天目的

规格书写明：README 要有简介、运行方法、示例、架构。现在 `projects/project-2-rag/README.md` 能跑问答，但缺这几块：

1. **架构**（Load → Split → Embed → Chroma → top-k → 塞进本轮 user → DeepSeek）
2. **评测怎么跑**（`eval_run.py`、不要覆盖 `eval/运行记录.md`）
3. **数字**（k=3 人工可接受 29/30；k=5 自动引用 28/30；CLI 默认 k=5）
4. **不要推什么**（`.env`、`chroma_db/`）
5. **有 RAG / `--no-rag` 对照**（规格书验收：演示时对比）

你对着现有 README 自己补段落。需要我直接改文件时再说「改 README」。

对照课：[GraphRAG 官方文档](https://microsoft.github.io/graphrag/) 看概念即可，不必跟着安装。

## GraphRAG 要能讲的三句话

**向量 RAG（你现在的项目）**：问句变成向量，按距离取最像的**文本块**，塞进 prompt。块和块之间没有「谁连着谁」。

**GraphRAG（微软那套索引思路）**：建库时用模型从文档里抽 **实体和关系**（人、公司、视频、主题……），连成图；还可以按社区做摘要。提问时可以走「实体邻居」（local）或「整库主题摘要」（global），补的是**块与块之间的连线**。

**和你库的关系**：约 10 篇拆解、单跳「哪篇说了转行」用向量 + `--source` 就够。多跳（A 提到 B、B 才有答案）或「这十篇整体在讲什么」时，纯 top-k 容易漏。本周不实现；面试被问到说清「适用场景」即可。

## 今天你做

打开 `projects/project-2-rag/README.md`，按上面 5 块补全（架构可用文字列表，不必画图工具）。评测命令示例：

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\project-2-rag
$env:HTTPS_PROXY = "http://127.0.0.1:7897"
python eval_run.py --all -k 3 --out eval/运行记录.md
python eval_run.py --all -k 5 --out eval/运行记录-k5.md
```

`eval_run.py` 的 `-k` **默认仍是 3**（保住基线文件）；CLI `main.py` 默认已经是 5。README 里写清楚这两个默认不一样。

GraphRAG：打开官方文档首页，用自己的话在日志里写「向量检索缺什么、图谱补什么」。不要 `pip install graphrag`。

## 明确不做

- 不上网页、不建知识图谱、不重切、不重 embed
- 不覆盖 `eval/运行记录.md`
- 不把密钥、chroma 路径里的向量库推进 GitHub

## 做完

答 [[Day68-自测5题]]。说「收尾」再批。
