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
            self.choose_attack()

    def choose_attack(self):
        if self.hero.get_weapon_damage() > self.hero.get_spell_damage():
                print("Hero hits with {} for {} damage. Enemy health is {}".format(self.hero._current_weapon.__name__, self.hero.get_weapon_damage(), self.enemy._current_health))
                self.enemy.take_damage(self.hero.attack(by="weapon"))
            
        else:
            if self.hero.can_cast(self.hero._current_spell):
                print("Hero casts a {} for {} damage. Enemy health is {}".format(self.hero._current_spell.__name__, self.hero.get_spell_damage(), self.enemy._current_health))
                self.enemy.take_damage(self.hero.attack(by="magic"))
            else:
                print("Hero does not have mana for another {}.".format(self.hero._current_spell))
