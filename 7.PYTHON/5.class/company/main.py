# 여러 클래스를 불러서 조립 후 실행
from person import Person
from employee import Employee
from driver import Driver

print('\n')
employee1 = Employee("James", 25, "Samsung")
employee1.greet()

print('\n')
employee2 = Employee("John", 27, "LG")
employee2.greet()

print('\n')
person1 = Person('Bob', 30)
person1.greet()

print('\n')
person1.set_age(40)
person1.greet()
print(person1.get_name())

print('\n')
driver1 = Driver("Alice", 35, "BMW")
driver1.drive()
driver1.greet()
driver1.drive_fast()