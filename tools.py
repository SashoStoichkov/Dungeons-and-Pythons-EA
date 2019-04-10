class Tool:
    def __init__(self, name, damage):
        self.validate_parameters(name, damage)
        self._name = name
        self._damage = damage

    @property
    def name(self):
        return self._name
    
    @property
    def damage(self):
        return self._damage
    
    @staticmethod
    def validate_parameters(name, damage):
        if not isinstance(name, str):
            raise TypeError('Name must be string!')

        if not isinstance(damage, int) and not isinstance(damage, float):
            raise TypeError('Damage must be either integer or float!')

        if damage < 0:
            raise ValueError('Damage must be non-negative!')



class Weapon(Tool):
    def __init__(self, name, damage):
        super().__init__(name, damage)



class Spell(Tool):
    def __init__(self, name, damage, mana_cost, cast_range):
        super().__init__(name, damage)
        self.validate_init_parameters(mana_cost, cast_range)
        self._mana_cost = mana_cost
        self._cast_range = cast_range

    @property
    def mana_cost(self):
        return self._mana_cost
    
    @property
    def cast_range(self):
        return self._cast_range
    
    @staticmethod
    def validate_init_parameters(mana_cost, cast_range):
        if not isinstance(mana_cost, int) and not isinstance(mana_cost, float):
            raise TypeError('Mana cost must be either integer of float!')

        if mana_cost < 0:
            raise ValueError('Mana cost must be non-negative!')

        if not isinstance(cast_range, int):
            raise TypeError('Cast range must be integer!')

        if cast_range < 1:
            raise ValueError('Cast range must be equal to or greater than one!')