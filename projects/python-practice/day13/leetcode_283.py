from typing import List   # List[int] 类型注解需要先导入

class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        slow = 0                          # 写字的人，从 0 号位开始
        for fast in range(len(nums)):     # 检查员挨个看
            if nums[fast] != 0:           # 不是 0，就搬到 slow 位置
                nums[slow] = nums[fast]
                slow += 1                 # 写字的人前进一位
        for i in range(slow, len(nums)):  # 搬完了：剩下的位置全部填 0
            nums[i] = 0


nums = [0, 1, 0, 3, 12]
Solution().moveZeroes(nums)   # 直接调用（返回 None，不接返回值）
print(nums)                   # 看数组本身改对没有
