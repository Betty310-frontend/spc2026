# 사람의 유형 중 하나인 직원(Employee)을 클래스로 표현
from person import Person

class Employee(Person):
    def __init__(self, name, age, company):
        super().__init__(name, age)
        self.company = company

    def greet(self): # 오버라이딩
        print(f"안녕하세요, 저는 {self.company} 에 다니고 있는 {self.age} 살 {self.name} 입니다.")