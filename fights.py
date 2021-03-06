from roles import Hero, Enemy
import sys

def fight(hero, enemy):
    if isinstance(hero, Hero) and isinstance(enemy, Enemy):
        print("A fight is started between our Hero(health={}, mana={}) and Enemy(health={}, mana={}, damage={})".format(hero.get_health(), hero.get_mana(), enemy.get_health(), enemy.get_mana(), enemy.damage))
        
        while True:
            if hero.is_alive() == False:
                print("Hero is Dead!")
                return 0

            hero.choose_attack(enemy)

            if enemy.is_alive() == False:
                print("Enemy is Dead!")
                return 1

            enemy.choose_attack(hero)