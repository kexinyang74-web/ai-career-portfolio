# 第 5 步：读写 CSV
import csv

# 写：先把数据写成一个 csv 文件
rows = [
    ["姓名","语文","数学"],
    ["小明",90,85],
    ["小红",88,92],
]

with open("scores.csv","w",encoding="utf-8",newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

# 读：把 csv 读回来，一行一个列表
with open("scores.csv","r",encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        