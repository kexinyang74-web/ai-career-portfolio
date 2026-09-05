"""LeetCode 389. 找不同

给定字符串 s 和 t，t 由 s 打乱后加一个字母得到。返回多出来的那个字母。

本地期望：
  findTheDifference("abcd", "abcde") -> "e"
  findTheDifference("", "y") -> "y"
"""


class Solution:
    def findTheDifference(self, s: str, t: str) -> str:  # 位运算
        result = 0 # 初始化结果为0
        for char in s: # 遍历s中每个字符
            result ^= ord(char) # 将字符的ASCII码与结果进行异或运算
        for char in t: # 遍历t中每个字符
            result ^= ord(char) # 将字符的ASCII码与结果进行异或运算
        return chr(result) # 返回结果的ASCII码对应的字符
    def findTheDifference2(self, s: str, t: str) -> str: # 哈希表
        from collections import Counter # 计数器
        counter_s = Counter(s) # 统计s中每个字符出现的次数
        counter_t = Counter(t) # 统计t中每个字符出现的次数
        for char in counter_t: # 遍历t中每个字符
            if counter_t[char] != counter_s[char]: # 如果t中字符出现的次数与s中字符出现的次数不同
                return char
        return "" # 如果t中字符出现的次数与s中字符出现的次数相同
    def findTheDifference3(self, s: str, t: str) -> str: # 排序
        return "".join(sorted(t) - sorted(s)) # 返回t中字符减去s中字符的差集
if __name__ == "__main__":
    sol = Solution()
    print(sol.findTheDifference("abcd", "abcde"))  # e
    print(sol.findTheDifference2("abcd", "abcde"))  # e
    print(sol.findTheDifference3("abcd", "abcde"))  # e
    print(sol.findTheDifference("", "y"))  # y
    print(sol.findTheDifference2("", "y"))  # y
    print(sol.findTheDifference3("", "y"))  # y
