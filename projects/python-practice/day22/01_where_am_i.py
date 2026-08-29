"""练习 1：我现在在哪个环境？

目的：学会"看清自己正在用哪个 Python"。
同一个 Python 解释器=同一个环境。venv 的作用就是换一个解释器路径。

运行：python 01_where_am_i.py
对比：激活虚拟环境后再次运行，两行输出应该不同。
"""
import sys
import requests

print("当前 Python 解释器路径:", sys.executable)
print("requests 版本:", requests.__version__)
