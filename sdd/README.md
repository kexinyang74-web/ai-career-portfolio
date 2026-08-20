# SDD+TDD 工作台

依据 `sdd笔记.txt`（AI 生成图文笔记：规格驱动开发 + 测试驱动开发）搭建的
Python 开发工具链，用于"做项目前先出规格、先写测试再实现"的流程。

## 已配置的工具

| 工具 | 用途 | 验收命令 |
|------|------|----------|
| pytest | TDD 动态测试（红→绿→重构） | `python -m pytest` |
| pyright | 静态类型/错误校验 | `python -m pyright` |
| FastAPI + uvicorn | 后端 API（笔记演示技术栈） | `python -c "import fastapi"` |
| httpx | API 测试客户端 | `python -c "import httpx"` |
| Playwright + Chromium | 前端自动化测试 | `python -m playwright install --dry-run chromium` |

## 三层验收机制（笔记 7 节）

1. 静态校验：`python -m pyright`（类型错误、导入缺失、参数不匹配）
2. 动态测试：`python -m pytest`（全量测试用例）
3. 人工复检：检查易用性与业务逻辑

## 快速开始

```powershell
cd sdd
.\.venv\Scripts\python.exe -m pytest    # 跑测试（冒烟测试应全绿）
.\.venv\Scripts\python.exe -m pyright    # 静态校验
```

## 目录结构

```text
sdd/
├─ spec/                 ← 规格文档区（先 Spec 再实现）
│  ├─ working_agreement.md  协作规范
│  ├─ product_spec.md       产品规格模板
│  ├─ api_contract.md       API 契约方法卡（OpenAPI）
│  ├─ planned/              待实现规格
│  ├─ implemented/          已完成规格
│  └─ archived/             历史版本存档
├─ tests/                ← 测试用例区（TDD）
│  ├─ conftest.py           共享夹具
│  └─ test_smoke.py         工具链冒烟测试
├─ requirements.txt
├─ pyrightconfig.json
└─ pytest.ini
```

新项目起步：复制本目录到项目根，或按 `spec/working_agreement.md` 的流程操作。
