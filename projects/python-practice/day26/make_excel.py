"""把脏 CSV 转成脏 Excel(为 xlsx 清洗演示制造素材)

顺便演示 openpyxl【写】Excel 的三句话:
  1. Workbook()         新建工作簿
  2. ws.append([...])   一行一行往里塞
  3. wb.save(路径)      保存成文件

跑法:python make_excel.py → 生成 销售数据_脏.xlsx
"""
import csv

import openpyxl

输入 = "销售数据_脏.csv"
输出 = "销售数据_脏.xlsx"

wb = openpyxl.Workbook()
ws = wb.active                      # 新工作簿默认带一个空 sheet
ws.title = "销售原始数据"            # 给 sheet 起名

with open(输入, encoding="utf-8-sig", newline="") as f:
    for row in csv.reader(f):       # csv 每一行
        ws.append(row)              # → Excel 每一行(照原样,保持脏)

wb.save(输出)
print(f"已生成 {输出}")
