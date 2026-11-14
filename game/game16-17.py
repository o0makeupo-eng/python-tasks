# ================================================
# ИГРА «ПОДЗЕМЕЛЬЕ: ЛЕДЯНЫЕ ПЕЩЕРЫ»
# Автор: Валиуллина Эмилия 
# Дата: сентябрь 2026
# ================================================
import random
import json
import os
import dungeon

VERSION = "1.0"

try:
    from colorama import Fore, Style, init
    init()
    COLOR = True
except ImportError:
    COLOR = False

title = "ЛЕДЯНЫЕ ПЕЩЕРЫ"
frame = "=" * 21
print(frame)
print(f"  {title}  ")
print(f"  v{VERSION}")
print(frame)
print()

# --- Глобальное состояние мира (по умолчанию) ---------------------------
running = True
menu_last = 14
actions = 0
outcome = "прерывание"
enemies = ["skeleton", "zombi", "spider", "bat"]
inventory = {}
hero_r, hero_c = 4, 2
visited = {(4, 2)}
found_loot = set()
log = []
gold_total = 0
ability_bonus = 0
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
    
    hero = dungeon.Hero(hero_name, health, strength, agility, endurance)
    max_health = hero.health
    max_stamina = hero.stamina
    print(hero)
    print()
else:
    # ВОССТАНОВЛЕНИЕ ВСЕГО СОСТОЯНИЯ ИЗ СОХРАНЕНИЯ
    hero = dungeon.Hero.from_dict(loaded["hero"])
    hero_name = hero.name  # <-- ВОТ ЭТА СТРОКА (чтобы имя героя сохранилось для прощания)
    
    max_health = loaded.get("max_health", hero.health)
    max_stamina = loaded.get("max_stamina", hero.stamina)
    
    gold_total = loaded.get("gold", 0)
    actions = loaded.get("actions", 0)
    enemies = loaded.get("enemies", ["skeleton", "zombi", "spider", "bat"])
    inventory = loaded.get("inventory", {})
    hero_r, hero_c = loaded.get("position", [4, 2])
    visited = {tuple(p) for p in loaded.get("visited", [[4, 2]])}
    found_loot = set(loaded.get("loot", []))
    log = loaded.get("log", [])
    ability_bonus = loaded.get("ability_bonus", 0)
    
    print(f"Забег продолжен: здоровье {hero.health}, золото {gold_total}, врагов осталось {len(enemies)}.")

# --- Константы и меню -----------------------------------
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
    "1 - осмотреться (look)", "2 - идти вперёд (go)", "3 - отдохнуть (rest)",
    "4 - прислушаться (listen)", "5 - зажечь факел (torch)", "6 - тренировка (train)",
    "7 - спуститься глубже (descend)", "8 - таблица лидеров (leaders)",
    "9 - магазин (shop)", "10 - рюкзак (backpack)", "11 - выпить зелье (drink)",
    "12 - показать карту (map)", "13 - разведка (scout)",
    "0 - выйти из подземелья (exit)", "14 - начать новый забег (newgame)"
]

def parse_command(line):
    """Возвращает пару (verb, words): глагол и слова команды."""
    cmd = line.strip().lower()
    words = cmd.split()
    if not words:
        return "", []
    verb = words[0]
    if cmd in num_to_verb:
        verb = num_to_verb[cmd]
    return verb, words

def write_save():
    save = {
        "hero": hero.to_dict(),
        "hero_name": hero.name,
        "max_health": max_health,
        "max_stamina": max_stamina,
        "gold": gold_total,
        "actions": actions,
        "enemies": enemies,
        "position": [hero_r, hero_c],
        "visited": [list(p) for p in visited],
        "loot": sorted(found_loot),
        "inventory": inventory,
        "log": log,
        "ability_bonus": ability_bonus
    }

    with open("save.json", "w", encoding="utf-8") as f:
        json.dump(save, f, ensure_ascii=False, indent=2)

def print_run_summary(log):
    """Печатает итог забега: суммарный и средний урон героя."""
    total = sum(r[1] for r in log)
    rounds_count = len(log)
    if rounds_count > 0:
        print(f"Урон: {total:.1f} за {rounds_count} раундов, средний {total / rounds_count:.1f}.")
    else:
        print("В этом забеге не было сражений.")

try:
    while running:
        print("\n".join(MENU))
        print()

        line = input()
        verb, words = parse_command(line)
        
        while verb == "":
            print("Пустая команда. Введите команду или номер.")
            line = input()
            verb, words = parse_command(line)

        match verb:
            case "look":
                print("Вы осмотрелись. Комната пуста, только пыль на полу.")

            case "go":
                if len(words) > 1 and words[1] in DIRECTIONS:
                    dr, dc = DIRECTIONS[words[1]]
                    nr, nc = hero_r + dr, hero_c + dc
                    if 0 <= nr < len(MAP) and 0 <= nc < len(MAP[nr]) and MAP[nr][nc] != "#":
                        hero_r, hero_c = nr, nc
                        visited.add((hero_r, hero_c))
                        if (hero_r, hero_c) in LOOT:
                            item = LOOT[(hero_r, hero_c)]
                            if item not in found_loot:
                                found_loot.add(item)
                                print(f"Вы нашли {item}! Уникальных предметов: {len(found_loot)}.")
                        print(f"Вы шагаете на {words[1]}. Комната ({hero_r}, {hero_c}).")
                    else:
                        print(f"Нельзя идти на {words[1]}: стена или край карты.")
                else:
                    exhausted = hero.spend_stamina(2)
                    if exhausted:
                        print("Сил больше нет — вы идёте на одном упорстве.")
                    else:
                        print("Вы осторожно идёте вперёд. Пол скрипит под ногами.")

            case "rest":
                hero.stamina += 5 
                print("Вы решили передохнуть и присели у ближайшего камня.")
                print(f"Запас силы: {hero.stamina:.1f}")

            case "listen":
                print("Вы решили прислушаться, но ничего не услышали.")

            case "torch":
                hero.health -= 2 
                print("Вы решили зажечь факел. В процессе вы пару раз поранились.")
                print(f"Здоровье: {hero.health}")

            case "train":
                strikes = 5
                total_damage = 0
                crit_count = 0
                print("Вы подходите к тренировочному чучелу.")
                print("Оно стоит здесь с тех пор, как сюда приходил последний искатель приключений.")
                print()
                print(f"Наносите {strikes} ударов.")

                for i in range(1, strikes + 1):
                    hit_damage, crit = hero.strike(i)
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
                hero.spend_stamina(4)
                print(f"Тренировка отняла силы: -4")

            case "descend":
                if not enemies:
                    print("Вы хотите спуститься глубже, но подземелье уже пусто.")
                else:
                    enemy_name = random.choice(enemies)
                    foe = dungeon.Enemy(enemy_name, dungeon.enemy_stats[enemy_name])
                    rounds, won, loot = dungeon.fight(foe, hero, ability_bonus)
                    
                    for r in rounds:
                        log.append(r)
                        
                    if won:
                        gold_total += loot
                        enemies.remove(enemy_name)
                        enemy_names_ru = {"skeleton": "Скелет", "zombi": "Зомби", "spider": "Паук", "bat": "Летучая мышь"}
                        enemy_ru = enemy_names_ru.get(enemy_name, enemy_name)
                        win_msg = f"{enemy_ru} побеждён! В подземелье осталось врагов: {len(enemies)}. Трофеи: {loot} золота."
                        if COLOR:
                            print(Fore.YELLOW + win_msg + Style.RESET_ALL)
                        else:
                            print(win_msg)
                    else:
                        enemy_names_ru = {"skeleton": "Скелет", "zombi": "Зомби", "spider": "Паук", "bat": "Летучая мышь"}
                        enemy_ru = enemy_names_ru.get(enemy_name, enemy_name)
                        print(f"{enemy_ru} одолел вас.")
                    print(f"Бой: {len(rounds)} раундов.")

            case "leaders":
                dungeon.print_leaderboard(log)

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
                item = " ".join(words[1:]) or "potion"
                if inventory.get(item, 0) == 0:
                    print(f"В рюкзаке нет {item}.")
                else:
                    hero.heal(10, max_health)
                    inventory[item] -= 1
                    if inventory[item] == 0:
                        del inventory[item]
                    print(f"Вы выпили {item}. Здоровье: {hero.health}. Осталось {item}: {inventory.get(item, 0)}.")

            case "buy":
                if len(words) > 1 and words[-1].isdigit():
                    qty = int(words[-1])
                    item = " ".join(words[1:-1])
                else:
                    qty = 1
                    item = " ".join(words[1:])

                if item == "":
                    print("Купить что? Введите: buy <предмет>.")
                    continue
                if item not in dungeon.prices:
                    print("Такого предмета в магазине нет.")
                    continue

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
                print(f"Разведка: доступно {dungeon.scout(hero_r, hero_c, seen, MAP, DIRECTIONS)} комнат.")

            case "exit":
                print("Вы поднимаетесь обратно к свету. Подземелье остаётся позади.")
                write_save()
                print("Прогресс сохранён.")
                outcome = "выход"
                running = False

            case _:
                print(f"Не понимаю команду: '{line.strip()}'. Введите 'help'.")
                continue

        if hero.health <= 0:
            print(f"{hero.name} падает без сил. Подземелье забирает ещё одного искателя.")
            if os.path.exists("save.json"):
                os.remove("save.json")
            outcome = "гибель"
            running = False

        if running:
            actions += 1 

        print()
        state = f"Здоровье: {hero.health} Запас сил: {hero.stamina} Врагов осталось: {len(enemies)} Золото: {gold_total}"
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