# Day 17 第 3 步补充：__name__ == "__main__"（练习文件）
# 每个 .py 文件都有隐藏变量 __name__：
#   - 直接运行本文件时 → __name__ 是 "__main__"
#   - 被别人 import 时 → __name__ 是文件名

print(f"我在 04_main.py 里，我的 __name__ 是：{__name__!r}")

if __name__ == "__main__":
    print("我被直接运行了 → 所以这段测试代码会执行")
else:
    print("我是被别的文件 import 进来的 → 所以测试代码不会执行")

# 试一下：新建一个文件写 import 04_main（或 import 上一题做的 my_shop），
# 看"被导入"时哪部分代码不跑
