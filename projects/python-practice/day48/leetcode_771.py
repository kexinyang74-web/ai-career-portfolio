"""LeetCode 771. 宝石与石头

jewels 中的字母代表宝石，stones 是你拥有的石头。
大小写敏感。返回 stones 中宝石的数量。

本地期望：
  numJewelsInStones("aA", "aAAbbbb") -> 3
  numJewelsInStones("z", "ZZ") -> 0
"""


class Solution:
    def numJewelsInStones(self, jewels: str, stones: str) -> int:
        raise NotImplementedError


if __name__ == "__main__":
    sol = Solution()
    print(sol.numJewelsInStones("aA", "aAAbbbb"))  # 3
    print(sol.numJewelsInStones("z", "ZZ"))  # 0
