# Proc12. Описать функцию sort_inc3(a, b, c), возвращающую три значения, упорядоченные по возрастанию.
# Упорядочить два данных набора из трёх чисел.

def sort_inc3(a, b, c):
    if a > b:
        a, b = b, a
    if b > c:
        b, c = c, b
    if a > b:
        a, b = b, a
    return a, b, c

a1, b1, c1 = float(input()), float(input()), float(input())
a2, b2, c2 = float(input()), float(input()), float(input())

print(sort_inc3(a1, b1, c1))
print(sort_inc3(a2, b2, c2))