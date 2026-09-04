"""LeetCode 383. 赎金信

给你两个字符串 ransomNote 和 magazine，判断 ransomNote 能不能由 magazine 里面的字符构成。
magazine 中每个字符只能用一次。
"""


class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        for i in ransomNote:
            if i not in magazine:
                return False
            magazine = magazine.replace(i, "", 1) # 将magazine中的i字符替换为空字符串，并只替换第一个出现的字符
        return True


if __name__ == "__main__":
    s = Solution()
    print(s.canConstruct("a", "b"))  # False
    print(s.canConstruct("aa", "ab"))  # False
    print(s.canConstruct("aa", "aab"))  # True
