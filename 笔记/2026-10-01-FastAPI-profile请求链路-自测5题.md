# FastAPI `/api/profile` 请求链路 · 自测 5 题

日期：2026-10-01

> 不看复习笔记作答。答案写在“你的答案”下面，本文件暂不提供答案。

## 第 1 题：完整请求链路

从浏览器访问地址开始，到浏览器收到结果为止，用箭头写出 `/api/profile` 的完整请求链路。至少包含：完整地址、`app.py` 函数、`store.py` 方法、SQL、数据转换和返回结果。

你的答案：

## 第 2 题：路由与函数名

阅读代码：

```python
@app.get("/api/user")
def get_profile():
    return db.profile()
```

浏览器应该访问哪个完整地址？访问后首先运行哪个函数？函数名是否必须改成 `get_user()`？说明原因。

你的答案：

## 第 3 题：解释 SQL

不用代码术语堆砌，用一句中文准确解释下面的 SQL。注意区分“`id=1`”和“第一行”。

```sql
SELECT data FROM settings WHERE id=1
```

你的答案：

## 第 4 题：数据类型变化

分别写出以下三个位置的数据类型：

1. SQLite 刚取出的 `data`。
2. `json.loads()` 执行后的结果。
3. 浏览器最终收到的结果。

你的答案：

## 第 5 题：删除 `return`

如果把代码改为：

```python
def get_profile():
    db.profile()
```

数据库查询是否还会执行？查询结果是否会返回给浏览器？分别说明 `db.profile()` 和 `return` 的职责。

你的答案：

