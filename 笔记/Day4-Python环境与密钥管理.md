# Day 4 · Python 环境与密钥管理（venv / pip / .env / .gitignore）

> 目标：① 能在虚拟环境里安装依赖并运行脚本；② 学会用 `.env` 保存密钥，理解"密钥绝不提交到 Git"。

## 一、环境现状（本机已就绪）

- Python 3.13.5（`D:\proflim\python.exe`），满足 3.12+ 要求 ✅
- pip 25.1 ✅
- 编辑器：VS Code 已安装（`C:\Users\Administrator\AppData\Local\Programs\Microsoft VS Code\Code.exe`，v1.131.0）；也可用 Cursor（VS Code 同系编辑器）
- 实战项目：`projects/project-1-ai-assistant`（项目一骨架，第 5 周开始真正开发）

## 二、venv：项目的"独立小房间"

**为什么要隔离**：不同项目要的依赖版本可能不同，全装进全局 Python 会互相打架；venv 给每个项目一个独立的 Python + 包环境。

心智模型：**venv = 项目专属小房间，全局 Python = 公共大厅**。在房间里装什么，都影响不到大厅和其他房间。

常用命令（PowerShell）：

```powershell
# 1. 创建虚拟环境（在项目目录下执行一次）
python -m venv .venv

# 2. 激活（激活后命令行前面出现 (.venv)，python/pip 都用房间里的）
.\.venv\Scripts\Activate.ps1

# 如果报"禁止运行脚本"，先给当前终端放行：
Set-ExecutionPolicy -Scope Process Bypass

# 3. 安装依赖 / 查看已装 / 退出
pip install -r requirements.txt
pip list
deactivate
```

**实战结果**：项目一的 `.venv` 已创建，`requests` 和 `python-dotenv` 已装好；`python main.py --help` 正常运行，说明环境可用。

## 三、requirements.txt：依赖清单

- 作用：告诉别人/未来的你"这个项目需要装哪些包"，是项目的"购物清单"
- 换电脑三步走：`python -m venv .venv` → `pip install -r requirements.txt` → 运行
- 想看当前环境装了全部什么（含间接依赖）：`pip freeze`

## 四、.env 密钥管理（安全底线）

**为什么密钥绝不能提交到 Git**：仓库是公开的，提交 = 把密钥公开给全世界。别人拿到你的密钥可以盗刷你的 API 额度，真金白银地花钱。

正确姿势：

1. 密钥写进 `.env`（绝不写进代码）
2. 代码里用 `os.getenv("DEEPSEEK_API_KEY")` 读取（配合 `python-dotenv` 的 `load_dotenv()`）
3. `.env` 写进 `.gitignore`，Git 永远不跟踪它
4. 仓库里提交一份 `.env.example`（占位符版），告诉别人"要填哪些变量"，但不含真实值

**实战验证**（本项目）：

```powershell
git check-ignore -v projects/project-1-ai-assistant/.env
# 输出：projects/project-1-ai-assistant/.gitignore:1:.env  .env
# 意思是：.env 被 .gitignore 第 1 行规则排除
```

`git status` 里看不到 `.env` 和 `.venv`——文件在硬盘上存在，但 Git 假装没看见，这就是"不提交"。

口诀：**密钥进 .env，.env 进 .gitignore，代码只读环境变量；真实密钥永远只在本地。**

## 五、Day 4 检查单（怎么算过关）

- [x] `python -m venv` 能创建虚拟环境
- [x] `pip install -r requirements.txt` 能装依赖
- [x] 在 venv 里能运行脚本（`python main.py --help`）
- [x] 知道密钥为什么不能提交 + 会用 `.env` / `.gitignore`
- [x] `git status` 确认 `.env` 没有被跟踪
