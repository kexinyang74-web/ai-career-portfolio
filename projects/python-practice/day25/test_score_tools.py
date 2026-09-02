"""pytest 测试文件:测 score_tools.py 的三个函数

pytest 认文件的规则(必须遵守):
1. 文件名以 test_ 开头  → pytest 才会收集它
2. 测试函数名以 test_ 开头 → pytest 才会执行它
3. 测试里用 assert 判断"期望 vs 实际" → 不对就红

运行(在 day25 目录下,二选一):
  .venv/Scripts/python.exe -m pytest   # 不激活也能跑;路径写正斜杠(反斜杠会被当转义符!)
  先激活 venv(Activate.ps1),再直接敲: pytest
"""
from score_tools import 计算平均分, 转换等级, 过滤不及格

def test_平均分_正常情况():
    assert 计算平均分([80, 90, 100]) == 90.0

def test_平均分_单个成绩():
    assert 计算平均分([5]) == 5.0

def test_平均分_空列表():
    # 空列表要返回 0,而不是崩掉(代码里 if not score_list 就是干这个的)
    assert 计算平均分([]) == 0

def test_转换等级_优秀和不及格():
    assert 转换等级(95) == "优秀"
    assert 转换等级(45) == "不及格"

def test_转换等级_边界值():
    # 边界最容易写错:60 到底算及格还是不及格?用测试钉死它
    assert 转换等级(60) == "及格"
    assert 转换等级(59) == "不及格"

def test_过滤不及格_正常情况():
    assert 过滤不及格([80, 50, 90, 30]) == [50, 30]

def test_过滤不及格_没有不及格():
    assert 过滤不及格([80, 90]) == []
