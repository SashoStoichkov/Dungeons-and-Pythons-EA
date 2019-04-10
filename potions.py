class Potion:
    def __init__(self, points):
        self.validate_parameters(points)
        self._points = points

    @property
    def points(self):
        return self._points
    
    @staticmethod
    def validate_parameters(points):
        if not isinstance(points, int) and not isinstance(points, float):
            raise TypeError('Points must be either integer or float!')

        if points <= 0:
            raise ValueError('Points must be positive!')


class ManaPotion(Potion):
    def __init__(self, points):
        super().__init__(points)


class HealthPotion(Potion):
    def __init__(self, points):
        super().__init__(points)