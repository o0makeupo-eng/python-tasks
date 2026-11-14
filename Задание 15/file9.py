#File9 Даны имена двух файлов: один существует и непуст (не обязательно первый), другой
#отсутствует. Создать отсутствующий и записать в него конечный и начальный элементы существующего

import os

f1 = input()
f2 = input()

if not os.path.isfile(f1):
    f1, f2 = f2, f1

with open(f1, 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

first = lines[0]
last = lines[-1]

with open(f2, 'w') as f:
    f.write(last + '\n')
    f.write(first + '\n')
