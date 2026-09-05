"""假设历史列表叫 history，请你写一小段代码：先把 user_count 设为 0，再遍历历史，只统计 role 为 "user" 的消息。"""
 
user_count = 0
for message in history:
    if message["role"] == "user":
        user_count += 1
print(user_count)
在这段代码中加上助手消息计数 assistant_count，用户和助手的数量分别输出。

assistant_count = 0
for message in history:
    if message["role"] == "assistant":
        assistant_count += 1
print(assistant_count)
print(user_count)
print(assistant_count)

开头初始化两个计数变量，只用一个 for 循环，分别判断用户和助手，最后各输出一次。

user_count = 0
assistant_count = 0
for message in history:
    if message["role"] == "user":
        user_count += 1
    elif message["role"] == "assistant":
        assistant_count += 1
print(user_count)
print(assistant_count)

先在循环前定义 total_chars = 0，再让用户消息和助手消息的 content 长度累加进去，系统消息不计入。

total_chars = 0
for message in history:
    if message["role"] == "user" or message["role"] == "assistant":
        total_chars += len(message["content"])
print(total_chars)

现在把它和前面的两种消息计数合起来，只用一个 for 循环，最后输出用户条数、助手条数和字符总数。你试着写完整。

user_count = 0
assistant_count = 0
total_chars = 0
for message in history:
    if message["role"] == "user":
        user_count += 1
    elif message["role"] == "assistant":
        assistant_count += 1
    if message["role"] == "user" or message["role"] == "assistant":
        total_chars += len(message["content"])
print(user_count)
print(assistant_count)
print(total_chars)