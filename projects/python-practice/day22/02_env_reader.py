"""练习 2：从 .env 读配置（不装任何包也能懂原理）

规则约定：
- .env 文件：存真实值（密钥等），已被 .gitignore 排除，不会传上 GitHub
- .env.example 文件：存模板（同样的 key，空值/示例值），提交进 git，告诉别人"你需要填什么"

第一次运行：复制 .env.example 为 .env（终端执行：Copy-Item .env.example .env）
"""
def 读env(文件名=".env"):
    """把 .env 里的"KEY=值"逐行读成一个字典。

    做了什么：打开文件，跳过空行和 # 注释行，遇到 = 就按"键=值"切开存进字典。
    为什么这样做：配置集中放一个文件，改配置不用改代码。
    """
    配置 = {}
    try:
        with open(文件名, "r", encoding="utf-8") as f:
            for 行 in f:
                行 = 行.strip()
                if not 行 or 行.startswith("#") or "=" not in 行:
                    continue  # 空行 / 注释 / 没等号的，跳过
                key, value = 行.split("=", 1)  # 只切第一个 =，值里再有 = 也不怕
                配置[key.strip()] = value.strip()
    except FileNotFoundError:
        print("⚠️ 没找到 .env 文件（第一次运行先复制 .env.example 为 .env）")
    return 配置


配置 = 读env()
API_URL = 配置.get("API_URL", "https://open.er-api.com/v6/latest/USD")
TIMEOUT = int(配置.get("TIMEOUT", "15"))  # .env 里是字符串，要用要转 int

print("API_URL:", API_URL)
print("TIMEOUT:", TIMEOUT)
