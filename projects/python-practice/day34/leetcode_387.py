"""LeetCode 387. 字符串中的第一个唯一字符

给定一个字符串 s，找到它的第一个不重复字符，返回它的索引。如果不存在，返回 -1。
"""


class Solution:
    def firstUniqChar(self, s: str) -> int:
        # 你来写：先计数，再从左到右找次数为 1 的
        ...


if __name__ == "__main__":
    sol = Solution()
    print(sol.firstUniqChar("leetcode"))  # 0
    print(sol.firstUniqChar("loveleetcode"))  # 2
    print(sol.firstUniqChar("aabb"))  # -1
