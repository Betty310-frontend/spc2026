import os

print(os.getcwd())
print(os.listdir())

# 폴더 만들기와 삭제하기
# os.mkdir('test_dir')
# os.rmdir('test_dir')

os.chdir('C:/src')
cwd = os.getcwd()

print(os.listdir(cwd))
