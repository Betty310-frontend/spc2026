print('*')
print('**')
print('***')
print('****')
print('*****')

print('\n - 1 - ')
for i in range(1, 6): # 1부터 시작해서 6을 포함하지 않음. (1, 2, 3, 4, 5)
    print('*' * i)

print('\n - 2 - ')
print('='*30)
print('=' + '성적표'.center(25) + '=')
print('='*30)

num = 5

print('\n - 3 - ')
for i in range(1, 6):
    print(' ' * (num - i), end='')
    print('*' * i)

print('\n - 4 - ')
for i in range(1, 6):
    print(' ' * (num - i), end='')
    print('*' * (2*i - 1))