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
menu_last = 8
actions = 0
outcome = "прерывание"
enemies = ["зомби", "скелет", "паук", "летучая мышь"]
log = []

# --- Функции игры -----------------------------------
def hero_hit(strike_n):
    #Урон героя в удар номер strike_n.Возвращает пару (урон, крит): число урона и признак критического удара.
    if strike_n % 3 == 0:
        return crit_damage, True
    return damage, False


def fight(enemy, hero_health):
    #Бой с enemy до гибели одного из двоих. Возвращает (раунды, победа_героя, здоровье_героя).
    enemy_hp = 45.0
    rounds = []
    round_n = 0
    print(f"Вы спускаетесь по лестнице. Из темноты выступает {enemy}!")
    
    while enemy_hp > 0 and hero_health > 0:
        round_n += 1
        hit, crit = hero_hit(round_n)
        enemy_hp -= hit
        crit_mark = " — критический!" if crit else ""
        
        if enemy_hp <= 0:
            print(f"Раунд {round_n}: вы наносите {hit:.1f} урона{crit_mark}. Враг повержен.")
            rounds.append([round_n, hit, 0])
        else:
            blow = random.randint(2, 6)
            hero_health -= blow
            print(f"Раунд {round_n}: вы наносите {hit:.1f} урона{crit_mark}. Здоровье {enemy}: {enemy_hp:.1f}. {enemy} бьёт в ответ на {blow}.")
            rounds.append([round_n, hit, blow])
            
    return rounds, enemy_hp <= 0, hero_health


def print_leaderboard(log):
    #Печатает топ-3 раундов по урону героя и рекорд врага. Возвращает None.
    if not log:
        print("Вы ещё не вступали в бой.")
        return
    top = sorted(log, key=lambda r: r[1], reverse=True)[:3]
    print("Таблица лидеров (урон героя):")
    for i in range(len(top)):
        print(f"{i + 1}. Раунд {top[i][0]}: {top[i][1]:.1f}")
    
    worst = max(log, key=lambda r: r[2])
    print(f"Самый сильный удар врага: {worst[2]} (раунд {worst[0]}).")


def print_run_summary(log):
    #Печатает итог забега: суммарный и средний урон героя. Возвращает None.
    total = sum(r[1] for r in log)
    rounds_count = len(log)
    if rounds_count > 0:
        print(f"Урон: {total:.1f} за {rounds_count} раундов, средний {total / rounds_count:.1f}.")
    else:
        print("В этом забеге не было сражений.")


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
        print("8 - таблица лидеров")
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
                    hit_damage, crit = hero_hit(i)
                    if crit:
                        crit_count += 1
                        print(f"Удар {i}: {hit_damage:.1f} — критический!")
                    else:
                        print(f"Удар {i}: {hit_damage:.1f}")
                    total_damage += hit_damage

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
                    enemy = random.choice(enemies)
                    rounds, won, health = fight(enemy, health)
                    
                    for r in rounds:
                        log.append(r)
                        
                    if won:
                        enemies.remove(enemy)
                        print(f"{enemy.capitalize()} побеждён! В подземелье осталось врагов: {len(enemies)}.")
                    else:
                        print(f"{enemy.capitalize()} одолел вас.")
                        
                    print(f"Бой: {len(rounds)} раундов.")

            case "8":
                print_leaderboard(log)

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
    
    print_run_summary(log)
    print(frame)