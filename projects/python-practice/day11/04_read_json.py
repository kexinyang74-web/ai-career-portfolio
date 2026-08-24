# 第 4 步：读 JSON 文件
import json

with open("user.json","r", encoding="utf-8") as f:
    data = json.load(f)

# 现在 data 和普通字典一样用
print(data["name"])
print(data["age"])
print(data["skills"][0])

# 进阶：json.loads 管的是"字符串"
# 把 dumps 的字符串再变回字典
text = '{"name": "小红", "age": 18}'
d = json.loads(text)
print(d["name"])
