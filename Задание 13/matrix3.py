#Matrix3 Даны M, N и набор из M чисел. Сформировать матрицу, у которой в каждом столбце
#содержатся все числа набора в том же порядке
m = int(input())
n = int(input())
numbers = [int(x) for x in input().split()]
a = []
for i in range(m):
    row = numbers[i::m] if i < len(numbers) else [0] * n
    a.append(row)
for row in a:
    print(row)