#String5 Дано N (1 ≤ N ≤ 26). Вывести строку из N последних строчных латинских букв в обратном порядке, начиная с «z»

N = int(input())
for i in range(N):
    print(chr(ord("z") - i), end="")