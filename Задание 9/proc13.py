# Proc13. Функция sort_dec3(a, b, c) возвращает три значения по убыванию. 
# Упорядочить два набора

def sort_dec3(a, b, c):
    sort_abc = sorted([a, b, c], reverse=True)
    return sort_abc[0], sort_abc[1], sort_abc[2] 

a1, b1, c1 = float(input()), float(input()), float(input())
a2, b2, c2 = float(input()), float(input()), float(input())

print(sort_dec3(a1, b1, c1))
print(sort_dec3(a2, b2, c2))