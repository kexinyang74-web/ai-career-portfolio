# Day 18 第 3 步：状态码（练习文件）

import requests

# httpbin.org 提供各种状态的测试地址：/status/404、/status/500 等
网址们 = [
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
]

for 网址 in 网址们:
    r = requests.get(网址)
    print(f"{网址} → {r.status_code}")

    # ---- 练习：把下面改成"判断成功"的标准写法 ----
    # if r.status_code == 200:
    #     print("成功")
    # else:
    #     print("失败")
    if r.status_code == 200:
        print("成功")
    else:
        print("失败")