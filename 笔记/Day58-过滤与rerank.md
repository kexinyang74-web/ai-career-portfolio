# Day 58 元数据过滤与 rerank（第 9 周第 2 天）

> 同一问句跑两遍 Chroma：不过滤 vs `where source=02.md`。不调 Chat，不上 LangChain。库仍是昨天的 `day57/chroma_db/`。

## 今天必须能讲清

**元数据**：跟在切块旁边的标签，不是向量本身。你写入时带了 `source`（如 `02.md`）。过滤 = 先按标签缩小范围，再在剩下的里面比距离。

**top-k**：向量检索直接留前 k 名（你第 8 周、昨天都在做）。

**rerank（重排）**：先多拿一些（比如 10 块），再用另一套打分（交叉编码器、规则、更贵的模型）把顺序改一下，最后只留 3 块给 Chat。今天**不写 rerank 代码**，只要能和「过滤」分开：

| | 过滤 where | rerank |
|---|---|---|
| 干什么 | 不合格的块直接丢掉 | 先召回，再改名次 |
| 例子 | 只要 `02.md`，`03.md` 再像也不进 | 转行问句仍可能先拿到 02/03/05，再把 02 提到最前、丢掉 05 |
| 今天脚本 | 有 | 无 |

转行那句不过滤时，第 2、3 名可能是 `03.md`/`05.md`（噪音）。过滤后集合里往往只剩 `02.md` 一块，top-3 也凑不满三名，这是正常的。

## 今天你做

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\python-practice\day58
python 01_filter.py
```

若提示没有 chroma_db，先回 day57 跑一遍 `python 01_chroma.py`。代理需要则设 `HTTPS_PROXY`。

## 明确不做

- 不调 Chat、不装 LangChain、不写 rerank 模型
- 不提交 `.env` / `chroma_db`

## 做完

答 [[Day58-自测5题]]。说「收尾」再批。
