# 예외 처리 예시
try:
    result = 10 / 0
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다.")
except:
    print("알 수 없는 오류가 발생했습니다.")
else:
    print(result)

try:
    number = int('abc')
except ValueError:
    print("유효한 정수를 입력하세요.")
else:
    print(f"입력한 숫자는 {number}입니다.")

try:
    a_list = [1,2,3]
    print(a_list[3])
except IndexError:
    print("리스트 인덱스가 범위를 벗어났습니다.")
else:
    print(a_list[3])

try:
    with open('없는파일.txt', 'r') as file:
        data = file.read()
except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
else:
    print(data)