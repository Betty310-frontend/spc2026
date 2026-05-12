class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"안녕하세요, 저는 {self.name} 입니다.")

    def study(self, subject):
        print(f"{self.name} 는 {subject} 를 공부하고 있습니다.")

person1 = Person("Alice", 25)
person2 = Person("Bob", 27)

person1.greet()  # Output: 안녕하세요, 저는 Alice 입니다.
person2.greet()  # Output: 안녕하세요, 저는 Bob 입니다.

person1.study("Python")  # Output: Alice 는 Python 를 공부하고 있습니다.
person2.study("영어")    # Output: Bob 는 영어 를 공부하고 있습니다.