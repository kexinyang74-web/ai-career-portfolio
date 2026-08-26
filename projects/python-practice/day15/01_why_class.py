# 函数式写法：数据和操作分开，每个函数都要手动传数据
def exam(student_name,score):
    return {"name": student_name, "score": score+10}

def report(student):
    return f"{student['name']} 考了{student['score']}分"

student = exam("小明",80)
print(report(student))



# 面向对象写法：数据和操作打包成一个"类"
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def exam(self):
        self.score += 10

    def report(self):
        return f"{self.name} 考了{self.score}分"

xiaoming = Student("小明",80)
xiaoming.exam()
print(xiaoming.report())

xiaohong = Student("小红",60)
xiaohong.exam()
xiaohong.exam()
print(xiaohong.report())
