# Day 19 · 练习 3：params——GET 带"查询参数"
# 运行前想清楚：地址栏里 ?关键词=xxx 就是查询参数。requests 用 params 自动拼，
# 不用自己手写网址。

import requests

# 不带参数
r1 = requests.get("https://httpbin.org/get")
print("不带参数时服务器收到的 args：")
print(r1.json()["args"])
print()

# 带参数：等价于 GET https://httpbin.org/get?城市=北京&单位=摄氏度
params = {"城市": "北京", "单位": "摄氏度"}
r2 = requests.get("https://httpbin.org/get", params=params)
print("带参数时服务器收到的 args：")
print(r2.json()["args"])
print("实际请求的完整网址：")
print(r2.url)

# ============ 练习 ============
# 1. 把参数改成"查天气"的样子：{"城市": "上海", "天气": "晴", "温度": "35度"}，运行看 args 回显。
# 2. 观察 r2.url 的输出——requests 把字典自动拼成了 ?a=b&c=d 的格式。
#    想一想：中文在网址里变成了什么样子？（观察输出，不用回答，记到日志里）
