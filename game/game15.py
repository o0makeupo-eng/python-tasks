# ================================================
# ИГРА «ПОДЗЕМЕЛЬЕ: ЛЕДЯНЫЕ ПЕЩЕРЫ»
# Автор: Валиуллина Эмилия 
# Дата: сентябрь 2026
# ================================================
import random
import json
import os
import dungeon

# Попытка подключить цветной вывод с откатом, если библиотеки нет
try:
    from colorama import Fore, Style, init
    init()
    COLOR = True
except ImportError:
    COLOR = False

title = "ЛЕДЯНЫЕ ПЕЩЕРЫ"
frame = "=" * 21
print(frame)
print("  " + title + "  ")
print(frame)
print()

# --- Начальные значения по умолчанию (для нового забега) ---
hero_name = ""
health = 100
stamina = 100
gold_total = 0
actions = 0
enemies = ["skeleton", "zombi", "spider", "bat"]
inventory = {}
hero_r, hero_c = 4, 2
visited = {(4, 2)}
found_loot = set()
log = []
ability_bonus = 0
damage = 10.0
crit_damage = 20.0
max_health = 100
max_stamina = 100

# --- Проверка сохранения и знакомство ----------------
loaded = None
if os.path.exists("save.json"):
    print("Найдено сохранение. Продолжить забег? (yes/no)")
    answer = input().strip().lower()
    if answer == "yes":
        with open("save.json", encoding="utf-8") as f:
            loaded = json.load(f)

if loaded is None:
    # Новый забег: спрашиваем имя и настраиваем героя
    print("Как зовут героя?")
    hero_name = input()

    print(f"Добро пожаловать, {hero_name}!")
    print("Ты входишь в подземелье. Здесь холодно и пахнет сыростью.")
    print()

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
            if "invalid literal" in str(e):
                print("Ой: одна из строк не число. Введите все четыре снова:")
            else:
                print(f"{e}. Введите все четыре снова:")

    print()

    base_attack = 10
    damage = base_attack + strength * 1.5
    crit_damage = damage * 2
    stamina = health // strength
    max_health = health
    max_stamina = stamina

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
else:
    # Продолжение забега: восстанавливаем состояние из сохранения
    hero_name = loaded["hero"]
    health = loaded["health"]
    stamina = loaded["stamina"]
    gold_total = loaded["gold"]
    actions = loaded["actions"]
    enemies = loaded["enemies"]
    hero_r, hero_c = loaded["position"]
    visited = {tuple(p) for p in loaded["visited"]}
    found_loot = set(loaded["loot"])
    # Восстанавливаем дополнительные поля, чтобы игра не сломалась
    inventory = loaded.get("inventory", {})
    log = loaded.get("log", [])
    ability_bonus = loaded.get("ability_bonus", 0)
    damage = loaded.get("damage", 10.0)
    crit_damage = loaded.get("crit_damage", 20.0)
    max_health = loaded.get("max_health", health)
    max_stamina = loaded.get("max_stamina", stamina)
    
    print(f"Забег продолжен: здоровье {health}, золото {gold_total}, врагов осталось {len(enemies)}.")

# --- Главный цикл игры ---------------------------
# --- Константы игры (не меняются при загрузке) ---
MAP = [
    ["#", "#", "#", "#", "#"],
    ["#", ".", ".", "#", "#"],
    ["#", ".", "#", ".", "#"],
    ["#", ".", ".", ".", "#"],
    ["#", "#", "S", ".", "#"],
]

LOOT = {(1, 1): "старая монета", (2, 3): "пыльное зелье", (3, 3): "самоцвет стража"}
DIRECTIONS = {"north": (-1, 0), "south": (1, 0), "west": (0, -1), "east": (0, 1)}

num_to_verb = {
    "1": "look", "2": "go", "3": "rest", "4": "listen",
    "5": "torch", "6": "train", "7": "descend", "8": "leaders",
    "9": "shop", "10": "backpack", "11": "drink", 
    "12": "map", "13": "scout", "14": "newgame", "0": "exit"
}

commands = [
    "look", "go", "rest", "listen", "torch", "train", "descend",
    "leaders", "shop", "backpack", "drink", "buy <предмет> [кол-во]", 
    "exit", "help", "map", "scout", "go <направление>", "newgame"
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
    "0 - выйти из подземелья (exit)",
    "14 - начать новый забег (newgame)"
]

# --- Управление циклом ---
running = True
menu_last = 14
outcome = "прерывание"

# --- Функции игры -----------------------------------
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
def write_save():
    """Собирает состояние забега и пишет его в save.json.
    Кортежи и множества превращает в списки: JSON их не знает.
    Возвращает None.
    """
    save = {}
    save["hero"] = hero_name
    save["health"] = health
    save["stamina"] = stamina
    save["gold"] = gold_total
    save["actions"] = actions
    save["enemies"] = enemies
    save["position"] = [hero_r, hero_c]
    save["visited"] = [list(p) for p in visited]
    save["loot"] = sorted(found_loot)
    
    # Добавляем недостающие поля для корректной загрузки
    save["inventory"] = inventory
    save["log"] = log
    save["ability_bonus"] = ability_bonus
    save["damage"] = damage
    save["crit_damage"] = crit_damage
    save["max_health"] = max_health
    save["max_stamina"] = max_stamina

    with open("save.json", "w", encoding="utf-8") as f:
        json.dump(save, f, ensure_ascii=False, indent=2)

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
                    hit_damage, crit = dungeon.hero_hit(i, damage, crit_damage)
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
                    
                    rounds, won, health, loot = dungeon.fight(enemy, health, ability_bonus, damage, crit_damage)
                    
                    for r in rounds:
                        log.append(r)
                        
                    if won:
                        gold_total += loot
                        enemies.remove(enemy)
                        win_msg = f"{enemy_ru} побеждён! В подземелье осталось врагов: {len(enemies)}. Трофеи: {loot} золота."
                        if COLOR:
                            print(Fore.YELLOW + win_msg + Style.RESET_ALL)
                        else:
                            print(win_msg)
                    else:
                        print(f"{enemy_ru} одолел вас.")
                        
                    print(f"Бой: {len(rounds)} раундов.")

            case "leaders":
                print_leaderboard(log)

            case "shop":
                print("Магазин:")
                for name, price in dungeon.prices.items():
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

                if item not in dungeon.prices:
                    print("Такого предмета в магазине нет.")
                    continue # Не тратит игровой круг

                gold_total, ok = dungeon.buy(dungeon.prices[item], gold_total, quantity=qty)
                if ok:
                    inventory[item] = inventory.get(item, 0) + qty
                    print(f"Куплено {qty} {item} за {dungeon.prices[item] * qty} золота. Осталось золота: {gold_total}.")
                else:
                    print(f"Недостаточно золота: нужно {dungeon.prices[item] * qty}, есть {gold_total}.")

            case "help":
                print("Команды: " + ", ".join(commands) + ".")
                print("Номера 0-14 работают как раньше.")

            case "newgame":
                if os.path.exists("save.json"):
                    os.remove("save.json")
                    print("Сохранение уничтожено. Следующий забег начнётся с чистого листа.")
                else:
                    print("Нет сохранения для уничтожения.")
                continue

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
                write_save()
                print("Прогресс сохранён.")
                outcome = "выход"
                running = False

            case _:
                print(f"Не понимаю команду: '{line.strip()}'. Введите 'help'.")
                continue # Не тратит игровой круг

        if health <= 0:
            print(f"{hero_name} падает без сил. Подземелье забирает ещё одного искателя.")
            if os.path.exists("save.json"):
                os.remove("save.json")
            outcome = "гибель"
            running = False

        if running:
            actions += 1 

        print()
        state = f"Здоровье: {health} Запас сил: {stamina} Врагов осталось: {len(enemies)} Золото: {gold_total}"
        if COLOR:
            print(Fore.GREEN + state + Style.RESET_ALL)
        else:
            print(state)

# --- Прощание ---
except KeyboardInterrupt:
    print("\nИгрок прервал сеанс (Ctrl+C).")
    write_save()

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