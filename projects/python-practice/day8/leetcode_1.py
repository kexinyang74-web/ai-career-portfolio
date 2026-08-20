# 题目：给一个整数数组 nums 和一个目标值 target，找出数组中两个数相加等于 target 的那两个，返回它们的下标。
# 示例：
# - nums = [2, 7, 11, 15]、target = 9 → 返回 [0, 1]（因为 2 + 7 = 9）
# - nums = [3, 2, 4]、target = 6 → 返回 [1, 2]（因为 2 + 4 = 6，注意不是 3+2，下标要对应）
# - nums = [3, 3]、target = 6 → 返回 [0, 1]
nums = [2, 7, 11, 15]
target = 9
for i in range(len(nums)):
    for j in range(i+1,len(nums)):
        if nums[i] + nums[j] == target:
            print([i,j])
            break
    else:
        continue
    break




#高级解法：
# def two_sum(nums, target):
#     for i in range(len(nums)):
#         for j in range(i + 1, len(nums)):
#             if nums[i] + nums[j] == target:
#                 return [i, j]   # return 一出口，函数立刻结束，不用 break 两层

# print(two_sum([2, 7, 11, 15], 9))   # 输出 [0, 1]