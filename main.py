import dungeons_and_treasures as dt

if __name__ == "__main__":
    map1 = dt.Dungeon("dungeons/level1.txt")
    map2 = dt.Dungeon("dungeons/level2.txt")
    map3 = dt.Dungeon("dungeons/level3.txt")

    m1 = map1.create_matrix()
    map1.spawn(m1)

    m2 = map2.create_matrix()
    map1.spawn(m2)

    m3 = map3.create_matrix()
    map1.spawn(m3)

    map1.move_hero(m1)
    map2.move_hero(m2)
    map3.move_hero(m3)
