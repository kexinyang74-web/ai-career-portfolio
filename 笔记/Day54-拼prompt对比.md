# Day 54 拼进 prompt 并对比（第 8 周第 5 天）

> 同一问句跑两遍 Chat：**不检索** vs **把 top-k 放进本轮 `user`**。不上 LangChain/Chroma。密钥仍只在 `.env`。不改项目一人设定位句。

代码：`projects/python-practice/day54/01_rag_chat.py`  
仍读：`day52/embeddings.json` + `day52/.env`（Embedding）+ 项目一或 day52 的 `DEEPSEEK_API_KEY`（Chat）

## 今天必须能讲清

- 人设/规则放 `system`；**检索到的片段和问题放这一轮 `user`**（Day 50 结论）。不要把 10 篇全文写进人设。
- 片段里带上 `02.md` 这种文件名，回答才能引用第几篇。
- 无检索时模型没读过你的拆解，可能泛泛而谈或编标题；有检索时应能碰到你写过的钩子/判断，并出现来源名。
- 检索错了，Chat 仍可能编。资料不够要说不够。

## 今天你做

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\python-practice\day54
python 01_rag_chat.py
```

默认问句针对转行那条笔记。可选第二句：

```powershell
python 01_rag_chat.py "大体重膝盖不好怎么跟练减肥" 3
```

代理：`$env:HTTPS_PROXY = 'http://127.0.0.1:7897'`

日志用自己的话写对比（各 3～5 句即可）：有没有胡编、有没有写到来源、有没有用到你的「为什么可能火」。不要贴完整回复若太长，摘关键句。

Chat 走 DeepSeek，Embedding 走百炼，两套 Key、两个 BASE，不要混。

## 明确不做

- 不上 Chroma / LangChain
- 不改项目一 README 定位
- 不提交 `.env`
- 不要求 40 篇、不写 30 条评测集

## 做完

填日志 + [[Day54-自测5题]]。说「收尾」再批。
