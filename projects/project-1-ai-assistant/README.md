# 项目一：行业场景 AI 助手（命令行版）

> 面向 **XX 行业** 的 AI 应用 ——（在这里写你的行业定位语，例如：面向电商运营的商品文案助手）

基于大模型 API 的多轮对话助手，支持流式输出、行业人设、对话保存。
默认对接 DeepSeek API，可切换到任意 OpenAI 兼容接口。

## 功能

- 多轮对话（维护对话历史）
- 流式输出开关（`/stream`）
- 行业人设（编辑 `system_prompt.md` 即可切换角色）
- 对话保存 / 清空（`/save`、`/new`）
- 错误处理（无密钥、超时、API 报错均有提示）

## 快速开始（Windows）

```powershell
cd outputs/projects/project-1-ai-assistant
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env
```

用编辑器打开 `.env`，填入你的 DeepSeek API 密钥：

```text
DEEPSEEK_API_KEY=sk-你的密钥
```

运行：

```powershell
# 交互模式
python main.py

# 单次提问
python main.py "帮我写一段 XX 行业的新品推广文案"
```

## 使用示例

```text
====================================================
行业场景 AI 助手
模型：deepseek-chat ｜ 流式：关
命令：/new 清空对话 ｜ /stream 切换流式 ｜ /save 保存 ｜ /exit 退出
====================================================

你 > 帮我分析一下这个月销量下滑可能的原因
AI > （模型回答）
```

## 如何换成其他模型

编辑 `.env`：

```text
BASE_URL=https://api.openai.com  （或 Qwen/智谱等兼容接口）
MODEL=gpt-4o-mini               （换成对应模型名）
```

## 目录结构

```text
project-1-ai-assistant/
├─ main.py            ← 主程序
├─ system_prompt.md   ← 行业人设（编辑这里定制角色）
├─ requirements.txt   ← 依赖
├─ .env.example       ← 配置模板
└─ .gitignore
```

## 常见问题

- **报错"未配置 DEEPSEEK_API_KEY"**：检查 `.env` 文件是否创建、密钥是否填写。
- **401 鉴权失败**：密钥错误或未生效，去 DeepSeek 平台重新创建。
- **请求超时**：网络问题，重试；或把 `timeout` 调大（main.py 中 `timeout=120`）。
- **回答被截断**：在 `.env` 中给请求加 `max_tokens`（可在 main.py 的 payload 中加）。

## 后续扩展方向（第 14 周后）

- 用 FastAPI 包一层 HTTP 接口，做成网页版
- 加 Function Calling，让助手能查数据、调工具（项目三的雏形）
- 加对话历史落库、限流、日志

