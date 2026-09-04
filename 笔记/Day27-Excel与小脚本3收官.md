# Day 27 Excel 数据清洗 + 小脚本 3 收官

> 第 4 周第 6 天。Day 26 洗 CSV；今天把同一套清洗接到 Excel（openpyxl），并做本周验收：README、力扣 2 道、检查点自测、周复盘。代码在 `projects/python-practice/day26/`。

## 一、今天要记住的一句话

**清洗逻辑不碰文件，只碰 dict 行。** CSV 和 Excel 的差别停在 `loader.py`；`cleaner.py` 一个字不用改。

```
文件(csv/xlsx) → loader 变成 dict 行 → cleaner 清洗 → main 写出干净文件 + 报告
```

Day 26 设计留下的红利：加一种格式 = 加一个读函数 + 一个写函数，清洗流水线零改动。

## 二、openpyxl 最少要会的几句

**读：**

1. `load_workbook(路径)` — 打开已有文件
2. `wb.active` — 拿当前工作表
3. `ws.iter_rows(values_only=True)` — 逐行取值；第一行当表头

**写：**

1. `Workbook()` — 新建
2. `ws.append([...])` — 一行一行塞
3. `wb.save(路径)` — 存盘

Excel 空格子是 `None`，CSV 空格子是 `""`。loader 里把 `None` 转成 `""`，下游才能和 CSV 行为一致。

## 三、CSV vs Excel（对照你日志里那条原理）

| | CSV | Excel（openpyxl） |
|---|---|---|
| 本质 | 纯文本 | 工作簿 + 工作表 |
| 默认类型 | 几乎全是字符串 | 可保留数字、日期、布尔 |
| 空格子 | `""` | `None` |
| 没有的东西 | 公式、合并单元格、多 sheet | 这些都有（本周脚本用不到） |

所以「共用清洗」成立的前提是：**入口先统一成同一种 dict（值都变成字符串）**。不统一，cleaner 就要为两种类型各写一套，测试也会翻倍。

## 四、交叉验证

同一份脏数据：

```powershell
python make_excel.py      # 脏 CSV → 脏 xlsx（照抄，保持脏）
python main.py csv
python main.py xlsx
```

两份报告的「无效 / 重复 / 干净行数 / 区域合计」必须一致。不一致 = loader 把某行读歪了，先查 Excel 空行和 `None`。

## 五、pytest 的 tmp_path

`test_loader.py` 里读 Excel 用的是 pytest 给的临时目录：测完自动删，不往项目里丢垃圾文件。这是「测试不污染工作区」的习惯，后面写文件类测试接着用。

## 六、本周力扣（125 / 350）

- **125 验证回文串**：先 `lower()`，再只留 `isalnum()`，最后 `s == s[::-1]`。你日志里那句「关键点是 return s == s[::-1]」对，但前面两步漏了——题目要求忽略大小写和非字母数字。
- **350 两数组交集 II**：排序 + 双指针；相等则收进结果并两边 +1，谁小谁前进。出现次数取两边较小值，排序后指针自然做到。跑本地脚本前注意：`List[int]` 需要 `from typing import List`（或改成 `list[int]`，3.9+ 可以）。

## 七、第 4 周工程化三件套（收官对照）

- **可复现**：venv + `requirements.txt`（别人三步能跑）
- **可测试**：cleaner 纯函数 → 测试钉死期望
- **可调试**：断点看变量，不靠瞎 print

小脚本 3 是本周核心验收物：分层（loader / cleaner / main）+ 测试 + README。
