# 숫자를 할당하면 int 타입이 된다.
x = 5
y = 3

print('\n- 사칙연산 -')
print(x + y)
print(x - y)
print(x * y)
print(x / y) # 나누기 연산은 항상 float 타입이 된다.

print('\n- 나머지 연산 -')
print(x % y) # 나누기 연산의 나머지를 구하는 연산자

print('\n- 몫 연산 -')
print(x // y) # 나누기 연산의 몫을 구하는 연산자

print('\n- 제곱 연산 -')
print(x ** y) # x의 y 제곱을 구하는 연산자

print('\n- 진법 변환 -')
x = 11
print(bin(x)) # x를 2진수 문자열로 변환하는 함수
print(oct(x)) # x를 8진수 문자열로 변환하는 함수 (잘 안 씀)
print(hex(x)) # x를 16진수 문자열로 변환하는 함수 (많이 쓰임)

print('\n- 절대값 -')
x = -10
print(x)
print(abs(x)) # x의 절댓값을 구하는 함수

print('\n- 정수 변환 -')
y = 4.5
print(y)
print(int(y)) # y를 정수로 변환하는 함수 (소수점 아래는 버림)

print('\n- 타입 변환 -')
z = '100'
print(z) # 문자열
print(int(z)) # 숫자


print('\n- 비트 연산 -')
x = 5
y = 3
print(x & y) # 5 = 101, 3 = 011, 5 & 3 = 001 = 1
print(x | y) # 5 = 101, 3 = 011, 5 | 3 = 111 = 7
print(x ^ y) # XOR, 5 = 101, 3 = 011, 5 ^ 3 = 110 = 6
print(~x) # NOT, 5 = 00000101, ~5 = 11111010 = -6 (2의 보수 표현)
print (x << 1) # 왼쪽으로 1자리 이동, 0000_0101 -> 0000_1010 = 10
print(x >> 1) # 오른쪽으로 1자리 이동, 0000_0101 -> 0000_0010 = 2
