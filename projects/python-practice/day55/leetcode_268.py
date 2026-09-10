"""LeetCode 268. 丢失的数字

给定 [0, n] 中缺一个数的数组 nums（长度为 n），返回那个缺失的数。

本地期望：
  missingNumber([3, 0, 1]) -> 2
  missingNumber([0, 1]) -> 2
  missingNumber([9, 6, 4, 2, 3, 5, 7, 0, 1]) -> 8
"""


class Solution:
    def missingNumber(self, nums: list[int]) -> int:
        # 自己写：可用求和公式 n*(n+1)//2 减去现有之和，或异或
        ...


if __name__ == "__main__":
    sol = Solution()
    print(sol.missingNumber([3, 0, 1]))  # 2
    print(sol.missingNumber([0, 1]))  # 2
    print(sol.missingNumber([9, 6, 4, 2, 3, 5, 7, 0, 1]))  # 8
