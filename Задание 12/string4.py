#String4 Дано N (1 ≤ N ≤ 26). Вывести строку из N первых заглавных латинских букв
N = int(input())
for i in range(N):
    print(chr(ord("A") + i), end="")