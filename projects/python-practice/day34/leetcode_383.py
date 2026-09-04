"""LeetCode 383. 赎金信

给你两个字符串 ransomNote 和 magazine，判断 ransomNote 能不能由 magazine 里面的字符构成。
magazine 中每个字符只能用一次。
"""


class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        # 你来写：统计 magazine 各字母次数，再逐个减 ransomNote
        ...


if __name__ == "__main__":
    s = Solution()
    print(s.canConstruct("a", "b"))  # False
    print(s.canConstruct("aa", "ab"))  # False
    print(s.canConstruct("aa", "aab"))  # True
