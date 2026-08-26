class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} 在吃东西")

    def sleep(self):
        print(f"{self.name} 在睡觉")

class Dog(Animal):
    pass

class Cat(Animal):
    pass

wangcai = Dog("旺财")
wangcai.eat()
wangcai.sleep()
miaomiao = Cat("喵喵")
miaomiao.sleep()
miaomiao.eat()