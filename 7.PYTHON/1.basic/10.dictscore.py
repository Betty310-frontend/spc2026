students = {
    "김철수": 70,
    "이영희": 85,
    "박민수": 90,
    "최지우": 75,
    "정다은": 80,
    "한지민": 95,
    "강다현": 88,
    "홍길동": 65,
    "유재석": 92,
    "박명수": 32,
}

print('--- 학생 점수 Dictionary ---')
print(students)

def get_a_student(students):
    a_students = []
    for name, score in students.items(): # dict의 요소 key, value 쌍을 반환
        if score >= 90:
            a_students.append(name)
    return a_students

print('\n--- A 학점 학생 ---')
print(get_a_student(students))