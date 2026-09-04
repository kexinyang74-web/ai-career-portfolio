"""LeetCode 387. 字符串中的第一个唯一字符

给定一个字符串 s，找到它的第一个不重复字符，返回它的索引。如果不存在，返回 -1。
"""


class Solution:
    def firstUniqChar(self, s: str) -> int:
        for i in range(len(s)): # 遍历字符串s
            if s.count(s[i]) == 1: # 如果字符串s中第i个字符只出现一次   
                return i # 则返回第i个字符的索引
        return -1 # 如果字符串s中没有不重复的字符，则返回-1





if __name__ == "__main__":
    sol = Solution()
    print(sol.firstUniqChar("leetcode"))  # 0
    print(sol.firstUniqChar("loveleetcode"))  # 2
    print(sol.firstUniqChar("aabb"))  # -1
