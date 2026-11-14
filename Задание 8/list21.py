# Дан список A из N чисел. Генератором с фильтром вывести 
# только положительные элементы и их количество

n = int(input())
a = []
k = 0

for i in range(n):
    a.append(int(input()))

pos = [x for x in a if x > 0]
count = len(pos)

print(pos)
print(count)