#Matrix6 Даны M, N, число Q и набор из N чисел. Первая строка — набор; каждая следующая строка
#равна предыдущей, умноженной на Q по столбцам

m = int(input())
n = int(input())
q = int(input())
numbers = [int(x) for x in input().split()]

for i in range(m):
    row = [x * q ** i for x in numbers]
    print(*row)
