# 사람의 유형 중 하나인 운전자(Driver)를 클래스로 표현
from person import Person

class Driver(Person):
    def __init__(self, name, age, car):
        super().__init__(name, age)
        self.car = car

    def drive(self):
        print(f"{self.name}은 {self.car} 운전을 시작합니다.")

    def drive_fast(self):
        print(f"{self.name}은 {self.car} 과속 운전을 합니다.")