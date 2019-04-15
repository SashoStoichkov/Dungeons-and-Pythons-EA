from dungeons import *
from roles import Hero

if __name__ == "__main__":

    hero = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=5)

    levels = ["dungeons/level1.txt", "dungeons/level2.txt", "dungeons/level3.txt"]
    treasures = ['treasures/level1_treasures.json', 'treasures/level2_treasures.json', 'treasures/level3_treasures.json']
    enemies = ['enemies/level1_enemies.json', 'enemies/level2_enemies.json', 'enemies/level3_enemies.json']
    
    for index in range(len(levels)):
        level = Dungeon(levels[index], treasures[index], enemies[index], hero)
        level.spawn()
        level.move_hero()