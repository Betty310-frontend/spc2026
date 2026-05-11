# 딕셔너리
# 키:값 쌍으로 이루어진 자료형
my_dict = {
    "name": "Alice",
    "age": 25,
    "location": "Seoul"
}

print(my_dict)  # {'name': 'Alice', 'age': 25, 'location': 'Seoul'}

# JSON과 유사한 구조, 웹 서비스 만들 때 많이 사용. But, JSON은 아님
print(my_dict["name"])  # Alice
print(my_dict["age"])  # 25

my_dict["car"] = 'BMW'
print(my_dict)  # {'name': 'Alice', 'age': 25, 'location': 'Seoul', 'car': 'BMW'}

print(my_dict['location'])  # Seoul
del my_dict['location']
# print(my_dict['location']) # KeyError: 'location'
print(my_dict)  # {'name': 'Alice', 'age': 25, 'car': 'BMW'}

my_age = my_dict.pop('age')
# print(my_dict["age"])  # KeyError: 'age'
print(my_age) # 25
print(my_dict)  # {'name': 'Alice', 'car': 'BMW'}

my_dict.clear() # 딕셔너리의 모든 요소 제거
print(my_dict)  # {}

my_squares = {str(x):x**2 for x in range(1,10)}
print(my_squares)

print(my_squares.keys())
print(my_squares.values())