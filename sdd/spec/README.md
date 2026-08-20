# spec 规格文档区

依据笔记的 SDD 规范：**规格是首要产物，代码从规格构建**。

## 阅读顺序

1. `working_agreement.md` — 团队/个人协作规范（先 Spec → 再测试 → 后实现）
2. `product_spec.md` — 产品规格模板（数据模型、接口 I/O、校验规则等）
3. `planned/`、`implemented/`、`archived/` — 渐进式披露的规格版本管理

## 渐进式披露（笔记 5 节）

- `planned/`：待实现规格（开发前评审）
- `implemented/`：已完成并验收的规格
- `archived/`：历史版本存档

新增功能前检查所有相关 Spec 的兼容性；重大变更建立新的 feature 目录隔离。
