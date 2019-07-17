from Characters import Character
from Places import Map


def main():
    enemy_appeared = False
    hero = Character.Player("ja", hp=10, power=5, x=1, y=1)
    bidoof = Character.Enemy("Troll", level=1, exp=6)
    bidoof1 = Character.Enemy("Troll", level=1, exp=6)
    pikachu = Character.Enemy("Pikachu", level=6, power=10, exp=60)
    NPCdict = {}
    NPCdict[(1, 1)] = bidoof
    NPCdict[(0, 0)] = bidoof1
    NPCdict[(1, 5)] = pikachu
    mapka = Map.Map(NPCdict)
    inp = input("Next action: ")
    while inp != 'q':
        if inp == 'f':
            if (hero.x, hero.y) in NPCdict.keys():
                hero.attack(NPCdict[hero.x, hero.y])
                if NPCdict[hero.x, hero.y].state == "dead":
                    NPCdict.pop((hero.x, hero.y))
                    enemy_appeared = False
            else:
                print("You can't attack, there's not an enemy nearby.")
        elif inp == 'a':
            if hero.move(mapka, x=-1):
                print("You're going west.")
        elif inp == 's':
            if hero.move(mapka, y=1):
                print("You're going south.")
        elif inp == 'd':
            if hero.move(mapka, x=1):
                print("You're going east.")
        elif inp == 'w':
            if hero.move(mapka, y=-1):
                print("You're going north.")
        elif inp == 'i':
            print("Hero name: {}\nLevel: {}\nHP: {}\nEXP: {}\nGold: {}\nCoordinates: ({}, {})".format(hero.name, hero.level, hero.hp, hero.exp, hero.money,     hero.x, hero.y))
        if (hero.x, hero.y) in NPCdict.keys() and not enemy_appeared:
            print("{} is attacking you! Fight or run!".format(NPCdict[(hero.x, hero.y)].name))
            print("Level: {}\nHP: {}\nPower: {}".format(NPCdict[(hero.x, hero.y)].level, NPCdict[(hero.x, hero.y)].hp, NPCdict[(hero.x, hero.y)].power))
            enemy_appeared = True
        if hero.state == "dead":
            print("Try again!")
            exit()
        inp = input("Next action: ")


if __name__ == '__main__':
    main()
