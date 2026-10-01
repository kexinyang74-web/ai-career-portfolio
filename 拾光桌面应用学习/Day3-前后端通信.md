# Day 3：理解前后端通信

## 今天要得到什么

读懂一次保存如何跨过 JavaScript 与 Rust 的边界，并能画出携带的数据。

## 从 `storage.js` 开始

`src/storage.js` 是前端与 Tauri 之间的薄封装。重点看：

```js
export async function saveNote(note) {
  return invoke('save_note', {note});
}
```

真实源码为了紧凑写在一行，但理解时可以像上面一样展开。`invoke` 的第一个参数是 Rust 命令名，第二个参数是传给命令的对象。

## 继续到 Rust

在 `src-tauri/src/main.rs` 中找：

- `#[tauri::command] fn save_note(...)`
- `tauri::generate_handler![...]` 中的 `save_note`
- `AppDatabase(Mutex<Database>)`
- `.setup(...)` 中的 `Database::open(...)`

调用链如下：

```text
Library.svelte
  save()
    input = { id, title, text, kind, baseRevision }
      ↓
storage.js
  invoke('save_note', { note: input })
      ↓ Tauri 序列化边界
main.rs
  save_note(state, note: NoteInput)
      ↓ 获取 Mutex 中的数据库
storage.rs
  Database::save(note)
      ↓
返回 Result<Note, String>
      ↓ Tauri 转成 Promise
Library.svelte 更新 current 或 error
```

## 名字为什么能对应

JavaScript 使用 `baseRevision`，Rust 字段是 `base_revision`。`NoteInput` 上的 `#[serde(rename_all="camelCase")]` 负责名称转换。没有这个规则，前后端字段可能匹配失败。

## 错误如何返回

Rust 返回 `Result<Note, String>`：

- `Ok(note)`：前端的 `await` 得到保存结果。
- `Err(message)`：前端 Promise 被拒绝，进入 `catch(e)`。

页面没有因为错误清空 `title` 和 `text`，这是“失败时保留用户输入”的重要产品规则。

## 小实验

1. 先找出浏览器模式下 `saveNote()` 主动抛出的错误文字。
2. 在学习副本修改这段提示。
3. 运行 `npm run check`。
4. 运行 `git diff -- src/storage.js`，指出唯一变化。
5. 手工恢复原提示，再确认 `git diff` 中该变化消失。

## 今日验收

- [ ] 能不看讲义画出完整保存调用链
- [ ] 每个箭头旁标出了传递的数据或返回值
- [ ] 能解释 `invoke`、`#[tauri::command]` 和 `serde` 的作用
- [ ] 能说明 Rust 错误如何出现在 Svelte 页面
- [ ] 已完成 `Day3-自测5题.md`

## 学习日志（请自己填写）

- 今天遇到的问题：
- 我能讲清的原理：
- 我还没搞懂的部分：
- 今天的一句话总结：
