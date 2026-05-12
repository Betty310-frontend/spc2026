with open("file.txt", "r", encoding="utf-8") as file:
    contents = file.read()
    print(contents)

"""
NOTE: 과거에 사용하던 방법. close() 메서드를 사용하여 파일을 닫아야 한다.
Legacy 파일 open / read / close 패턴
"""
# file = open('file.txt', 'r', encoding='utf-8')
# data = file.read()
# file.close()

# print(data)

# NOTE: 3. 큰 파일 읽기
with open("file.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

    for line in lines:
        print("파일 내용:", line)