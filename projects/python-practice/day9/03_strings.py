# s = "  hello, python  "
# print(s.strip())
# print(s.upper())
# print(s.replace("hello", "hi"))
# print(s.split(","))
# print("-".join(["a","b","c"]))
# 把 `s.strip().split(", ")` 和 `" | ".join(...)` 组合起来，打印 `hello | python`（提示：先切出列表，再用 `" | ".join` 拼回去）。
s = " hello,python "
print (s.strip().split(","))
print ("|".join(["hello","python"]))
# print(" | ".join(s.strip().split(",")))正确答案