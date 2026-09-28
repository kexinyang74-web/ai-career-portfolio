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
.
├─ README.md                    ← 本文件
├─ 总览看板.md                  ← 每日进度总览（Obsidian 主入口）
├─ Obsidian使用说明.md          ← Obsidian 配置与插件说明
├─ plan/
│  ├─ 01-24周执行计划.md         ← 每周任务清单（核心文件）
│  ├─ 02-学习资源清单.md         ← 免费/付费资源导航
│  ├─ 03-项目三件套规格书.md     ← 三个作品的验收标准
│  ├─ 04-进度追踪表.md           ← 24 周打卡记录
│  └─ 第1周-定稿版.md            ← 第 1 周执行版
├─ templates/
│  ├─ 学习日志模板.md
│  ├─ 简历项目描述模板.md
│  ├─ 面试题记录模板.md
│  └─ 岗位JD调研模板.md          ← 任务 1 产出物模板
└─ projects/
   └─ project-1-ai-assistant/   ← 项目一：行业 AI 助手（可用代码骨架）
```

## 铁律（2026-09-28 修订）

- **只动手不看片**：每天 **6 小时**（实际专注上限，原定 8 小时是按理想排的，执行不了）
  = 3.5 小时写代码 + 1.5 小时理论 + 1 小时写笔记和投递。
  **最难的写代码排在上午 9–10 点**（状态最好的时段）。健身不砍。力扣两个月一次。
- **一套工具栈走到底**：Python + FastAPI + LangChain/LangGraph + Chroma + Docker，不反复换框架。
- **每周一检查点**：检查点没过，宁可在本周多留一周，也不带病进入下一阶段。
- **学习日志本人写，AI 不代笔**：三栏、十分钟、写「想不起来」完全合格。
  详见 [学习日志模板](templates/学习日志模板.md)。这一条是 2026-09-28 改回的，
  此前四十天的代填直接造成了「能做出项目但脱离 AI 写不出代码」。
- **投递从现在开始，不等第 19 周**：每周 3–5 份，和学习并行。
  第 15 周设第一次决策门。详见 [进度追踪表](plan/04-进度追踪表.md)。
- **中断之后不补课**：落下的直接勾销，从今天继续。重启的门槛比坚持高得多。

## 快速开始（项目一）

```powershell
cd projects/project-1-ai-assistant
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env
# 用记事本打开 .env，填入你的 DEEPSEEK_API_KEY
python main.py "你是我的行业助手，帮我分析今天的工作重点"
```

## 日常更新（已关联 GitHub）

本仓库已推送到 GitHub：https://github.com/kexinyang74-web/ai-career-portfolio

```powershell
git add -A
git commit -m "更新学习进度"
git push
```

也可以让 AI 代跑，或在 Obsidian 里用 Git 插件自动备份（见 [Obsidian使用说明](Obsidian使用说明.md)）。

每天的学习笔记、每周进度、三个项目都往这个仓库推。**面试官看的就是这个仓库。**
