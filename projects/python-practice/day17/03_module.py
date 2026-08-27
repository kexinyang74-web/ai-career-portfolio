# Day 17 第 3 步：模块与包（练习文件）
# 模块 = 一个 .py 文件。导入 = 把别的文件的功能拿过来用

import math                  # 整体导入：用的时候写 math.sqrt(16)
from math import sqrt        # 只拿一个功能：用的时候写 sqrt(16)
import math as m             # 起别名：用的时候写 m.sqrt(16)

print(math.sqrt(16))         # 4.0
print(sqrt(16))              # 4.0
print(m.sqrt(16))            # 4.0

# ---- 练习：把奶茶店拆成两个文件 ----
# 1. 新建 my_shop.py：写一个 奶茶店 类（店名、菜单 dict、点单() 方法），
#    底部加 if __name__ == "__main__": 的测试代码
# 2. 新建 main.py：from my_shop import 奶茶店，创建一家店并点单
# 3. 分别运行 python main.py 和 python my_shop.py，观察输出差异
