# ================================================
# ИГРА «ПОДЗЕМЕЛЬЕ: ЛЕДЯНЫЕ ПЕЩЕРЫ»
# Автор: Валиуллина Эмилия 
# Дата: сентябрь 2026

# Пункт 4 — «прислушаться»: герой замирает
# и слушает, что происходит в темноте. Пока
# пункт только выводится в меню — обрабатывать
# его будем на третьем занятии.
# ================================================

import random

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

# --- Настройка героя ----------------------------------
print("Настройка героя.")
print("Здоровье, сила, ловкость, выносливость — по одному числу в строке:")

while True:
    try:
        health = int(input())
        strength = int(input())
        agility = int(input())
        endurance = int(input())
        
        if health <= 0:
            raise ValueError(f"Здоровье должно быть положительным, а введено {health}")
        if strength < 0 or agility < 0 or endurance < 0:
            raise ValueError("Характеристики не могут быть отрицательными")
            
        break 
    except ValueError as e:
        # Проверяем, была ли это ошибка формата (буквы) или наше правило (raise)
        if "invalid literal" in str(e):
            print("Ой: одна из строк не число. Введите все четыре снова:")
        else:
            print(f"{e}. Введите все четыре снова:")

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


# --- Главный цикл игры ---------------------------
running = True
menu_last = 7
actions = 0
outcome = "прерывание"
enemies = ["зомби", "скелет", "паук", "летучая мышь"]
log = []

try:
    while running:
        print("Что делаешь?")
        print("1 - осмотреться")
        print("2 - идти вперёд")
        print("3 - отдохнуть")
        print("4 - прислушаться")
        print("5 - зажечь факел")
        print("6 - тренировка")
        print("7 - спуститься глубже")
        print("0 - выйти из подземелья")
        print()

        while True:
            choice = input()
            try:
                menu_number = int(choice)
            except ValueError:
                print("Это не число. Введи номер пункта из меню.")
                continue
            
            if 0 <= menu_number <= menu_last:
                break
                
            print("Такого пункта нет. Введи номер пункта из меню.")

        match choice:
            case "1":
                print("Вы осмотрелись. Комната пуста, только пыль на полу.")

            case "2":
                cost = 2
                if stamina >= cost:
                    stamina -= cost
                    print("Вы осторожно идёте вперёд. Пол скрипит под ногами.")
                else:
                    health -= cost - stamina
                    stamina = 0
                    print("Сил больше нет — вы идёте на одном упорстве.")

            case "3":
                stamina = stamina + 5 
                print("Вы решили передохнуть и присели у ближайшего камня.")
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

                stamina_cost = 4
                stamina -= stamina_cost
                print(f"Тренировка отняла силы: -{stamina_cost}")

            case "7":
                if not enemies:
                    print("Вы хотите спуститься глубже, но подземелье уже пусто.")
                else:
                    print("Вы спускаетесь по лестнице. Из темноты выступает враг!")
                    enemy = random.choice(enemies)
                    enemy_hp = 45
                    round_n = 0
                    hero_strikes = 0
                    print(f"Это {enemy}!")

                    while enemy_hp > 0 and health > 0:
                        round_n += 1
                        hero_strikes += 1

                        if hero_strikes % 3 == 0:
                            hit_damage = crit_damage
                            crit_mark = " — критический!"
                        else:
                            hit_damage = damage
                            crit_mark = ""

                        enemy_hp -= hit_damage
                        log_entry = f"раунд {round_n}: герой -{hit_damage:.1f}, {enemy} "

                        if enemy_hp <= 0:
                            print(f"Раунд {round_n}: вы наносите {hit_damage:.1f} урона{crit_mark}. Враг повержен.")
                            log_entry += f"повержен"
                            log.append(log_entry)
                            break

                        enemy_damage = random.randint(2, 6)
                        health -= enemy_damage
                        print(f"Раунд {round_n}: вы наносите {hit_damage:.1f} урона{crit_mark}. Здоровье {enemy}: {enemy_hp:.1f}. {enemy} бьёт в ответ на {enemy_damage}.")
                        log_entry += f"-{enemy_damage}"
                        log.append(log_entry)

                    if enemy_hp <= 0:
                        enemies.remove(enemy)
                        print(f"{enemy} побеждён! В подземелье осталось врагов: {len(enemies)}.")
                    else:
                        print(f"{enemy} одолел вас.")

                    print(f"Бой: {round_n} раундов.")
                    print(f"Последняя запись журнала: {log[-1]}")

            case "0":
                print("Вы поднимаетесь обратно к свету. Подземелье остаётся позади.")
                outcome = "выход"
                running = False

            case _:
                print("Такого действия нет.")

        if health <= 0:
            outcome = "гибель"
            print(f"{hero_name} падает без сил. Подземелье забирает ещё одного искателя.")
            running = False

        if running:
            actions += 1 

        print()
        print(f"Здоровье: {health} Запас сил: {stamina} Врагов осталось: {len(enemies)}")

# --- Прощание ---
except KeyboardInterrupt:
    print("\nИгрок прервал сеанс (Ctrl+C).")

finally:
    print(frame)
    if outcome == "гибель":
        print(f"Ты не дошёл, {hero_name}. Действий совершено: {actions}.")
    elif outcome == "выход":
        print(f"Забег окончен, {hero_name}. Действий совершено: {actions}.")
    else:
        print(f"Сеанс прерван, {hero_name}. Действий совершено: {actions}.")
    print(frame)