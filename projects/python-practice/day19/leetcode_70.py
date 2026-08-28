# 你正在爬楼梯，每次可以爬 1 阶或 2 阶。问爬到第 n 阶有多少种不同的爬法？
# 例子：
# n = 3 → 3 种（1+1+1、1+2、2+1）
# n = 4 → 5 种
class Solution:
    def climbStairs(self, n: int) -> int:
        if n == 1:
            return 1
        a, b = 1, 2          # a = f(1)，b = f(2)
        for _ in range(3, n + 1):
            a, b = b, a + b  # 往前滚：新的 b = 前两个之和
        return b

print(Solution().climbStairs(3))
print(Solution().climbStairs(4))
print(Solution().climbStairs(5))
print(Solution().climbStairs(6))
print(Solution().climbStairs(7))
print(Solution().climbStairs(8))
print(Solution().climbStairs(9))
print(Solution().climbStairs(10))