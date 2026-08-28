# Day 18 第 2 步：JSON 解析（练习文件）
# jsonplaceholder 是一个"假数据" API，专门给学习者练手

import requests

# 拿一条"待办事项"
r = requests.get("https://jsonplaceholder.typicode.com/todos/1")
数据 = r.json()  # JSON 文字 → Python 字典

print("解析后的类型:", type(数据))  # <class 'dict'>
print("title:", 数据["title"])
print("completed:", 数据["completed"])  # 注意：JSON 的 false 变成了 Python 的 False

# ---- 练习：拿全部 200 条待办，统计已完成/未完成的条数 ----
# 提示：r.json() 这次会返回一个"列表"（列表里每个元素是字典）
# r = requests.get("https://jsonplaceholder.typicode.com/todos")
# todos = r.json()
# ...用 for 循环数一数 completed 为 True 的有多少条


r = requests.get("https://jsonplaceholder.typicode.com/todos")
todos = r.json()
completed = 0
not_completed = 0

for todo in todos:
    if todo["completed"]:
        completed += 1
    else:
        not_completed += 1
print("已完成:", completed)
print("未完成:", not_completed)
