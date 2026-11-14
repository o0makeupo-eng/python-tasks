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
max_health = health
max_stamina = stamina

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
menu_last = 11
actions = 0
outcome = "прерывание"
enemies = ["скелет", "zombi", "spider", "bat"]

prices = {"potion": 10, "torch_oil": 15, "war_elixir": 40}
inventory = {}

enemy_stats = {
    "skeleton": {"hp": 45, "damage": 6, "loot": 25},
    "zombi": {"hp": 30, "damage": 4, "loot": 15},
    "spider": {"hp": 20, "damage": 3, "loot": 10},
    "bat": {"hp": 12, "damage": 2, "loot": 5},
}
log = []
gold_total = 0
ability_bonus = 0

# --- Функции игры -----------------------------------
def hero_hit(strike_n):
    """Урон героя в удар номер strike_n.
    Возвращает пару (урон, крит): число урона и признак критического удара.
    Читает глобальные damage и crit_damage, не меняет ничего.
    """
    if strike_n % 3 == 0:
        return crit_damage, True
    return damage, False


def fight(enemy, hero_health, bonus=0):
    """Бой с enemy до гибели одного из двоих.
    Карточка врага берётся из enemy_stats по имени: нужны ключи hp, damage, loot.
    bonus — надбавка к урону героя, по умолчанию 0.
    Возвращает (раунды, победа_героя, здоровье_героя, трофеи).
    """
    stats = enemy_stats[enemy]
    enemy_hp = float(stats["hp"])
    rounds = []
    round_n = 0
    
    # Переводим имя врага для красивого вывода
    enemy_names_ru = {"skeleton": "скелет", "zombi": "зомби", "spider": "паук", "bat": "летучая мышь"}
    enemy_ru = enemy_names_ru.get(enemy, enemy)
    
    print(f"Вы спускаетесь по лестнице. Из темноты выступает {enemy_ru}!")
    
    while enemy_hp > 0 and hero_health > 0:
        round_n += 1
        hit, crit = hero_hit(round_n)
        hit = hit + bonus
        enemy_hp -= hit
        crit_mark = " — критический!" if crit else ""
        
        if enemy_hp <= 0:
            print(f"Раунд {round_n}: вы наносите {hit:.1f} урона{crit_mark}. Враг повержен.")
            rounds.append([round_n, hit, 0])
        else:
            blow = stats["damage"]
            hero_health -= blow
            print(f"Раунд {round_n}: вы наносите {hit:.1f} урона{crit_mark}. Здоровье {enemy_ru}: {enemy_hp:.1f}. {enemy_ru} бьёт в ответ на {blow}.")
            rounds.append([round_n, hit, blow])
            
    won = enemy_hp <= 0
    loot = stats["loot"] if won else 0
    return rounds, won, hero_health, loot


def buy(price, gold, quantity=1):
    """Покупает quantity штук товара ценой price за золото gold.
    quantity по умолчанию 1. Возвращает (gold_left, ok): остаток золота и признак успешной покупки.
    Ничего не печатает.
    """
    cost = price * quantity
    if gold >= cost:
        return gold - cost, True
    return gold, False


def print_leaderboard(log):
    """Печатает топ-3 раундов по урону героя и рекорд врага.
    Возвращает None: контракт функции — печать, а не данные.
    """
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
    """Печатает итог забега: суммарный и средний урон героя.
    Возвращает None. Безопасна на пустом журнале.
    """
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
        print("9 - магазин")
        print("10 - рюкзак")
        print("11 - выпить зелье")
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
                    enemy_names_ru = {"skeleton": "Скелет", "ghoul": "Гуль", "spider": "Паук", "bat": "Летучая мышь"}
                    enemy_ru = enemy_names_ru.get(enemy, enemy)
                    
                    rounds, won, health, loot = fight(enemy, health, bonus=ability_bonus)
                    
                    for r in rounds:
                        log.append(r)
                        
                    if won:
                        gold_total += loot
                        enemies.remove(enemy)
                        print(f"{enemy_ru} побеждён! В подземелье осталось врагов: {len(enemies)}. Трофеи: {loot} золота.")
                    else:
                        print(f"{enemy_ru} одолел вас.")
                        
                    print(f"Бой: {len(rounds)} раундов.")

            case "8":
                print_leaderboard(log)

            case "9":
                print("Магазин:")
                for name, price in prices.items():
                    print(f"{name}: {price} золота")
                print("Название предмета (пустая строка — не покупать):")
                name = input()
                
                if name != "":
                    if name in prices:
                        price = prices[name]
                        print("Количество (Enter для одного):")
                        qty_line = input()
                        
                        if qty_line == "":
                            qty = 1
                            gold_total, ok = buy(price, gold_total)
                        else:
                            qty = int(qty_line)
                            gold_total, ok = buy(price, gold_total, quantity=qty)
                        
                        if ok:
                            inventory[name] = inventory.get(name, 0) + qty
                            print(f"Куплено {qty} {name} за {price * qty} золота. Осталось золота: {gold_total}.")
                        else:
                            print(f"Недостаточно золота: нужно {price * qty}, есть {gold_total}.")
                    else:
                        print("Такого предмета в магазине нет.")

            case "10":
                if not inventory:
                    print("Рюкзак пуст.")
                else:
                    print("Рюкзак:")
                    for name, qty in inventory.items():
                        print(f"{name}: {qty} шт.")

            case "11":
                if inventory.get("potion", 0) == 0:
                    print("В рюкзаке нет зелий.")
                else:
                    health = min(health + 10, max_health)
                    inventory["potion"] -= 1
                    if inventory["potion"] == 0:
                        del inventory["potion"]
                    print(f"Вы выпили зелье. Здоровье: {health}. Осталось зелий: {inventory.get('potion', 0)}.")

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
        print(f"Здоровье: {health} Запас сил: {stamina} Врагов осталось: {len(enemies)} Золото: {gold_total}")

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

    if inventory:
        print("Оставлено в рюкзаке:")
        for name, qty in inventory.items():
            print(f"{name}: {qty} шт.")
    else:
        print("Оставлено в рюкзаке: ничего.")
    
    print_run_summary(log)
    print(frame)