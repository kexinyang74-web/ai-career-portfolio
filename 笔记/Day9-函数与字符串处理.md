# Day 9 · 函数与字符串处理（手把手版）

> 用法：跟着步骤一步一步做，**每做完一步就运行一次、看一次输出**。卡住了把报错原文贴给我。
> 练习文件都放在 `projects/python-practice/day9/`，做完会进 GitHub，是你"坚持写代码"的证据。

## 第 0 步：准备（5 分钟）

1. 打开 VS Code，文件 → 打开文件夹 → 选择 `C:\Users\Administrator\Desktop\学习安排`
2. 左侧资源管理器找到 `projects\python-practice` → 右键新建文件夹 `day9`
3. `Ctrl + \`` 打开终端，先 `cd projects\python-practice\day9`，运行 `D:\proflim\python.exe --version` 确认环境

## 第 1 步：函数入门（01_greet.py）

**30 秒知识点**：函数 = 把一段代码打包、起个名字，以后每次叫名字就能用。`def` 是"定义"的意思；`return` 是把结果交出去。

**动手**：新建 `01_greet.py`，**自己敲**（别复制）：

```python
# 函数：打招呼
def greet(name):
    return "你好，" + name + "！"

print(greet("小明"))
print(greet("小红"))
```

运行 → 预期输出（2 行）：

```text
你好，小明！
你好，小红！
```

**挑战**：把 `greet` 改成两个参数 `greet(name, greeting)`，`print(greet("小明", "早上好"))` 应输出 `早上好，小明！`——体会"参数 = 函数要的输入"。

## 第 2 步：return 和 print 的区别（02_add.py）

**30 秒知识点**：`return` 把结果"交出去"，调用处可以存进变量继续用；只 `print` 不 `return` 的函数，调用处拿到的结果是 `None`（什么都没有）。

**动手**：新建 `02_add.py`：

```python
# return 版：结果可以存进变量
def add(a, b):
    return a + b

result = add(3, 5)
print(result)          # 8

# print 版：只是打印，没有返回值
def show(a, b):
    print(a + b)

result2 = show(3, 5)   # 打印 8
print(result2)         # None
```

运行 → 预期输出（3 行）：

```text
8
8
None
```

看到 `None` 就说明：**只打印 ≠ 交结果**。写函数要返回数据时，必须用 `return`。

**挑战**：写 `is_even(n)`，`n` 是偶数返回 `True`，否则返回 `False`（提示：`return n % 2 == 0`），调用 `is_even(4)` 和 `is_even(7)` 验证。

## 第 3 步：字符串方法（03_strings.py）

**30 秒知识点**：字符串是"不可变"的，方法不会改原字符串，而是**返回一个新字符串**。常用方法：`strip` 去空白、`upper/lower` 大小写、`replace` 替换、`split` 分割、`join` 拼接。

**动手**：新建 `03_strings.py`：

```python
# 字符串方法
s = "  hello, python  "

print(s.strip())               # 去两端空格 → hello, python
print(s.upper())               # 全大写 → HELLO, PYTHON
print(s.replace("hello", "hi"))  # 替换 → hi, python
print(s.split(", "))           # 按", "分割 → ['hello', 'python']
print("-".join(["a", "b", "c"]))  # 拼接 → a-b-c
```

运行，逐行对照预期（4 行 + 1 行）。全对 = 成功 ✅

⚠️ 防坑：`split(", ")` 是**按"逗号+空格"切**；想按任意空白切就用不带参数的 `split()`。

**挑战**：把 `s.strip().split(", ")` 和 `" | ".join(...)` 组合起来，打印 `hello | python`（提示：先切出列表，再用 `" | ".join` 拼回去）。

## 第 4 步：字符串切片（04_slice.py）

**30 秒知识点**：切片写法 `s[起点:终点:步长]`，**含头不含尾**；负索引从右往左数（`-1` 是最后一个字符）；`[::-1]` 是反转。

**动手**：新建 `04_slice.py`：

```python
# 字符串切片
s = "python"

print(s[0])      # p
print(s[1:4])    # yth
print(s[:3])     # pyt
print(s[::2])    # pto
print(s[::-1])   # nohtyp
print(s[-1])     # n
```

运行 → 预期输出 6 行：`p` / `yth` / `pyt` / `pto` / `nohtyp` / `n`。全对 = 成功 ✅

**挑战**：`s = "abcdef"`，用切片取出 `ace`（隔一个取一个，提示：步长用 2）。

## 第 5 步：综合练习（05_word_count.py）

把今天的函数 + 字符串方法合起来用：

```python
# 统计一句话有几个单词
def count_words(text):
    return len(text.split())

print(count_words("I love python"))        # 3

# 格式化人名：去空格 + 首字母大写
def format_name(first, last):
    return first.strip().title() + " " + last.strip().title()

print(format_name("  ada ", "  lovelace "))  # Ada Lovelace
```

运行 → 预期输出 2 行：`3` 和 `Ada Lovelace`。

**要能讲明白**（今天的核心原理）：`count_words` 里的 `text.split()` 把句子按空白切成单词列表，`len()` 数个数，`return` 把数字交出去——**一行代码 = 先切、再数、再交出去**。

## 第 6 步：LeetCode 2 道（独立做，约 1 小时）

打开 [力扣](https://leetcode.cn/problemset/all/) 筛选"简单"，做这两道：

1. **反转字符串**（题号 344）：把字符数组 `["h","e","l","l","o"]` 原地反转成 `["o","l","l","e","h"]`。提示：双指针——左指针从 0、右指针从最后，交换后左+1、右-1，直到相遇。
2. **最长公共前缀**（题号 14）：字符串数组里所有字符串共同的前缀，比如 `["flower","flow","flight"]` → `"fl"`；没有共同前缀返回 `""`。提示：先假设第一个字符串就是答案，再和后面的逐个比，比到不匹配就缩短。

规则：先自己想 20 分钟，想不出再看提示；必须跑通再贴给我看。每道在日志里写一句思路。

## 第 7 步：收尾

1. 做 [[Day9-自测5题]]（不许翻笔记）
2. 把练习代码路径 + 每道题思路 + "一个我能讲清楚的原理"写进 [[2026-08-21-Day9-学习日志]]
3. 发我：自测作答 + 2 道 LeetCode 的代码和输出，我批改
