"""LeetCode 485. 最大连续 1 的个数

给定二进制数组 nums（只含 0 和 1），返回其中最大连续 1 的个数。

本地期望：
  findMaxConsecutiveOnes([1,1,0,1,1,1]) -> 3
  findMaxConsecutiveOnes([1,0,1,1,0,1]) -> 2
"""


class Solution:
    def findMaxConsecutiveOnes(self, nums: list[int]) -> int:
        max_count = 0 # 最大连续 1 的个数
        count = 0 # 当前连续 1 的个数
        for num in nums:
            if num == 1: # 当前元素为 1，则连续 1 的个数加 1
                count += 1
            else: # 当前元素为 0，则更新最大连续 1 的个数，并重置当前连续 1 的个数
                max_count = max(max_count, count) # 更新最大连续 1 的个数
                count = 0 # 重置当前连续 1 的个数
        return max(max_count, count) # 返回最大连续 1 的个数


if __name__ == "__main__":
    sol = Solution()
    print(sol.findMaxConsecutiveOnes([1, 1, 0, 1, 1, 1]))  # 3
    print(sol.findMaxConsecutiveOnes([1, 0, 1, 1, 0, 1]))  # 2
