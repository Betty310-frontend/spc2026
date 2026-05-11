# 10명의 유저 name, age, location, car를 가진 딕셔너리 리스트
users = [
    {"name": "홍길동", "age": 30, "location": "서울", "car": "소나타"},
    {"name": "김길동", "age": 25, "location": "부산", "car": "아반떼"},
    {"name": "박길동", "age": 27, "location": "대구", "car": "그랜저"},
    {"name": "이길동", "age": 29, "location": "부산", "car": "K5"},
    {"name": "최길동", "age": 32, "location": "부산", "car": "쏘렌토"},
    {"name": "정길동", "age": 28, "location": "서울", "car": "스포티지"},
    {"name": "조길동", "age": 31, "location": "대전", "car": "모닝"},
    {"name": "강길동", "age": 26, "location": "광주", "car": "레이"},
    {"name": "윤길동", "age": 33, "location": "인천", "car": "투싼"},
    {"name": "김길동", "age": 38, "location": "울산", "car": "캐스퍼"},
    {"name": "장길동", "age": 34, "location": "울산", "car": "싼타페"}
]

def find_user_and_print(name):
    """
    이 함수는 유저의 이름을 받아서 해당 유저의 정보를 반환하는 함수입니다.
    @params name: 찾고자 하는 유저의 이름
    @return: 유저의 정보 딕셔너리 또는 '유저를 찾을 수 없습니다.' 메시지
    """
    for user in users:
        # if user["name"] == name: # 정확히 일치하는 이름을 찾는 경우
        if user["name"].startswith(name): # 주어진 문자열로 시작하는 (name = 성) 유저를 찾는 경우
            return user
    return "유저를 찾을 수 없습니다."

user = find_user_and_print("김")

def find_user_and_return(name):
    """
    이 함수는 유저의 이름을 받아서 해당 유저의 정보를 반환하는 함수입니다.
    @params name: 찾고자 하는 유저의 이름
    @return: 유저의 정보 딕셔너리 리스트
    """
    found = [] # 일치하는 유저를 저장할 리스트
    for user in users:
        if user["name"].startswith(name): # 주어진 문자열로 시작하는 (name = 성) 유저를 찾는 경우
            found.append(user)
    return found

print("\n--- find_user_and_return 결과 ---")
users_found = find_user_and_return("백")
print("사용자 정보:",users_found)

def find_users2(name=None, age=None):
    """
    이름 또는 나이를 입력받아 매칭되는 사람을 반환 하는 함수입니다.
    @params name: 찾고자 하는 유저의 이름 (부분 일치 허용)
    @params age: 찾고자 하는 유저의 나이
    @return: 매칭되는 유저의 정보 딕셔너리 리스트

    NOTE: 좋지 않은 예시. 매개변수의 개수가 늘어날 때마다 조건문이 복잡해지고, 유지보수가 어려워질 수 있습니다.
    """
    found = []
    print(f"\n검색 조건 - 이름: {name}, 나이: {age}")

    for user in users:
        if name and age:
            if user['name'].startswith(name) and user['age'] == age:
                found.append(user)
        elif name:
            if user['name'].startswith(name):
                found.append(user)
        elif age:
            if user['age'] == age:
                found.append(user)
    return found

print("\n--- find_users2 결과 ---")
print("사용자 정보:", find_users2('최', 32))
print("사용자 정보:", find_users2('김', 25))
print("사용자 정보:", find_users2('김'))
print("사용자 정보:", find_users2(age=30))

print('\n'+'-'*30+'\n')

def find_users2_better(name=None, age=None, location=None):
    """
    이름 또는 나이를 입력받아 매칭되는 사람을 반환 하는 함수입니다.
    @params name: 찾고자 하는 유저의 이름 (부분 일치 허용)
    @params age: 찾고자 하는 유저의 나이
    @return: 매칭되는 유저의 정보 딕셔너리 리스트
    """
    found = []
    for user in users:
        if (name is None or user['name'].startswith(name)) \
        and (age is None or user['age'] == age) \
        and (location is None or user['location'] == location):
            found.append(user)
    return found

print("\n--- find_users2_better 결과 ---")
print("사용자 정보:", find_users2_better('최', 32))
print("사용자 정보:", find_users2_better('김'))
print("사용자 정보:", find_users2_better(age=30))
print("사용자 정보:", find_users2_better(location='부산'))

print('\n'+'-'*30+'\n')
def find_users2_best(condition):
    """
    이름 또는 나이를 입력받아 매칭되는 사람을 반환 하는 함수입니다.
    @params condition: 검색 조건이 담긴 딕셔너리 (예: {'name': '김', 'age': 25})
    @return: 매칭되는 유저의 정보 딕셔너리 리스트
    """
    found = []
    for user in users:
        if all(
            user.get(key).startswith(value) if key == 'name' else user.get(key) == value
            for key, value in condition.items()
        ):
            found.append(user)
    return found

# search_condition = {'name': '김', 'car': '캐스퍼'}
# search_condition = {'name': '김'}
search_condition = {'age': 30}
print("\n--- find_users2_best 결과 ---")
print("사용자 정보:", find_users2_best(search_condition))

