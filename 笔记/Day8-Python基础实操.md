# Day 8 · Python 基础实操（手把手版）

> 用法：跟着步骤一步一步做，**每做完一步就运行一次、看一次输出**。卡住了把报错原文贴给我。
> 练习文件都放在 `projects/python-practice/day8/`，做完会进 GitHub，是你"坚持写代码"的证据。

## 第 0 步：准备（5 分钟）

1. 打开 VS Code
2. 文件 → 打开文件夹 → 选择 `C:\Users\Administrator\Desktop\学习安排`
3. 左侧资源管理器找到 `projects` → 右键新建文件夹 `python-practice` → 在里面再新建 `day8`
4. 按 `Ctrl + \`` 打开终端，输入 `D:\proflim\python.exe --version`，看到 `Python 3.13.5` 就 OK

## 第 1 步：变量与打印（01_variables.py）

**30 秒知识点**：变量 = 给数据贴标签。`age = 18` 就是把数字 18 贴上了 `age` 这个标签；之后用 `age` 就是在用 18。

**动手**：

1. 在 `day8` 文件夹新建 `01_variables.py`
2. **自己敲**下面代码（别复制，敲一遍比看十遍有用）：

```python
# 变量与打印
name = "小明"
age = 18
print(name)
print(age)
print("我叫" + name + "，今年" + str(age) + "岁")   # 字符串拼接版
print(f"我叫{name}，今年{age}岁")                    # f-string 版（推荐）
```

3. 终端先 `cd projects\python-practice\day8`，再运行 `D:\proflim\python.exe 01_variables.py`
4. **预期输出**（4 行）：

```text
小明
18
我叫小明，今年18岁
我叫小明，今年18岁
```

5. 看到 4 行输出 = 成功 ✅
6. **挑战**：把 `age` 改成 `20` 再跑，第 2、3、4 行都应变成 20——体会"变量是标签，改一处，所有用到的地方跟着变"
7. 报错的话：把错误原文贴给我。最常见的坑：中文引号（必须用英文 `"`）、f-string 前面漏了 `f`

## 第 2 步：if/elif/else 成绩分级（02_grade.py）

**30 秒知识点**：`if` 从上往下判断，命中一个条件就结束，不再往下看。

1. 新建 `02_grade.py`，输入：

```python
# 成绩分级
score = 85

if score >= 90:
    print("优秀")
elif score >= 60:
    print("及格")
else:
    print("不及格")
```

2. 运行 → 预期输出：`及格`
3. **挑战**：把 `score` 改成 `95`、`59`、`60` 各跑一次，应分别输出 优秀 / 不及格 / 及格
4. 想一想：为什么 `score=60` 输出"及格"而不是"优秀"？（因为 `60 >= 90` 不成立，会继续看 elif）

## 第 3 步：for + range 偶数求和（03_sum_even.py）

**30 秒知识点**：`range(1, 101)` 生成 1 到 100（含头不含尾）；`i % 2 == 0` 判断偶数。

1. 新建 `03_sum_even.py`，输入：

```python
# 1-100 偶数求和
total = 0
for i in range(1, 101):
    if i % 2 == 0:
        total += i   # 等价于 total = total + i
print(total)
```

2. 运行 → 预期输出：`2550`（1-100 偶数和的正确答案，输出这个就是成功 ✅）
3. **挑战**：`range(1, 101)` 改成 `range(1, 11)`，输出应是 `30`（2+4+6+8+10）

## 第 4 步：for vs while（04_loop_compare.py）

**30 秒知识点**：`for` 适合"知道循环几次"（遍历/数数）；`while` 适合"不知道几次、靠条件停"（比如直到用户输入 q）。

1. 新建 `04_loop_compare.py`，输入：

```python
# for：数 1-5
for i in range(1, 6):
    print("for:", i)

# while：数到 5 停
j = 1
while j <= 5:
    print("while:", j)
    j = j + 1
```

2. 运行 → 预期输出：for 1-5、while 1-5 共 10 行
3. **挑战**：用 while 打印 `10、8、6、4、2`（提示：`j = j - 2`，条件 `j >= 2`）
4. ⚠️ 防坑：while 里必须有让条件变化的语句（上面的 `j = j + 1`），否则死循环。真遇到死循环就按 `Ctrl + C` 停

## 第 5 步：找最大值（05_max.py）

1. 新建 `05_max.py`，输入：

```python
# 找最大值（不用内置 max）
nums = [3, 7, 2, 9, 5]
max_num = nums[0]      # 先假设第一个最大
for n in nums:
    if n > max_num:    # 发现有更大的，就更新
        max_num = n
print(max_num)
```

2. 运行 → 预期输出：`9`
3. **要能讲明白**（今天的核心原理）：`max_num` 像擂台主，循环里每个数上来挑战，谁大谁当擂主，循环结束擂主就是最大值
4. **挑战**：改成找最小值——只改一处比较符号和变量名

## 第 6 步：LeetCode 2 道（独立做，约 1 小时）

打开 [力扣](https://leetcode.cn/problemset/all/) 筛选"简单"，做这两道：

1. **交替合并字符串**（题号 1768）：`word1`、`word2` 交替取字符拼成一个新字符串。提示：`for i in range(max(len(word1), len(word2)))`，短的取完就只取长的
2. **两数之和**（题号 1）：给一个数组和目标值，找出哪两个数的下标相加等于目标值。提示：先写双层 `for` 暴力解（第 10 周学了字典再优化）

规则：先自己想 20 分钟，想不出再看提示；必须跑通再贴给我看。

## 第 7 步：收尾

1. 做 [[Day8-自测5题]]（不许翻笔记）
2. 把练习代码路径 + 每道题思路写进 [[2026-08-20-Day8-学习日志]]
3. 发我：自测作答 + 2 道 LeetCode 的代码和输出，我批改
