# 给定一个整数数组 nums 和一个目标值 target，找出数组中和等于 target 的两个数，返回它们的下标。
# 例子：
# nums = [2, 7, 11, 15]，target = 9
# → 返回 [0, 1]（因为 2 + 7 = 9）
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
print(two_sum([2, 7, 11, 15], 9))