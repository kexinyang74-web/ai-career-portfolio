from typing import List

class Solution:
    """LeetCode 的答题盒: 一个类里可以装很多道题的方法"""
    def removeElement(self, nums: List[int], val: int) -> int:
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != val:
                nums[slow] = nums[fast]
                slow += 1
        return slow

    def moveZeroes(self, nums: List[int]) -> None:
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != 0:
                nums[slow] = nums[fast]
                slow += 1
        for i in range(slow, len(nums)):
            nums[i] = 0


    def search_insert(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1          # 边界：数组两端
        while left <= right:      # 条件自己写
            mid = (left + right) // 2  # 猜中间
            if nums[mid] == target:
                return mid             # 猜中了，直接交卷
            elif nums[mid] < target:
                left = mid + 1                    # 猜小了怎么办？left 怎么动？
            else:
                right = mid - 1                    # 猜大了怎么办？right 怎么动？
        return left
           
    

s = Solution()
print(s.removeElement([3,2,2,3], 3))
nums = [0,1,0,3,12]
s.moveZeroes(nums)
print(nums)
print(s.search_insert([1,3,5,6], 7))
