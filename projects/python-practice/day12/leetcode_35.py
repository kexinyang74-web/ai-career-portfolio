def search_insert(nums, target):
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
    return left                     # 没找到，left 停在哪，插入位置就是哪

nums = [1,3,5,6]
target =  7
print(search_insert(nums, target))