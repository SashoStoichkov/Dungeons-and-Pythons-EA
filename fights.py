from roles import Hero, Enemy

class Fights:
    def __init__(self, hero, enemy):
        if isinstance(hero, Hero):
            self.hero = hero
        if isinstance(enemy, Enemy):
            self.enemy = enemy

    def fight(self):
        print("A fight is started between our Hero(health={}, mana={}) and Enemy(health={}, mana={}, damage={})".format(self.hero.get_health(), self.hero.get_mana(), self.enemy.get_health(), self.enemy.get_mana(), self.enemy.damage()))
        
        while True:
            if self.hero.is_alive() == False:
                print("Hero is Dead!")
                break
            elif self.enemy.is_alive() == False:
                print("Enemy is Dead!")
                break

            self.hero.choose_attack()
            self.enemy.choose_attack()