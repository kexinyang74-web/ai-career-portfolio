# Day 5：通过测试理解冲突与历史版本

## 今天要得到什么

把测试当成“可执行的需求说明”，理解项目如何阻止过期内容覆盖新内容。

## Arrange–Act–Assert

阅读 `src-tauri/tests/storage_test.rs` 时，把每个测试拆成三段：

- **Arrange（准备）**：创建内存数据库和初始记录。
- **Act（执行）**：用某个版本号保存、恢复或搜索。
- **Assert（断言）**：确认结果、错误或数据库内容。

源码为了紧凑可能写在同一行；阅读时请主动把它们在纸上分段。

## 重点测试

优先找这些行为：

- 过期版本不能覆盖新版本。
- 重复创建不能覆盖原记录。
- 数据库关闭再打开后记录仍存在。
- 保存项目与普通素材互不混淆。
- 历史恢复前先备份当前内容。

## 两窗口冲突示例

```text
窗口 A 读取版本 1
窗口 B 读取版本 1
窗口 A 用 baseRevision=1 保存 → 数据库变成版本 2
窗口 B 仍用 baseRevision=1 保存
UPDATE ... WHERE revision=1 匹配不到任何行
→ changed != 1
→ 返回冲突错误
→ 窗口 B 的输入仍保留，可另存副本
```

## 测试先行小实验

不要改正式规则。选择一个容易恢复的验证，例如给 `validates_input` 临时增加“非法 kind 必须失败”的新样例：

1. 写下预期行为。
2. 先让断言故意写成相反结果，运行单个测试并确认失败。
3. 把断言改为正确预期，确认通过。
4. 用 `git diff` 检查只改了测试。
5. 手工还原实验，保留自己的实验记录。

运行命令：

```powershell
cargo test --manifest-path src-tauri/Cargo.toml --test storage_test validates_input
cargo test --manifest-path src-tauri/Cargo.toml --test storage_test
npm run check
node --test tests/*.test.mjs
```

## 今日验收

- [ ] 能把一个真实测试拆成 Arrange、Act、Assert
- [ ] 看到了实验测试先失败再通过
- [ ] 能解释 `baseRevision` 如何阻止旧内容覆盖
- [ ] 能解释恢复历史为什么会产生新的版本
- [ ] 已完成 `Day5-自测5题.md`

## 学习日志（请自己填写）

- 今天遇到的问题：
- 我能讲清的原理：
- 我还没搞懂的部分：
- 今天的一句话总结：
