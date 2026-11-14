# Proc15. Функция shift_left3(a, b, c) возвращает тройку после левого циклического сдвига: a на место c,
# c на место b, b на место a. Сдвинуть два набора

def shift_left3(a, b, c):
    return b, c, a

a1, b1, c1 = float(input()), float(input()), float(input())
a2, b2, c2 = float(input()), float(input()), float(input())


print(shift_left3(a1, b1, c1))
print(shift_left3(a2, b2, c2))