class Student:
    school = "第一中学"

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def exam(self):
        self.score += 10
        return self.score

    @staticmethod
    def rule():
        return "禁止作弊"

xiaoming = Student("小明", 80)
xiaohong = Student("小红", 60)

print(xiaoming.school,xiaohong.school)
print(xiaoming.name,xiaohong.name)
print(Student.rule())