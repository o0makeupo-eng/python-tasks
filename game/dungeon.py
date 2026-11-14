"""Модуль правил подземелья: классы, бой, покупки, характеристики врагов."""
import random

prices = {"potion": 10, "torch_oil": 15, "war_elixir": 40}

enemy_stats = {
    "skeleton": {"hp": 45, "damage": 6, "loot": 25},
    "zombi": {"hp": 30, "damage": 4, "loot": 15},
    "spider": {"hp": 20, "damage": 3, "loot": 10},
    "bat": {"hp": 12, "damage": 2, "loot": 5},
}


class Hero:
    def __init__(self, name, health, strength, agility, endurance):
        self.name = name
        self.health = health
        self.strength = strength
        self.agility = agility
        self.endurance = endurance
        self.damage = 10 + strength * 1.5
        self.crit_damage = self.damage * 2
        self.stamina = health // strength  # Исходная формула из твоего кода

    def __str__(self):
        return f"{self.name}: здоровье {self.health}, урон {self.damage:.1f}, запас сил {self.stamina}"

    def strike(self, n):
        if n % 3 == 0:
            return self.crit_damage, True
        return self.damage, False

    def spend_stamina(self, cost):
        if self.stamina >= cost:
            self.stamina -= cost
            return False
        self.health -= cost - self.stamina
        self.stamina = 0
        return True

    def heal(self, amount, cap):
        self.health = min(self.health + amount, cap)

    def to_dict(self):
        return {
            "name": self.name,
            "health": self.health,
            "stamina": self.stamina,
            "strength": self.strength,
            "agility": self.agility,
            "endurance": self.endurance
        }

    @staticmethod
    def from_dict(data):
        hero = Hero(data["name"], data["health"], data["strength"], data["agility"], data["endurance"])
        hero.stamina = data["stamina"]
        return hero


class Enemy:
    def __init__(self, name, stats):
        self.name = name
        self.hp = stats["hp"]
        self.damage = stats["damage"]
        self.loot = stats["loot"]


def fight(enemy, hero, bonus=0):
    """Бой с enemy до гибели одного из двоих.
    Возвращает (раунды, победа_героя, трофеи).
    """
    rounds = []
    round_n = 0
    
    enemy_names_ru = {"skeleton": "Скелет", "zombi": "Зомби", "spider": "Паук", "bat": "Летучая мышь"}
    enemy_ru = enemy_names_ru.get(enemy.name, enemy.name)
    
    print(f"Вы спускаетесь по лестнице. Из темноты выступает {enemy_ru}!")
    
    while enemy.hp > 0 and hero.health > 0:
        round_n += 1
        hit, crit = hero.strike(round_n)
        hit = hit + bonus
        enemy.hp -= hit
        crit_mark = " — критический!" if crit else ""
        
        if enemy.hp <= 0:
            print(f"Раунд {round_n}: вы наносите {hit:.1f} урона{crit_mark}. Враг повержен.")
            rounds.append([round_n, hit, 0])
        else:
            blow = enemy.damage
            hero.health -= blow
            print(f"Раунд {round_n}: вы наносите {hit:.1f} урона{crit_mark}. Здоровье {enemy_ru}: {enemy.hp:.1f}. {enemy_ru} бьёт в ответ на {blow}.")
            rounds.append([round_n, hit, blow])
            
    won = enemy.hp <= 0
    loot = enemy.loot if won else 0
    return rounds, won, loot


def buy(price, gold, quantity=1):
    """Покупает quantity штук товара. Возвращает (gold_left, ok)."""
    cost = price * quantity
    if gold >= cost:
        return gold - cost, True
    return gold, False

def scout(r, c, seen, map_data, directions):
    if (r, c) in seen or map_data[r][c] == "#":
        return 0
    seen.add((r, c))
    total = 1
    for dr, dc in directions.values():
        total += scout(r + dr, c + dc, seen, map_data, directions)
    return total

def print_leaderboard(log):
    """Печатает топ-3 раундов по урону героя и рекорд врага."""
    if not log:
        print("Вы ещё не вступали в бой.")
        return
    top = sorted(log, key=lambda r: r[1], reverse=True)[:3]
    print("Таблица лидеров (урон героя):")
    for i in range(len(top)):
        print(f"{i + 1}. Раунд {top[i][0]}: {top[i][1]:.1f}")
    
    worst = max(log, key=lambda r: r[2])
    print(f"Самый сильный удар врага: {worst[2]} (раунд {worst[0]}).")

if __name__ == "__main__":
    hero = Hero("Тест", 100, 10, 10, 10)
    foe = Enemy("skeleton", enemy_stats["skeleton"])
    rounds, won, loot = fight(foe, hero, 0)
    print(f"self-test: {len(rounds)} rounds, won={won}, loot={loot}")