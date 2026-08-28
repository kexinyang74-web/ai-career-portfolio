# Day 18 · requests 基础（手把手版）

> 用法：跟着步骤一步一步做，**每做完一步就运行一次、看一次输出**。卡住了把报错原文贴给我。
> 练习文件放在 `projects/python-practice/day18/`。
> 先想一个问题：你在浏览器地址栏输入网址按回车，发生了什么？——浏览器向那台服务器**要**了一个网页（请求），服务器把网页**送回**给你（响应）。今天用 Python 干同一件事：**用代码发请求、拿响应**。这是第 5 周调大模型 API 的直接基础。

## 第 0 步：准备（5 分钟）

1. VS Code 左侧 `projects\python-practice` → 新建文件夹 `day18`
2. 安装 requests（第 1 周学过的 pip，回忆一下）：

```powershell
pip install requests
```

装完验证：`python -c "import requests; print(requests.__version__)"`

---

## 第 1 步：第一个网络请求（01_get.py）

**30 秒知识点**：`requests.get(网址)` = 用 Python 发出一个 GET 请求（GET = "给我东西"）。它会返回一个**响应对象**，里面装着服务器回给你的所有内容。

```python
import requests

r = requests.get("https://httpbin.org/get")
print(r.status_code)     # 状态码：200 = 成功
print(r.text)            # 响应内容（文字形式）
```

**响应对象 r 的三个常用成员**：

| 成员 | 是什么 | 例子 |
|------|--------|------|
| `r.status_code` | 状态码，服务器说"这次请求结果如何" | 200 成功 / 404 找不到 / 500 服务器坏了 |
| `r.text` | 响应内容，纯文字 | 网页 HTML、JSON 文本 |
| `r.json()` | 把 JSON 文字**解析成 Python 的字典/列表** | 见第 2 步 |

**浏览器和 requests 的区别**：浏览器会把响应渲染成好看的网页；requests 只把内容原样给你——它不负责"好看"，只负责"拿到"。

---

## 第 2 步：JSON 是什么 + 怎么解析（02_json.py）

**30 秒知识点**：服务器之间传数据最爱用 **JSON**——一种长得**几乎和 Python 字典/列表一模一样**的纯文字格式。区别只有几个：`true/false`（不是 True/False）、字符串必须用双引号。

服务器返回的 JSON 长这样：

```json
{"userId": 1, "id": 1, "title": "delectus aut autem", "completed": false}
```

`r.json()` 一解析，它就成了 Python 的字典——**你 Day 10 学的东西全部能用了**：

```python
import requests

r = requests.get("https://jsonplaceholder.typicode.com/todos/1")
数据 = r.json()                 # 解析成 Python 字典

print(数据["title"])            # 按键取值，和普通字典一样！
print(数据["completed"])        # False（注意：JSON 的 false 变成 Python 的 False）
```

---

## 第 3 步：状态码怎么用（03_status.py）

**30 秒知识点**：状态码是服务器给你的"回执单"——这次请求成没成功、为什么。

| 状态码 | 意思       | 你该干什么       |
| --- | -------- | ----------- |
| 200 | 成功       | 放心用数据       |
| 404 | 你要的东西不存在 | 检查网址对不对     |
| 500 | 服务器自己坏了  | 不是你的错，等会儿再试 |


**判断成功的标准写法**（记住这个模式）：

```python
import requests

r = requests.get("https://httpbin.org/status/404")   # 故意访问一个不存在的
if r.status_code == 200:
    print("成功，处理数据")
else:
    print(f"出错了，状态码：{r.status_code}")
```

---

## 第 4 步：超时——不加会出大事（04_timeout.py）

**30 秒知识点**：不设超时，如果服务器一直不响应，你的程序会**永远等下去**（卡死）。加 `timeout=5` = "5 秒内不回我就放弃"。

```python
import requests

try:
    r = requests.get("https://httpbin.org/delay/3", timeout=5)
    print("拿到了！")
except requests.exceptions.Timeout:
    print("超时了：服务器 5 秒没回应")
```

**两个新东西**：
- `timeout=5`：参数，秒数
- `try / except`：Day 12 学的异常处理，正好用上——超时会抛 `Timeout` 异常，捕获它就不会让程序崩掉

---

## 第 5 步：LeetCode 2 道（任务 3）

今天继续 2 道简单题。写一句思路进日志。

---

## 小结（一天看完版）

| 知识点 | 一句话 |
|--------|--------|
| requests.get(网址) | 发一个 GET 请求，拿到响应对象 |
| r.status_code | 服务器回执单：200 成功 / 404 不存在 / 500 服务器坏了 |
| r.text | 响应内容（文字） |
| r.json() | 把 JSON 文字解析成 Python 字典/列表 |
| timeout=5 | 5 秒不回就放弃，防止程序永远卡住 |
| try/except | 捕获超时等异常，程序不崩 |

## 进阶预告（Day 19）

POST（往服务器送东西）、headers（请求头）、异常捕获全家桶——把"请求失败怎么办"补完整。
