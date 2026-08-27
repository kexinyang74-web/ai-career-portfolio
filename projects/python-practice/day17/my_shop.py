print(f"我 my_shop.py 被加载了，我的 __name__ 是：{__name__!r}")

class 奶茶店:
    def __init__(self, 店名: str, 菜单: dict[str, int]) -> None:
        self.店名 = 店名
        self.菜单 = 菜单  

    def 点单(self, 饮品: str) -> str:
        if 饮品 in self.菜单:
            return f"{self.店名}: {饮品} {self.菜单[饮品]} 元"
        return f"不好意思，{self.店名}没有这个饮品"


if __name__ == "__main__":
    shop = 奶茶店("我的小店", {"珍珠奶茶": 10, "波霸奶茶": 12, "红豆奶茶": 15})
    print(shop.点单("珍珠奶茶"))