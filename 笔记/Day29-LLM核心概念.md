# Day 29 LLM 核心概念（第 5 周第 1 天）

> 今天**可以不调 API**。先把五个词讲准，明天才 POST。练习在 `projects/python-practice/day29/`。

## 一、一次请求在干什么（先记这张图）

```
你的脚本
  → HTTP POST  https://api.deepseek.com/chat/completions
  → Header: Authorization: Bearer 密钥     ← 鉴权（你是谁）
  → Body:  JSON { model, messages, temperature, stream }
  → 服务端：计费 / 安全检查 / 把 messages 编成 token / 模型逐个生成 token
  → 响应 JSON（非流式）或一行行 data:（流式）
  → 你的脚本取出文字：choices[0].message.content
```

检查点要的就是把上面每一步用自己的话讲一遍。Day 18/19 的 requests 已经会 POST JSON；新内容只有 **Bearer 密钥** 和 **messages 协议**。

## 二、五个词

### 1. token

模型不按「汉字/单词」计费和计长度，按 **token**。中文常常接近「一个字 ≈ 一个 token」，英文往往几个字母拼成一个 token。账单上的 `prompt_tokens`（你发给它的）+ `completion_tokens`（它生成的）= `total_tokens`。

**和你的关系**：上下文塞太满、回答太长，都会烧 token、也可能被截断（`finish_reason` 为 `length`）。

### 2. 上下文窗口

一次请求里，**已经发出去的 messages + 即将生成的回复**，加起来不能超过模型的上限。多轮对话时，历史每一轮都还在 `messages` 里，窗口会被越撑越大。超了就要删旧轮、总结、或开 `/new`（项目一就是清空 history）。

### 3. temperature（0～2）

控制「下一个 token 抽得多随机」。低：更稳、更重复；高：更散、更有创意。选题助手可以略高；要格式死、JSON 稳，就偏低。DeepSeek 文档默认常是 1；骨架 `.env` 里写的是 `0.7`。

### 4. top_p

另一套采样：只在概率质量前 p 的那些 token 里抽。文档建议 **改 temperature 或改 top_p，不要两个一起猛拧**。本周作业以 temperature 为主即可。

### 5. 流式输出（stream）

`stream: false`：等整段生成完，一次返回 JSON。  
`stream: true`：服务器用 SSE 一行行推 `data: {...}`，里面是 `delta.content` 小碎片；结束是 `data: [DONE]`。项目一的 `_consume_stream` 就是在拼这些碎片。

用户体验：流式可以边生成边看；非流式实现更简单，适合先打通。

## 三、messages 长什么样

```python
messages = [
    {"role": "system", "content": "你是选题助手……"},  # 人设，通常每轮都带
    {"role": "user", "content": "给我 5 个 B站 减肥选题"},
    {"role": "assistant", "content": "1. ……"},          # 上一轮模型说过的话
    {"role": "user", "content": "第 2 个展开成口播稿"}, # 新问题
]
```

- `system`：人设 / 边界（对应 `system_prompt.md`）
- `user` / `assistant` 交替：多轮记忆靠这个列表，不是模型「真的记住了你这个人」

## 四、密钥（今天就要开始管）

1. 打开 https://platform.deepseek.com 注册，在控制台创建 API Key
2. 复制到本地文件，**不要出现在聊天里、不要 commit**
3. 项目一已有 `.env.example` → 复制为 `.env` 填 `DEEPSEEK_API_KEY`
4. 明天 `git check-ignore .env` 应显示被忽略

充值 10–20 元可放到第一次调用前。可选：编程导航会员——计划写的是先看免费文档，不作为本周检查点。

## 五、和项目一的对应（提前瞄一眼，先不改代码）

| 概念 | 骨架里在哪 |
|---|---|
| 密钥 / 模型 / 温度 | `.env` → `main.py` 读 `DEEPSEEK_API_KEY` / `MODEL` / `TEMPERATURE` |
| system | `system_prompt.md` |
| 单轮 | `python main.py "一句话"` → `ask_once` |
| 多轮 | 交互模式 `history` 列表 |
| 流式 | `/stream` → `call_llm(..., stream=True)` |

## 六、今日练习

跑 `projects/python-practice/day29/01_messages.py`，看打印出来的 JSON 和「粗算 token」。然后做 `笔记/Day29-自测5题.md`。
