# NOTE: 서버에서 바뀌는 데이터를 알아서 반환한다.
# 아래처럼 함수를 부르면 1을 줬다가, 2가 돼면 2를 줬다가, 3이 돼면 3을 주는 식으로 계속 바뀌는 데이터를 반환할 수 있다.

def test():
    yield 1
    yield 2
    yield 3

x = test()

print(x) # <generator object test at 0x00000225E40550C0>, 동적으로 바뀌는 데이터를 전달하는 객체

print(next(x))
print(next(x))
print(next(x)) 
# print(next(x)) # StopIteration: 더 이상 반환할 데이터가 없을 때 발생하는 에러