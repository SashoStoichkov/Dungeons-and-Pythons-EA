import sys, tty, termios, subprocess, time

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

class Dungeon():
    def __init__(self, s_level):
        self.s_level = s_level

    def print_map(self, m):

        for line in m:
            for el in line:
                print(el, end=" ")
            print()

    def spawn(self, m):
        coor = self.find_coordinates(m, 'S')

        m[coor[0]][coor[1]] = 'H'

        return m

    def create_matrix(self):
        m = []

        with open(self.s_level, 'r') as file:
            for line in file:
                m.append([ch for ch in line if ch != "\n"])

        return m

    def find_coordinates(self, m, ch):
        for i, sub_list in enumerate(m):
            if ch in sub_list:
                coor = (i, sub_list.index(ch))

        return coor

    def move_hero(self, m):
        key = _Getch()

        while True:
            subprocess.call(["clear"])
            self.print_map(m)
            print("Enter direction (use arrow keys)")
            k = key()

            x, y = self.find_coordinates(m, "H")

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

                if x + move_x >= 0 and x + move_x < len(m) and y + move_y >= 0 and y + move_y < len(m[0]) and m[x + move_x][y + move_y] != '#':
                    if m[x + move_x][y + move_y] == "T":
                        print("Found treasure!")
                        time.sleep(1.5)
                    elif m[x + move_x][y + move_y] == "E":
                        print("Fight!")
                        time.sleep(1.5)
                    elif m[x + move_x][y + move_y] == "G":
                        print("Goal reached!")
                        time.sleep(1.5)
                        break

                    m[x][y] = "."
                    m[x + move_x][y + move_y] = "H"

                else:
                    print("You can't go there!")
                    time.sleep(1.5)

            else:
                print("Invalid key")
                time.sleep(1.5)


map1 = Dungeon("dungeons/level1.txt")
map2 = Dungeon("dungeons/level2.txt")

m1 = map1.create_matrix()
map1.spawn(m1)

m2 = map2.create_matrix()
map1.spawn(m2)

map1.move_hero(m2)