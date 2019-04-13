import sys, tty, termios, subprocess, time, random

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

    def move(self, m):
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
                        self.pick_treasure()
                        time.sleep(1.5)
                    elif m[x + move_x][y + move_y] == "E":
                        print("Fight!")
                        time.sleep(1.5)
                    elif m[x + move_x][y + move_y] == "G":
                        self.goal_reached()
                        time.sleep(1.5)
                        break

                    m[x][y] = "."
                    m[x + move_x][y + move_y] = "H"

                else:
                    print("You can't go there!")
                    time.sleep(1.5)

                self.move_enemy(m)

            else:
                print("Invalid key")
                time.sleep(1.5)

    def pick_treasure(self):
        print("Treasure picked!")

    def goal_reached(self):
        print("You reached the goal! CONGRATS!")
        return True

    def move_enemy(self, m):
        coor = []
        for a in range(len(m)):
            for b in range(len(m[0])):
                if m[a][b] == "E":
                    coor.append((a, b))

        for c in coor:
            a = c[0]
            b = c[1]
            poss_dir_e = []

            if a-1 >= 0 and m[a-1][b] != "#":
                poss_dir_e.append("up")
            if a+1 < len(m) and m[a+1][b] != "#":
                poss_dir_e.append("down")
            if b-1 >= 0 and m[a][b-1] != "#":
                poss_dir_e.append("left")
            if b+1 < len(m[0]) and m[a][b+1] != "#":
                poss_dir_e.append("right")

            rand_index = random.randint(0, len(poss_dir_e)-1)

            if poss_dir_e[rand_index] == "up":
                move_a = -1
                move_b = 0

            elif poss_dir_e[rand_index] == "down":
                move_a = 1
                move_b = 0

            elif poss_dir_e[rand_index] == "right":
                move_a = 0
                move_b = 1

            elif poss_dir_e[rand_index] == "left":
                move_a = 0
                move_b = -1

            if m[a + move_a][b + move_b] == "T":
                print("Enemy found treasure!")
                time.sleep(1.5)

            elif m[a + move_a][b + move_b] == "H":
                print("Enemy Fight!")
                time.sleep(1.5)
                break
            elif m[a + move_a][b + move_b] == "G":
                break

            m[a][b] = "."
            m[a + move_a][b + move_b] = "E"