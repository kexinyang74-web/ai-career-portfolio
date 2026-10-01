# FastAPI `/api/profile` 请求链路

日期：2026-10-01

## 本次目标

看懂浏览器访问 `/api/profile` 后，请求如何从 FastAPI 路由进入数据库，再把结果返回给浏览器。

## 完整链路

```text
浏览器访问 http://127.0.0.1:8765/api/profile
→ FastAPI 根据 @app.get("/api/profile") 找到 get_profile()
→ get_profile() 调用 db.profile()
→ 进入 store.py 的 Store.profile()
→ SQLite 执行 SELECT data FROM settings WHERE id=1
→ fetchone() 取出一行，[0] 取这一行的第一个值
→ json.loads() 把 JSON 字符串转换成 Python 字典
→ profile() 把字典返回给 get_profile()
→ FastAPI 把 Python 字典转换成 JSON 响应
→ 浏览器收到 JSON
```

## 第一层：浏览器地址与 FastAPI 路由

```python
@app.get("/api/profile")
def get_profile():
    return db.profile()
```

### `@app.get("/api/profile")`

这是路由装饰器（把请求地址绑定到下面的函数）。

它表示：收到对 `/api/profile` 的 GET 请求时，运行紧挨在下面的 `get_profile()`。

浏览器必须访问完整地址：

```text
http://127.0.0.1:8765/api/profile
```

只访问 `http://127.0.0.1:8765` 不会触发 `get_profile()`，因为缺少 `/api/profile` 路径。

路由地址由 `@app.get(...)` 决定，不由函数名决定。例如：

```python
@app.get("/api/test")
def abc():
    ...
```

访问 `/api/test` 时运行的是 `abc()`。

## 第二层：`get_profile()` 与 `profile()` 不是同一个函数

```python
def get_profile():
    return db.profile()
```

- `get_profile()`：在 `app.py` 中接收 FastAPI 请求。
- `db.profile()`：调用 `Store` 对象中的数据库方法。
- `def profile(self)`：在 `store.py` 中定义真正读取数据库的方法。

因此调用顺序是：

```text
get_profile() → db.profile() → Store.profile()
```

## 第三层：数据库查询

```python
def profile(self):
    with self.connection() as db:
        return json.loads(
            db.execute("SELECT data FROM settings WHERE id=1").fetchone()[0]
        )
```

SQL（数据库查询语句）是：

```sql
SELECT data FROM settings WHERE id=1
```

它的准确含义是：

> 从 `settings` 表中，找到 `id` 等于 `1` 的那一行，读取这一行的 `data` 列。

注意：`id=1` 是按条件寻找记录，不等于“取数据库的第一行”。

## 第四层：`fetchone()[0]`

```python
.fetchone()[0]
```

- `fetchone()`：获取查询结果中的一行。
- `[0]`：获取这一行中的第一个值。

Python 序号从 `0` 开始：

- `[0]` 是第一个值。
- `[1]` 是第二个值。

这里的 SQL 只选择了 `data` 一列，所以 `[0]` 取得的就是 `data`。

## 第五层：字符串、Python 字典与 JSON

数据类型变化如下：

```text
数据库中的 data
→ 取出时是 JSON 格式的字符串
→ json.loads() 解析
→ Python 程序内部得到 dict（Python 字典）
→ FastAPI 生成 JSON 响应
→ 浏览器收到 JSON
```

需要区分：

- 数据库刚取出的值：字符串。
- `json.loads()` 的结果：Python 字典。
- 网络返回给浏览器的结果：JSON。

如果删除 `json.loads()`，直接返回 `fetchone()[0]`，`profile()` 返回的就是字符串。

## 第六层：`return db.profile()` 做了什么

```python
return db.profile()
```

这一行同时做两件事：

1. `db.profile()` 执行数据库查询并得到 Python 字典。
2. `return` 把这个字典交回 FastAPI。

下面两种写法效果相同：

```python
return db.profile()
```

```python
result = db.profile()
return result
```

第二种写法保留了中间变量，更方便打断点（暂停程序查看状态）或打印检查。

如果只写：

```python
def get_profile():
    db.profile()
```

数据库查询仍然会执行，但因为没有 `return`，查询结果不会被返回，浏览器会收到空结果 `null`。

## 第七层：`self.connection()` 初步展开

项目中的代码是：

```python
@contextmanager
def connection(self):
    with closing(sqlite3.connect(self.path, timeout=10)) as db:
        with db:
            db.execute("PRAGMA foreign_keys=ON")
            yield db
```

目前先掌握第一步：

```python
sqlite3.connect(self.path, timeout=10)
```

- `self.path`：SQLite 数据库文件的位置。
- `sqlite3.connect(...)`：打开数据库文件并建立连接，不负责查询具体表。
- `timeout=10`：数据库被占用时最多等待 10 秒。
- `as db`：把建立好的数据库连接命名为 `db`，后面的代码通过它操作数据库。

## 本次易错点

1. 把本机根地址误当成完整接口地址；必须带上 `/api/profile`。
2. 混淆 `get_profile()` 与 `profile()`；前者接收接口请求，后者读取数据库。
3. 把表名 `settings` 写成 `setting`。
4. 把 `WHERE id=1` 理解成“取第一行”；它实际是寻找 `id` 等于 `1` 的行。
5. 混淆数据库字符串、Python 字典和浏览器收到的 JSON。
6. 以为删除 `return` 后数据库查询也不会执行；实际是查询仍执行，但结果没有返回。

