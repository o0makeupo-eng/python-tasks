#Matrix5 Даны M, N, число D и набор из M чисел. Первый столбец — набор; каждый следующий столбец равен предыдущему плюс D по строкам

m = int(input())
n = int(input())
numbers = [int(x) for x in input().split()]

for i in range(m):
    row = [numbers[i]] * n
    print(*row)
