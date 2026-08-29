# Day 20 · 小脚本 2 第 2 步：解析——把字典转成"一行一条"
# 运行前想清楚：API 返回的是一个字典（166 个币种塞在里面），
# 但 CSV 是"一行一条数据"的表格。这一步把字典变成行。

import requests

r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=15)
r.raise_for_status()
data = r.json()

想要 = ["CNY", "THB", "MXN", "GBP", "KRW", "HKD", "AUD", "CAD"]   # 只留关心的币种
for 币种 in 想要:
    print(f"1 USD = {data['rates'][币种]} {币种}")

# ============ 练习 ============
# 1. 往"想要"里加 2 个你感兴趣的币种（提示：THB 泰铢、MXN 墨西哥比索、RUB 卢布……）
# 2. 想一想：如果某个币种代码写错了（比如 "CNY1"），会报什么错？改成错的运行验证
#    （这正好说明：字典取不存在的键会 KeyError——解析时要知道数据里到底有什么）
