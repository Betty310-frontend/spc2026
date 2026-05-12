import csv 

filename = "data.csv"

# NOTE: list 형태로 복원
data = []

with open(filename, "r", encoding="utf-8") as file:
    """
    csv.reader()는 각 행을 리스트로 반환합니다.
    """
    rows = csv.reader(file)
    for row in rows:
        data.append(row)

print(data) # 데이터 복원


# NOTE: dict 형태로 복원
data2 = []

with open(filename, "r", encoding="utf-8") as file:
    """
    CSV 파일을 딕셔너리 형태로 읽어옵니다.
    각 행은 딕셔너리로 반환되며, 키는 CSV 파일의 헤더를 사용합니다.
    """
    rows = csv.DictReader(file)
    for row in rows:
        data2.append(row)

print(data2)
