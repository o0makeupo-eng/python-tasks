# Proc14. Функция shift_right3(a, b, c) возвращает тройку после правого циклического сдвига: 
# a переходит на место b, b — на место c, c — на место a. Сдвинуть два набора

def shift_right3(a, b, c):
    return c, a, b
    
a1, b1, c1 = float(input()), float(input()), float(input())
a2, b2, c2 = float(input()), float(input()), float(input())

print(shift_right3(a1, b1, c1))
print(shift_right3(a2, b2, c2))