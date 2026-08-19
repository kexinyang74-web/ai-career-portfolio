# Day 3 · 学会读 Git 状态（status / log / diff）

> 教学目标：能独立看懂 `git status`、`git log --oneline`、`git diff` 的输出。这三条命令是"检查单"——AI 提交/推送前，靠它们确认改了什么、有没有误提交敏感文件。

## 一、git status：当前仓库的"体检报告"

真实示例（本仓库 2026-08-19）：

```text
On branch main
Your branch is ahead of 'origin/main' by 4 commits.
  (use "git push" to publish your local commits)

Changes not staged for commit:
        modified:   .obsidian/app.json
        modified:   总览看板.md

Untracked files:
        当前状态.md
        笔记/Day1-岗位JD调研.md
```

逐行翻译：

- `On branch main`：当前在 main 分支上（你的主时间线）
- `ahead of 'origin/main' by 4 commits`：本地比 GitHub 多 4 个存档点，还没 push。看到这个 = 该推送了
- `Changes not staged for commit`：这些文件被改过，但还没加入暂存区（还没"选中"）
- `Untracked files`：从未被 Git 跟踪的新文件。Git 不知道它们存在，也不管它们——必须 `git add` 才会纳入版本管理
- **为什么 commit 前必须看 status**：确认"这次到底要提交什么"，防止误提交密钥/垃圾文件

关键词：`staged` = 已加入暂存区（已选中）；`untracked` = 新文件，Git 还没跟踪；`modified` = 已跟踪文件被改过。

## 二、git log --oneline：存档点时间线

真实示例：

```text
554f688 (HEAD -> main) vault backup: 2026-08-19 15:32:27
7a48c37 vault backup: 2026-08-19 15:02:26
4d849ad vault backup: 2026-08-19 10:47:50
dae9458 vault backup: 2026-08-19 10:17:58
b9c6c63 (origin/main, origin/HEAD) vault backup: 2026-08-19 09:48:21
6b297d8 docs: 更新 README 目录结构与日常更新说明
017cd74 chore: 排除个人作品集网站项目与多余空库配置
5d04bbb init: 6个月转行学习操作系统 + Obsidian总览看板 + 项目一骨架
```

- 一行 = 一个存档点（commit）
- 左边 7 位字母数字 = 存档编号（完整编号很长，前 7 位足够区分）
- 右边 = 提交时写的一句话说明
- 从上到下 = 从最新到最旧（最新在顶）
- `(HEAD -> main)`：HEAD = "你现在站在哪个存档点"，`-> main` = 在 main 分支上
- `(origin/main, origin/HEAD)`：GitHub 上的 main 停在这个存档点
- 对比：HEAD 在 `554f688`，origin/main 在 `b9c6c63` → 本地领先 4 个提交，和 status 里的 "ahead by 4" 对上了

## 三、git diff：精确到行的"改动清单"

真实示例（总览看板.md 的改动）：

```diff
diff --git a/总览看板.md b/总览看板.md
@@ -3,6 +3,17 @@
 > 每天打开这个页面就够了：更新今日打卡 → 看本周任务 → 确认检查点。
 > 所有改动自动保存在本地，记得定期让 AI 提交并推送到 GitHub（每天结束时一次即可）。
 
+## 📁 文件导航（打开看板先看这里）
+
+| 文件 | 管什么 | 什么时候打开 |
...
@@ -18,7 +29,7 @@
-  - [ ] 仓库里有第一条真实提交
+  - [x] 仓库里有第一条真实提交
```

怎么读：

- 第一行 `diff --git a/... b/...`：a = 已提交的旧版本，b = 当前工作区的新版本
- `--- a/...` = 旧版本；`+++ b/...` = 新版本
- `@@ -3,6 +3,17 @@` = 改动位置：旧版本第 3 行起 6 行，新版本第 3 行起 17 行（因为插入了新内容）
- 以 `-` 开头的行 = 旧版本里有、新版本里没了（被删/被改前）
- 以 `+` 开头的行 = 新版本里新增的（被改后）
- 没有 `+` / `-` 前缀的行 = 上下文（没变，帮你定位）

**重要提醒**：`git diff` 只看"已跟踪文件"的改动。Untracked 的新文件看不到——想看必须 `git add` 之后用 `git diff --cached`（或 `--staged`）。

## 四、三命令配合使用（日常检查单）

1. `git status` → 现在仓库整体什么状态？有没有未提交/未推送的东西？
2. `git diff` → 具体改了哪些行？（提交前确认没有敏感文件）
3. `git log --oneline` → 历史存档长什么样？本地和 GitHub 差几个？

检查单口诀：**status 看全局，diff 看细节，log 看历史。** AI 说"提交并推送"前，先用这三条验证它要做的事。

## 五、实战记录（Day 3 实录）

本次在真实仓库里走了一遍 add → commit → branch → clone，逐段看懂每一步输出：

1. **add**：`git add 笔记/Day3-读懂Git状态.md` → `git status` 里该文件从 `??`（未跟踪）变成 `A`（已选中）
2. **diff --cached**：`git diff --cached --stat` → `1 file changed, 96 insertions(+)`，即"这次要存 96 行新内容"
3. **commit**：`git commit -m "docs: Day3 学会读懂 Git 状态"` → 输出 `[main 169ee4b] ... 1 file changed, 96 insertions(+)`
4. **log**：`git log --oneline --decorate` → 新提交出现在最顶，标着 `(HEAD -> main)`
5. **branch**：
   - `git switch -c demo/day3-read` → `Switched to a new branch`
   - `git branch -a -v` → `*` 标出当前分支；新分支和 main 指向同一个提交
   - `git switch main` → 切回主时间线
   - `git branch -d demo/day3-read` → `Deleted branch ... (was 169ee4b)`，main 毫发无损
   - 理解：**分支只是一个指向提交的指针**。新建 = 从某提交分叉；删除 = 只删指针，提交和历史都还在
6. **clone**：`git clone <仓库路径> <临时目录>` → 复制出完整的一份，`git log` 看到和本地一模一样的全部历史。clone = 完整备份/换电脑同步
7. **push（待办）**：本次代理未开（127.0.0.1:7890 不通），本地领先远程数个提交；打开代理后执行 `git push` 即可

一句话总结：**status 看全局，diff 看细节，log 看历史，branch 是指针，clone 是复制，commit 只存本地、push 才上传。**

## 六、Day 3 自测 5 题

> 先不看书、凭记忆作答。把答案写在《Day3-自测作答.md》里，写完让 AI 批改（会像 Day 2 一样生成批改版，指出对错和补充讲解）。

**第 1 题**：`git status` 里出现下面两行，请解释它们的意思，并说你现在该做什么：

```text
Your branch is ahead of 'origin/main' by 8 commits.
Changes not staged for commit:
	modified:   总览看板.md
```

**第 2 题**：解释 `git log --oneline` 输出中的三样东西：`(HEAD -> main)`、`(origin/main)`、以及为什么最新提交排在最上面。如果 `origin/main` 停在第 4 行，说明什么？

**第 3 题**：`git diff` 输出中，`-` 开头的行、`+` 开头的行、`@@` 分别代表什么？为什么一个"刚创建的新文件"在 `git diff` 里看不到改动？要看它该用什么命令？

**第 4 题**：判断对错并说明理由：

- A. `git commit` 之后，GitHub 网页上立刻就能看到这次改动。
- B. 删除一个分支，这个分支上的所有提交都会永久丢失。
- C. `git clone` 会复制一份包含全部历史的仓库。
- D. `git status` 显示 "up to date with 'origin/main'" 时，说明本地没有任何未提交的改动。

**第 5 题**：用你自己的话说清楚 `git status` / `git diff` / `git log --oneline` 分别看什么。另外，如果 AI 对你说"我把最近的修改提交并推送了"，你作为监督者应该先用哪两条命令验证？
