import random
import string

def generate_random_password(length=8):
    """
    주어진 길이의 랜덤한 비밀번호를 생성하는 함수입니다.
    비밀번호는 대문자, 소문자, 숫자, 특수문자를 포함할 수 있습니다.
    """

    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

print((generate_random_password()))
print((generate_random_password(16)))
print((generate_random_password(32)))