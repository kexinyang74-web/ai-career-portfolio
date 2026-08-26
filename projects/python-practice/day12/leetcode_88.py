def merge(nums1, m, nums2, n):
    p1 = m - 1          # nums1 有效区最后一个
    p2 = n - 1          # nums2 最后一个
    p = m + n - 1       # nums1 最末尾的空位（颁奖台）

    # 主循环：两位选手比大小，大的放颁奖台，直到有一方走完
    while p1 >= 0 and p2 >= 0:
        if nums1[p1] > nums2[p2]:   # nums1 的选手更大
            nums1[p] = nums1[p1]    # 复制到颁奖台
            p1 -= 1                 # nums1 选手往前挪
        else:                       # nums2 的选手更大（或相等）
            nums1[p] = nums2[p2]    # 复制到颁奖台
            p2 -= 1                 # nums2 选手往前挪
        p -= 1                      # 颁奖台往前挪

    # 收尾：nums1 先走完的话，nums2 剩下的直接抄到最前面
    while p2 >= 0:
        nums1[p] = nums2[p2]
        p2 -= 1
        p -= 1

    return nums1


# nums1 = [1, 2, 3, 0, 0, 0]
# print(merge(nums1, 3, [2, 5, 6], 3))   # 输出 [1, 2, 2, 3, 5, 6]
nums1 = [4, 0, 0, 0]
nums2 = [1, 2, 3]
print(merge(nums1, 1, nums2, 3))   # 输出 [1, 1, 2, 2, 3, 3]