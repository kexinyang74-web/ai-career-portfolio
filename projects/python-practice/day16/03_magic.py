class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __str__(self):
        return f"学生{self.name}的分数是{self.score}"

    def __repr__(self):
        return f"Student('{self.name}', {self.score})"

xiaoming = Student("小明", 80)
print(xiaoming)
print([xiaoming])