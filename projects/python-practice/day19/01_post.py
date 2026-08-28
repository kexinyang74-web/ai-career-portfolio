# Day 19 · 练习 1：POST——往服务器"送"东西
# 运行前想清楚：GET 是"给我"，POST 是"给你"。
# 下面的代码可以直接运行。运行后，完成文件末尾的练习。

import requests

# 方式一：data= 送表单格式（像填网页表单）
r1 = requests.post("https://httpbin.org/post", data={"名字": "杨可新", "年龄": 23})
print("data= 的返回：")
print(r1.json())
print()

# 方式二：json= 送 JSON 格式（调 API 最常用！）
r2 = requests.post("https://httpbin.org/post", json={"名字": "杨可新", "年龄": 23})
print("json= 的返回：")
print(r2.json())

# 观察：httpbin 会把收到的数据回显。data= 的结果在 "form" 里，json= 的结果在 "json" 里。

# ============ 练习 ============
# 1. 把上面 json= 里的数据改成你自己的信息（比如 {"名字": "你的名字", "专业": "转行AI"}），再运行一次。
# 2. 想一想：如果我把 data= 和 json= 都写上，服务器会怎么处理？运行验证你的猜测（不用回答，留到日志里）。
