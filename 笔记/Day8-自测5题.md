# Day 8 · Python 基础语法（自测 5 题）

> 作答规则：先自己写，不许翻笔记/文档；写不出来的地方标注"没掌握"。写完后发给 Codex 批改，批改后生成批改版。

## 第 1 题：变量与打印（写代码）

定义变量 `name = "小明"`、`age = 18`，用一行 f-string 打印出：`我叫小明，今年 18 岁`。

作答：
print(f"我叫{name}，今年{age}岁")
## 第 2 题：流程控制（写代码）

用 if/elif/else 写成绩分级：`>= 90` 优秀，`>= 60` 及格，否则不及格。`score` 自己给个值。

作答：
score = 60

  

if score >= 90:

    print("优秀")

elif score >= 60:

    print("及格")

else:

    print("不及格")
## 第 3 题：for 循环（写代码）

用 `for` + `range` 求 1 到 100 所有偶数的和，打印结果。

作答：
total =0

for i in range(1,11):

    if i % 2 == 0:

        total += i

print(total)
## 第 4 题：for vs while（用自己的话）

`for` 循环和 `while` 循环分别适合什么场景？各举一个例子。

作答：
for：数1-5

for i in range(1,6):

    print("for:",i)

  

while：数到5停

j = 10

while j >= 2:

    print("while:",j)

    j =j- 2
## 第 5 题：找最大值（LeetCode 热身）

列表 `nums = [3, 7, 2, 9, 5]`，不用内置 `max()`，用循环找出最大值并打印。

作答：
