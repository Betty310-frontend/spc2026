# 튜플 (읽기 전용 리스트)

my_list = [1,2,3,4,5]
my_tuple = (1,2,3,4,5)

print(my_list)
print(my_tuple)

print(my_list[2])
print(my_tuple[2])

my_list[2] = 99
# my_tuple[2] = 99 # 튜플은 읽기 전용이므로 수정 불가능, 오류 발생

print(my_list[-1])
print(my_tuple[-1])

print(my_list[3:5])
print(my_tuple[3:5])

print(my_list[0:1]) # [1]
print(my_tuple[0:1]) # (1,) 튜플에서 요소가 하나인 경우, 쉼표를 붙여야 튜플로 인식됨

# 튜플을 가져왔는데 값을 쓰고 싶다면?
my_new_list = list(my_tuple) # 튜플을 리스트로 변환
print(my_new_list)
my_new_list[2] = 99 # 리스트는 수정 가능
print(my_new_list)
print(my_tuple) # 원래 튜플은 변하지 않음

my_new_tuple = tuple(my_new_list) # 리스트를 다시 튜플로 변환
print(my_new_tuple)

my_new_list[2] = 77
print(my_new_list)
print(my_new_tuple) # 튜플은 변하지 않음

print('-'*30)
a, b, c = (1, 2, 3) # 튜플의 요소를 각각 변수에 할당하는 방법, 언패킹(unpacking)이라고도 불림
print(a, b, c)

a_person = ('John', 23, 'Student')
print(a_person)
name, age, occ = a_person # 튜플의 요소를 각각 변수에 할당
print(f"{name} is {age} years old and He is a {occ}.")