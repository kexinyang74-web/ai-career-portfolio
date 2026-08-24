# Day 12 · 异常处理（try/except）与 logging（手把手版）

> 用法：跟着步骤一步一步做，**每做完一步就运行一次、看一次输出**。卡住了把报错原文贴给我。
> 练习文件放在 `projects/python-practice/day12/`，做完会进 GitHub。
> 今天的内容是为第 13 天「小脚本 1」做准备的——脚本要处理真实文件，真实文件就会出错、就要记录日志。

## 第 0 步：准备（5 分钟）

1. 打开 VS Code，左侧找到 `projects\python-practice` → 右键新建文件夹 `day12`
2. 开始前先想一个扎心的问题：你运行脚本时看到过 `Traceback (most recent call last)` 吗？（肯定见过！）今天学的就是**怎么不让它吓到你**。

---

## 第 1 步：try/except 基础（01_exception.py）

**30 秒知识点**：程序出错了会「翻车」——Python 会**当场停住**并扔出一大段红色报错（Traceback），这叫做「抛出异常」。`try/except` 就像给车装上**安全气囊**：出事时不翻车，而是被接住，程序继续跑。

**先看翻车现场**（新建 `01_exception.py`，自己敲）：

```python
# 第 1 步：try/except 基础
# 先制造一个「翻车」：读取一个不存在的文件
with open("不存在的文件.txt", "r", encoding="utf-8") as f:
    content = f.read()
print("文件读到了！")
```

运行 → 报错（FileNotFoundError）→ 最后一行的 `print` **根本没执行**。这就是翻车：程序在出错的第 2 行就停了。

**再装安全气囊**：

```python
# 第 1 步：try/except 基础
try:
    with open("不存在的文件.txt", "r", encoding="utf-8") as f:
        content = f.read()
    print("文件读到了！")
except FileNotFoundError:
    print("⚠️ 文件不存在，请检查文件名")
print("程序继续跑，没翻车")
```

运行 → 没有红色报错，输出友好提示，最后一行的 `print` **正常执行**了。

**语法拆解**：

```python
try:
    # 可能出错的代码放这里
    ...
except 错误类型:
    # 出错时执行的代码（救生垫）
    ...
```

**要能讲明白**：
- 报错信息里 `FileNotFoundError` 就是「错误类型」。Python 有几十种：`ZeroDivisionError`（除 0）、`ValueError`（值不对）、`KeyError`（键不存在）……
- `except` 后面**必须写错误类型**——新手最大的坑是写 `except:`（裸捕），等于「什么错都接」。这样真正的 bug 也被吞掉，**调试时哭都来不及**。规则：**接住能预期的错，其他的让它暴露出来**。

**挑战 1**：把 `with open` 的文件名换成存在的文件（比如你自己建的 `hello.txt`），再看看输出是什么？——注意：`try` 里的代码**成功执行**时，`except` 里的代码**不会运行**。

**挑战 2（看不同的错）**：

```python
try:
    number = int("abc")     # 字符串转整数，转不了！
    print(number)
except ValueError:
    print("⚠️ 转不了整数")
```

预测一下输出，再运行验证。

---

## 第 2 步：else 和 finally（02_try_else_finally.py）

**30 秒知识点**：`try/except` 还有两个「兄弟」：

| 关键字 | 什么时候执行 | 比喻 |
|--------|------------|------|
| `else` | **没出错时**执行 | 安全气囊没弹出，正常下车 |
| `finally` | **不管出没出错，一定执行** | 下车后必须关车门 |

**动手**（新建 `02_try_else_finally.py`）：

```python
# 第 2 步：else 和 finally
try:
    with open("hello.txt", "r", encoding="utf-8") as f:
        content = f.read()
except FileNotFoundError:
    print("文件不存在")
else:
    print("文件读到了：", content)     # 没出错才执行
finally:
    print("收尾：无论发生什么，这句都会打印")
```

**要能讲明白**：`finally` 是不是让你想起昨天学的 `with open`？——对！**`with` 的「自动关闭文件」底层就是靠 `finally` 实现的**：不管里面代码成功还是报错，finally 保证文件一定被关闭。昨天学的今天用上了，知识是连通的 🎯

**挑战**：把 `hello.txt` 改成一个不存在的文件名再运行，观察：`else` 不执行了，但 `finally` 依然执行——对照表格验证你的理解。

---

## 第 3 步：主动抛错 raise（03_raise.py）

**30 秒知识点**：`except` 是「接住别人的错」，`raise` 是「**自己主动扔错**」。什么时候用？——**发现参数不对劲，当场拒绝干活**，比算出一堆垃圾结果强。

**动手**（新建 `03_raise.py`）：

```python
# 第 3 步：主动抛错 raise
def calc_score(score):
    if score < 0 or score > 100:
        raise ValueError(f"分数 {score} 不合法，必须在 0-100 之间")
    return score * 2

try:
    print(calc_score(50))    # 正常，输出 100
    print(calc_score(999))   # 出问题：主动抛 ValueError
except ValueError as e:
    print("⚠️ 捕获到主动抛出的错：", e)
```

**要能讲明白**：`raise ValueError(信息)` = 主动扔出一个错误，扔的时候**附带一句说明**；`except ValueError as e` 里的 `as e` = 把错误说明「接住」存到变量 `e` 里，打印出来就是那句中文提示。

---

## 第 4 步：logging 基础（04_logging.py）

**30 秒知识点**：到目前你记录程序信息全靠 `print`。print 就像**对现场喊话**——喊完就没了，人走了什么证据都不剩。`logging` 是**写工作日志**——带时间、带级别、能存文件、随时能查。真实项目（包括你以后写的 API 调用）**没人用 print 排障**，都用 logging。

**动手**（新建 `04_logging.py`）：

```python
# 第 4 步：logging 基础
import logging

# 配置日志：级别 + 格式（时间 | 级别 | 消息）
logging.basicConfig(
    level=logging.INFO,        # 只记录 INFO 及以上级别
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logging.debug("这是 DEBUG：最啰嗦的细节")      # 不会显示（级别不够）
logging.info("程序开始运行了")                  # 会显示
logging.warning("警告：文件快满了")             # 会显示
logging.error("出错啦！文件读不了")             # 会显示
```

**5 个级别（从低到高，像「危机程度」分级）**：

| 级别 | 含义 | 什么时候用 |
|------|------|-----------|
| DEBUG | 调试细节 | 查 bug 时临时开 |
| INFO | 正常流程 | 「程序开始」「读到了 100 条数据」 |
| WARNING | 有点问题但不致命 | 「磁盘快满了」 |
| ERROR | 出错了但程序还能活 | 「这次请求失败，重试」 |
| CRITICAL | 致命，程序活不了 | 「数据库连不上了」 |

**要能讲明白（面试也常问）**：`print` 和 `logging` 的区别？

| | print | logging |
|---|---|---|
| 带时间戳吗 | ❌ 没有 | ✅ 有 |
| 分级别吗 | ❌ 只有一种 | ✅ 5 级 |
| 能存文件吗 | ❌ 只能屏幕上 | ✅ 可写文件 |
| 能关掉吗 | ❌ 要一行行删 | ✅ 改一行级别 |

**挑战（把日志写进文件）**：在 `basicConfig` 里加一个参数 `filename="app.log"`，再运行——注意屏幕没输出了，去 `day12` 文件夹里找 `app.log` 打开看，日志全记在文件里了。

---

## 今天的产出物（重要！）

把 **Day 11 的 04_read_json.py 改造**成新文件 `05_read_json_guarded.py`：

- 用 `try/except` 接住两种情况：文件不存在（FileNotFoundError）、JSON 内容损坏（json.JSONDecodeError）
- 用 `logging` 记录：开始、成功、出错三个信息（INFO/ERROR）
- 运行验证：① 正常读 user.json 成功 ② 删掉 user.json 再运行 → 不翻车、有日志

这是「小脚本 1」的预演——**真实脚本 = 干活 + 防出错 + 记日志**，今天你就学会了全套。
