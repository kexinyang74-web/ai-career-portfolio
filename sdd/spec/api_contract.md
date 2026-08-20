# API 契约方法卡

用 OpenAPI 契约约束前后端行为（笔记：生成 OpenAPI 契约，用契约约束前端开发）。

## 做法

1. FastAPI 应用自动生成 OpenAPI 文档：
   - JSON：`GET /openapi.json`
   - 交互式文档：`GET /docs`（Swagger UI）
2. 启动本地服务后导出契约：

   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn main:app --port 8000
   # 浏览器打开 http://127.0.0.1:8000/openapi.json 另存为 backend/openapi.json
   ```

3. 前端按契约实现，不各自脑补字段。

## 验收点

- 契约中的每个端点都有对应的 pytest 用例（成功 + 失败路径）
- 字段命名、校验规则与 `spec/product_spec.md` 逐条一致
- 契约变更时同步更新 spec 与测试，不"边写边猜"
