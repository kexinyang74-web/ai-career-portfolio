"""pytest 测试:测 cleaner.py 的清洗函数(红绿闭环复习)

现在跑:clean_money / clean_date 还没实现 → 一片红
任务:去 cleaner.py 实现这两个函数 → 全绿 → 再跑 main.py
"""
from cleaner import clean_money, clean_date, parse_int
from cleaner import 清洗一行, 去重, 按区域汇总


# ---------- clean_money ----------

def test_clean_money_人民币符号和千分位():
    assert clean_money("¥1,200.50") == 1200.5

def test_clean_money_元字后缀():
    assert clean_money("800元") == 800.0

def test_clean_money_符号和数字间有空格():
    assert clean_money("¥ 450.5") == 450.5

def test_clean_money_本来就是纯数字():
    assert clean_money("1200") == 1200.0

def test_clean_money_乱数据():
    assert clean_money("abc") is None

def test_clean_money_空字符串():
    assert clean_money("") is None


# ---------- clean_date ----------

def test_clean_date_斜杠分隔没补零():
    assert clean_date("2024/1/5") == "2024-01-05"

def test_clean_date_点分隔():
    assert clean_date("2024.1.5") == "2024-01-05"

def test_clean_date_本来就是标准格式():
    assert clean_date("2024-01-05") == "2024-01-05"

def test_clean_date_不存在的日期():
    assert clean_date("2024/2/30") is None

def test_clean_date_空字符串():
    assert clean_date("") is None


# ---------- parse_int ----------

def test_parse_int_正常():
    assert parse_int("2") == 2

def test_parse_int_乱数据():
    assert parse_int("两") is None


# ---------- 清洗一行(整行流水) ----------

def test_清洗一行_正常行():
    row = {"日期": "2024/1/5", "区域": "华东", "产品": "键盘",
           "金额": "¥1,200", "数量": "2", "负责人": "张伟"}
    result = 清洗一行(row)
    assert result["日期"] == "2024-01-05"   # 日期被统一格式
    assert result["金额"] == 1200.0          # 金额被转成数字
    assert result["数量"] == 2               # 数量被转成数字

def test_清洗一行_金额乱没救():
    row = {"日期": "2024/1/5", "区域": "华东", "产品": "键盘",
           "金额": "abc", "数量": "2", "负责人": "张伟"}
    assert 清洗一行(row) is None

def test_清洗一行_区域空没救():
    row = {"日期": "2024/1/5", "区域": "", "产品": "键盘",
           "金额": "100", "数量": "2", "负责人": "张伟"}
    assert 清洗一行(row) is None


# ---------- 去重 / 汇总 ----------

def test_去重_相同行只留第一个():
    a = {"区域": "华东", "金额": 1.0}
    b = {"区域": "华东", "金额": 1.0}
    c = {"区域": "华南", "金额": 2.0}
    assert 去重([a, b, c]) == [a, c]

def test_按区域汇总():
    rows = [{"区域": "华东", "金额": 100.0},
            {"区域": "华东", "金额": 50.0},
            {"区域": "华北", "金额": 30.0}]
    assert 按区域汇总(rows) == {"华东": 150.0, "华北": 30.0}
