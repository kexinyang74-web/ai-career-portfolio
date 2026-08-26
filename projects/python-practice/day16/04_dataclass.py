from dataclasses import dataclass

@dataclass
class 奶茶:
    口味:str
    温度:str
    甜度:int = 3

    def 介绍(self):
        return f"{self.口味}奶茶，{self.温度},{self.甜度}分糖"

我的茶 = 奶茶("珍珠奶茶","去冰")
print(我的茶)
print(我的茶.介绍())
print(我的茶 == 奶茶("珍珠奶茶", "去冰"))