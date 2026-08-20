# def greet(name):
#     return "你好，" + name + "!"

# print(greet("小明"))
# print(greet("小红"))
# 把 `greet` 改成两个参数 `greet(name, greeting)`，`print(greet("小明", "早上好"))` 应输出 `早上好，小明！`——体会"参数 = 函数要的输入"。
def greet(name, greeting):
    return greeting + "，" + name + "!"
print(greet("小明", "早上好"))
print(greet("小红", "晚上好"))