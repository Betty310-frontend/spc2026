def add_numbers(a, b):
    """
    이 함수는 인자를 2개 받아서 그 두 수의 합을 반환하는 함수입니다.
    @params a: 첫 번째 숫자
    @params b: 두 번째 숫자
    @return: 두 수의 합
    """
    return a + b

result = add_numbers(3, 5)
print(f"3과 5의 합은 {result} 입니다.")

def add_numbers2(a, b):
    return a, b, a + b

input1, input2, sum = add_numbers2(3, 4)
print(f"\n입력된 숫자: {input1}, {input2} \n합: {sum}")

def calculate_all(a, b):
    """
    이 함수는 2개의 인자를 받아 사칙연산 결과를 모두 반환하는 함수입니다.
    @params a: 첫 번째 숫자
    @params b: 두 번째 숫자
    @return: 덧셈, 뺄셈, 곱셈, 나눗셈 결과
    """
    addition = a + b
    subtraction = a - b
    multiplication = a * b
    division = a / b if b != 0 else '0으로 나눌 수 없습니다.' # division by zero 방지

    return addition, subtraction, multiplication, division

add, sub, mul, div = calculate_all(10, 2)
print(f"\n덧셈: {add}")
print(f"뺄셈: {sub}")
print(f"곱셈: {mul}")
print(f"나눗셈: {div}")

add, _, mul, _ = calculate_all(10, 2)
print(f"\n덧셈: {add}")
print(f"곱셈: {mul}")

print('\n'+'-'*30+'\n')

def create_profile(name, age, city = '서울', job="학생"):
    """
    이 함수는 이름, 나이, 도시, 직업을 받아서 프로필 문자열을 반환하는 함수입니다.
    도시의 기본값은 '서울'이고, 직업의 기본값은 '학생'입니다.
    """
    profile = f"이름: {name}, 나이: {age}, 도시: {city}, 직업: {job}"
    return profile

print(create_profile("홍길동", 30))
print(create_profile("김길동", 25))
print(create_profile("박길동", 27, "대구"))
print(create_profile("이길동", 29, "부산"))
print(create_profile("최길동", 32, "부산", "직장인"))

