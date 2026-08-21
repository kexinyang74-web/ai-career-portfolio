# 输入：s = ["h","e","l","l","o"]
# 输出：["o","l","l","e","h"]
s = ["h", "e", "l", "l", "o"]
left = 0
right = len(s) - 1

while left < right:
    temp = s[left]   # 第 1 步：把 a 的值先存到 temp，别弄丢
    s[left] = s[right]     # 第 2 步：把 b 的值给 a（这时 a 的旧值已经安全存在 temp 里了）
    s[right] = temp   # 第 3 步：把 temp 里存的旧值给 b

    left += 1
    right -= 1

print(s)