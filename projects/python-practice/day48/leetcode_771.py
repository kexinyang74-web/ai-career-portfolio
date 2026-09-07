"""LeetCode 771. 宝石与石头

jewels 中的字母代表宝石，stones 是你拥有的石头。
大小写敏感。返回 stones 中宝石的数量。

本地期望：
  numJewelsInStones("aA", "aAAbbbb") -> 3
  numJewelsInStones("z", "ZZ") -> 0
"""


class Solution:
    def numJewelsInStones(self, jewels: str, stones: str) -> int:
        count = 0 # 宝石的数量
        for stone in stones: # 遍历 stones 中的每个石头
            if stone in jewels: # 如果石头是宝石，则宝石的数量加 1
                count += 1 # 宝石的数量加 1
        return count # 返回宝石的数量


if __name__ == "__main__":
    sol = Solution()
    print(sol.numJewelsInStones("aA", "aAAbbbb"))  # 3
    print(sol.numJewelsInStones("z", "ZZ"))  # 0
