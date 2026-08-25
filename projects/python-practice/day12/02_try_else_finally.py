# 第 2 步：else 和 finally
try:  # 尝试执行可能出错的代码
    with open("hello.txt","r", encoding="utf-8") as f:  # 打开 hello.txt（这个文件不存在，会抛 FileNotFoundError）
        count = f.read()  # 读取文件内容（文件不存在，这行不会执行到）
except FileNotFoundError:  # 接住「文件不存在」异常
    print("文件不存在,请检查文件名是否正确")  # 异常时的友好提示
else:  # else 块：只有 try 里没抛异常才会执行（和 except 是「二选一」的关系）
    print("文件读到了:\n",count)  # 文件读成功才打印内容
finally:  # finally 块：无论 try 成功还是 except 接住，都会执行——专门用来做「收尾」
    print("收尾：无论发生什么，这句都会打印")  # 收尾语，证明 finally 一定会执行
