# ================================================
# ИГРА «ПОДЗЕМЕЛЬЕ: ЛЕДЯНЫЕ ПЕЩЕРЫ»
# Автор: Валиуллина Эмилия
# Дата: сентябрь 2026

# Пункт 4 — «прислушаться»: герой замирает
# и слушает, что происходит в темноте. Пока
# пункт только выводится в меню — обрабатывать
# его будем на третьем занятии.
# ================================================

title = "ЛЕДЯНЫЕ ПЕЩЕРЫ"
frame = "=" * 21
print(frame)
print("  " + title + "  ")
print(frame)
print()

print("Как зовут героя?")
hero_name = input()

print(f"Добро пожаловать, {hero_name}!")
print("Ты входишь в подземелье. Здесь холодно и пахнет сыростью.")
print()

print("Настройка героя.")
print("Здоровье, сила, ловкость, выносливость — по одному числу в строке:")
health = int(input())
strength = int(input())
agility = int(input())
endurance = int(input())
print()

# --- Расчёт урона ----------------------------------
base_attack = 10
damage = base_attack + strength * 1.5
crit_damage = damage * 2
stamina = health // strength


# --- Формуляр героя --------------------------------
print("Характеристики героя:")
print(f"Здоровье: {health}")
print(f"Сила: {strength}")
print(f"Ловкость: {agility}")
print(f"Выносливость: {endurance}")
print()
print(f"Урон героя: {damage:.1f}")
print(f"Критический урон: {crit_damage:.1f}")
print(f"Запас силы: {stamina:.1f}")
print()

# --- Меню действий ---------------------------------
print("Что делаешь?")
print("1 - осмотреться")
print("2 - идти вперёд")
print("3 - отдохнуть")
print("4 - прислушаться")
print("5 - зажечь факел")
print("6 - тренировка")

print()

# --- Выбор героя -----------------------------------
choice = input()

match choice:
    case "1":
        print("Вы осмотрелись. Комната пуста, только пыль на полу.")

    case "2":
        stamina = stamina - 2
        print("Вы осторожно идёте вперёд. Пол скрипит под ногами.")
        print(f"Запас силы: {stamina:.1f}")

    case "3":
        stamina = stamina + 5 
        print("Вы решили передохнуть и присели у ближайщего камня.")
        print(f"Запас силы: {stamina:.1f}")

    case "4": 
        print("Вы решили прислушиться, но ничего не услышали.")

    case "5":
        health = health - 2 
        print("Вы решили зажечь факел. В процессе вы пару раз поранились.")
        print(f"Здоровье: {health}")

    case "6": 
        strikes = 5
        total_damage = 0
        crit_count = 0
        print("Вы подходите к тренировочному чучелу.")
        print("Оно стоит здесь с тех пор, как сюда приходил последний искатель приключений.")
        print()

        print(f"Наносите {strikes} ударов.")

        for i in range(1, strikes + 1):
            if i % 3 == 0:
                hit_damage = crit_damage
                mark = " — критический!"
            else:
                hit_damage = damage
                mark = ""

            print(f"Удар {i}: {hit_damage:.1f} урона{mark}")

            total_damage += hit_damage
            if i % 3 == 0:
                crit_count += 1

        print()
        print(f"Итог: {strikes} ударов, критических ударов: {crit_count}")
        print(f"Общий урон: {total_damage:.1f}")
        print(f"Средний урон: {total_damage / strikes:.1f}")

        print()
        print(f"Здоровье: {health}")
        print(f"Запас сил: {stamina:.1f}")
        
    case _:
        print("Такого действия нет.")
print()


# --- Прощание ---
print(frame)
print(f"Удачи, {hero_name}!")
print(frame)
