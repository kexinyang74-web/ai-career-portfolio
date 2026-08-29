# Day 22 迷你项目：环境可复现演示

展示"虚拟环境 + 依赖管理 + 配置管理"三位一体：

- `01_where_am_i.py`：看当前在哪个 Python 环境里跑
- `02_env_reader.py`：从 .env 读配置（API_URL / TIMEOUT）
- `requirements.txt`：依赖清单（别人一键复现）
- `.env.example`：配置模板（进 git）
- `.env`：真实配置（**不进 git**，需自己复制）

## 复现步骤（别人拿到你的项目这么跑）

```powershell
# 1. 建环境
python -m venv .venv

# 2. 激活（Windows PowerShell）
.\.venv\Scripts\Activate.ps1

# 3. 装依赖
pip install -r requirements.txt

# 4. 准备配置
Copy-Item .env.example .env

# 5. 跑
python 01_where_am_i.py
python 02_env_reader.py
```

## 原理一句话

**环境可复现 = 解释器（venv）+ 依赖清单（requirements.txt）+ 配置模板（.env.example）三件套，别人从 git 拉到你的项目，按上面 5 步就能跑起来。**
