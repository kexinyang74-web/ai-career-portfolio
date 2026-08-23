# Day 11 · 文件读写：txt / JSON / CSV（手把手版）

> 用法：跟着步骤一步一步做，**每做完一步就运行一次、看一次输出**。卡住了把报错原文贴给我。
> 练习文件放在 `projects/python-practice/day11/`，做完会进 GitHub，是你"坚持写代码"的证据。
> 今天所有内容都是为了第 4 周小脚本 3（CSV/Excel 清洗）和第 8 周 RAG 文档加载做准备的。

## 第 0 步：准备（5 分钟）

1. 打开 VS Code，左侧资源管理器找到 `projects\python-practice` → 右键新建文件夹 `day11`
2. `Ctrl + \`` 打开终端，`cd projects\python-practice\day11`，运行 `D:\proflim\python.exe --version` 确认环境
3. 现在就开始，跟着每一步敲代码

---

## 第 1 步：读 txt 文件（01_read_txt.py）

**30 秒知识点**：电脑上的文件就像一封**封好的信**。Python 要"拆信封"（`open`）才能读，读完要"合上信封"（`close`）。最好的拆法是用 `with`——它会**自动合上**，不用你记。

**动手**：新建 `01_read_txt.py`，**自己敲**：

```python
# 第 1 步：读 txt 文件
# 先用 w 模式写一个小文件（明天你会自己会写，今天先借用）
with open("hello.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n第二行\n第三行\n")

# 然后读它：r 模式 = 只读
with open("hello.txt", "r", encoding="utf-8") as f:
    content = f.read()      # read() = 一次读完整个文件，得到一个字符串
    print(content)
```

运行，看到三行文字就是成功 ✅

**要能讲明白**：
- 为什么每次 `open` 都带 `encoding="utf-8"`？→ Windows 系统默认编码不是 utf-8，不带它**中文会乱码**。这是新手最常见的坑。
- `\n` 是什么？→ 换行符。写文件时每行末尾要自己加。

**挑战 1**：把 `f.read()` 换成 `f.readlines()`，看看返回的是字符串还是一个列表？（提示：列表，每个元素是一行，每行后面还带着 `\n`）

**挑战 2（指针实验，很重要）**：

```python
with open("hello.txt", "r", encoding="utf-8") as f:
    print(f.read())     # 第一次读，有内容
    print("----- 第二次 -----")
    print(f.read())     # 第二次读，怎么是空的？！
```

想明白为什么吗？→ 文件有个"隐形指针"，像录音机的磁头。**读完一遍，磁头就到了文件末尾**，再读就是空。想倒带可以 `f.seek(0)`（先记住，不急着用）。

---

## 第 2 步：写 txt 文件（02_write_txt.py）

**30 秒知识点**：写文件有 3 种模式，最容易混，背下来：

| 模式 | 意思 | 结果 |
|------|------|------|
| `"w"` | write 写 | **清空旧内容**，重新写（危险！） |
| `"a"` | append 追加 | 在末尾接着写，不清空 |
| `"r"` | read 读 | 只能读，写会报错 |

**动手**：新建 `02_write_txt.py`：

```python
# 第 2 步：写 txt 文件
lines = ["苹果", "香蕉", "樱桃"]

# 方式一：一行一行写（别忘了 \n）
with open("fruits.txt", "w", encoding="utf-8") as f:
    for item in lines:
        f.write(item + "\n")

# 方式二：writelines 一次写多行（它不会自动加换行！）
with open("fruits2.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)     # 结果：苹果香蕉樱桃挤在一行

# 方式三：追加模式 a——不清空，接着写
with open("fruits.txt", "a", encoding="utf-8") as f:
    f.write("榴莲\n")

# 读回来看看结果
with open("fruits.txt", "r", encoding="utf-8") as f:
    print(f.read())
```

运行，最后应该打印出 苹果/香蕉/樱桃/榴莲 四行 ✅

**要能讲明白**：`"w"` 为什么会清空？→ 因为 `w` 的意思是"打开一个全新的空白文件"，旧内容直接抹掉。**如果你只想加东西，用 `a`**。不小心用 `w` 覆盖了重要文件 = 数据丢失，所以写代码前先想清楚模式。

**挑战**：把 `fruits.txt` 用 `a` 模式再追加一行"西瓜"，再读出来，确认旧内容还在。

---

## 第 3 步：JSON——"让数据变成字符串"（03_write_json.py）

**30 秒知识点**：JSON 是一种**全世界通用的文本格式**，长这样：

```json
{"name": "小明", "age": 20}
```

它看起来像 Python 字典，但它是**字符串**。Python 程序之间传数据、网页和程序之间传数据，都用它。

json 模块有 **4 个函数**，新手必混，先记口诀：

| 函数 | 作用 | 输入 → 输出 |
|------|------|-------------|
| `json.dumps(d)` | 字典 → 字符串 | dumps = **d**ict → **s**tring |
| `json.loads(s)` | 字符串 → 字典 | loads = string → dict（反着来） |
| `json.dump(d, f)` | 字典 → **直接写进文件** | 最后的 s 没了 = 不返回字符串 |
| `json.load(f)` | **直接从文件读** → 字典 | 有 s 的管字符串，没 s 的管文件 |

**动手**：新建 `03_write_json.py`：

```python
# 第 3 步：字典写成 JSON 文件
import json

user = {
    "name": "小明",
    "age": 20,
    "skills": ["Python", "Git"],
    "is_active": True,
}

# dumps：字典 → 字符串（先看看变成什么样）
text = json.dumps(user, ensure_ascii=False, indent=2)
print(text)             # 加了 indent=2 才会换行缩进，否则是一长串

# dump：字典 → 直接写进文件（s 没了！）
with open("user.json", "w", encoding="utf-8") as f:
    json.dump(user, f, ensure_ascii=False, indent=2)

print("写完了，去文件夹里看看 user.json 长什么样")
```

运行，用 VS Code 打开 `user.json`，应该是一行一行缩进的 JSON ✅

**要能讲明白**：
- `ensure_ascii=False` 是什么？→ 不写的话，中文会变成 `"\u5c0f\u660e"` 这种乱码（ASCII 转义）。**写中文数据，必须带上它**。
- `indent=2` 是什么？→ 缩进 2 格，文件变得人看得懂。不给它，全挤一行也能读，只是不好看。

**挑战**：把 `user` 改成你自己的信息（名字、年龄、喜欢的语言），重新跑一遍。

---

## 第 4 步：读 JSON 文件（04_read_json.py）

**30 秒知识点**：读回来就是 `json.load(f)`，一个函数搞定——文件里的 JSON 自动变回字典。

**动手**：新建 `04_read_json.py`（读取第 3 步写出的 user.json）：

```python
# 第 4 步：读 JSON 文件
import json

with open("user.json", "r", encoding="utf-8") as f:
    data = json.load(f)     # 读出来，直接就是字典！

# 现在 data 和普通字典一样用
print(data["name"])         # 小明
print(data["age"])          # 20
print(data["skills"][0])    # Python（字典里套着列表）

# 进阶：json.loads 管的是"字符串"
# 把 dumps 的字符串再变回字典
text = '{"name": "小红", "age": 18}'
d = json.loads(text)
print(d["name"])            # 小红
```

运行，看到 小明/20/Python/小红 就是成功 ✅

**要能讲明白**：`load` 和 `loads` 的输入区别？→ **有 s = 管字符串，没 s = 管文件**（`dumps`/`loads` 成对记，`dump`/`load` 成对记）。这个区别考试必考、写代码必踩。

**挑战**：手动改一改 `user.json`（比如把 age 改成 30），再运行程序，看读出来的值变没变——证明数据**存在文件里，程序结束也不会丢**。

---

## 第 5 步：CSV——"表格文件"（05_csv_io.py）

**30 秒知识点**：CSV 就是**用逗号分隔的表格**，Excel 能直接打开。每一行是一条记录：

```csv
姓名,语文,数学
小明,90,85
小红,88,92
```

第 4 周要写的"CSV/Excel 清洗"就是这个东西，今天先学会读写。

**动手**：新建 `05_csv_io.py`：

```python
# 第 5 步：读写 CSV
import csv

# 写：先把数据写成一个 csv 文件
rows = [
    ["姓名", "语文", "数学"],   # 第一行是表头
    ["小明", 90, 85],
    ["小红", 88, 92],
]

with open("scores.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)      # 造一个"写入器"
    writer.writerows(rows)      # 一次写多行

# 读：把 csv 读回来，一行一个列表
with open("scores.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)      # 造一个"读取器"
    for row in reader:          # 一行一行遍历
        print(row)              # 每行是一个列表
```

运行，看到 3 行列表 ✅。然后去文件夹双击 `scores.csv`，用 Excel/记事本打开看看——注意！用 Excel 打开才看得出"表格"，记事本打开是纯文本。

**要能讲明白**：
- `newline=""` 是干嘛的？→ Windows 下不写它，写出的 csv 每两行之间会**多一个空行**。这是 Windows 专属坑，固定带上就对了。
- 为什么 `csv.reader` 得到的是列表？→ CSV 天然就是"表格的每一行"，列表正是"有序的一串数据"，最贴切。

**挑战**：给 scores.csv 追加一行 `["小刚", 75, 88]`（提示：用 `"a"` 模式 + `csv.writer`），再读出来确认有 4 行。

---

## 今日总结（默念 3 遍）

1. `with open(...) as f:` 自动关门，永远是首选写法
2. 模式：`"r"` 读 / `"w"` 清空重写 / `"a"` 追加
3. 中文文件：`encoding="utf-8"` 必须带，CSV 还要带 `newline=""`
4. json 四兄弟：`dumps`/`loads` 管字符串，`dump`/`load` 管文件；中文加 `ensure_ascii=False`
5. 读文件会"读到底"，二次读取是空的（指针在末尾）

## 任务 2 产出物（今天结束前要有的东西）

- ✅ `projects/python-practice/day11/` 下 5 个练习文件全部跑通
- ✅ 一个小练习：能读 `user.json`（第 4 步）、写出 `scores.csv`（第 5 步）——这就是任务要求"读 json、写 csv"的完成证明
