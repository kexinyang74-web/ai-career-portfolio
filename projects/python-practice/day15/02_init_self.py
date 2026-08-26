class 奶茶:
    def __init__(self, 口味, 温度):
        # 把传进来的值贴到对象身上
        self.口味 = 口味
        self.温度 = 温度

    def 加料(self):
        print(f"给{self.口味}加了珍珠")

    def 介绍(self):
        return f"这杯是{self.口味},{self.温度}的"

我的茶 = 奶茶("珍珠奶茶", "去冰")
我的茶.加料()
print(我的茶.介绍())