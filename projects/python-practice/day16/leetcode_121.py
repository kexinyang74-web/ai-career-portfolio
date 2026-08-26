from typing import List

# m*n 的二维数组 plants 记录了园林景观的植物排布情况，具有以下特性：

# 每行中，每棵植物的右侧相邻植物不矮于该植物；
# 每列中，每棵植物的下侧相邻植物不矮于该植物。
# 请判断 plants 中是否存在目标高度值 target。


# 示例 1：

# 输入：plants = [[2,3,6,8],[4,5,8,9],[5,9,10,12]], target = 8

# 输出：true

class Solution:
    def findTargetIn2DPlants(self, plants: List[List[int]], target: int) -> bool:
        # 空表格：没有任何植物，直接说"没有"
        if not plants:
            return False

        # 从右上角出发：第 0 行、最后一列
        row = 0
        col = len(plants[0]) - 1

        # 只要还没走出表格，就一直走
        while row < len(plants) and col >= 0:
            current = plants[row][col]

            if current > target:
                col -= 1          # 数字太大 → 往左走，排除整列
            elif current < target:
                row += 1          # 数字太小 → 往下走，排除整行
            else:
                return True       # 正好相等 → 找到了！

        return False              # 走出表格都没找到 → 没有


solution = Solution()
print(solution.findTargetIn2DPlants([[2, 3, 6, 8], [4, 5, 8, 9], [5, 9, 10, 12]], 8))   # 有 8 → True
print(solution.findTargetIn2DPlants([[2, 3, 6, 8], [4, 5, 8, 9], [5, 9, 10, 12]], 7))   # 没有 7 → False
print(solution.findTargetIn2DPlants([], 0))                                              # 空表格 → False
