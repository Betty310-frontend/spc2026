def numbers():
    for i in range(1_000_000):
        yield i

for num in numbers():
    print(num)
    if num >= 5:
        break