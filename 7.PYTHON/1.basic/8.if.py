print('--- if 구문 ---')

score = 80
if score >= 80:
    # print('성적은 A 입니다.')
    grade = 'A'
elif score >= 70:
    # print('성적은 B 입니다.')
    grade = 'B'
elif score >= 60:
    # print('성적은 C 입니다.')
    grade = 'C'
else:
    # print('성적은 F 입니다.')
    grade = 'F'

print(f"이 학생의 점수는 {score}점 이고, 학점은 {grade} 입니다.")

print('\n--- if 구문 2 ---')
# 12, 1, 2 겨울 / 3, 4, 5 봄 / 6, 7, 8 여름 / 9, 10, 11 가을
month = 7
if month in [12, 1, 2]:
    # print(f'{month}월은 겨울입니다.')
    season = '겨울'
elif month in [3, 4, 5]:
    # print(f'{month}월은 봄입니다.')
    season = '봄'
elif month in [6, 7, 8]:
    # print(f'{month}월은 여름입니다.')
    season = '여름'
elif month in [9, 10, 11]:
    # print(f'{month}월은 가을입니다.')
    season = '가을'
else:
    # print(f'{month}는 잘못된 값 입니다.')
    season = '알 수 없음'

print(f'{month}월은 {season}입니다.')


print('\n--- if 구문 3 ---')
height = 175 # cm
weight = 70 # kg
bmi = weight / ((height / 100) ** 2)

if bmi < 18.5:
    category = '저체중'
elif bmi < 25:
    category = '정상체중'
elif bmi < 30:
    category = '과체중'
else:
    category = '비만'

print(f"키 {height}cm, 몸무게 {weight}kg인 사람의 BMI는 {bmi:.2f}이며, 체형은 {category}입니다.")

print('\n--- if 구문 4 ---')
username = 'admin'
# username = 'user'
password = '1234'

if username and password:
    if username == 'admin' and password == '1234':
        print('관리자 로그인 성공')
    elif username == 'user' and password == '1234':
        print('일반 사용자로 로그인 성공')
    else:
        print('로그인 실패: 유저네임 또는 비밀번호가 잘못되었습니다.')
else:
    print('로그인 실패: 유저네임과 비밀번호를 입력하세요.')
    