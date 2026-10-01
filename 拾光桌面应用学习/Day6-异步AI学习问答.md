# Day 6：挑战异步 AI 学习问答链路

## 今天要得到什么

用学习问答模块认识比普通保存更复杂的流程：请求可能耗时、失败、中断或已经计费，因此需要请求编号、状态记录与显式重试。

## 阅读顺序

1. `src/Learning.svelte`：找发送问题、查询状态和保存单题的界面动作。
2. `src/learning.js`：找 `generate_learning`、`query_learning`、`save_learning_item` 的 invoke 封装。
3. `src-tauri/src/main.rs`：找对应 Tauri commands，以及 `spawn_blocking`。
4. `src-tauri/src/learning_service.rs`：看生成、日志、验证和查询流程。
5. `src-tauri/src/learning.rs`：看会话、轮次、请求与保存到素材库。

## 一次提问的主链路

```text
Learning.svelte 组装 request
  → invoke('generate_learning')
  → main.rs 把阻塞任务交给 spawn_blocking
  → learning_service::generate()
  → 检查本机模型配置
  → build_context()
  → reserve() 先保存 pending 轮次
  → Journal::begin() 记录模型请求
  → 调用 DeepSeek
  → 校验模型 JSON
  → Journal::finish() 保存调用结果
  → query() 把结果写回学习轮次
  → 返回前端显示
```

## 为什么不能自动重试

网络中断不等于服务端没有收到请求。如果程序没拿到响应就自动重试，可能产生第二次调用和费用。因此项目保存请求 ID 和状态，让用户先查询原请求，再明确决定是否发起新尝试。

## 幂等性的白话解释

同一个请求 ID 再次到达时，系统应识别它是同一件事，而不是重复创建。若请求 ID 相同但内容不同，则拒绝，避免日志与结果对不上。

## 与素材保存对比

| 普通素材保存 | AI 学习问答 |
|---|---|
| 本机事务通常很快 | 外部服务可能很慢或中断 |
| 成败可以直接返回 | 可能需要稍后查询状态 |
| 不涉及调用费用 | 重试可能再次计费 |
| 用版本号处理编辑冲突 | 还需要请求 ID、pending 状态和调用日志 |

## 运行测试

```powershell
cargo test --manifest-path src-tauri/Cargo.toml --test learning_test
cargo test --manifest-path src-tauri/Cargo.toml --test learning_service_test
```

这些测试使用模拟调用或本地数据库，不要求真实密钥。

## 今日验收

- [ ] 能画出一次学习提问的主要链路
- [ ] 能解释请求 ID、pending、query、Journal
- [ ] 能说明为何网络失败不能直接自动重试
- [ ] 能说出普通保存与 AI 请求的至少三点区别
- [ ] 已完成 `Day6-自测5题.md`

## 学习日志（请自己填写）

- 今天遇到的问题：
- 我能讲清的原理：
- 我还没搞懂的部分：
- 今天的一句话总结：
