#String14 Дана строка. Подсчитать количество прописных латинских букв в ней

s = input()
count = 0
for c in s:
    if c.isupper() and c.isalpha():
        count += 1
print(count)