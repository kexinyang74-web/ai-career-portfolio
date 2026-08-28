# Day 18 第 1 步：第一个网络请求（练习文件）
# 运行前确认已安装 requests：pip install requests

import requests

r = requests.get("https://httpbin.org/get")

print("状态码:", r.status_code)      # 200 = 成功
print("响应内容:", r.text)           # 看看到底回了个啥
print()
print("类型:", type(r.text))         # 是字符串
