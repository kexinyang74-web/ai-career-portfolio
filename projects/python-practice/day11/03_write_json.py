# 第 3 步：字典写成 JSON 文件
import json

user = {
    "name": "小明",
    "age": 20,
    "skills": ["python", "Git"],
    "is_active": True,
}

# dumps：字典 → 字符串（先看看变成什么样）
text = json.dumps(user,ensure_ascii=False,indent=2)
print(text)

# dump：字典 → 直接写进文件（s 没了！）
with open("user.json","w",encoding="utf-8") as f:
    json.dump(user,f,ensure_ascii=False,indent=2)
print("写完了，去文件夹里看看 user.json 长什么样")
