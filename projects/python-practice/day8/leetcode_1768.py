#题目：给你两个字符串 word1 和 word2 。请你从 word1 开始，通过交替添加字母来合并字符串。如果一个字符串比另一个字符串长，就将多出来的字母追加到合并字符串的末尾。
#word1 = "abc"
#word2 = "pqr"
#合并字符串为 "apbqcr"
#如果一个字符串比另一个字符串长，就将多出来的字母追加到合并字符串的末尾。
#word1 = "ab"
#word2 = "pqrs"
#合并字符串为 "apbqrs"


word1 = "ab"
word2 = "pqrs"
result = ""



for i in range(max(len(word1),len(word2))):
    if i < len(word1):
        result += word1[i]
    if i < len(word2):
        result += word2[i]
print(result)



