# Day 10 · 容器：列表/字典/元组/集合（手把手版）

> 用法：跟着步骤一步一步做，**每做完一步就运行一次、看一次输出**。卡住了把报错原文贴给我。
> 练习文件都放在 `projects/python-practice/day10/`，做完会进 GitHub，是你"坚持写代码"的证据。

## 第 0 步：准备（5 分钟）

1. 打开 VS Code，文件 → 打开文件夹 → 选择 `C:\Users\Administrator\Desktop\学习安排`
2. 左侧资源管理器找到 `projects\python-practice` → 右键新建文件夹 `day10`
3. `Ctrl + \`` 打开终端，先 `cd projects\python-practice\day10`，运行 `D:\proflim\python.exe --version` 确认环境

## 第 1 步：列表 list——"能改的袋子"（01_list.py）

**30 秒知识点**：列表用方括号 `[]`，可以装任何东西，**按位置（索引）存取**，索引从 0 开始。核心操作四个字：**增、删、改、查**。

**动手**：新建 `01_list.py`，**自己敲**（别复制）：

```python
# 列表：增删改查
fruits = ["apple", "banana", "cherry"]

# 查：按索引取值 + 数长度
print(fruits[0])        # apple（索引从 0 开始）
print(fruits[-1])       # cherry（-1 是最后一个）
print(len(fruits))      # 3

# 增：末尾加 append，指定位置插 insert
fruits.append("orange")        # 加到末尾
fruits.insert(1, "grape")      # 插到索引 1
print(fruits)          # ['apple', 'grape', 'banana', 'cherry', 'orange']

# 改：按索引重新赋值
fruits[0] = "watermelon"
print(fruits[0])       # watermelon

# 删：按值删 remove，按位置删 pop，清空 clear
fruits.remove("banana")     # 删掉值为 "banana" 的那项
fruits.pop()                # 删掉最后一项并返回它
print(fruits)          # ['watermelon', 'grape', 'cherry']

# 遍历：for 循环一个一个拿出来
for f in fruits:
    print(f)
```

运行，逐行对照预期。全对 = 成功 ✅

**要能讲明白**：`fruits[0] = "watermelon"` 是在**改原袋子里的东西**（跟字符串不一样，字符串改不了，列表能改——这个区别后面记笔记）。

**挑战**：新建一个列表 `numbers = [3, 1, 4, 1, 5]`，用 `numbers.append(9)`、`numbers.sort()` 和 `numbers.pop(0)` 各操作一次，打印看看结果（提示：`sort()` 原地排序，`pop(0)` 删第一项）。

## 第 2 步：字典 dict——"带标签的储物柜"（02_dict.py）

**30 秒知识点**：字典用花括号 `{}`，存的是**键值对**（`key: value`），用"标签（键）"取"东西（值）"，不用记位置。核心操作同样是：**增、删、改、查**。

**动手**：新建 `02_dict.py`：

```python
# 字典：增删改查
student = {"name": "小明", "age": 18, "city": "上海"}

# 查：按键取值（键不存在会报错！）
print(student["name"])       # 小明
print(student.get("age"))    # 18（get 不存在时返回 None，不报错）
print(student.get("score", "没有这个键"))   # 没有这个键（默认值）

# 判断键在不在
print("name" in student)     # True

# 增：直接给新键赋值
student["score"] = 95
print(student)               # {'name': '小明', 'age': 18, 'city': '上海', 'score': 95}

# 改：给已有键重新赋值
student["age"] = 19
print(student["age"])        # 19

# 删：pop 删指定键，del 也行
student.pop("city")
print(student)               # 键 city 没了

# 遍历：items() 一次拿键和值
for key, value in student.items():
    print(key, "→", value)
```

运行，逐行对照预期。全对 = 成功 ✅

⚠️ 防坑：`student["不存在的键"]` 会直接报 `KeyError`；不确定键在不在时，用 `.get()` 更安全。

**要能讲明白**：字典 = 用"名字（键）"找"东西（值）"，查找速度跟字典大小无关（哈希表，第 3 周学哈希时还会遇到）。列表用位置找，字典用名字找——这是两者最大的区别。

**挑战**：建一个 `scores = {"语文": 90, "数学": 85}`，用 `for` 循环打印"语文 90 分"这种格式；再把数学改成 95，把英语 `update` 进去（提示：`scores.update({"英语": 88})`）。

## 第 3 步：元组 tuple——"封起来的列表"（03_tuple.py）

**30 秒知识点**：元组用圆括号 `()`，**创建后就不能增删改**（不可变）。能查、能遍历，但 `t[0] = 1` 会报错。什么时候用？"这份数据不该被改动"的时候——比如坐标、配置项、常量集合。

**动手**：新建 `03_tuple.py`：

```python
# 元组：只读列表
point = (10, 20)

print(point[0])        # 10（能查）
print(len(point))      # 2

# 元组可以拆包（把里面的值一个个拿出来）
x, y = point
print(x, y)            # 10 20

# 尝试修改会报错（试试看）
# point[0] = 99        # TypeError: 'tuple' object does not support item assignment

# 元组和列表互转
lst = list(point)      # 元组 → 列表（列表可变）
lst.append(30)
t2 = tuple(lst)        # 列表 → 元组
print(t2)              # (10, 20, 30)
```

运行 → 预期输出：`10` / `2` / `10 20` / `(10, 20, 30)`。全对 = 成功 ✅

**要能讲明白**：为什么要有不能改的元组？——**约定**：看到元组就知道"这数据不会变"，代码更好懂；另外元组能做字典的键，列表不能（因为列表会变，后面学到）。

**挑战**：定义一个 `week = ("一", "二", "三")`，用拆包写 `a, b, c = week` 打印三个字；再想想：`"一" in week` 输出什么？（自己验证）

## 第 4 步：集合 set——"自动去重的袋子"（04_set.py）

**30 秒知识点**：集合用花括号 `{}`（但没有键值对），**自动去重**、**没有顺序**、不能按索引取。核心用途：去重、快速判断"在不在"、集合运算（交集/并集）。

**动手**：新建 `04_set.py`：

```python
# 集合：去重 + 判断 + 运算
nums = {1, 2, 2, 3, 3, 3}
print(nums)            # {1, 2, 3}（重复的自动去掉！）

# 增删
nums.add(4)            # 加一个
nums.remove(2)         # 删一个（不存在会报错，用 discard 不报错）
nums.discard(99)       # 不存在也不报错
print(nums)            # {1, 3, 4}

# 判断在不在（速度极快）
print(3 in nums)       # True

# 去重神器：把列表转集合再转回列表
words = ["a", "b", "a", "c", "b"]
unique = list(set(words))
print(unique)          # ['a', 'b', 'c']（顺序可能不同）

# 集合运算
a = {1, 2, 3}
b = {3, 4, 5}
print(a & b)           # 交集 {3}
print(a | b)           # 并集 {1, 2, 3, 4, 5}
print(a - b)           # 差集 {1, 2}（a 里有 b 没有的）
```

运行，逐行对照预期。全对 = 成功 ✅

**要能讲明白**：`list(set(words))` 是"转集合去重 → 转回列表"，这行代码背下来，LeetCode 第 217 题直接用它。集合为什么不能按索引取？因为它是**无序**的，没有"第几个"的概念。

**挑战**：两个列表 `a = [1, 2, 3, 4]`、`b = [3, 4, 5, 6]`，打印出"同时在两个列表里的数"（提示：`set(a) & set(b)`）。

## 第 5 步：综合练习（05_word_freq.py）

把今天的容器知识合起来用——统计一句话里每个单词出现几次（这是面试高频题，LeetCode 242 也用到）：

```python
# 统计每个单词出现次数（字典 + split）
def word_freq(text):
    freq = {}
    for word in text.split():
        freq[word] = freq.get(word, 0) + 1
    return freq

print(word_freq("the cat and the dog"))   # {'the': 2, 'cat': 1, 'and': 1, 'dog': 1}

# 找出出现次数最多的单词
def most_common(freq):
    best_word = None
    best_count = 0
    for word, count in freq.items():
        if count > best_count:
            best_word = word
            best_count = count
    return best_word, best_count

freq = word_freq("the cat and the dog")
print(most_common(freq))                  # ('the', 2)
```

运行 → 预期输出 2 行：`{'the': 2, 'cat': 1, 'and': 1, 'dog': 1}` 和 `('the', 2)`。

**要能讲明白**（今天的核心原理）：`freq.get(word, 0) + 1` = "如果这个单词还没统计过就按 0 算，然后 +1"——第一次见到 `the` 是 `0 + 1 = 1`，第二次是 `1 + 1 = 2`。**字典存状态 + 循环累加**，是统计类程序的万能套路。

## 第 6 步：LeetCode 2 道（独立做，约 1 小时）

打开 [力扣](https://leetcode.cn/problemset/all/) 筛选"简单"，做这两道（都跟今天的容器有关）：

1. **存在重复元素**（题号 217）：数组里只要有任意一个数出现至少两次，返回 `True`，否则 `False`。提示：集合自动去重——**去重后长度变短了，就说明有重复**。
2. **有效的字母异位词**（题号 242）：两个字符串字母相同、顺序不同，如 `"anagram"` 和 `"nagaram"` 是异位词。提示：异位词 = 每个字母出现次数一样——可以用第 5 步的"字典计数"比一比，或者把两个字符串排序后比较。

规则：先自己想 20 分钟，想不出再看提示；必须跑通再贴给我看。每道在日志里写一句思路。

## 第 7 步：收尾

1. 做 [[Day10-自测5题]]（不许翻笔记）
2. 把练习代码路径 + 每道题思路 + "一个我能讲清楚的原理"写进 [[2026-08-22-Day10-学习日志]]
3. 发我：自测作答 + 2 道 LeetCode 的代码和输出，我批改
