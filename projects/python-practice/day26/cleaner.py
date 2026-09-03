"""CSV 数据清洗工具(小脚本 3 的"清洗心脏")

设计原则:
1. 每个清洗动作是一个【纯函数】——同样的输入永远同样的输出,
   不碰文件、不打印,所以可以被 pytest 测试(Day 25 技能直接上场)
2. 脏数据 → 干净数据的流水线:
   原始行 → 去掉首尾空格 → 修格式(金额/日期/数量)
   → 丢弃无效行 → 去重 → 干净行
3. 今天要你动手实现的是两个 TODO 函数:clean_money 和 clean_date。
   测试已经写好——现在跑是红的,你实现后变绿:复习 Day 25 红绿闭环。
"""
import datetime

# ========== 单值解析(输入一个字符串,输出修好的值或 None)==========

def clean_money(text):
    """把金额字符串转成 float;转不了就返回 None。

    要处理的情况:
      '¥1,200.50' → 1200.5   (人民币符号 + 千分位逗号)
      '800元'      → 800.0   ('元' 后缀)
      '¥ 450.5'    → 450.5   (符号和数字之间有空格)
      '1200'       → 1200.0  (本来就是纯数字)
      'abc'        → None    (乱七八糟,转不了)
      ''           → None
    """
    
    if not text: # 如果文本为空，返回None
        return None 
    if text.endswith("元"): # 去掉元
        text = text[:-1] # 去掉最后一个字符
    if text.startswith("¥"): # 去掉¥
        text = text[1:] # 去掉第一个字符
    if text.startswith("¥"): # 防御性编程
        return None
    try:
        return float(text.strip().replace(",", "")) # 去掉空格和逗号
    except ValueError: # 如果转换失败，返回None
        return None

def clean_date(text):
    """把日期字符串统一成 'YYYY-MM-DD' 格式;解析不了就返回 None。

    要处理的情况:
      '2024/1/5'   → '2024-01-05'  (斜杠分隔,没补零)
      '2024.1.5'   → '2024-01-05'  (点分隔)
      '2024-01-05' → '2024-01-05'  (本来就对)
      '2024/2/30'  → None          (2 月没有 30 号——strptime 会拆穿它)
      ''           → None
    提示:用 datetime.datetime.strptime(text, 格式) 逐个格式试,
         第 3 个参数格式 %Y/%m/%d、%Y-%m-%d、%Y.%m.%d 都试一遍,
         成功就 strftime('%Y-%m-%d') 统一输出,
         全部失败(strptime 抛 ValueError)就返回 None。
    """
    
    if not text: # 如果文本为空，返回None
        return None
    for fmt in ("%Y/%m/%d", "%Y-%m-%d", "%Y.%m.%d"): # 尝试三种格式
        try:
            return datetime.datetime.strptime(text, fmt).strftime("%Y-%m-%d") # 转换为标准格式
        except ValueError: # 如果转换失败，继续尝试下一种格式
            continue
    return None # 如果所有格式都失败，返回None

def parse_int(text):
    """数量列:纯数字字符串 → int;转不了 → None(已实现,作为参考)"""
    if not text: # 如果文本为空，返回None
        return None
    try:
        return int(text.strip()) # 去掉空格和转换为整数
    except ValueError: # 如果转换失败，返回None
        return None


# ========== 行级清洗(一行 → 修好的行,或 None = 没救)==========

def 清洗一行(row):
    """把一行脏数据变成干净行;这行没救了就返回 None。

    row: dict(列名 → 字符串),来自 csv.DictReader
    返回: dict(列名 → 修好的值:金额是 float、日期是标准格式、数量是 int)
    """
    if not row:              # DictReader 读到空行会给空 dict(或 None)
        return None
    # 1. 所有字段去掉首尾空格(' 华东 ' → '华东')
    row = {k: v.strip() if isinstance(v, str) else v for k, v in row.items()}
    # 2. 三个"解析型"字段:修不好 → 整行没救
    row["金额"] = clean_money(row.get("金额", ""))
    row["日期"] = clean_date(row.get("日期", ""))
    row["数量"] = parse_int(row.get("数量", ""))
    if None in (row["金额"], row["日期"], row["数量"]):
        return None
    # 3. 三个关键文字字段不能为空
    for key in ("区域", "产品", "负责人"):
        if not row.get(key, ""):
            return None
    return row


# ========== 多行清洗 ==========

def 去重(rows):
    """整行内容完全相同的只保留第一个(保持原顺序)"""
    seen = set()
    result = []
    for row in rows:
        key = tuple(row.items())
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result


def 按区域汇总(rows):
    """统计每个区域的总销售额,按销售额从高到低返回 dict"""
    total = {}
    for row in rows:
        region = row["区域"]
        total[region] = total.get(region, 0.0) + row["金额"]
    return dict(sorted(total.items(), key=lambda x: x[1], reverse=True))
