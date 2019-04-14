from dungeons_and_treasures import *
from roles import Hero

if __name__ == "__main__":
    hero = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)

    map1 = Dungeon("dungeons/level1.txt", 'treasures/level1_treasures.json', 'enemies/level1_enemies.json', hero)
    map2 = Dungeon("dungeons/level2.txt", 'treasures/level2_treasures.json', 'enemies/level2_enemies.json', hero)
    map3 = Dungeon("dungeons/level3.txt", 'treasures/level3_treasures.json', 'enemies/level3_enemies.json', hero)

    map1.spawn()

    map2.spawn()

    map3.spawn()

    map1.move_hero()
    map2.move_hero()
    map3.move_hero()
