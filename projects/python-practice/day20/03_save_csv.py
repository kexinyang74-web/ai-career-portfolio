# Day 20 · 小脚本 2 第 3 步：存成 CSV
# 运行前想清楚：Day 11 学过的 csv.writer 今天用上；
# 关键参数 encoding="utf-8-sig"——没有它，Excel 打开中文会乱码。

import csv
import requests

r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=15)
r.raise_for_status()
data = r.json()

想要 = ["CNY", "JPY", "EUR", "GBP", "KRW", "HKD", "AUD", "CAD"]
rows = []                                    # 先收集所有行
for 币种 in 想要:
    # 第三列：反过来算"1 个该币种 = 多少 USD"（round 保留 6 位小数）
    rows.append([币种, data["rates"][币种], round(1 / data["rates"][币种], 6)])

with open("汇率.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["币种", "1 USD 兑换", "1 币种折合 USD"])   # 表头
    writer.writerows(rows)                   # 数据行

print("已保存 汇率.csv，用 Excel 打开看看（应该没有乱码）")

# ============ 练习 ============
# 1. 用 Excel（或记事本）打开 汇率.csv，确认：三列都有数据、中文没乱码
# 2. 把 encoding="utf-8-sig" 改成 encoding="utf-8" 再跑一次，打开对比——
#    亲眼看看"乱码"长什么样，就永远记住 utf-8-sig 的用途了（看完改回来）
