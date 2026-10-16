# Err4. Прочитать целое число; в else вывести 100 / n,
# в finally вывести "Вычисление завершено".

try:
    a = int(input())
    result = 100 / a
except ValueError:
    print("Ошибка ввода")
except ZeroDivisionError:
    print("Делить на ноль нельзя")
else:
    print(result)
finally:
    print("Вычисление завершено")