# Day 17 第 2 步：PEP 8（练习文件）
# PEP 8 = Python 官方代码排版"校规"。不遵守能跑，但难看。
# 最常用的 5 条：4 空格缩进 / 函数名小写+下划线 / 类名大驼峰 / 函数之间空 2 行 / 注释 # 后加空格

# ❌ 反面教材：能跑但难看
def calc(x, y):
    result = x + y
    return result


def show():
    print(calc(1, 2))


# ✅ 正面教材：符合 PEP 8（对比着看差在哪）
def calc(x: int, y: int) -> int:
    result = x + y
    return result


def show() -> None:
    print(calc(1, 2))


# 试一下：光标停在反面教材里，按 Shift + Alt + F，看 VS Code 自动把它排版成什么样
