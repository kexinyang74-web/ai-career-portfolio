# Day 30 单轮 Chat Completions（第 5 周第 2 天）

> 今天只做一件事：**用 requests 发出一次非流式 POST，把模型回复打印出来**。多轮和流式留到 Day 31-32。代码在 `projects/python-practice/day30/`。
> 密钥只在 `.env`，不要发给我、不要 print 出来。

## 一、和 Day 18/19 的差别

| | Day 18 汇率/httpbin | 今天 DeepSeek |
|---|---|---|
| 方法 | 多为 GET | **POST**（你要送一段 JSON） |
| 鉴权 | 常常没有 | Header：`Authorization: Bearer <密钥>` |
| body | 无或很少 | `model` + `messages` + `temperature` + `stream: false` |
| 取结果 | 自己定的字段 | `data["choices"][0]["message"]["content"]` |

`raise_for_status()`、`timeout=`、代理 `7897`，全部沿用 Day 19。

## 二、请求长什么样

```
POST https://api.deepseek.com/chat/completions
Header:
  Authorization: Bearer sk-……
  Content-Type: application/json
Body:
  {"model": "deepseek-chat", "messages": [...], "temperature": 0.7, "stream": false}
```

成功时 JSON 里至少有：

- `choices[0].message.content` — 回复正文
- `usage.prompt_tokens` / `completion_tokens` — 真实 token（比 Day 29 粗算准）

常见失败：

| 现象 | 先查 |
|---|---|
| 脚本提示没密钥 | `.env` 是否在 **day30 目录**、变量名是否 `DEEPSEEK_API_KEY` |
| 401 | 密钥错、没粘全、前后空格 |
| 402 / 余额 | 控制台充值 10–20 元 |
| SSL / 连接失败 | `$env:HTTPS_PROXY = "http://127.0.0.1:7897"` 后再跑 |
| 400 + 模型名 | `.env` 里 `MODEL` 改成控制台当前可用的 ID |

## 三、今天步骤（每步跑一次）

1. 在 `day30` 建 venv、装依赖（或暂时用项目一的 venv，但工作目录必须是 day30，才能读到这里的 `.env`）。
2. 把项目一的 `.env` **复制**过来（不要用资源管理器「移动」把项目一弄丢）：

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\python-practice\day30
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item ..\..\project-1-ai-assistant\.env .env
python 01_single_turn.py
```

3. 看终端：状态码 200、一段中文回复、三行 token 数。
4. 打开返回的 JSON（脚本会打印缩进后的字典），用眼睛找到 `choices` → `0` → `message` → `content`。
5. 把 `01` 里的用户问题改成你自己的一句（例如要 1 个 B站选题），再跑一次。
6. 答 `笔记/Day30-自测5题.md`，填学习日志。

## 四、和项目一骨架的关系

项目一的 `call_llm` 就是今天这件事包成函数。今天你**自己写一遍 POST**，明天再去对照 `main.py` 第 51–80 行。不要今天下午就改人设（Day 34）。
