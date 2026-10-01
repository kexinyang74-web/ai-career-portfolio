# Day 1：项目地图与启动链路

## 今天要得到什么

今天不追求看懂业务细节。目标是知道“文件在哪里、谁先启动、各层负责什么”。完成后，你应能在一分钟内找到前端入口、后端入口、数据库代码和测试。

## 五个角色的白话解释

- **Svelte**：负责页面长什么样，以及按钮点击后页面状态如何变化。
- **Vite**：开发时启动前端服务器，构建时把前端文件打包到 `dist/`。
- **Tauri**：把网页界面装进桌面窗口，并让 JavaScript 可以调用 Rust。
- **Rust**：处理本地数据库、文件、外部请求和需要保护的数据规则。
- **SQLite**：一个保存在本机单个文件中的数据库。

## 阅读顺序

1. `README.md`：先知道产品做什么，以及浏览器预览和桌面程序的区别。
2. `package.json`：看前端依赖与 `dev`、`build`、`check` 命令。
3. `src/main.js`：找到 Svelte 的挂载点。
4. `src/App.svelte`：看页面导航如何选择 `Home`、`Library`、`Learning` 等组件。
5. `src-tauri/Cargo.toml`：看 Rust 依赖，包括 Tauri、rusqlite、serde、reqwest。
6. `src-tauri/src/main.rs`：看模块声明、命令注册、数据库初始化与应用启动。

## 项目目录图

```text
shiguang-desktop-learning/
├─ src/                 Svelte 页面与 JavaScript 调用层
│  ├─ main.js           前端入口
│  ├─ App.svelte        页面外壳与导航
│  ├─ Library.svelte    素材库页面
│  └─ storage.js        素材库 invoke 封装
├─ src-tauri/
│  ├─ src/main.rs       Rust/Tauri 入口与命令注册
│  ├─ src/storage.rs    SQLite 素材库逻辑
│  └─ tests/            Rust 集成测试
├─ tests/               JavaScript 单元测试
├─ scripts/             构建和界面验证脚本
├─ docs/                设计、验收记录与截图
└─ 笔记/                本课程材料与作答
```

## 启动链路

```text
index.html
  → src/main.js
  → mount(App)
  → App.svelte
  → 根据 page 状态显示 Library / Learning / 其他页面

桌面启动：
src-tauri/src/main.rs
  → Tauri Builder
  → setup 中打开 shiguang.sqlite
  → 注册 invoke_handler
  → 创建桌面窗口并加载前端
```

## 动手任务

1. 依次找到上述 6 个文件，不急着逐行读。
2. 在纸上或自己的日志中重画目录图。
3. 运行并观察：

```powershell
git status --short
git log --oneline -3
```

4. 用自己的话回答：为什么浏览器预览不能完成真实素材保存？

## 今日验收

- [ ] 能找到前端入口 `src/main.js`
- [ ] 能找到后端入口 `src-tauri/src/main.rs`
- [ ] 能找到页面组件目录、数据库代码与两类测试目录
- [ ] 已亲自检查 Git 状态和首个提交
- [ ] 已完成 `Day1-自测5题.md`

## 学习日志（请自己填写）

- 今天遇到的问题：
- 我能讲清的原理：
- 我还没搞懂的部分：
- 今天的一句话总结：
