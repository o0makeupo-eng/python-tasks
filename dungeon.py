"""Модуль правил подземелья: бой, покупки, характеристики врагов."""
import random

prices = {"potion": 10, "torch_oil": 15, "war_elixir": 40}

enemy_stats = {
    "skeleton": {"hp": 45, "damage": 6, "loot": 25},
    "zombi": {"hp": 30, "damage": 4, "loot": 15},
    "spider": {"hp": 20, "damage": 3, "loot": 10},
    "bat": {"hp": 12, "damage": 2, "loot": 5},
}

def hero_hit(strike_n, damage, crit_damage):
    """Урон героя в удар strike_n; возвращает пару (hit, crit)."""
    if strike_n % 3 == 0:
        return crit_damage, True
    return damage, False

def fight(enemy, hero_health, bonus, damage, crit_damage):
    """Бой с enemy до гибели одного из двоих.
    Возвращает (раунды, победа_героя, здоровье_героя, трофеи).
    """
    stats = enemy_stats[enemy]
    enemy_hp = float(stats["hp"])
    rounds = []
    round_n = 0
    
    enemy_names_ru = {"skeleton": "Скелет", "zombi": "Зомби", "spider": "Паук", "bat": "Летучая мышь"}
    enemy_ru = enemy_names_ru.get(enemy, enemy)
    
    print(f"Вы спускаетесь по лестнице. Из темноты выступает {enemy_ru}!")
    
    while enemy_hp > 0 and hero_health > 0:
        round_n += 1
        hit, crit = hero_hit(round_n, damage, crit_damage)
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
    """Покупает quantity штук товара. Возвращает (gold_left, ok)."""
    cost = price * quantity
    if gold >= cost:
        return gold - cost, True
    return gold, False

# Самотест модуля (сработает только при прямом запуске python dungeon.py)
if __name__ == "__main__":
    rounds, won, hp, loot = fight("skeleton", 100, 0, 20.5, 41.0)
    print(f"self-test: {len(rounds)} rounds, won={won}, loot={loot}")