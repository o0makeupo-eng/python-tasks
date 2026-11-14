#String15 Дана строка. Подсчитать общее количество строчных латинских и русских букв в ней

s = input()
count = 0
for c in s:
    if c.islower():
        count += 1
print(count)
