# Day 20 · 小脚本 2 第 1 步：先调通 API，看看数据长什么样
# 运行前想清楚：这一步不写任何"功能"，只确认两件事——
#   1. 请求能成功（不报错）
#   2. 数据长什么样（为下一步解析做准备）

import requests

r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=15)
r.raise_for_status()              # 状态码不对直接抛异常
data = r.json()                   # 解析成字典

print("状态码:", r.status_code)
print("基准货币:", data["base_code"])                    # USD
print("更新时间:", data["time_last_update_utc"])
print("币种数量:", len(data["rates"]))
print("汇率样例: 1 USD =", data["rates"]["CNY"], "CNY")

# ============ 练习 ============
# 1. 再打印 2 个你认识的币种，比如：
#    print("1 USD =", data["rates"]["JPY"], "JPY")    # 日元
#    print("1 USD =", data["rates"]["EUR"], "EUR")    # 欧元
# 2. 观察 data["rates"] 到底是什么类型（可以用 type() 打印出来确认）         字典
print("1 USD =", data["rates"]["JPY"], "JPY")
print("1 USD =", data["rates"]["EUR"], "EUR")
print(type(data["rates"]))