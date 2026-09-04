"""给你两个整数数组 nums1 和 nums2 ，请你以数组形式返回两数组的交集。返回结果中每个元素出现的次数，应与元素在两个数组中都出现的次数一致（如果出现次数不一致，则考虑取较小值）。可以不考虑输出结果的顺序。"""
class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        nums1.sort() # 排序
        nums2.sort() # 排序
        i = 0 # 指针
        j = 0 # 指针
        result = [] # 结果数组
        while i < len(nums1) and j < len(nums2): # 两个指针都小于数组长度
            if nums1[i] == nums2[j]: # 如果两个指针指向的元素相等
                result.append(nums1[i]) # 将元素添加到结果数组中
                i += 1
                j += 1 # 两个指针都向后移动
            elif nums1[i] < nums2[j]:
                i += 1 # 如果第一个指针指向的元素小于第二个指针指向的元素，则第一个指针向后移动
            else:
                j += 1 # 如果第一个指针指向的元素大于第二个指针指向的元素，则第二个指针向后移动
        return result # 返回结果数组
if __name__ == "__main__":
    solution = Solution() # 创建Solution类对象
    print(solution.intersect([1,2,2,1], [2,2]))
    print(solution.intersect([4,9,5], [9,4,9,8,4])) # 调用intersect方法 