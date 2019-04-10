from tools import Weapon, Spell

class Role:

    def __init__(self, health, mana):
        self.validate_parameters(health, mana)
        self._max_health = health
        self._current_health = health
        self._max_mana = mana
        self._current_mana = mana
        self._current_weapon = None
        self._current_spell = None

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
                weapon_to_use = self._current_weapon
                self._current_weapon = None
                return weapon_to_use.damage
            else:
                return 0

        if by == 'magic':
            if self._current_spell != None:
                spell_to_use = self._current_spell
                self._current_spell = None
                return spell_to_use.damage
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
    def __init__(self, health, mana, damage):
        super().__init__(health, mana)
        self.validate_init_parameters(damage)
        self._damage = damage

    @property
    def damage(self):
        return self._damage
    
    def take_mana(self, mana_points):
        if not isinstance(mana_points, int) and not isinstance(mana_points, float):
            raise TypeError('Mana points must be either integer or float!')

        if self._current_mana + mana_points > self._max_mana:
            self._current_mana = self._max_mana
        else:
            self._current_mana += mana_points

    @staticmethod
    def validate_init_parameters(damage):
        if not isinstance(damage, int) and not isinstance(damage, float):
            raise TypeError('Damage must be either integer or float!')

        if damage < 0:
            raise ValueError('Damage must be non-negative!')