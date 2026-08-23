# 第 1 步：读 txt 文件
# 先用 w 模式写一个小文件（明天你会自己会写，今天先借用）
with open("hello.txt","w",encoding="utf-8") as f:
    f.write("第一行\n第二行\n第三行\n")

# 然后读它：r 模式 = 只读
with open("hello.txt","r",encoding="utf-8") as f:
    content = f.readlines()  # read() = 一次读完整个文件，得到一个字符串
    print(content)


# **挑战 2（指针实验，很重要）**：

with open("hello.txt","r",encoding="utf-8") as f:
    print(f.read())
    print("----- 第二次 -----")
    print(f.read())
