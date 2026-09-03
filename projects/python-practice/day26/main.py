"""小脚本 3 主程序:脏数据(CSV 或 Excel)→ 干净数据 + 统计报告

用法(在 day26 目录下;跑 xlsx 前先执行一次 make_excel.py):
    python main.py csv     # 清洗 销售数据_脏.csv
    python main.py xlsx    # 清洗 销售数据_脏.xlsx

产出:
    销售数据_干净.csv / 销售数据_干净.xlsx   干净数据
    清洗报告.txt                            统计报告(终端也打印)
"""
import csv
import sys

import openpyxl

import loader
from cleaner import 清洗一行, 去重, 按区域汇总

字段名 = ["日期", "区域", "产品", "金额", "数量", "负责人"]


def 写干净csv(rows, 路径):
    """dict 行 → CSV(utf-8-sig = Excel 打开不乱码,Day 20 经验)"""
    with open(路径, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=字段名)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in 字段名})


def 写干净xlsx(rows, 路径):
    """dict 行 → Excel(openpyxl 写:append 一行一行塞)"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(字段名)
    for row in rows:
        ws.append([row[k] for k in 字段名])
    wb.save(路径)


def 清洗流水线(rows):
    """Day 26 写好的流水线,原样搬到函数里:
    逐行清洗(没救记无效)→ 去重(记录删除数)→ 返回干净行

    CSV 和 Excel 共用这一份——因为 loader 已经把两种格式
    都变成了同一种 dict 行,清洗代码不认识"文件格式"。
    """
    干净行 = []
    无效数 = 0
    for row in rows:
        cleaned = 清洗一行(row)
        if cleaned is None:
            无效数 += 1
        else:
            干净行.append(cleaned)
    去重前 = len(干净行)
    干净行 = 去重(干净行)
    return 干净行, 无效数, 去重前 - len(干净行)


def 生成报告(数据来源, 原始行数, 无效数, 删重复数, 干净行):
    """统计报告:打印一份 + 写进 txt"""
    lines = []
    lines.append("销售数据清洗报告")
    lines.append("=" * 24)
    lines.append(f"数据来源:      {数据来源}")
    lines.append(f"原始数据:      {原始行数} 行(含空行/重复/脏格式)")
    lines.append(f"无效行丢弃:    {无效数} 行(空行 / 缺关键字段 / 金额日期数量格式错)")
    lines.append(f"重复行删除:    {删重复数} 行")
    lines.append(f"清洗后:        {len(干净行)} 行")
    lines.append("")
    lines.append("按区域销售额(降序):")
    for region, total in 按区域汇总(干净行).items():
        lines.append(f"  {region}: ¥{total:,.2f}")
    总额 = sum(row["金额"] for row in 干净行)
    lines.append(f"  合计: ¥{总额:,.2f}")

    报告 = "\n".join(lines)
    print(报告)
    with open("清洗报告.txt", "w", encoding="utf-8") as f:
        f.write(报告)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("csv", "xlsx"):
        print("用法:python main.py csv|xlsx")
        return
    格式 = sys.argv[1]

    # 1. 读(不同格式在这一层就变成同一种 dict 行)
    if 格式 == "csv":
        rows = loader.读csv("销售数据_脏.csv")
    else:
        rows = loader.读xlsx("销售数据_脏.xlsx")

    # 2. 清洗(与格式无关,一个字不用改——复用!)
    干净行, 无效数, 删重复数 = 清洗流水线(rows)

    # 3. 写干净文件(格式跟随输入)
    if 格式 == "csv":
        写干净csv(干净行, "销售数据_干净.csv")
    else:
        写干净xlsx(干净行, "销售数据_干净.xlsx")

    # 4. 报告
    生成报告(f"销售数据_脏.{格式}", len(rows), 无效数, 删重复数, 干净行)


if __name__ == "__main__":
    main()
