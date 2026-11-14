#File8 Даны имена двух файлов: первый существует и непуст, второй отсутствует. Создать второй и
#записать в него первый и последний элементы первого

file1 = input()
file2 = input()

with open(file1, 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

first = lines[0]
last = lines[-1]

with open(file2, 'w') as f:
    f.write(first + '\n')
    f.write(last + '\n')
