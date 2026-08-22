nums = {1,2,2,3,3,3}
print(nums)

#增删
nums.add(4)
nums.remove(2)
nums.discard(99)
print(nums)

#判断在不在
print(3 in nums)

#去重神器：把列表转集合再转回列表
words = ["a","b","a","c","b"]
unique = list(set(words))
print(unique)

#集合运算
a = {1,2,3}
b = {3,4,5}
print(a&b)
print(a|b)
print(a-b)


a=[1,2,3,4]
b=[3,4,5,6]
print(set(a)&set(b))
