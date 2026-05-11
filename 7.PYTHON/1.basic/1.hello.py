print('Hello, Python!')
print('Hello, ' + 'Python!')
print("Hello, " + "Python!")
print("Hello,", "Python!")

num = 5
name = '홍길동'

print("Hello, {}".format(name))
print("Hello, {}. My lucky number is {}.".format(name, num))
print("Hello, {0}. My lucky number is {1}.".format(name, num))
print(f"Hello, {name}, My Lucky number is {num}.")
print("Hello, %s" % name, end=" ")
print("Hello, %s" % name, end=" ")
print("Hello, %s" % name, end=" ")
print("Hello, %s" % name)

pi = 3.141592653589793
print(f"{pi:.2f}")

print(f"{10:<5}")
print(f"{10:>5}")
print(f"{10:^5}")

print(f"{7:03}")

multiline = """
    여기는 멀티라인으로
    긴 주석을 넣을 수 있습니다.
    사실은 주석이 아니고 여러 줄의 문자열입니다.
    하지만 변수에 할당하지 않으면 주석처럼 사용할 수 있습니다.
"""

print(multiline)