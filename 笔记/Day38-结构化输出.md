# Day 38 结构化输出（第 6 周第 3 天）

> 昨天用例子和步骤管「像不像」。今天管 **字段齐不齐**——后面程序要解析、Day 39 三版对比才有可比较的形状。仍用项目一或 day38 小脚本；密钥只在 `.env`。

## 一、为什么要结构

「写几个选题」得到的是散文。你要的是每条都能点名的格子，例如：

- `title` 标题
- `hook` 开头钩子
- `fit` 为什么符合转行人设（一句）

格子定了，你才能说「缺字段 = 这次 prompt 失败」，而不是感觉「好像还行」。

这是四件套里的 **输出格式** 加严版：不但说「一行一条」，还说 **每条必须有哪些键**。

## 二、两种要法（今天两种都试）

**1. 列表字段（项目一就能跑，不必改 main.py）**

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\project-1-ai-assistant
.\.venv\Scripts\activate
python main.py "只输出 2 条选题。每条必须含三行：标题： 钩子： 人设： 不要前言后记，不要 Markdown 代码块。"
```

**2. JSON（概念 + 真跑）**

API 可以设 `response_format: { "type": "json_object" }`，模型被约束成合法 JSON。文档要求：**系统或用户里必须写明要输出 JSON**，否则可能空转/卡住。

项目一骨架 **没有**传这个参数，所以今天用 `day38/01_json_mode.py`：在 body 里打开 json_object，user 里明确要一个 JSON 对象（一个根对象，里面是数组也可以包在键里）。

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\python-practice\day38
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item ..\..\project-1-ai-assistant\.env .env
python 01_json_mode.py
```

验收：打印出的是能 `json.loads` 的对象，且每条有 `title` / `hook` / `fit`。若 400，看报错；常见是没在 messages 里写「输出 JSON」。

## 三、和 few-shot 怎么配

可以给 **一条 JSON 样例**（少样本 + 格式）。样例键名必须和你要求的完全一样。

## 四、做完

答 `笔记/Day38-自测5题.md`，填学习日志。不要贴密钥。把 JSON 是否解析成功写进日志。
