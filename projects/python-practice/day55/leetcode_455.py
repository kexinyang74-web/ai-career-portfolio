"""LeetCode 455. 分发饼干

每个孩子 g[i] 胃口，每块饼 s[j] 尺寸。一块饼最多给一个孩子，须 s[j] >= g[i]。
返回最多能喂饱的孩子数。

本地期望：
  findContentChildren([1, 2, 3], [1, 1]) -> 1
  findContentChildren([1, 2], [1, 2, 3]) -> 2
"""


class Solution:
    def findContentChildren(self, g: list[int], s: list[int]) -> int:
        # 自己写：两边排序，小饼先喂胃口小的（贪心双指针）
        ...


if __name__ == "__main__":
    sol = Solution()
    print(sol.findContentChildren([1, 2, 3], [1, 1]))  # 1
    print(sol.findContentChildren([1, 2], [1, 2, 3]))  # 2
