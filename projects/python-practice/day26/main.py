"""小脚本 3 主程序:脏 CSV → 干净 CSV + 统计报告

用法(在 day26 目录下,二选一):
    python main.py
    .venv/Scripts/python.exe main.py

跑完看两个产出:
    销售数据_干净.csv   清洗后的数据(utf-8-sig,Excel 打开不乱码)
    清洗报告.txt        统计报告(终端也会打印一份)
"""
import csv

from cleaner import 清洗一行, 去重, 按区域汇总

字段名 = ["日期", "区域", "产品", "金额", "数量", "负责人"]


def 读脏csv(路径):
    """读原始 CSV → 行列表(csv.DictReader:每行变成 {列名: 值} 的 dict)"""
    with open(路径, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def 写干净csv(rows, 路径):
    """把干净行写回 CSV。utf-8-sig = Excel 打开不乱码(Day 20 学的)"""
    with open(路径, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=字段名)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in 字段名})


def 生成报告(原始行数, 无效数, 删重复数, 干净行, 路径):
    """统计报告:打印一份 + 写进 txt"""
    lines = []
    lines.append("销售数据清洗报告")
    lines.append("=" * 24)
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
    with open(路径, "w", encoding="utf-8") as f:
        f.write(报告)


def main():
    rows = 读脏csv("销售数据_脏.csv")
    原始行数 = len(rows)

    # 流水线第 1 段:逐行清洗(没救的行数出来,记入无效)
    干净行 = []
    无效数 = 0
    for row in rows:
        cleaned = 清洗一行(row)
        if cleaned is None:
            无效数 += 1
        else:
            干净行.append(cleaned)

    # 流水线第 2 段:去重(记录删了几行)
    去重前 = len(干净行)
    干净行 = 去重(干净行)
    删重复数 = 去重前 - len(干净行)

    # 产出 1:干净 CSV;产出 2:统计报告
    写干净csv(干净行, "销售数据_干净.csv")
    生成报告(原始行数, 无效数, 删重复数, 干净行, "清洗报告.txt")


if __name__ == "__main__":
    main()
