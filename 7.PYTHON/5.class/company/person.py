# 제네릭 유형

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def set_age(self, val):
        self.age = val
    
    def greet(self):
        print(f"안녕하세요, 저는 {self.age}살 {self.name} 입니다.")