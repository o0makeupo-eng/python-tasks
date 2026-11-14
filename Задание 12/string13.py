#String13. Дана строка. Подсчитать количество содержащихся в ней цифр.
s = input()
count = 0
for c in s:
    if "0" <= c <= "9":
        count += 1
print(count)