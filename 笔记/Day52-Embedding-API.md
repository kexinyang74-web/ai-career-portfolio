# Day 52 Embedding API（第 8 周第 3 天）

> 把 Day 51 的切块变成向量。和 Chat 不是同一个路径。不上检索、不调 Chat、不上 LangChain/Chroma。密钥只在 `.env`。

文档仍读：`projects/python-practice/day51/docs/`  
代码在：`projects/python-practice/day52/01_embed.py`

## 和 Chat 差在哪（今天必须能讲清）

| | Chat Completions | Embeddings |
|---|---|---|
| 路径 | `{BASE}/chat/completions` | `{BASE}/embeddings` |
| 模型名 | 例如 `deepseek-chat` | 专门的 embedding 模型，不能拿对话模型名硬套 |
| 你送进去 | `messages` | `input`（一段或一批文本） |
| 回来 | `choices[0].message.content` 字符串 | `data[0].embedding` **一串浮点数** |

项目一用的 DeepSeek Chat **通常没有** `/embeddings`。今天要另配你能 200 的兼容接口（通义兼容模式、硅基流动等，以控制台为准）。`.env.example` 里有两套地址示例，只填你实际开通的那套。

向量有固定**维度**（长度）。同一模型、同一段字，多次调用应得到同一方向的向量。不要把完整向量贴进日志，只记：几块、维度、前几个数。

## 今天你做

1. 把 `day52/.env.example` 复制为 `day52/.env`，填 `EMBEDDING_BASE_URL`、`EMBEDDING_MODEL` 和密钥。可从项目一拷密钥，但 **BASE 不要抄成** `https://api.deepseek.com`（除非你确认那家真有 embedding）。
2. 跑：

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\python-practice\day52
python 01_embed.py
```

脚本按空行切 Day 51 文档，跳过短于 40 字的块（你昨天的标题块），逐块请求，打印维度和前 5 个数，并写出 `embeddings.json`（已 gitignore）。

代理环境可先：`$env:HTTPS_PROXY = 'http://127.0.0.1:7897'`

失败时看 HTTP 状态码和响应前几行：404 多半是 Chat 地址没有 embedding；401 是密钥；模型名写错会 400。

## 明确不做

- 不写余弦、不取 top-k（明天）
- 不调 `/chat/completions`
- 不把 `.env` 提交或贴到对话里
- 不改项目一人设

## 做完

日志写：用了哪家 BASE（不要写密钥）、几块、维度。答 [[Day52-自测5题]]。说「收尾」再批。
