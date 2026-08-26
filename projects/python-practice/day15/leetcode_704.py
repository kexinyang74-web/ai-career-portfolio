# # 给定一个 n 个元素有序的（升序）整型数组 nums 和一个目标值 target  ，写一个函数搜索 nums 中的 target，如果 target 存在返回下标，否则返回 -1。

# # 你必须编写一个具有 O(log n) 时间复杂度的算法。
# 示例 1:

# 输入: nums = [-1,0,3,5,9,12], target = 9
# 输出: 4
# 解释: 9 出现在 nums 中并且下标为 4


class Solution:
    def search(self, nums, target): 
        left = 0
        right = len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

print(Solution().search([-1,0,3,5,9,12], 9))



print(Solution().search([-1,0,3,5,9,12], 2))     # 2 不存在 → 应该 -1
print(Solution().search([-1,0,3,5,9,12], 13))    # 比所有数都大 → 应该 -1
print(Solution().search([-1,0,3,5,9,12], -1))    # 第一个元素 → 应该 0
print(Solution().search([5], 5))                 # 只有一个元素 → 应该 0
print(Solution().search([], 1))                  # 空数组 → 应该 -1