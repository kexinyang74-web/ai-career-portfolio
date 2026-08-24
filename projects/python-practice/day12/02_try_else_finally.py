# 第 2 步：else 和 finally
try:
    with open("hello.txt","r", encoding="utf-8") as f:
        count = f.read()
except FileNotFoundError:
    print("文件不存在,请检查文件名是否正确")
else:
    print("文件读到了:",count)
finally:
    print("收尾：无论发生什么，这句都会打印")