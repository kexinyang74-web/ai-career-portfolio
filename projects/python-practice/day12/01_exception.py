# # 第 1 步：try/except 基础
# # 先制造一个「翻车」：读取一个不存在的文件
# with open("不存在的文件.txt","r", encoding="utf-8") as f:
#     count = f.read()
# print("文件读到了")
# ↓ 上面 5 行是被注释掉的「翻车演示」（直接跑会红字崩溃），留着和下面写法对比用

# 第 1 步：try/except 基础
try:  # 把可能出错的代码「关进笼子」：里面抛异常不会让程序崩溃，而是跳到对应的 except
    with open("不存在的文件.txt","r", encoding="utf-8") as f:  # 打开不存在的文件 → 立刻抛出 FileNotFoundError
        count = f.read()  # 读取文件内容（文件都不存在，这行永远不会执行到）
    print("文件读到了")  # 只有文件存在且读取成功才会打印（本例永远不会打印）
except FileNotFoundError:  # 接住「文件不存在」这一种异常，其他异常（如权限错误）接不住
    print("文件不存在,请检查文件名是否正确")  # 文件不存在时的友好提示，代替红字崩溃
print("程序继续跑，没翻车")  # 这行在 try/except 外面：无论有没有异常都会执行，证明程序没崩
