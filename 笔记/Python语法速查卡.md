# Python 语法速查卡（第 2 周 · Day 8-10）

> 原则：**能查到就行，不用背**。忘了就瞄一眼，多用几次自然就熟了。
> 用法：Obsidian 里把本页钉在左侧栏，或打印贴显示器边。

## 变量与打印

```python
name = "小明"        # 变量 = 给数据贴标签
age = 18
print(name)                          # 小明
print(f"我叫{name}，今年{age}岁")      # f-string，推荐
print("我叫" + name + "，今年" + str(age) + "岁")   # 拼接版（数字要 str() 包）
```

常见类型：字符串 `"hi"`、整数 `18`、浮点 `3.14`、布尔 `True/False`；`type(x)` 看类型。

## 流程控制（if / for / while）

```python
if score >= 90:        # 从上往下判断，命中一个就停
    print("优秀")
elif score >= 60:
    print("及格")
else:
    print("不及格")

for i in range(1, 101):   # range 含头不含尾 → 1~100
    print(i)

j = 1
while j <= 5:             # 不知道几次、靠条件停
    print(j)
    j = j + 1             # ⚠️ 必须有这句，否则死循环（Ctrl+C 停）
```

一句话：`for` 适合"知道循环几次"（遍历/数数）；`while` 适合"不知道几次、等条件停"。

## 函数（def / 参数 / return）

```python
def greet(name):          # 参数 = 函数要的输入
    return "你好，" + name + "！"   # return = 把结果交回去

print(greet("小明"))       # 调用：函数定义完不会自己跑，必须叫它
```

- `return` 交回去的结果能存进变量继续用：`result = add(3, 5)`
- 只 `print` 不 `return` → 调用结果拿到的是 `None`（"什么也没给我"）
- 别写 `print(return)`——`return` 是关键字，不能当值打印

## 字符串方法（都返回新字符串，不改原字符串）

```python
s = "  hello, python  "
s.strip()                # 去两端空白 → "hello, python"
s.upper()                # 全大写 → "HELLO, PYTHON"
s.lower()                # 全小写
s.replace("hello", "hi") # 替换 → "hi, python"
s.split(", ")            # 按", "切 → ["hello", "python"]
s.split()                # 无参数：按任意空白切
", ".join(["a", "b"])    # 拼接 → "a, b"
len(s)                   # 长度（数了才算）
```

常用套路（一条链，从左往右读）：

```python
" | ".join(s.strip().split(","))   # 去空格 → 切开 → 拼回
```

## 字符串切片 s[起点:终点:步长]

```python
"python"[1:4]    # "yth"（含头不含尾！）
"python"[:3]     # "pyt"
"python"[::2]    # "pto"（隔一个取一个）
"python"[::-1]   # "nohtyp"（反转）
"python"[-1]     # "n"（负索引从右往左数）
```

## 列表（增删改查）

```python
fruits = ["apple", "banana", "cherry"]

fruits[0]                 # 查："apple"（下标从 0 开始）
fruits[-1]                # 查："cherry"（-1 是最后一个）
len(fruits)               # 查：3

fruits.append("orange")   # 增：加到末尾
fruits.insert(1, "grape") # 增：插到指定位置

fruits[0] = "watermelon"  # 改：按索引重新赋值

fruits.remove("banana")   # 删：按值删
fruits.pop()              # 删：按位置删（默认删最后一项）
fruits.sort()             # 排序（原地改）

for f in fruits:          # 遍历
    print(f)

# 交换 s[left] 和 s[right]（temp 三步，防止被覆盖）
temp = s[left]
s[left] = s[right]
s[right] = temp
```

## 字典（键值对，用"名字"找"东西"）

```python
student = {"name": "小明", "age": 18}

student["name"]             # 查："小明"（键不存在会报 KeyError）
student.get("age")          # 查：不存在返回 None，不报错
student.get("score", 0)     # 查：不存在返回默认值 0
"name" in student           # 判断键在不在 → True

student["score"] = 95       # 增：直接给新键赋值
student["age"] = 19         # 改：给已有键重新赋值
student.pop("city")         # 删：按键删
student.update({"英语": 88})  # 增/改：一次加多个

for key, value in student.items():   # 遍历（键 + 值）
    print(key, "→", value)
```

## 元组（封起来的列表：不可变）

```python
point = (10, 20)

point[0]         # 查：10
len(point)       # 2
x, y = point     # 拆包：x=10, y=20
# point[0] = 99  # ❌ 报错：元组不能改

list(point)      # 元组 → 列表（可变了）
tuple(lst)       # 列表 → 元组
```

一句话：数据不该被改就用元组；元组能当字典的键，列表不能。

## 集合（自动去重的袋子）

```python
nums = {1, 2, 2, 3}              # {1, 2, 3}：重复自动去掉
nums.add(4)                      # 加
nums.remove(2)                   # 删（不存在报错）
nums.discard(99)                 # 删（不存在也不报错）
3 in nums                        # True（判断在不在，极快）

list(set(words))                 # 去重神器：列表 → 集合去重 → 列表
len(nums) != len(set(nums))      # 判重套路（LeetCode 217）

{1, 2, 3} & {3, 4}               # 交集 → {3}
{1, 2, 3} | {3, 4}               # 并集 → {1, 2, 3, 4}
{1, 2, 3} - {3, 4}               # 差集 → {1, 2}
```

## 统计套路（面试高频：数次数）

```python
freq = {}
for word in text.split():
    freq[word] = freq.get(word, 0) + 1   # 没记过按 0，遇到一次 +1
```

LeetCode 217（判重）、242（比异位词）、统计单词频率全用它。

## 防坑清单

- 引号必须用英文 `"`，中文引号会报错
- f-string 前面别漏 `f`
- `split(", ")` 是"逗号+空格"；字符串里没有空格就用 `split(",")`
- `while` 里必须有让条件变化的语句，否则死循环
- 函数定义完要调用才会执行；切片含头不含尾
- 字典取值用圆括号：`get("age")`，不是 `get["age"]`——`[]` 是拿东西，`()` 是做事
- `for`/`if`/`def`/`while` 行尾必须有冒号（报错 `expected ':'`）
- `.split()` 是字符串专属；列表已经是一个个元素，直接遍历，不能再切
- 循环变量名前后要一致：`for n in nums:` 里就用 `n`，别用别的名字
- `"一" in week` 返回 `True`/`False`（成员判断），不是变量
- 列表能被改（可变），字符串/元组不能（不可变）

## 运行代码（终端两连）

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\python-practice\day10
D:\proflim\python.exe 05_word_freq.py
```

已设置环境变量 `PYTHONUTF8=1`，中文输出正常（不用再加 `-X utf8`）。
