# 문자열을 변수에 할당. string 타입 추론
s = 'Hello, World!'

print(s)
print(s.lower()) # 모든 문자열 소문자
print(s.upper()) # 모든 문자열 대문자
print(s.capitalize()) # 각 문장의 시작이 대문자
print(s.title()) # 각 단어의 시작이 대문자

s = '     Hello, World!    '
print(s.lstrip()+'!!') # 왼쪽 공백 제거
print(s.rstrip()+'!!') # 오른쪽 공백 제거
print(s.strip()+'!!') # 양쪽 공백 제거

print(s.split()) # 문자열로 분할, 인자값이 없으면 공백으로 분할

s = 'apple banana cherry'
print(s.split()) # ['apple', 'banana', 'cherry']

s = "apple, banana, cherry"
print(s.split()) # ['apple,', 'banana,', 'cherry']
print(s.split(', ')) # ['apple', 'banana', 'cherry']

s = 'apple,banana,cherry' # csv 포맷
print(s.split(',')) # ['apple', 'banana', 'cherry']

s_list = s.split(',')
print(s_list) # ['apple', 'banana', 'cherry']
print(' '.join(s_list)) # apple banana cherry
print(', '.join(s_list)) # apple, banana, cherry

s = 'Hello, World'
print(s)
print(s.startswith('Hello')) # 문자열이 'Hello'로 시작하는지 확인 -> True
print(s.startswith('hello')) # 문자열이 'hello'로 시작하는지 확인 -> False
print(s.endswith('World')) # 문자열이 'World'로 끝나는지 확인 -> True
print(s.find('World')) # 문자열에서 'World'의 위치를 반환 -> 7
print(s.find('world')) # 문자열에서 'world'의 위치를 반환 -> -1 (없다)