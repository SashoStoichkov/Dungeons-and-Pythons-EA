import sys, tty, termios, subprocess, time, random, json
from tools import Weapon, Spell
from potions import ManaPotion, HealthPotion

class _Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(3)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class Parser:
    @classmethod
    def parse_matrix(cls, matrix_file):
        matrix = []

        with open(matrix_file, 'r') as file:
            for line in file:
                matrix.append([ch for ch in line if ch != "\n"])

        return matrix

    @classmethod
    def parse_treasures(cls, treasures_file):
        treasure_objects = []

        with open(treasures_file, 'r') as file:
            treasures_list = json.load(file)['treasures']
        
        for treasure in treasures_list:
            if treasure['type'] == 'Weapon':
                new_treasure = Weapon(treasure['dict']['_name'], treasure['dict']['_damage'])
                treasure_objects.append(new_treasure)
            if treasure['type'] == 'Spell':
                new_treasure = Spell(treasure['dict']['_name'], treasure['dict']['_damage'], treasure['dict']['_mana_cost'], treasure['dict']['_cast_range'])
                treasure_objects.append(new_treasure)
            if treasure['type'] == 'HealthPotion':
                new_treasure = HealthPotion(treasure['dict']['_points'])
                treasure_objects.append(new_treasure)
            if treasure['type'] == 'ManaPotion':
                new_treasure = ManaPotion(treasure['dict']['_points'])
                treasure_objects.append(new_treasure)

        return treasure_objects

class Dungeon():
    def __init__(self, level_map, treasures, hero):
        self._level_map = Parser.parse_matrix(level_map)
        self._treasures_list = Parser.parse_treasures(treasures)
        self._hero = hero

    def print_map(self):
        for line in self._level_map:
            for el in line:
                print(el, end=" ")
            print()

    def spawn(self):
        coor = self.find_coordinates('S')
        self._level_map[coor[0]][coor[1]] = 'H'

    def find_coordinates(self, ch):
        for i, sub_list in enumerate(self._level_map):
            if ch in sub_list:
                coor = (i, sub_list.index(ch))

        return coor

    def move_hero(self):
        key = _Getch()

        while True:
            subprocess.call(["clear"])
            self.print_map()
            print("Enter direction (use arrow keys)")
            k = key()

            x, y = self.find_coordinates("H")

            if k in ['\x1b[A', '\x1b[B', '\x1b[C', '\x1b[D']:

                if k == '\x1b[A':
                    move_x = -1
                    move_y = 0

                elif k == '\x1b[B':
                    move_x = 1
                    move_y = 0

                elif k == '\x1b[C':
                    move_x = 0
                    move_y = 1

                elif k == '\x1b[D':
                    move_x = 0
                    move_y = -1

                if x + move_x >= 0 and x + move_x < len(self._level_map) and y + move_y >= 0 and y + move_y < len(self._level_map[0]) and self._level_map[x + move_x][y + move_y] != '#':
                    
                    if self._level_map[x + move_x][y + move_y] == "T":
                        self.pick_treasure()
                        time.sleep(1.5)

                    elif self._level_map[x + move_x][y + move_y] == "E":
                        print("Fight!")
                        time.sleep(1.5)

                    elif self._level_map[x + move_x][y + move_y] == "G":
                        self.goal_reached()
                        time.sleep(1.5)
                        break

                    self._level_map[x][y] = "."
                    self._level_map[x + move_x][y + move_y] = "H"
                    self.move_enemy()

                else:
                    print("You can't go there!")
                    time.sleep(1.5)

            else:
                print("Invalid key!")
                time.sleep(1.5)

    def pick_treasure(self):
        treasure = random.choice(self._treasures_list)
        if isinstance(treasure, Weapon):
            self._hero.equip(treasure)
            print('Found {}'.format(str(treasure)))
        if isinstance(treasure, Spell):
            self._hero.learn(treasure)
            print('Found {}'.format(str(treasure)))
        if isinstance(treasure, HealthPotion):
            self._hero.take_healing(treasure.points)
            print('Found health potion. Hero\'s health is now {}'.format(self._hero.current_health))
        if isinstance(treasure, ManaPotion):
            self._hero.take_mana(treasure.points)
            print('Found mana potion. Hero\'s mana is now {}'.format(self._hero.current_mana))

    def goal_reached(self):
        print("You reached the goal! CONGRATS!")
        return True

    def move_enemy(self):
        enemy_coordinates = []
        for a in range(len(self._level_map)):
            for b in range(len(self._level_map[0])):
                if self._level_map[a][b] == "E":
                    enemy_coordinates.append((a, b))

        for coor in enemy_coordinates:
            a = coor[0]
            b = coor[1]
            possible_directions = []

            if a-1 >= 0 and self._level_map[a-1][b] != "#":
                possible_directions.append("up")
            if a+1 < len(self._level_map) and self._level_map[a+1][b] != "#":
                possible_directions.append("down")
            if b-1 >= 0 and self._level_map[a][b-1] != "#":
                possible_directions.append("left")
            if b+1 < len(self._level_map[0]) and self._level_map[a][b+1] != "#":
                possible_directions.append("right")

            rand_index = random.randint(0, len(possible_directions)-1)

            if possible_directions[rand_index] == "up":
                move_a = -1
                move_b = 0
            elif possible_directions[rand_index] == "down":
                move_a = 1
                move_b = 0
            elif possible_directions[rand_index] == "right":
                move_a = 0
                move_b = 1
            elif possible_directions[rand_index] == "left":
                move_a = 0
                move_b = -1

            if self._level_map[a + move_a][b + move_b] == "T":
                print("Enemy found treasure!")
                time.sleep(1.5)

            elif self._level_map[a + move_a][b + move_b] == "H":
                print("Enemy Fight!")
                time.sleep(1.5)
                break

            elif self._level_map[a + move_a][b + move_b] == "G":
                break

            self._level_map[a][b] = "."
            self._level_map[a + move_a][b + move_b] = "E"