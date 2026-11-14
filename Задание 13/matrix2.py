#Matrix2 Сформировать матрицу M × N, у которой все элементы J-го столбца равны 5·J (J = 1, ..., N)

m = int(input())
n = int(input())

for i in range(m):
    row = [5 * (j + 1) for j in range(n)]
    print(*row)
