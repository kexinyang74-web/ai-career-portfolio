# Day 1 自测 5 题

> 先独立作答，不要搜索标准答案。可以引用文件名，但要用自己的话解释。

## 1. Svelte、Tauri 和 SQLite 在本项目中分别负责什么？

你的回答：
svelte：负责页面长什么样，包括按钮点击后页面状态的变化
tauri：负责把页面装进桌面窗口，并且让JavaScript可以调用Rust
sqlite：一个保存在本地文件中的数据库
## 2. 前端从哪个文件开始运行？它把哪个组件挂到页面上？

你的回答：[src/main.js (line 2)](C:/Users/Administrator/Documents/Codex/2026-09-25/ai/outputs/shiguang-desktop-learning/src/main.js:2)
src/main.js
App.svelte
## 3. `src/App.svelte` 为什么可以称为页面导航中心？

你的回答：
App.svelte 用 page记录当前页面。点击导航按钮后，会读取按钮的 data-page 并更新当前页面，然后通过 if判断应该显示哪个页面组件。因此它负责管理各页面之间的切换。[App.svelte 第 11 行 (line 11)] 第 19 行25～30 行
## 4. Rust 后端在哪里打开 SQLite 数据库，又在哪里注册前端可调用的命令？

你的回答：[main.rs (line 125)](C:/Users/Administrator/Documents/Codex/2026-09-25/ai/outputs/shiguang-desktop-learning/src-tauri/src/main.rs:125)
open(dir.join("shiguang.sqlite"))
tauri::generate_handler
## 5. 为什么 `npm run dev` 的浏览器页面不能代替桌面存储验收？

你的回答：[README.md (line 17)](C:/Users/Administrator/Documents/Codex/2026-09-25/ai/outputs/shiguang-desktop-learning/README.md:17)
[storage.js (line 2)](C:/Users/Administrator/Documents/Codex/2026-09-25/ai/outputs/shiguang-desktop-learning/src/storage.js:2)
浏览器预览没有连接该数据库，不能代替桌面存储验收。
export const desktop=isTauri();