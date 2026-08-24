# 第 3 步：主动抛错 raise
def calc_score(score):
    if score < 0 or score > 100:
        raise ValueError(f"分数{score}不合法，必须在 0-100 之间")
    return score * 2

try:
    print(calc_score(50))
    print(calc_score(999))
except ValueError as e:
    print("捕捉到主动抛出的错误:",e)
