# 转行 AI 应用开发 · 6 个月学习操作系统

这是为你定制的 6 个月全职转行工具箱，目标岗位：**AI 应用开发工程师 / 大模型应用开发 / AI Agent 开发 / RAG 工程师**。

## 这套系统怎么用

1. 每周打开 [01-24周执行计划](plan/01-24周执行计划.md)，照着当周任务清单逐项打勾。
2. 每周末在 [04-进度追踪表](plan/04-进度追踪表.md) 里记录完成度和检查点结果，未达标的周次不要硬闯下一阶段。
3. 每天用 [学习日志模板](templates/学习日志模板.md) 写笔记（GitHub 上同步一份，作为作品集的门面）。
4. 做项目时对照 [项目三件套规格书](plan/03-项目三件套规格书.md)，写完项目段简历用 [简历 STAR 模板](templates/简历项目描述模板.md)。
5. 面试准备阶段用 [面试题记录模板](templates/面试题记录模板.md) 沉淀题库。

## 目录结构

```text
outputs/
├─ README.md                    ← 本文件
├─ plan/
│  ├─ 01-24周执行计划.md         ← 每周任务清单（核心文件）
│  ├─ 02-学习资源清单.md         ← 免费/付费资源导航
│  ├─ 03-项目三件套规格书.md     ← 三个作品的验收标准
│  └─ 04-进度追踪表.md           ← 24 周打卡记录
├─ templates/
│  ├─ 学习日志模板.md
│  ├─ 简历项目描述模板.md
│  └─ 面试题记录模板.md
└─ projects/
   └─ project-1-ai-assistant/   ← 项目一：行业 AI 助手（可用代码骨架）
```

## 三条铁律

- **只动手不看片**：每天 8 小时 = 4 小时写代码 + 2 小时理论 + 1 小时刷题 + 1 小时写笔记。
- **一套工具栈走到底**：Python + FastAPI + LangChain/LangGraph + Chroma + Docker，不反复换框架。
- **每周一检查点**：检查点没过，宁可在本周多留一周，也不带病进入下一阶段。

## 快速开始（项目一）

```powershell
cd outputs/projects/project-1-ai-assistant
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env
# 用记事本打开 .env，填入你的 DEEPSEEK_API_KEY
python main.py "你是我的行业助手，帮我分析今天的工作重点"
```

## 推送到 GitHub（第 1 周任务）

1. 在 GitHub 新建仓库 `ai-career-portfolio`（Public）。
2. 把这个 `outputs` 目录复制到本地新文件夹，执行：

```powershell
git init
git add .
git commit -m "init: 6个月转行学习操作系统 + 项目一骨架"
git branch -M main
git remote add origin https://github.com/你的用户名/ai-career-portfolio.git
git push -u origin main
```

3. 之后每天的学习笔记、每周进度、三个项目都往这个仓库推。**面试官看的就是这个仓库。**

