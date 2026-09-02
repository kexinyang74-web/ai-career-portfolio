# Day 22 虚拟环境 + 依赖管理 + 配置管理

> 第 4 周第 1 天（工程化）。今天全部内容围绕一个词：**环境可复现**——别人从 git 拉到你的项目，按几步就能跑起来。配套练习：projects/python-practice/day22/。

## 一、为什么要虚拟环境？

- 直接 `pip install` 装到**全局环境**，所有项目共用 → 版本打架（A 要 requests 2.31、B 要 2.32）
- venv = 每项目一个独立抽屉：解释器、包、配置互不干扰
- **铁证实验**：`01_where_am_i.py` 在全局跑 → requests 2.34.2 ✅；在 venv 里跑 → `ModuleNotFoundError` ❌
- 同一个脚本、同一个电脑，换环境结果不同 → 隔离是真的

## 二、venv 实操（Windows PowerShell）

| 操作 | 命令 | 说明 |
|---|---|---|
| 创建 | `python -m venv .venv` | 在当前目录生成 .venv 文件夹 |
| 激活 | `.\.venv\Scripts\Activate.ps1` | 成功后命令行前面出现 `(.venv)` |
| 查看环境 | `python 01_where_am_i.py` | 打印 `sys.executable`，路径带 `.venv` 就是在抽屉里 |
| 退出 | `deactivate` | 回到全局 |
| 报错处理 | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` | 激活时"禁止运行脚本"就先用它 |

**坑（今天实测）**：
1. **venv 必须建在项目文件夹里**——别人 clone 后进项目就能激活。建错在根目录要删掉重建
2. **新开终端窗口 = 目录回到默认位置**，相对路径命令全部失效 → 先 `Get-Location` 看目录，再 `cd` 到项目

## 三、requirements.txt（购物清单）

- 导出清单：`pip freeze > requirements.txt`
  - `>` = 重定向：把命令输出写进文件（Day 23 细讲）
- 一键复现：`pip install -r requirements.txt`
- 格式：`requests==2.34.2`（`==` 锁死精确版本，保证一字不差）
- **依赖树**：只装 requests，清单却出现 5 个包——requests 自带 4 个零件：
  - urllib3（网络传输底层）、certifi（SSL 证书）、idna（域名编码）、charset-normalizer（编码检测）
- **复现闭环**（今天演示）：删 .venv → `python -m venv .venv` → 激活 → `pip install -r requirements.txt` → 跑通 ✅
- pip 源：你的 pip 配了清华镜像（`pypi.tuna.tsinghua.edu.cn`），国内速度快

## 四、.env 配置管理

- 三文件约定：
  - `.env`：真实配置（密钥、URL），**被 git 忽略，不进仓库**
  - `.env.example`：模板（同样 key、空值/示例），**提交进 git**，告诉别人"要填什么"
  - 代码里 `读env()`：逐行解析 `KEY=值`，跳过空行和 `#` 注释
- **配置与代码分离**：改 `.env` 不改代码 → 程序行为变（TIMEOUT 15→5 演示）
- 验证忽略：`git check-ignore .env` 有输出 = 确认不进 git
- 第 5 周存大模型 API 密钥就用这套，推 GitHub 不泄露

## 五、速查命令卡（今天全部命令）

```powershell
python -m venv .venv              # 建环境
.\.venv\Scripts\Activate.ps1      # 激活
deactivate                        # 退出
pip install <包名>                 # 装包（装进当前激活的环境）
pip freeze > requirements.txt     # 导出依赖清单
pip install -r requirements.txt   # 按清单一键安装
Copy-Item .env.example .env       # 模板 → 真实配置
git check-ignore .env             # 验证 .env 被忽略
```

## 六、一句话总结

**环境可复现 = 解释器（venv）+ 依赖清单（requirements.txt）+ 配置模板（.env.example）三件套**，任何人 clone 后 5 步跑起来：建环境 → 激活 → 装依赖 → 准备配置 → 运行。
