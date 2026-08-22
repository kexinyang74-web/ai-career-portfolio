#字典：增删改查
student = {"name":"小明", "age":18,"city":"上海"}

#查：按键取值（键不存在会报错）
print(student["name"])
print(student.get("age"))
print(student.get("score","没有这个键"))

#判断键在不在
print("name" in student)

#增：直接给新键赋值
student["score"] = 95
print(student)

#改：给已有键重新赋值
student["age"] = 19
print(student["age"])

#删：pop 删指定键，del 也行
student.pop("city")
print(student)

#遍历：items()一次拿键和值
for key,value in student.items():
    print(key,"→", value)



score = {"语文":90, "数学": 85}

for key, value in score.items():
    print(key,value,"分")