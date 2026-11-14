# ================================================
# ИГРА «ПОДЗЕМЕЛЬЕ: ЛЕДЯНЫЕ ПЕЩЕРЫ»
# Автор: Валиуллина Эмилия 
# Дата: сентябрь 2026
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
menu_last = 13
actions = 0
outcome = "прерывание"
enemies = ["skeleton", "zombi", "spider", "bat"]

prices = {"potion": 10, "torch_oil": 15, "war_elixir": 40}
inventory = {}

# --- Данные карты и перемещения ---------------------
MAP = [
    ["#", "#", "#", "#", "#"],
    ["#", ".", ".", "#", "#"],
    ["#", ".", "#", ".", "#"],
    ["#", ".", ".", ".", "#"],
    ["#", "#", "S", ".", "#"],
]
hero_r, hero_c = 4, 2
visited = {(4, 2)}

LOOT = {(1, 1): "старая монета", (2, 3): "пыльное зелье", (3, 3): "самоцвет стража"}
found_loot = set()

DIRECTIONS = {"north": (-1, 0), "south": (1, 0), "west": (0, -1), "east": (0, 1)}

enemy_stats = {
    "skeleton": {"hp": 45, "damage": 6, "loot": 25},
    "zombi": {"hp": 30, "damage": 4, "loot": 15},
    "spider": {"hp": 20, "damage": 3, "loot": 10},
    "bat": {"hp": 12, "damage": 2, "loot": 5},
}
log = []
gold_total = 0
ability_bonus = 0

# Словарь перевода номеров в глаголы
num_to_verb = {
    "1": "look", "2": "go", "3": "rest", "4": "listen",
    "5": "torch", "6": "train", "7": "descend", "8": "leaders",
    "9": "shop", "10": "backpack", "11": "drink", 
    "12": "map", "13": "scout", "0": "exit"
}

# Списки для вывода через join
commands = [
    "look", "go", "rest", "listen", "torch", "train", "descend",
    "leaders", "shop", "backpack", "drink", "buy <предмет> [кол-во]", 
    "exit", "help", "map", "scout", "go <направление>"
]

MENU = [
    "Что делаешь? (номер или команда; help для справки)",
    "1 - осмотреться (look)",
    "2 - идти вперёд (go)",
    "3 - отдохнуть (rest)",
    "4 - прислушаться (listen)",
    "5 - зажечь факел (torch)",
    "6 - тренировка (train)",
    "7 - спуститься глубже (descend)",
    "8 - таблица лидеров (leaders)",
    "9 - магазин (shop)",
    "10 - рюкзак (backpack)",
    "11 - выпить зелье (drink)",
    "12 - показать карту (map)",
    "13 - разведка (scout)",
    "0 - выйти из подземелья (exit)"
]
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
    enemy_names_ru = {"skeleton": "Скелет", "zombi": "Зомби", "spider": "Паук", "bat": "Летучая мышь"}
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

def scout(r, c, seen):
    """Рекурсивный подсчёт доступных комнат.
    seen — множество уже посещённых в этом обходе клеток.
    """
    if (r, c) in seen or MAP[r][c] == "#":
        return 0
    seen.add((r, c))
    total = 1
    for dr, dc in DIRECTIONS.values():
        total += scout(r + dr, c + dc, seen)
    return total

try:
    while running:
        print("\n".join(MENU))
        print()

               # Чтение и нормализация команды
        line = input()
        cmd = line.strip().lower()
        
        while cmd == "":
            print("Пустая команда. Введите команду или номер.")
            line = input()
            cmd = line.strip().lower()

        words = cmd.split()
        verb = words[0]

        # Если ввели номер, превращаем его в глагол
        if cmd in num_to_verb:
            verb = num_to_verb[cmd]

        match verb:
            case "look":
                print("Вы осмотрелись. Комната пуста, только пыль на полу.")

            case "go":
                if len(words) > 1 and words[1] in DIRECTIONS:
                    dr, dc = DIRECTIONS[words[1]]
                    nr, nc = hero_r + dr, hero_c + dc
                    
                    # Проверка границ и стены (короткое замыкание and предотвращает IndexError)
                    if 0 <= nr < len(MAP) and 0 <= nc < len(MAP[nr]) and MAP[nr][nc] != "#":
                        hero_r, hero_c = nr, nc
                        visited.add((hero_r, hero_c))
                        
                        # Подбор лута (ПЕРЕД сообщением о шаге, как в образце)
                        if (hero_r, hero_c) in LOOT:
                            item = LOOT[(hero_r, hero_c)]
                            if item not in found_loot:
                                found_loot.add(item)
                                print(f"Вы нашли {item}! Уникальных предметов: {len(found_loot)}.")
                        
                        print(f"Вы шагаете на {words[1]}. Комната ({hero_r}, {hero_c}).")
                    else:
                        print(f"Нельзя идти на {words[1]}: стена или край карты.")
                else:
                    # Старая логика движения по коридору со стаминой
                    cost = 2
                    if stamina >= cost:
                        stamina -= cost
                        print("Вы осторожно идёте вперёд. Пол скрипит под ногами.")
                    else:
                        health -= cost - stamina
                        stamina = 0
                        print("Сил больше нет — вы идёте на одном упорстве.")
            case "rest":
                stamina = stamina + 5 
                print("Вы решили передохнуть и присели у ближайшего камня.")
                print(f"Запас силы: {stamina:.1f}")

            case "listen":
                print("Вы решили прислушаться, но ничего не услышали.")

            case "torch":
                health = health - 2 
                print("Вы решили зажечь факел. В процессе вы пару раз поранились.")
                print(f"Здоровье: {health}")

            case "train":
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

            case "descend":
                if not enemies:
                    print("Вы хотите спуститься глубже, но подземелье уже пусто.")
                else:
                    enemy = random.choice(enemies)
                    enemy_names_ru = {"skeleton": "Скелет", "zombi": "Зомби", "spider": "Паук", "bat": "Летучая мышь"}
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

            case "leaders":
                print_leaderboard(log)

            case "shop":
                print("Магазин:")
                for name, price in prices.items():
                    print(f"{name}: {price} золота")

            case "backpack":
                if not inventory:
                    print("Рюкзак пуст.")
                else:
                    print("Рюкзак:")
                    for name, qty in inventory.items():
                        print(f"{name}: {qty} шт.")

            case "drink":
                # Если дополнений нет, по умолчанию берём "potion"
                item = " ".join(words[1:]) or "potion"
                if inventory.get(item, 0) == 0:
                    print(f"В рюкзаке нет {item}.")
                else:
                    health = min(health + 10, max_health)
                    inventory[item] -= 1
                    if inventory[item] == 0:
                        del inventory[item]
                    print(f"Вы выпили {item}. Здоровье: {health}. Осталось {item}: {inventory.get(item, 0)}.")

            case "buy":
                # Разбор аргументов: последнее слово может быть числом
                if len(words) > 1 and words[-1].isdigit():
                    qty = int(words[-1])
                    item = " ".join(words[1:-1])
                else:
                    qty = 1
                    item = " ".join(words[1:])

                if item == "":
                    print("Купить что? Введите: buy <предмет>.")
                    continue # Не тратит игровой круг

                if item not in prices:
                    print("Такого предмета в магазине нет.")
                    continue # Не тратит игровой круг

                gold_total, ok = buy(prices[item], gold_total, quantity=qty)
                if ok:
                    inventory[item] = inventory.get(item, 0) + qty
                    print(f"Куплено {qty} {item} за {prices[item] * qty} золота. Осталось золота: {gold_total}.")
                else:
                    print(f"Недостаточно золота: нужно {prices[item] * qty}, есть {gold_total}.")

            case "help":
                print("Команды: " + ", ".join(commands) + ".")
                print("Номера 0-11 работают как раньше.")

            case "map":
                print("Карта:")
                for i in range(len(MAP)):
                    cells = []
                    for j in range(len(MAP[i])):
                        cell = "@" if (i, j) == (hero_r, hero_c) else MAP[i][j]
                        cells.append(cell)
                    print(" ".join(cells))

            case "scout":
                seen = set()
                print(f"Разведка: доступно {scout(hero_r, hero_c, seen)} комнат.")

            case "exit":
                print("Вы поднимаетесь обратно к свету. Подземелье остаётся позади.")
                outcome = "выход"
                running = False

            case _:
                print(f"Не понимаю команду: '{line.strip()}'. Введите 'help'.")
                continue # Не тратит игровой круг

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