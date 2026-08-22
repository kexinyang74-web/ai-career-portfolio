# 给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的 字母异位词。

 

# 示例 1:

# 输入: s = "anagram", t = "nagaram"
# 输出: true
# 示例 2:

# 输入: s = "rat", t = "car"
# 输出: false
 

# 提示:

# 1 <= s.length, t.length <= 5 * 104
# s 和 t 仅包含小写字母



def is_anagram(s, t):
    if len(s) != len(t):      # 小优化：长度都不一样，直接 False（想得通为什么吗？）
        return False

    count_s = {}              # ① 统计 s
    for ch in s:
        count_s[ch] = count_s.get(ch,0) + 1     # ② word_freq 核心行，把 ch 当单词

    count_t = {}              # ③ 统计 t（一样）
    for ch in t:
        count_t[ch] = count_t.get(ch,0) + 1 

    return count_s == count_t    # ④ 字典直接比较，填 == 还是 !=？

print(is_anagram("anagram", "nagaram"))
print(is_anagram("rat", "car"))