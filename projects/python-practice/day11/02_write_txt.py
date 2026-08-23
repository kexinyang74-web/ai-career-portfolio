# 第 2 步：写 txt 文件
lines = ["苹果", "香蕉", "樱桃"]

# 方式一：一行一行写（别忘了 \n）
with open("fruits.txt", "w",encoding="utf-8") as f:
    for item in lines:
        f.write(item + "\n")

# 方式二：writelines 一次写多行（它不会自动加换行！）     
with open("fruits2.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)   

# 方式三：追加模式 a——不清空，接着写
with open("fruits.txt", "a", encoding="utf-8") as f:
    f.write("榴莲\n")

# 读回来看看结果
with open("fruits.txt", "r", encoding="utf-8") as f:
    print(f.read())


# **挑战**：把 `fruits.txt` 用 `a` 模式再追加一行"西瓜"，再读出来，确认旧内容还在。

with open("fruits.txt", "a", encoding="utf-8") as f:
    f.write("西瓜\n")

with open("fruits.txt", "r", encoding="utf-8") as f:
    print(f.read())