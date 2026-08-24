# # 第 1 步：try/except 基础
# # 先制造一个「翻车」：读取一个不存在的文件
# with open("不存在的文件.txt","r", encoding="utf-8") as f:
#     count = f.read()
# print("文件读到了")
# 第 1 步：try/except 基础
try:
    with open("不存在的文件.txt","r", encoding="utf-8") as f:
        count = f.read()
    print("文件读到了")
except FileNotFoundError:
    print("文件不存在,请检查文件名是否正确")
print("程序继续跑，没翻车")
