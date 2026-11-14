#Дан список A из N чисел. Вывести элементы на нечётных позициях (1, 3, 5... при счёте позиций
#с 1) и их сумму

n = int(input())
a = []
for i in range(n):
    a.append(int(input()))
summa = 0
list = []
for i in range(1, len(a), 2):
    list.append(a[i])
    summa += a[i]
print(f"Итоговый список: {list}")
print(f"Сумма: {summa}")