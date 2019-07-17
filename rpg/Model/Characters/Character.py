class Character:
    def __init__(self, name, hp=10, power=1, level=1, x=0, y=0, exp=0):
        self.name = name
        self.state = "alive"
        self.hp = hp
        self.power = power
        self.level = level
        self.exp = exp
        self.bag = []
        self.money = 0
        self.x, self.y = x, y


class Player(Character):
    def move(self, place, x=0, y=0):
        if x != 0 and 0 <= self.x + x <= place.width - 1:
            self.x += x
            return True
        elif y != 0 and 0 <= self.y + y <= place.height - 1:
            self.y += y
            return True
        print("You can't go there!")
        return False

    def attack(self, enemy):
        enemy.hp -= self.power
        print("You hit {0} for {1} damage. {0} hp remaining: {2}".format(enemy.name, self.power, enemy.hp))
        if enemy.hp <= 0:
            enemy.state = "dead"
            print("{} was defeated!".format(enemy.name))
            self.bag += enemy.bag
            self.money += enemy.level
            self.exp += enemy.exp
            while self.exp >= self.level * 50:
                self.exp -= self.level * 50
                self.level += 1
        else:
            enemy.attack(self)


class Enemy(Character):
    def attack(self, hero):
        hero.hp -= self.power
        print("{} hit you for {} damage. Your hp remaining: {}".format(self.name, self.power, hero.hp))
        if hero.hp <= 0:
            hero.state = "dead"
            print("You're dead! :(")
