class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print("动物在叫")

class Dog(Animal):
    def speak(self):
        print(f"{self.name} 汪汪汪！")

class Cat(Animal):
    def __init__(self, name,color):
        super().__init__ (name)
        self.color = color

    def speak(self):
        print(f"{self.name} 喵喵喵！")

wangcai = Dog("旺财")
wangcai.speak()

miaomiao = Cat("喵喵", "白色")
miaomiao.speak()
print(miaomiao.color)