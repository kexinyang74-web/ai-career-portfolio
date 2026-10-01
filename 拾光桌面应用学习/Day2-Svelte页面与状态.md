# Day 2：读懂 Svelte 页面与状态

## 今天要得到什么

围绕 `src/Library.svelte`，看懂用户输入、页面状态和按钮事件如何连接。今天只追踪到 `saveNote(input)`，暂时不进入 Rust。

## 先认识六个符号

- `$props()`：接收父组件传来的数据或函数。
- `$state(...)`：创建会影响页面显示的状态。
- `$effect(...)`：当依赖变化时执行副作用。
- `bind:value={title}`：输入框和变量双向同步。
- `onclick={...}`：点击时执行函数。
- `{#if}`、`{#each}`：条件显示和循环显示。

## 阅读路线

在 `Library.svelte` 中按以下顺序找代码：

1. 状态声明：`notes`、`query`、`current`、`title`、`text`、`busy`、`dirty`。
2. `onMount(...)`：页面首次出现时加载列表、位置和本地草稿。
3. `changed()`：输入变化后标记未保存并缓存草稿。
4. `save(copy=false)`：组装 `input`、调用保存、更新页面或显示错误。
5. 页面模板中的标题输入、正文输入和“保存到本机”按钮。

## 保存按钮在页面内的路线

```text
用户输入
  → bind:value 更新 title / text
  → oninput 调用 changed()
  → dirty = true，并写入 localStorage 草稿
  → 点击“保存到本机”
  → save()
  → busy = true，避免重复点击
  → 组装 input
  → await saveNote(input)
  → 成功：更新 current、清除 dirty、刷新列表
  → 失败：保留输入并显示 error
  → finally：busy = false
```

## 四个重点状态

- `dirty`：当前输入和已保存版本是否不同。
- `busy`：保存或恢复是否正在执行，用于防止重复操作。
- `current`：当前编辑的是哪条已保存记录；新建时为 `null`。
- `baseRevision`：保存时携带的旧版本号，为后端冲突检查做准备。

## 运行与实验

先预测两个命令会检查什么，再运行：

```powershell
npm install
npm run check
npm run build
```

小实验：只修改 `Library.svelte` 中一段非关键说明文字。刷新浏览器确认效果，然后运行：

```powershell
git diff -- src/Library.svelte
```

观察差异后决定保留还是手工改回，不要使用破坏性 Git 命令。

## 今日验收

- [ ] 能解释 `save()`、`refresh()`、`dirty`、`busy`
- [ ] 能从保存按钮找到 `save()`
- [ ] 能说出成功和失败时页面状态的区别
- [ ] 已运行前端检查与构建
- [ ] 已完成 `Day2-自测5题.md`

## 学习日志（请自己填写）

- 今天遇到的问题：
- 我能讲清的原理：
- 我还没搞懂的部分：
- 今天的一句话总结：
