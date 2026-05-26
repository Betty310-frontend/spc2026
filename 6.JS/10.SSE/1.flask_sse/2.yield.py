def test():
    print('A') # 이 부분은 yield 1이 실행되기 전에 실행된다.
    yield 1 # yield 1이 실행되면 test 함수는 일시 중지되고, 1이 반환된다. 다음에 next(x)를 호출하면 test 함수가 다시 실행되면서 yield 2로 넘어간다.

    print('-' *  50) # 구분선
    print('B') # 이 부분은 yield 2가 실행되기 전에 실행된다.
    yield 2 # yield 2가 실행되면 test 함수는 일시 중지되고, 2가 반환된다. 다음에 next(x)를 호출하면 test 함수가 다시 실행되면서 yield 3로 넘어간다.

    print('-' *  50) # 구분선
    print('C') # 이 부분은 yield 3이 실행되기 전에 실행된다.
    yield 3 # yield 3이 실행되면 test 함수는 일시 중지되고, 3이 반환된다. 다음에 next(x)를 호출하면 test 함수가 다시 실행되면서 함수가 종료된다.

x = test()

# print(next(x))
# print(next(x))
# print(next(x)) 
# print(next(x)) # StopIteration: 더 이상 반환할 데이터가 없을 때 발생하는 에러

try:
    while True:
        print(next(x))
except StopIteration:
    print('-' *  50) # 구분선
    print('모든 데이터 사용 완료')