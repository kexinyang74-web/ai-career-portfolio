# Day 18 第 4 步：超时（练习文件）
# httpbin.org/delay/N 会故意等 N 秒才回复——用来演示超时

import requests

# 不设超时，跑到它回为止（试试 delay/3 要等几秒）
r = requests.get("https://httpbin.org/delay/1")
print("拿到:", r.status_code)

# ---- 练习：加 timeout + try/except ----
# 1. 给下面这行加 timeout=2
# 2. 用 try/except 包住，捕获 requests.exceptions.Timeout
# 3. 访问 delay/5（等 5 秒），观察 timeout=2 的效果
# r = requests.get("https://httpbin.org/delay/5", timeout=2)
# print("拿到:", r.status_code)
try:
    r = requests.get("https://httpbin.org/delay/5", timeout=2)
    print("拿到:", r.status_code)
except requests.exceptions.Timeout:
    print("超时")