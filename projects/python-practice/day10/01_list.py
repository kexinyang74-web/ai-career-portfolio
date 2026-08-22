#列表：增删改查
fruits = ["apple","banana","cherry"]

#查：按索引取值 + 数长度
print(fruits[0])                 #apple(索引从0开始)
print(fruits[-1])                #cherry
print(len(fruits))            #3

#增：末尾加 append，指定位置插 insert
fruits.append("orange")          #加到末尾
fruits.insert(1,"grape")         #插到索引1
print(fruits)

#改：按索引重新赋值
fruits[0] = "watermelon"
print(fruits[0])

#删：按值删 remove,按位置删 pop,清空 clear
fruits.remove("banana")
fruits.pop()
print(fruits)

#遍历： for 循环一个一个拿出来
for f in fruits:
    print(f)






number = [3,1,4,1,5]
number.append(9)
number.sort()
number.pop(0)
print(number)