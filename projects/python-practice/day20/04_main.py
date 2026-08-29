# Day 20 · 小脚本 2 完整版：汇率查询 → 存 CSV
# 结构：一个函数一个职责（本周检查点"模块化"验收对象）
#   fetch_rates —— 只负责抓数据（返回解析好的字典）
#   build_rows  —— 只负责解析（字典 → 行列表）
#   save_csv    —— 只负责存文件
#   main        —— 组装三兄弟 + 异常处理
#
# 网络提醒：直连不通时，运行前先设代理（新终端要重设）：
#   $env:HTTPS_PROXY = "http://127.0.0.1:7897"
#   $env:HTTP_PROXY = "http://127.0.0.1:7897"

import csv
import requests

API_URL = "https://open.er-api.com/v6/latest/USD"
币种表 = ["CNY", "JPY", "EUR", "GBP", "KRW", "HKD", "AUD", "CAD"]


def fetch_rates():
    """抓数据：请求 API，失败直接抛异常（交给 main 处理）"""
    r = requests.get(API_URL, timeout=15)
    r.raise_for_status()
    return r.json()


def build_rows(data):
    """解析：把 166 个币种的字典，挑出关心的，整理成「一行一条」"""
    rows = []
    for 币种 in 币种表:
        rows.append([币种, data["rates"][币种], round(1 / data["rates"][币种], 6)])
    return rows


def save_csv(rows):
    """存文件：utf-8-sig 保证 Excel 打开中文不乱码"""
    with open("汇率.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["币种", "1 USD 兑换", "1 币种折合 USD"])
        writer.writerows(rows)


def main():
    try:
        data = fetch_rates()      # ① 抓
        rows = build_rows(data)   # ② 解析
        save_csv(rows)            # ③ 存
        print(f"✅ 成功！共 {len(rows)} 种货币，已保存到 汇率.csv")
    except requests.exceptions.Timeout:
        print("① 超时：服务器没响应，稍后再试")
    except requests.exceptions.ConnectionError:
        print("② 连不上：检查网络或代理")
    except requests.exceptions.HTTPError as e:
        print("③ HTTP 错误:", e)
    except Exception as e:
        print("④ 其他错误:", e)


if __name__ == "__main__":
    main()
