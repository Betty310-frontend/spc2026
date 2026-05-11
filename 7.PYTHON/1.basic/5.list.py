my_list = [1, 3, 5, 7, 9]

print(my_list)
print(len(my_list)) # 리스트의 길이 (요소의 개수)

print(my_list[0]) # 리스트의 첫 번째 요소
# print(my_list[5]) # my_list에서 없는 요소. IndexError: list index out of range, 프로그램 중단

print(my_list[-1])  # 리스트의 마지막 요소, -1은 뒤에서 첫 번째 요소를 의미

print(my_list[1:3]) # 슬라이싱. [1] 포함, [3] 미포함. -> [3, 5]
print(my_list[3:5]) # [3] 포함, [5] 미포함. -> [7, 9]
print(my_list[:2]) # 처음부터, [2] 미포함 -> [1, 3]
print(my_list[2:]) # [2] 포함, 끝까지 -> [5, 7, 9]

# 원본 리스트에 멤버 추가
my_list.append(11) # 리스트의 끝에 11 추가
print(my_list)

# 특정 위치에 멤버 추가
my_list.insert(2, 99) # 인덱스 2에 99 추가
print(my_list)

# 해당 값의 요소 삭제
my_list.remove(99)
print(my_list)

# 해당 인덱스의 요소 삭제
my_list.pop(3) # 인덱스 3의 요소 삭제
print(my_list)

my_list.pop() # 인덱스를 지정하지 않으면 마지막 요소 삭제
print(my_list)

my_list.clear() # 리스트의 모든 요소 삭제
print(my_list)

my_list = [5, 2, 1, 3, 4, 7, 6, 8, 9]
print(my_list)

new_list = sorted(my_list) # [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(new_list) # sorted() 함수는 원본 리스트를 변경하지 않고 정렬된 새로운 리스트를 반환
print(my_list) # 원본 리스트는 그대로

print(my_list.sort()) # sort() 메서드는 원본 리스트를 정렬하고 None을 반환 -> None
print(my_list) # 원본 리스트가 정렬됨 -> [1, 2, 3, 4, 5, 6, 7, 8, 9]

my_list = [5, 2, 1, 3, 4, 7, 6, 8, 9]
copied_list = my_list.copy() # 리스트의 복사본 생성
print('copied_list: ', copied_list) # [5, 2, 1, 3, 4, 7, 6, 8, 9]
copied_list.sort(reverse=True) # 복사본을 내림차순으로 정렬 
print('copied_list (reverse sorted): ', copied_list) # [9, 8, 7, 6, 5, 4, 3, 2, 1]
print('my_list: ', my_list) # 원본 리스트는 그대로 -> [5, 2, 1, 3, 4, 7, 6, 8, 9]

# 리스트 컴프리핸션
numbers = [x for x in range(10)] # 0부터 9까지의 숫자를 포함하는 리스트 생성
print(numbers) # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

numbers = [x for x in range(5)] # 0 ~ 4까지의 숫자를 포함하는 리스트 생성
print(numbers) # [0, 1, 2, 3, 4]

squares = [x**2 for x in range(5)] # 0 ~ 4까지의 숫자의 제곱을 포함하는 리스트 생성
print(squares) # [0, 1, 4, 9, 16]

numbers = [x for x in range(1, 10) if x % 2 == 0] # 1 ~ 9까지의 숫자 중에서 짝수인 숫자를 포함하는 리스트 생성
print(numbers) # [2, 4, 6, 8]

numbers = [x for x in range(1, 10) if x % 2 == 1] # 1 ~ 9까지의 숫자 중에서 홀수인 숫자를 포함하는 리스트 생성
print(numbers) # [1, 3, 5, 7, 9] 

list1 = [1,2,3]
list2 = [4,5,6]
list12 = list1 + list2
print(list12) # [1, 2, 3, 4, 5, 6]
print(list1 * 3) # [1, 2, 3, 1, 2, 3, 1, 2, 3] 리스트를 반복해서 새로운 리스트 생성