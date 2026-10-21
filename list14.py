#Дан список A из N чисел и число D. Вывести число вхождений D (count) и индекс первого
#вхождения (или -1, если D нет)

n = int(input())
a = []
for i in range(n):
    a.append(int(input()))

d = int(input("Введите d "))

print(f"Число вхождение числа d: {a.count(d)}")
print(f"Индекс первого вхождения: {a[0]}")