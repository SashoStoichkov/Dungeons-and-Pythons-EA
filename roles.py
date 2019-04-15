from tools import Weapon, Spell
from potions import HealthPotion, ManaPotion
import random

class Role:

    def __init__(self, health, mana):
        self.validate_parameters(health, mana)
        self._max_health = health
        self._current_health = health
        self._max_mana = mana
        self._current_mana = mana
        self._current_weapon = None
        self._current_spell = None

    @property
    def max_health(self):
        return self._max_health
    
    @property
    def current_health(self):
        return self._current_health

    @property
    def max_mana(self):
        return self._max_mana
    
    @property
    def current_mana(self):
        return self._current_mana
    
    @property
    def current_weapon(self):
        return self._current_weapon

    @property
    def current_spell(self):
        return self._current_spell
    
    def get_health(self):
        return self._current_health

    def is_alive(self):
        return self._current_health > 0

    def get_mana(self):
        return self._current_mana

    def can_cast(self, spell):
        if spell.mana_cost <= self._current_mana:
            return True
        return False

    def take_damage(self, damage_points):
        if not isinstance(damage_points, int) and not isinstance(damage_points, float):
            raise TypeError('Damage points must be either integer or float!')

        if damage_points > self._current_health:
            self._current_health = 0
        else:
            self._current_health -= damage_points

    def take_healing(self, healing_points):
        if not isinstance(healing_points, int) and not isinstance(healing_points, float):
            raise TypeError('Healing points must be either integer or float!')

        if not self.is_alive():
            return False

        if healing_points + self._current_health > self._max_health:
            self._current_health = self._max_health
        else:
            self._current_health += healing_points
        return True

    def equip(self, weapon):
        if not isinstance(weapon, Weapon):
            raise TypeError('Weapon must be an instance of class Weapon!')

        self._current_weapon = weapon

    def learn(self, spell):
        if not isinstance(spell, Spell):
            raise TypeError('Spell must be an instance of class Spell!')

        self._current_spell = spell

    def get_weapon_damage(self):
        if self._current_weapon != None:
            return self._current_weapon.damage
        return 0

    def get_spell_damage(self):
        if self._current_spell != None:
            return self._current_spell.damage
        return 0

    def attack(self, by=None):
        if by == 'weapon':
            if self._current_weapon != None:
                return self._current_weapon.damage
            else:
                return 0

        if by == 'magic':
            if self._current_spell != None:
                return self._current_spell.damage
            else:
                return 0


    @staticmethod
    def validate_parameters(health, mana):
        if not isinstance(health, int) and not isinstance(health, float):
            raise TypeError('Health must be either integer or float!')

        if health < 0:
            raise ValueError('Health must be non-negative!')

        if not isinstance(mana, int) and not isinstance(mana, float):
            raise TypeError('Mana must be either integer or float!')

        if mana < 0:
            raise ValueError('Mana must be non-negative!')



class Hero(Role):
    def __init__(self, name, title, health, mana, mana_regeneration_rate):
        super().__init__(health, mana)
        self.validate_init_parameters(name, title, mana_regeneration_rate)
        self._name = name
        self._title = title
        self._mana_regeneration_rate = mana_regeneration_rate

    @property
    def name(self):
        return self._name

    @property
    def title(self):
        return self._title
    
    @property
    def mana_regeneration_rate(self):
        return self._mana_regeneration_rate
    
    def known_as(self):
        return '{} the {}'.format(self._name, self._title)

    def take_mana(self, mana_points=0):
        if not isinstance(mana_points, int) and not isinstance(mana_points, float):
            raise TypeError('Mana points must be either integer or float!')

        if self._current_mana + self._mana_regeneration_rate + mana_points > self._max_mana:
            self._current_mana = self._max_mana
        else:
            self._current_mana += self._mana_regeneration_rate + mana_points

    def choose_attack(self, enemy):
        if not isinstance(enemy, Enemy):
            raise TypeError()

        if self.get_weapon_damage() > self.get_spell_damage():
            enemy.take_damage(self.attack(by='weapon'))
            print("Hero hits with {} for {} damage. Enemy health is {}".format(self._current_weapon.name, self._current_weapon.damage, enemy.current_health))

        elif self._current_spell != None:
            if self.can_cast(self._current_spell):
                enemy.take_damage(self.attack(by='magic'))
                print("Hero casts a {} for {} damage. Enemy health is {}".format(self._current_spell.name, self._current_spell.damage, enemy.current_health))
            else:
                print("Hero does not have mana for another {}.".format(self._current_spell))
                if self._current_weapon != None:
                    enemy.take_damage(self.attack(by='weapon'))
                    print("Hero hits with {} for {} damage. Enemy health is {}".format(self._current_weapon.name, self._current_weapon.damage, enemy.current_health))
                else:
                    print('Hero does not have any weapon to use!')

    def pick_treasure(self, treasures_list):
        treasure = random.choice(treasures_list)
        if isinstance(treasure, Weapon):
            self.equip(treasure)
            print('Found {}'.format(str(treasure)))
        if isinstance(treasure, Spell):
            self.learn(treasure)
            print('Found {}'.format(str(treasure)))
        if isinstance(treasure, HealthPotion):
            self.take_healing(treasure.points)
            print('Found health potion. Hero\'s health is now {}'.format(self._current_health))
        if isinstance(treasure, ManaPotion):
            self.take_mana(treasure.points)
            print('Found mana potion. Hero\'s mana is now {}'.format(self._current_mana))


    @staticmethod
    def validate_init_parameters(name, title, mana_regeneration_rate):
        if not isinstance(name, str):
            raise TypeError('Name must be string!')

        if not isinstance(title, str):
            raise TypeError('Title must be string!')

        if not isinstance(mana_regeneration_rate, int) and not isinstance(mana_regeneration_rate, float):
            raise TypeError('Mana regeneration rate must be either integer or float!')

        if mana_regeneration_rate < 0:
            raise ValueError('Mana regeneration rate must be non-negative!')


class Enemy(Role):
    def __init__(self, health, mana, damage, coordinates):
        super().__init__(health, mana)
        self.validate_init_parameters(damage, coordinates)
        self._damage = damage
        self._coordinates = coordinates

    @property
    def damage(self):
        return self._damage

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, new_coordinates):
        if not isinstance(new_coordinates, list):
            raise TypeError('Coordinates must be stored in a list!')
        if len(new_coordinates) != 2:
            raise ValueError('Enemy must have exactly 2 coordinates!')

        self._coordinates = new_coordinates

    def take_mana(self, mana_points):
        if not isinstance(mana_points, int) and not isinstance(mana_points, float):
            raise TypeError('Mana points must be either integer or float!')

        if self._current_mana + mana_points > self._max_mana:
            self._current_mana = self._max_mana
        else:
            self._current_mana += mana_points

    def choose_attack(self, hero):
        if not isinstance(hero, Hero):
            raise TypeError()

        if self.get_weapon_damage() > self.get_spell_damage():
            hero.take_damage(self.attack(by='weapon'))
            print("Enemy hits with {} for {} damage. Hero health is {}".format(self._current_weapon.name, self._current_weapon.damage, hero.current_health))
        elif self._current_spell != None:
            if self.can_cast(self._current_spell):
                hero.take_damage(self.attack(by='magic'))
                print("Enemy casts a {} for {} damage. Hero health is {}".format(self._current_spell.name, self._current_spell.damage, hero.current_health))
            else:
                print("Enemy does not have mana for another {}.".format(self._current_spell))
                if self._current_weapon != None:
                    hero.take_damage(self.attack(by='weapon'))
                    print("Enemy hits with {} for {} damage. Hero health is {}".format(self._current_weapon.name, self._current_weapon.damage, hero.current_health))
                else:
                    print('Enemy does not have any weapon to use!')

        else:
            hero.take_damage(self._damage)
            print('Enemy hits hero for {} damage. Hero health is {}.'. format(self._damage, hero.current_health))

    def pick_treasure(self, treasures_list):
        treasure = random.choice(treasures_list)
        if isinstance(treasure, Weapon):
            self.equip(treasure)
        if isinstance(treasure, Spell):
            self.learn(treasure)
        if isinstance(treasure, HealthPotion):
            self.take_healing(treasure.points)
        if isinstance(treasure, ManaPotion):
            self.take_mana(treasure.points)


    @staticmethod
    def validate_init_parameters(damage, coordinates):
        if not isinstance(damage, int) and not isinstance(damage, float):
            raise TypeError('Damage must be either integer or float!')

        if damage < 0:
            raise ValueError('Damage must be non-negative!')

        if not isinstance(coordinates, list):
            raise TypeError('Coordinates must be stored in a list!')

        if len(coordinates) != 2:
            raise ValueError('Enemy must have exactly 2 coordinates!')