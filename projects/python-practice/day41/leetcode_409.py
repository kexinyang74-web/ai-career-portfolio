"""LeetCode 409. 最长回文串

给定由大小写字母组成的字符串 s，用其中的字母能构造的最长回文串的长度。
字母区分大小写（'Aa' 不能配成一对）。

本地期望：
  longestPalindrome("abccccdd") -> 7
  longestPalindrome("a") -> 1
"""


class Solution:
    def longestPalindrome(self, s: str) -> int:
        raise NotImplementedError


if __name__ == "__main__":
    sol = Solution()
    print(sol.longestPalindrome("abccccdd"))  # 7
    print(sol.longestPalindrome("a"))  # 1
