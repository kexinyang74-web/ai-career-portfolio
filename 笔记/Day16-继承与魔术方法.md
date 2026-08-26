# Day 16 · 继承 + 魔术方法（__str__/__repr__）+ dataclass（手把手版）

> 用法：跟着步骤一步一步做，**每做完一步就运行一次、看一次输出**。卡住了把报错原文贴给我。
> 练习文件放在 `projects/python-practice/day16/`。
> 先看一个事实：昨天你写的 `class 奶茶` 里，`__init__` 前后有双下划线——这类方法叫**魔术方法**，Python 会在特定时机**自动调用**它们。今天学 3 个新的，还会学怎么让一个类"继承"另一个类。

## 第 0 步：准备（5 分钟）

1. VS Code 左侧 `projects\python-practice` → 新建文件夹 `day16`
2. 想一个问题：如果世界上有 100 种动物，每种都有名字、都会吃、都会叫——难道每种动物都要把这三样写一遍吗？今天的答案：**继承**。

---

## 第 1 步：为什么要继承？（01_inherit.py）

**30 秒知识点**：现实世界有"大类套小类"的关系——狗**是**动物，猫**是**动物。狗和猫有很多共同点（名字、会吃、会睡），也有各自的特色（叫法不同）。

**不用继承的写法（反面教材）**：

```python
class Dog:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} 在吃东西")

    def sleep(self):
        print(f"{self.name} 在睡觉")

class Cat:
    def __init__(self, name):      # ← 和 Dog 一模一样!
        self.name = name

    def eat(self):                 # ← 和 Dog 一模一样!
        print(f"{self.name} 在吃东西")

    def sleep(self):               # ← 和 Dog 一模一样!
        print(f"{self.name} 在睡觉")
```

**问题**：同样的代码写了 2 遍。如果 100 种动物就写 100 遍——改一处得改 100 处。

**继承的写法**：把公共的东西放进"动物"父类，狗和猫**自动拿到**：

```python
class Animal:                       # 父类（基类）：所有动物的公共部分
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} 在吃东西")

    def sleep(self):
        print(f"{self.name} 在睡觉")

class Dog(Animal):                  # 子类（派生类）：括号里写父类
    pass                            # 什么都不用写，自动继承全部!

class Cat(Animal):
    pass

wangcai = Dog("旺财")
wangcai.eat()      # 旺财 在吃东西    ← 从 Animal 继承来的
miaomiao = Cat("咪咪")
miaomiao.sleep()   # 咪咪 在睡觉     ← 从 Animal 继承来的
```

**要能讲明白**：
- `class Dog(Animal)` = "狗是动物的一种"，括号里是**父类**
- 子类**自动拥有**父类的所有属性和方法（不用重新写）
- 比喻：**继承 = 儿子的基因来自父母**——不用重新发明，直接拿到手

---

## 第 2 步：方法重写 + super()（02_override.py）

**30 秒知识点**：继承拿到的"通用能力"可能不够用——狗叫"汪汪"，猫叫"喵喵"，不能共用。这时在子类里**重新定义一个同名方法**，就叫**重写（override）**。

**动手**（新建 `02_override.py`）：

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print("动物在叫")

class Dog(Animal):
    def speak(self):               # 重写：和父类同名方法
        print(f"{self.name} 汪汪汪!")

class Cat(Animal):
    def __init__(self, name, color):   # 父类没有 color，要自己补
        super().__init__(name)         # super() = 调父类的方法，先让父类登记 name
        self.color = color

    def speak(self):
        print(f"{self.name} 喵喵喵!")

wangcai = Dog("旺财")
wangcai.speak()      # 旺财 汪汪汪!    ← 用自己的版本

miaomiao = Cat("咪咪", "橘色")
miaomiao.speak()     # 咪咪 喵喵喵!    ← 用自己的版本
```

**要能讲明白**：
- **重写** = 子类定义同名方法，调用时**优先用子类的**
- `super().__init__(name)` = "**先让爸登记**"——父类能干的活（登记 name）不用重写，叫 super() 代劳
- 比喻：孩子有自己独特的爱好（speak 重写），但身份证照常用流程（__init__ 登记）还是走爸妈的

---

## 第 3 步：魔术方法 __str__/__repr__（03_magic.py）

**30 秒知识点**：昨天学了 `__init__`（出生时自动调用）。今天学 2 个：`__str__`（打印时自动调用）和 `__repr__`（调试时自动调用）。

**先看没有它们会发生什么**：

```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

xiaoming = Student("小明", 80)
print(xiaoming)
# 输出:<__main__.Student object at 0x000001B3...>
#      ↑ 一坨天书，根本看不懂谁是谁
```

**加上 __str__ 之后**：

```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __str__(self):                     # print 时自动调用
        return f"学生 {self.name}，分数 {self.score}"

    def __repr__(self):                    # 调试/列表里显示时自动调用
        return f"Student('{self.name}', {self.score})"

xiaoming = Student("小明", 80)
print(xiaoming)              # 学生 小明，分数 80    ← __str__ 生效
print([xiaoming])            # [Student('小明', 80)] ← __repr__ 生效
```

**要能讲明白**：
- `print(对象)` 时，Python 自动找 `__str__`；找不到就显示天书地址
- `__str__` = **给人看**的友好介绍（"学生 小明，分数 80"）
- `__repr__` = **给程序员看**的还原格式（`Student('小明', 80)`，能看出怎么造出来的）
- 两个都是**双下划线 = 魔术方法 = 特定时机自动触发**，和 `__init__` 一个家族
- 偷懒技巧：只写 `__repr__`，`print` 和调试都能用上

---

## 第 4 步：dataclass（04_dataclass.py）

**30 秒知识点**：昨天你写"奶茶"类，每个属性都要写 `self.口味 = 口味`，还要写 `__str__`——**样板代码**太多了。dataclass 帮你**自动生成**这些。

**动手**（新建 `04_dataclass.py`）：

```python
from dataclasses import dataclass

@dataclass                        # 装饰器：告诉 Python "这是一个数据类"
class 奶茶:
    口味: str                     # 只声明属性，不用写 self.xxx = xxx
    温度: str
    糖度: int = 3                 # 默认值：不传就默认 3 分糖

    def 介绍(self):              # 方法照常写
        return f"{self.口味}，{self.温度}，{self.糖度}分糖"

我的茶 = 奶茶("珍珠奶茶", "去冰")   # __init__ 自动生成，自动登记
print(我的茶)                      # 奶茶(口味='珍珠奶茶', 温度='去冰', 糖度=3)  ← __repr__ 自动生成
print(我的茶.介绍())               # 珍珠奶茶，去冰，3分糖
```

**和手写版对比**（同样一个类）：

```python
# 手写版:15 行
class 奶茶:
    def __init__(self, 口味, 温度, 糖度=3):
        self.口味 = 口味
        self.温度 = 温度
        self.糖度 = 糖度
    def __repr__(self):
        return f"奶茶(口味={self.口味!r}, 温度={self.温度!r}, 糖度={self.糖度!r})"

# dataclass 版:7 行,上面那些自动生成
@dataclass
class 奶茶:
    口味: str
    温度: str
    糖度: int = 3
```

**要能讲明白**：
- `@dataclass` = 一个**装饰器**，`@` 开头，写在类上面，给类"加功能"
- 只要**声明属性**（`口味: str`），`__init__` 和 `__repr__` 就**自动生成**——不用写 `self.xxx = xxx`
- 写法 `属性: 类型` 叫**类型注解**——明天 Day 17 正式学
- **什么时候用 dataclass**：类主要就是"装数据"（学生、奶茶、订单），没什么复杂逻辑时
- 如果类里有复杂方法逻辑，用普通 class 更合适

---

## 今天的产出物（重要！）

1. `01_inherit.py`：继承（子类自动拿到父类属性/方法）
2. `02_override.py`：方法重写 + super() 调父类
3. `03_magic.py`：__str__/__repr__ 魔术方法
4. `04_dataclass.py`：dataclass 自动生成样板代码
5. `leetcode_58.py`、`leetcode_121.py`：LeetCode 2 道

**挑战**（任选 2 个）：
- **挑战 A（继承）**：写一个 `Bird` 类继承 `Animal`，加一个 `fly` 方法，还要重写 `speak` 让它"叽叽喳喳"
- **挑战 B（重写+super）**：给 `Dog` 加一个 `color` 属性（用 super().__init__ 调父类登记 name）
- **挑战 C（dataclass）**：把昨天的"奶茶"类改写成 dataclass 版，加一个"加珍珠"方法

**自查清单**：
- [ ] 能讲清：子类**自动拿到**父类的什么？用什么语法？
- [ ] 能讲清：重写是什么意思？`super().__init__` 在干什么？
- [ ] 能讲清：`print(对象)` 时 Python 自动调哪个魔术方法？
- [ ] 能讲清：dataclass 帮你省了什么代码？
