#String9 Даны чётное N (> 0) и символы C1, C2. Вывести строку длины N из чередующихся C1 и C2, начиная с C1

N = int(input())
C1 = input()
C2 = input()
for i in range(N):
    if i % 2 == 0:
        print(C1, end="")
    else:
        print(C2, end="")