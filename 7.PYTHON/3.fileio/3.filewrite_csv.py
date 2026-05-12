import csv

data = [
    ["Name", "Age", "City"], # Header = 첫번째 줄
    ["Alice", 30, "New York"],
    ["Bob", 25, "Los Angeles"],
    ["Charlie", 35, "Chicago"]
]

filename = "data.csv"

with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

# NOTE: 좀 더 모던한 방식 - 딕셔너리 형태로 작성
data2 = [
    {"Name":"Alice", "Age":30, "City":"New York"},
    {"Name":"Bob", "Age":25, "City":"Los Angeles"},
    {"Name":"Charlie", "Age":35, "City":"Chicago"}
]

with open("data_dict.csv", "w", newline="") as file:
    fieldnames = data2[0].keys() # Header = 딕셔너리의 키
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader() # Header 작성
    writer.writerows(data2)