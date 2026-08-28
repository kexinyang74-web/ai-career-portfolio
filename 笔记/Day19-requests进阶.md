# Day 19 · requests 进阶（手把手版）

> 用法：跟着步骤一步一步做，**每做完一步就运行一次、看一次输出**。卡住了把报错原文贴给我。
> 练习文件放在 `projects/python-practice/day19/`。
> 先想一个问题：昨天你只会"问服务器要东西"（GET）。但现实里你还要**送东西**（发帖、登录、搜索）——今天学"送"（POST）、学"自我介绍"（headers）、学"请求失败怎么办"的完整答案（异常全家桶）。学完这些，Day 20 的小脚本 2 就能做了。

## 第 0 步：准备（5 分钟）

1. VS Code 左侧 `projects\python-practice` → 新建文件夹 `day19`

---

## 第 1 步：POST——往服务器"送"东西（01_post.py）

**30 秒知识点**：GET = "给我东西"，POST = "给你东西"。POST 把数据放在**请求体**里送给服务器，服务器处理后再回给你。

```python
import requests

# 方式一：data= 送表单格式（像填网页表单）
r = requests.post("https://httpbin.org/post", data={"名字": "小明", "年龄": 18})

# 方式二：json= 送 JSON 格式（调 API 最常用！）
r = requests.post("https://httpbin.org/post", json={"名字": "小明", "年龄": 18})

print(r.json())   # httpbin 会把收到的数据回显给你
```

**data 和 json 的区别**（重要）：

| 参数 | 送出去的格式 | 服务器看到的 |
|------|-------------|-------------|
| `data=` | 表单格式 | `"form": {"名字": "小明"}` |
| `json=` | JSON 格式 | `"json": {"名字": "小明"}` |

**为什么调 API 用 json= 多**：大模型 API、天气 API 这些"程序对程序"的接口都约好用 JSON 交流——你 Day 18 学过 JSON 解析，正好闭环。

---

## 第 2 步：headers——请求的"自我介绍"（02_headers.py）

**30 秒知识点**：请求不只带"要什么"，还带一叠"信封信息"（headers）：你是谁（User-Agent）、接受什么格式（Accept）……服务器靠这些决定怎么回你。

**有些 API 要求必须带特定 header**（比如认证信息 `Authorization`），不带就拒绝。

```python
import requests

headers = {
    "User-Agent": "我的学习脚本/1.0",
    "Accept": "application/json",
}

r = requests.get("https://httpbin.org/headers", headers=headers)
print(r.json())   # httpbin 会把服务器收到的 headers 原样回显
```

**试试看**：对比不带 headers 和带 headers 两次请求，`User-Agent` 字段的变化——你昨天看到过默认是 `python-requests/2.34.2`，这次变成你自定义的。

---

## 第 3 步：params——GET 带"查询参数"（03_params.py）

**30 秒知识点**：浏览器地址栏里的 `?关键词=xxx` 就是查询参数。requests 里用 `params` 字典自动拼——**不用自己拼网址**。

```python
import requests

params = {"城市": "北京", "单位": "摄氏度"}
r = requests.get("https://httpbin.org/get", params=params)
print(r.json()["args"])   # 服务器回显收到的参数
```

**相当于**：`https://httpbin.org/get?城市=北京&单位=摄氏度`

**params 的用途**：天气 API 要你传城市、搜索 API 要你传关键词——都是参数。Day 20 小脚本 2 一定会用到。

---

## 第 4 步：异常捕获全家桶（04_exceptions.py）

**30 秒知识点**：网络请求有**四种**常见的失败方式，每种对应一种异常。只处理一种是不够的。

| 失败方式 | 异常 | 什么时候发生 |
|---------|------|-------------|
| 连不上 | `requests.exceptions.ConnectionError` | 网址写错、域名不存在、断网 |
| 等太久 | `requests.exceptions.Timeout` | 服务器一直不响应（配合 timeout 用） |
| 服务器拒绝 | `requests.exceptions.HTTPError` | 状态码 4xx/5xx，用 `r.raise_for_status()` 触发 |
| 其他一切 | `requests.exceptions.RequestException` | 以上所有异常的"爸爸"，兜底用 |

**全家桶写法**（记住这个模式，这就是标准姿势）：

```python
import requests

try:
    r = requests.get("https://httpbin.org/delay/5", timeout=2)
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
```

**两个新东西**：
- `r.raise_for_status()`：一句话——"状态码不对就抛异常"。这样就不用每次手动 `if r.status_code == 200` 了
- `except 异常 as e`：把异常对象存到变量 `e` 里，打印它就能看到错误详情

---

## 第 5 步：LeetCode 2 道（任务 3）

今天继续 2 道简单题。写一句思路进日志。

---

## 小结（一天看完版）

| 知识点 | 一句话 |
|--------|--------|
| `requests.post(网址, json=数据)` | 往服务器送数据（调 API 用 json=） |
| `headers={...}` | 请求的"自我介绍"，认证/伪装 UA 都靠它 |
| `params={...}` | GET 的查询参数，自动拼 `?a=b&c=d` |
| `r.raise_for_status()` | 状态码不对就抛异常，替代手动 if 判断 |
| 异常全家桶 | Timeout / ConnectionError / HTTPError / RequestException 兜底 |

## 预告（Day 20）

**小脚本 2**：选一个公开 API（天气/汇率）→ requests 拉数据 → 解析 → 存 CSV。今天是最后一块拼图。
