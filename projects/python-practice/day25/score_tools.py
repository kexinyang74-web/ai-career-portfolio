"""成绩处理工具(被测模块)

Day 25 的主角不是这些函数,而是旁边那个 test_score_tools.py——
这里的函数是"被测对象",测试文件才是今天的练习。
"""

def 计算平均分(score_list):
    """传入成绩列表,返回平均分"""
    if not score_list:          # 空列表保护:直接除会崩(ZeroDivisionError)
        return 0
    total = 0
    for score in score_list:
        total += score          # Day 24 的 bug(sum = score)就藏在这类行
    return total / len(score_list)


def 转换等级(score):
    """百分制成绩 → 等级(优秀/良好/及格/不及格)"""
    if score >= 90:
        return "优秀"
    if score >= 80:
        return "良好"
    if score >= 60:
        return "及格"
    return "不及格"


def 过滤不及格(score_list):
    """返回所有 <60 的成绩(组成新列表)"""
    result = []
    for score in score_list:
        if score < 60:
            result.append(score)
    return result
