"""LeetCode 409. 最长回文串

给定由大小写字母组成的字符串 s，用其中的字母能构造的最长回文串的长度。
字母区分大小写（'Aa' 不能配成一对）。

本地期望：
  longestPalindrome("abccccdd") -> 7
  longestPalindrome("a") -> 1
"""


class Solution:
    def longestPalindrome(self, s: str) -> int:
        from collections import Counter # 计数器
        counter = Counter(s) # 统计s中每个字符出现的次数
        result = 0 # 初始化结果为0
        has_odd = False # 初始化是否有奇数为False
        for char in counter: # 遍历s中每个字符
            if counter[char] % 2 == 0: # 如果字符出现的次数为偶数
                result += counter[char] # 将字符出现的次数加入结果
            else: # 如果字符出现的次数为奇数
                result += counter[char] - 1 # 将字符出现的次数减1加入结果
                if not has_odd: # 如果还没有奇数
                    has_odd = True # 设置为True
        return result + (1 if has_odd else 0) # 返回结果


if __name__ == "__main__":
    sol = Solution()
    print(sol.longestPalindrome("abccccdd"))  # 7
    print(sol.longestPalindrome("a"))  # 1
