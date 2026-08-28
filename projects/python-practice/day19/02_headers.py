# Day 19 · 练习 2：headers——请求的"自我介绍"
# 运行前想清楚：每次请求，浏览器/程序都会自动带上一堆"信封信息"（headers），
# 服务器靠这些信息决定怎么回你。今天试试自己自定义。

import requests

# 先看默认的 headers 长什么样（不传 headers 参数）
r1 = requests.get("https://httpbin.org/headers")
print("默认 headers 里的 User-Agent：")
print(r1.json()["headers"]["User-Agent"])
print()

# 再自定义 headers 发一次
headers = {
    "User-Agent": "我的学习脚本/1.0",
    "Accept": "application/json",
}

r2 = requests.get("https://httpbin.org/headers", headers=headers)
print("自定义后服务器收到的 User-Agent：")
print(r2.json()["headers"]["User-Agent"])

# ============ 练习 ============
# 1. 把 User-Agent 改成你自己的代号（比如 "转行AI训练中/1.0"），运行看效果。
# 2. 试着在 headers 里加一个自定义字段（比如 "X-我的标记": "第19天"），
#    运行后看服务器收到的 headers 里有没有它——httpbin 会原样回显。
