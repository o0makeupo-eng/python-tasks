#File3 Дано имя файла и вещественные A и D. Записать в файл 10 первых членов прогрессии A, A+D, A+2·D, ...

filename = input()
A = float(input())
D = float(input())

with open(filename, 'w') as f:
    for i in range(10):
        f.write(str(A + i * D) + '\n')
