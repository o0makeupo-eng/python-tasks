#Прочитать два числа и вывести их частное. Обе возможные ошибки 
#обработать одним кортежем в except с сообщением «Посчитать не 
#удалось»; при успехе в else вывести частное с двумя знаками
#после точки.
try:
    a, b = int(input()), int(input())
    result = a / b
except (ZeroDivisionError, ValueError):
    print("Почситать не удалось")
else:
    print(round(result, 2))