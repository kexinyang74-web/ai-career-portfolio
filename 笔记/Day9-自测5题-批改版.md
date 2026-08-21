# Day 9 · 函数与字符串处理（自测 5 题批改版）

> 基于你的原作答（projects/python-practice/day9/ 里的 5 个文件）批改生成：**✅ = 已确认正确，⚠️ = 已修正/补充**。你的原作答已并入本文档。复习时优先看 ⚠️ 的部分。

**整体掌握情况**：第 1、4、5 题 ✅ 已掌握；第 2 题 ⚠️ 缺"一句话说明"；第 3 题 ⚠️ 挑战版差一个空格。你把每道题的"挑战版"都做了，主动求难是好事，但**基础版要先跑通再做挑战**——这次基础版大多只留在注释里没运行。

## 一、核心要点（一页速记）

- 函数：`def 名字(参数):` 定义；`return` 把结果**交回去**，调用处能存进变量继续用；只 `print` 不 `return` → 调用结果是 `None`
- 交换两个元素（temp 三步）：先存旧值 → 再覆盖 → 最后放回，防止数据丢失
- 字符串方法：`strip()` 去空白、`upper()` 大写、`replace(旧,新)` 替换、`split(分隔符)` 切成列表、`"分隔".join(列表)` 拼回字符串
- 切片 `s[起点:终点:步长]`：**含头不含尾**；`[::-1]` 反转；`[::2]` 隔一个取一个
- 双指针反转：左指针从 0、右指针从最后，交换后往中间走，直到相遇（left >= right 停）
- 最长公共前缀：先假设第一个字符串是答案，跟后面的逐个比，对不上就用 `prefix[:-1]` 削短

## 二、自测 5 题批改

### 第 1 题：函数定义与调用（✅ 挑战版正确）

- 你的作答（01_greet.py 实际运行部分）：
  ```python
  def greet(name, greeting):
      return greeting + "，" + name + "!"
  print(greet("小明", "早上好"))
  print(greet("小红", "晚上好"))
  ```
- 实际输出：`早上好，小明!` / `晚上好，小红!`
- 批注：✅ 两参数版本完全正确，参数用法（"参数 = 函数要的输入"）掌握了。基础版 `greet(name)` 在注释里保留着，写法也正确。小细节：题目要求输出"你好，小明！"，你做的是挑战版输出"早上好，小明!"——题目本身做的是挑战，基础版下次顺手跑一遍。

### 第 2 题：return 的作用（⚠️ 缺"一句话说明"）

- 你的作答（02_add.py）：
  ```python
  # def add(a, b):
  #     return a + b
  # result = add(3, 5)
  # print(result)
  # def show(a,b):
  #     print(a + b)
  # result2 = show(3, 5)
  # print(result2)

  def is_even(n):
      return n % 2 == 0
  print(is_even(4))
  print(is_even(7))
  ```
- 实际输出：`True` / `False`
- 批注：
  - ✅ `is_even` 挑战完全正确：`n % 2 == 0` 本身就是布尔表达式，直接 `return`，简洁标准
  - ⚠️ 题目要求两件事你没做：① `add(a, b)` 只留在注释里，没实际跑过；② **"一句话说明 return 和 print 的区别"没写**（这是这道题的重点，也是本周检查点"能讲清楚"的要求）
  - 你的补答（2026-08-21）：**"Return 它能保留它那个变量的值"**
  - 批注：方向对了——return 确实让"值"能被调用处接着用。但"保留"这个词不太准：return 不是把值留在函数里，而是**把值交回给调用处**，调用处才能把它存进变量；而且这句话只说了 return，没对比 print（题目要的是两者的区别）。参考说法：**"return 把结果交回调用处，能存进变量继续用；print 只是打印出来看一眼，调用处拿到的还是 None。"**

### 第 3 题：字符串方法（⚠️ 挑战版差一个空格）

- 你的作答（03_strings.py 实际运行部分）：
  ```python
  s = " hello,python "
  print (s.strip().split(","))
  print ("|".join(["hello","python"]))
  ```
- 实际输出：`['hello', 'python']` / `hello|python`
- 批注：
  - ✅ `s.strip().split(",")` 切得对：去空白 → 按逗号切 → `['hello', 'python']`
  - ⚠️ `"|".join(...)` 拼出来是 `hello|python`，题目要求 `hello | python`（**竖线两边有空格**），分隔符应该是 `" | "`
  - ⚠️ 更关键的是：你已经把正确答案写在注释里了（`print(" | ".join(s.strip().split(",")))`），但**实际运行的代码还是旧版**——把注释变成真正运行的代码，删掉旧的错误行，再跑一遍
  - 小习惯：`print (` 和 `print(` 之间不要空格（PEP 8）

### 第 4 题：字符串切片（✅ 挑战正确）

- 你的作答（04_slice.py 实际运行部分）：
  ```python
  s = "abcde"
  print(s[::2])
  ```
- 实际输出：`ace`
- 批注：✅ 挑战正确，`[::2]` 就是"隔一个取一个"。基础版 6 个切片（`s[0]`、`s[1:4]`、`s[:3]`、`s[::2]`、`s[::-1]`、`s[-1]`）在注释里也都写对了。题目要求的 `yth`（`s[1:4]`）、`nohtyp`（`s[::-1]`）、`pto`（`s[::2]`）下次把注释取消、真正跑一遍。

### 第 5 题：综合（✅ 全对 + 额外挑战也对）

- 你的作答（05_word_count.py）：
  ```python
  def count_words(text):
      return len(text.split())

  print(count_words("I love python"))

  def format_name(first,last):
      return first.strip().title() + " " + last.strip().title()

  print(format_name(" ada ", " lovelace "))
  ```
- 实际输出：`3` / `Ada Lovelace`
- 批注：✅ 完全正确，而且远超题目要求——`count_words` 用 `text.split()` 切词 + `len()` 数个数 + `return` 交回去，一步不差；还自己做了 `format_name` 挑战（去空格 + 首字母大写），输出 `Ada Lovelace`，也对。

## 三、小结与复习建议

- 已经掌握 ✅：函数定义/参数/return、is_even 布尔返回、切片步长、split/join 链条、count_words 综合
- 需要补 ⚠️：
  1. **第 2 题的一句话**：return 和 print 的区别（自己写，写完发我看）
  2. **第 3 题**：把注释里的 `print(" | ".join(s.strip().split(",")))` 变成实际运行的代码，输出 `hello | python`
  3. 习惯：先做基础版并跑通，再做挑战——这次 1、2、3、4 题的基础版都在注释里没运行
- 建议：把 14 最长公共前缀补上调用行（`print(longest_common_prefix(strs))`）跑通并提交力扣，今天内容就全齐了
