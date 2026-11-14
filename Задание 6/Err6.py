#Та же задача, что Err5, но с двумя ветками: нечисловой индекс — «Ошибка ввода», индекс вне границ — «Нет такого символа».

stroka = input()
index = int(input())

try: 
    print(stroka[index])
except ValueError:
    print("Ошибка ввода")
except IndexError:
    print("Нет такого символа")
