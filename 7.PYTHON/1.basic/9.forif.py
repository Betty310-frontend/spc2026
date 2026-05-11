numbers = [x for x in range(1, 6)]
print('숫자 리스트:', numbers)

print('\n--- for if 구문 1 ---')
for num in numbers:
    # print(num)
    if num % 2 == 0:
        print(f"숫자 {num}은 짝수입니다.")
    else:
        print(f"숫자 {num}은 홀수입니다.")

print('\n--- for if 구문 2 ---')


even_numbers = []
odd_numbers = []

for num in numbers:
    if num % 2 == 0:
        even_numbers.append(num)
    else:
        odd_numbers.append(num)

print(f'짝수: {even_numbers}')
print(f'홀수: {odd_numbers}')

print('\n--- for if 구문 3 ---')
# NOTE: 너무 많은 반복문이 중첩되면 성능에 영향을 줄 수 있습니다.
# 코드의 효율성, 시간복잡도 / 공간복잡도 고려 필요

import time

n = 10000
count = 0

start_time = time.time() # 현재 시간 기록

# nested loop (중첩 반복문) 의 시간복잡도는? 
# -> O(n^2) 입니다. (n이 10000일 때, 10000 * 10000 = 100,000,000 번 반복)
for i in range(n):
    for j in range(n):
        # for k in range(n):
        #     for l in range(n):
                count += 1

end_time = time.time() # 반복문이 끝난 후 시간 기록
exec_time = end_time - start_time # 실행 시간 계산

print(f"합산: {count}")
print(f"총 소요 시간: {exec_time:.1f}초")