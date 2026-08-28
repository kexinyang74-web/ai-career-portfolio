# Day 19 · 练习 4：异常捕获全家桶
# 运行前想清楚：网络请求有四种常见失败方式，每种是一种异常。今天全学会。
# 这个文件直接运行会触发"超时"（delay/5 表示服务器故意拖 5 秒，timeout=2 只等 2 秒）。

import requests

try:
    r = requests.get("https://httpbin.org/delay/5", timeout=10)
    r.raise_for_status()          # 状态码 4xx/5xx 会抛 HTTPError
    print("成功:", r.status_code)
except requests.exceptions.Timeout:
    print("① 超时：服务器没响应")
except requests.exceptions.ConnectionError:
    print("② 连不上：检查网址/网络")
except requests.exceptions.HTTPError:
    print("③ 服务器返回了错误状态码:", r.status_code)
except requests.exceptions.RequestException as e:
    print("④ 其他请求错误:", e)

# ============ 练习 ============
# 1. 直接运行，看会不会走进"① 超时"分支。
# 2. 把 timeout=2 改成 timeout=10 再运行——服务器 5 秒后响应了，看看这次走进哪个分支？
# 3. 把网址故意改错（比如 https://httpbin.org/xxxxx 或把 .org 写成 .com）再运行——这次是哪种失败？
#    把网址改回正确的，再故意把端口改错？看看连接失败长什么样。
# 4. 用 https://httpbin.org/status/404 试试：这个网址专门返回 404，看 raise_for_status() 会不会报"③"。
