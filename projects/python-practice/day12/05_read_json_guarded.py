# 第 5 步：给 JSON 读取套上「防弹衣」——try/except + logging
# 真实脚本 = 干活 + 防出错 + 记日志
import json
import logging

# 配置日志：写到 app.log，INFO 级别，带时间
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("开始读取 user.json")

try:
    with open("user.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("user.json 不存在，请检查文件")
    logging.error("user.json 不存在")
except json.JSONDecodeError as e:
    print("user.json 内容损坏，不是合法的 JSON")
    logging.error(f"user.json 内容损坏: {e}")
else:
    # 只有上面没抛异常，才会执行到这里
    print(data["name"])
    print(data["age"])
    print(data["skills"][0])
    logging.info("读取成功")
