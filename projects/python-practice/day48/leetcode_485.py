"""LeetCode 485. 最大连续 1 的个数

给定二进制数组 nums（只含 0 和 1），返回其中最大连续 1 的个数。

本地期望：
  findMaxConsecutiveOnes([1,1,0,1,1,1]) -> 3
  findMaxConsecutiveOnes([1,0,1,1,0,1]) -> 2
"""


class Solution:
    def findMaxConsecutiveOnes(self, nums: list[int]) -> int:
        raise NotImplementedError


if __name__ == "__main__":
    sol = Solution()
    print(sol.findMaxConsecutiveOnes([1, 1, 0, 1, 1, 1]))  # 3
    print(sol.findMaxConsecutiveOnes([1, 0, 1, 1, 0, 1]))  # 2
