# 第 3 步：主动抛错 raise
def calc_score(score):  # 定义函数 calc_score：接收一个分数，返回它的两倍
    if score < 0 or score > 100:  # 如果分数不合法（小于 0 或大于 100）
        raise ValueError(f"分数{score}不合法，必须在 0-100 之间")  # 主动抛出 ValueError 异常，f-string 把具体分数拼进提示里
    return score * 2  # 分数合法才走到这行：返回两倍分数

try:  # 把可能出错的函数调用包进 try
    print(calc_score(50))  # 50 合法 → 打印 100（这行正常执行）
    print(calc_score(999))  # 999 不合法 → 函数内部 raise 抛异常，程序立刻跳去 except，不再继续往下
except ValueError as e:  # 接住主动抛出的 ValueError，用 as e 把错误信息存进变量 e
    print("捕捉到主动抛出的错误:",e)  # 打印错误信息（e 里存的就是 f-string 拼出来的那句话）
