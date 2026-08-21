# Python 语法速查卡（第 2 周 · Day 8-9）

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

## 列表基础 + 交换两个元素

```python
s = ["h", "e", "l", "l", "o"]
s[0]             # "h"（下标从 0 开始）
len(s)           # 5

# 交换 s[left] 和 s[right]（temp 三步，防止被覆盖）
temp = s[left]
s[left] = s[right]
s[right] = temp
```

## 防坑清单

- 引号必须用英文 `"`，中文引号会报错
- f-string 前面别漏 `f`
- `split(", ")` 是"逗号+空格"；字符串里没有空格就用 `split(",")`
- `while` 里必须有让条件变化的语句，否则死循环
- 函数定义完要调用才会执行；切片含头不含尾

## 运行代码（终端两连）

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\python-practice\day9
D:\proflim\python.exe -X utf8 01_greet.py
```

中文乱码 = 显示编码问题（exit code 0 即程序正常），加 `-X utf8` 可正常显示。
