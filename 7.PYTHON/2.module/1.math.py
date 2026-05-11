print('--- math 모듈 ---')
import math

print(math.pi) 
print(math.e)
print(math.sqrt(16))
print(math.sin(5)) # 라디안 단위로 입력해야 합니다. 5 라디안은 약 286.48도입니다.
print(math.sin(2*math.pi))


print('\n--- datetime 모듈 ---')
import datetime as dt

print(dt.datetime.now())
print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print(dt.datetime.now().strftime("%Y-%m-%d"))
print(dt.datetime.now().strftime("%H:%M:%S"))

a_day = dt.datetime(2025, 1, 1, 10, 0, 0)
b_day = dt.datetime(2025, 1, 1)
print(a_day)
print(b_day)


print('\n--- random 모듈 ---')
import random

print(random.random()) # 0.0 이상 1.0 미만의 난수 생성
print(math.floor(random.random() * 100)) # 0 이상 100 미만의 정수 난수 생성 (math + random 조합)
print(random.randint(1, 100)) # 1 이상 100 이하의 정수 난수 생성

# 주사위 던지기
def roll_dice():
    return random.randint(1, 6)

print("주사위 결과:", roll_dice())

fruits = ['apple', 'banana', 'cherry', 'grape', 'orange', 'pineapple']

print("\n--- random.randint ---")
def pick_fruit():
    """
    randint 함수를 사용하여 fruits 리스트에서 무작위로 과일을 선택하는 함수입니다.
    """
    index = random.randint(0, len(fruits) - 1)
    return fruits[index]

print("내가 고른 과일:", pick_fruit())

print('\n--- random.choice ---')
def pick_fruit2():
    """
    모듈 안의 메소드로 간단하게 구현할 수 있습니다. random.choice()는 주어진 시퀀스에서 무작위로 요소를 선택하는 함수입니다.
    """
    return random.choice(fruits)

print("내가 고른 과일:", pick_fruit2())
print("내가 고른 과일:", pick_fruit2())
print("내가 고른 과일:", pick_fruit2())