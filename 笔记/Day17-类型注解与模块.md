# Day 17 · 类型注解 + PEP 8 + 模块与包（手把手版）

> 用法：跟着步骤一步一步做，**每做完一步就运行一次、看一次输出**。卡住了把报错原文贴给我。
> 练习文件放在 `projects/python-practice/day17/`。
> 先看一个事实：昨天 leetcode_121.py 里你写过 `plants: List[List[int]]` 和 `-> bool`——**你已经用过类型注解了**。今天把这件事讲透，再学"代码排版规范"和"把代码拆成多个文件"。

## 第 0 步：准备（5 分钟）

1. VS Code 左侧 `projects\python-practice` → 新建文件夹 `day17`
2. 想一个问题：一份 500 行的代码，和 5 个 100 行的文件，哪个更好看懂、更好改？今天的答案：**模块**——拆开。

---

## 第 1 步：类型注解（01_typing.py）

**30 秒知识点**：类型注解 = 给代码写"说明书"。格式是 `变量: 类型` 和 `-> 类型`（表示函数返回什么类型）。

```python
# 函数注解：参数 a 和 b 是 int，返回 int
def add(a: int, b: int) -> int:
    return a + b

# 变量注解：声明这个变量将来装 str
name: str = "小明"
```

**三个必须知道的事实**：

| 事实 | 说明 |
|------|------|
| 注解不强制检查 | 你写 `a: int` 却传 "abc" 进来，Python **不报错**，照样跑 |
| 但 VS Code 会提醒 | 光标悬停能看到类型，传错类型会有黄色波浪线——相当于免费的代码检查员 |
| 复杂类型要 import | `List[str]`、`Dict[str, int]` 需要 `from typing import List`（Python 3.9+ 可以写小写 `list[str]`，不用 import） |

**昨天你已经见过它**：`def findTargetIn2DPlants(self, plants: List[List[int]], target: int) -> bool:` —— 读出来就是："plants 是列表套列表、都是整数，target 是整数，函数返回布尔值"。**这就是为什么 LeetCode 模板要写注解**——让你不用跑代码就知道这个函数要什么、给什么。

**练习**（写到 01_typing.py 里跑通）：
1. 写一个 `def 平均分(分数列表: list[int]) -> float`，返回 `sum(分数列表) / len(分数列表)`
2. 把昨天奶茶类加上注解：`口味: str`、`甜度: int`

---

## 第 2 步：PEP 8——代码"校规"（02_pep8.py）

**30 秒知识点**：PEP 8 是 Python 官方出的**代码排版规范**（PEP = Python 改进提案）。不遵守代码照样跑，但**面试官、同事、开源项目**都在意它。

**五条最常用的规则**：

| 规则 | 写法 | 反面例子 |
|------|------|---------|
| 缩进用 4 个空格 | `    if x > 0:` | 2 空格 / Tab |
| 变量、函数名用小写+下划线 | `get_price()` | `getPrice()` |
| 类名用大驼峰 | `class 奶茶店` | `class 奶茶店` 本身 OK，英文如 `class MilkTeaShop` |
| 函数之间空 2 行 | 两个 def 之间 2 个空行 | 1 行 / 0 行 |
| 注释 `# 后要有一个空格` | `# 这是注释` | `#这是注释` |

**反面教材 → 正面教材**：

```python
# ❌ 反面教材（能跑但难看的代码）
def calc(x,y):
  result=x+y
  return result
def show():
  print(calc(1,2))

# ✅ 正面教材
def calc(x: int, y: int) -> int:
    result = x + y
    return result


def show() -> None:
    print(calc(1, 2))
```

**怎么自动检查**：VS Code 里按 `Shift + Alt + F`（格式化），会自动帮你排版成 PEP 8。这是最省事的办法。

---

## 第 3 步：模块与包（03_module.py + 04_main.py）

**30 秒知识点**：
- **模块（module）** = 一个 `.py` 文件。`math` 就是一个模块
- **包（package）** = 一个装了一堆 `.py` 文件的文件夹。你之前看的 `pip` 就是包
- **导入（import）** = 把别的文件里的功能拿过来用

**三种导入写法**：

```python
import math                  # 整体导入，用的时候写 math.sqrt(16)
from math import sqrt        # 只拿 sqrt 这一个功能，用的时候写 sqrt(16)
import math as m             # 起个短别名，用的时候写 m.sqrt(16)
```

**为什么拆模块？三个理由（本周检查点会考）**：
1. **复用**：写一次，多个文件都能 import
2. **好读**：一个文件只干一件事，500 行变 5 个 100 行
3. **好测**：哪个文件坏了，单独修它

**`if __name__ == "__main__":` 是什么（重点！）**

每个 `.py` 文件都有个隐藏变量 `__name__`：
- 文件**被直接运行**时，`__name__` 是 `"__main__"` → 下面的测试代码才执行
- 文件**被别人 import** 时，`__name__` 是文件名 → 测试代码**不执行**

```python
# my_shop.py —— 被 import 时不想执行测试代码
class 奶茶店:
    def __init__(self, 店名: str):
        self.店名 = 店名

if __name__ == "__main__":          # ← 只有"直接运行本文件"才走这里
    shop = 奶茶店("测试店")
    print(shop.店名)
```

**练习**（这是今天的重头戏）：
1. 新建 `my_shop.py`：写一个 `奶茶店` 类（店名、菜单 dict、`点单()` 方法），底部加 `if __name__ == "__main__":` 测试代码
2. 新建 `main.py`：`from my_shop import 奶茶店`，创建一个店并点单
3. 运行 `python main.py`（正常运行）；再运行 `python my_shop.py`（测试代码执行）；再试试在 main.py 里也 import 后，my_shop 的测试代码会不会跑（答案是：不会）

---

## 第 4 步：LeetCode 2 道（任务 3）

今天继续 2 道简单题（数组/字符串/哈希表/双指针标签）。写一句思路进日志。

---

## 小结（一天看完版）

| 主题 | 一句话 |
|------|--------|
| 类型注解 | 给变量/函数写"说明书"：`变量: 类型`、`-> 类型`；不强制但 VS Code 会帮你检查 |
| PEP 8 | Python 官方排版"校规"：4 空格缩进、小写+下划线命名、类名大驼峰、空 2 行；`Shift+Alt+F` 自动格式化 |
| 模块 | 一个 .py 文件 = 一个模块；`import` 拿来用 |
| 包 | 装模块的文件夹 |
| `__main__` | "直接运行"才执行 `if __name__ == "__main__":` 里的代码；被 import 时不执行 |
