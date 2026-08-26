# Day 15 · 面向对象基础（class/self/__init__/方法/属性）（手把手版）

> 用法：跟着步骤一步一步做，**每做完一步就运行一次、看一次输出**。卡住了把报错原文贴给我。
> 练习文件放在 `projects/python-practice/day15/`，做完会进 GitHub。
> 先看一个事实：**你已经在用面向对象了**——LeetCode 网站的 `class Solution:` 就是类。今天彻底弄懂它。

## 第 0 步：准备（5 分钟）

1. VS Code 左侧 `projects\python-practice` → 新建文件夹 `day15`
2. 开始前想一个问题：你写了 12 道 LeetCode，模板都是 `class Solution: def xxx(self, nums)`——`class` 是什么？`self` 是谁？今天揭晓。

---

## 第 1 步：为什么要 class？（01_why_class.py）

**30 秒知识点**：你已经会写函数（def）。函数是"把动作打包"。但现实世界的东西是**数据 + 动作**在一起：

- 一个**学生**：有名字、分数（数据），能干的事：考试、汇报成绩（动作）
- 一个**银行账户**：有余额（数据），能干的事：存钱、取钱（动作）

如果用函数写，数据和操作是**分开的、容易乱**：

```python
# 函数式写法：数据和操作分开，每个函数都要手动传数据
def exam(student_name, score):
    return {"name": student_name, "score": score + 10}

def report(student):
    return f"{student['name']} 考了 {student['score']} 分"

student = exam("小明", 80)
print(report(student))     # 小明 考了 90 分
```

**问题**：`exam` 和 `report` 靠字典传数据，一旦字段名拼错（`score` vs `scroe`），查半天。

**class 的写法：把数据和动作打包在一起**：

```python
# 面向对象写法：数据和操作打包成一个"类"
class Student:
    def __init__(self, name, score):   # 构造方法：一出生就登记
        self.name = name               # 属性：这个学生的名字
        self.score = score             # 属性：这个学生的分数

    def exam(self):                    # 方法：学生能干的事
        self.score += 10

    def report(self):                  # 方法：学生能干的事
        return f"{self.name} 考了 {self.score} 分"

xiaoming = Student("小明", 80)          # 造一个"小明"（对象）
xiaoming.exam()                        # 小明考试
print(xiaoming.report())               # 小明 考了 90 分
```

**要能讲明白**：
- **类（class）= 设计图纸**；**对象（object）= 按图纸造出来的实物**。一张图纸能造无数个学生
- `xiaoming = Student("小明", 80)` = 按图纸造一个具体的学生
- 属性（name/score）= 这个学生自己的数据；方法（exam/report）= 这个学生能干的事
- **数据跟着对象走**：`xiaoming.score` 和 `xiaohong.score` 互不干扰

**挑战**：再造一个学生 `xiaohong = Student("小红", 60)`，让她考试两次，打印成绩。看看两个学生的分数是不是互不影响？

---

## 第 2 步：__init__ 和 self 到底是什么？（02_init_self.py）

**30 秒知识点**：这两个是新手最懵的，拆开讲：

**`__init__`（构造方法）**：名字前后**双下划线**的特殊方法。它干的活 = **"一出生就登记"**——你写 `Student("小明", 80)` 时，Python 自动调用 `__init__`，把"小明"和 80 存进这个新对象。双下划线的方法叫**魔术方法**，Python 在特定时机自动调用它们（明天学更多）。

**`self`**：就是**"这个对象自己"**——哪个对象调用方法，self 就是谁：

```python
xiaoming = Student("小明", 80)
xiaoming.exam()
# Python 实际翻译成：Student.exam(xiaoming)
#                   ↑ self 就是 xiaoming 自己
```

| 写法 | 真正的执行 |
|------|-----------|
| `xiaoming.exam()` | `Student.exam(xiaoming)` |
| `xiaoming.report()` | `Student.report(xiaoming)` |
| `xiaoming.name` | 找到 xiaoming 这个对象里的 name |

**这就是 LeetCode 模板的秘密**：网站写 `Solution().removeElement(nums, val)`，Python 翻译成 `Solution.removeElement(solution对象, nums, val)`——**self 被 Python 偷偷塞进来**，所以你定义方法时第一个参数写 self，但调用时不用传。现在懂了吧！

**要能讲明白**：`__init__` 里 `self.name = name`——等号左边是"往这个对象上贴标签"，右边是"外面传进来的值"。同名是因为习惯，改成 `self.name = n` 也行，但大家约定写同名。

---

## 第 3 步：实例属性和方法（03_methods.py）

**30 秒知识点**：属性有"实例属性"（每个对象自己的）和"类属性"（所有对象共用的，写在 __init__ 外面）；方法有"实例方法"（带 self，操作自己的数据）和"静态方法"（不带 self，和类无关的辅助功能）。

**动手**（新建 `03_methods.py`）：

```python
# 第 3 步：实例属性 vs 类属性；实例方法 vs 静态方法
class Student:
    school = "第一中学"            # 类属性：所有学生共用一个学校

    def __init__(self, name, score):
        self.name = name           # 实例属性：每个学生自己的
        self.score = score

    def exam(self):                # 实例方法：带 self，操作自己的数据
        self.score += 10
        return self.score

    @staticmethod                  # 静态方法：不碰任何学生数据
    def rule():
        return "禁止作弊"

xiaoming = Student("小明", 80)
xiaohong = Student("小红", 60)

print(xiaoming.school, xiaohong.school)   # 第一中学 第一中学（共用）
print(xiaoming.name, xiaohong.name)       # 小明 小红（各自独立）
print(Student.rule())                     # 静态方法：用类名直接调
```

**要能讲明白**：
- 类属性写在 `__init__` 外面，**所有对象共享**（学校只有一个）
- 实例属性写在 `__init__` 里 `self.xxx`，**每个对象一份**（名字各不同）
- 实例方法必须带 self（要操作自己的数据）；静态方法加 `@staticmethod` 装饰器，不碰数据
- **什么时候用静态方法**：功能上跟这个类有关、但不需要访问任何学生数据（比如规则、换算工具）

---

## 第 4 步：把 LeetCode 模板翻译成人话（04_leetcode_class.py）

**30 秒知识点**：现在回头看你的老朋友——LeetCode 模板。其实你早就写会面向对象了！

**动手**（新建 `04_leetcode_class.py`，把 27 题包装成"类"）：

```python
# 第 4 步：用 LeetCode 模板理解类
from typing import List

class Solution:
    """LeetCode 的答题盒：一个类里可以装很多道题的方法"""
    def removeElement(self, nums: List[int], val: int) -> int:
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != val:
                nums[slow] = nums[fast]
                slow += 1
        return slow

    def moveZeroes(self, nums: List[int]) -> None:
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != 0:
                nums[slow] = nums[fast]
                slow += 1
        for i in range(slow, len(nums)):
            nums[i] = 0

# 用类：造一个 Solution 对象，两个方法都能调
s = Solution()
print(s.removeElement([3, 2, 2, 3], 3))     # 2
nums = [0, 1, 0, 3, 12]
s.moveZeroes(nums)
print(nums)                                   # [1, 3, 12, 0, 0]
```

**要能讲明白**：
- 一个类 = 一个"工具箱"，里面装相关的方法（`removeElement` 和 `moveZeroes` 都是数组操作，放一起）
- `s = Solution()` 就是 LeetCode 网站的 `Solution()`——网站造一个答题盒，然后调里面的方法
- 这就是**为什么要拆类**：把"同一类事情"的操作打包，别人用起来一目了然（`s.removeElement(...)` 读起来像"盒子帮你移除了元素"）

**挑战**：把你做过的 35 题（二分查找）也加进这个类里，用 `s.searchInsert(...)` 调用。

---

## 今天的产出物（重要！）

1. `01_why_class.py`：函数式 vs 类写法对比（亲手敲）
2. `02_init_self.py`：__init__ 和 self 的理解实验
3. `03_methods.py`：实例属性/类属性、实例方法/静态方法
4. `04_leetcode_class.py`：把 LeetCode 题包装成类（27 + 283 + 35）

**自查清单**：
- [ ] 能跟别人讲清：类 = 图纸，对象 = 实物
- [ ] 能讲清 self = 调用方法的那个对象自己
- [ ] 能讲清为什么网站模板方法要写 self，但调用时不传
- [ ] 能讲清类属性和实例属性的区别
- [ ] 04 里 3 道题都能通过类调用跑通
