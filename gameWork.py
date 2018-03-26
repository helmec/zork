from random import randint
from random import random
import sys

count = 0

class Observable:
    def __init__(self):
        self.observers = set()
    def register(self, who):
        self.observers.add(who)
    def unregister(self, who):
        self.observers.discard(who)
    def dispatch(self, message):
        for observer in self.observers:
            observer.update(message)
            
class Observer:
    def __init__(self, name):
        self.name = name
    def update(self, message):
        return message

class Weapon:
    def __init__(self, attMod, numUses, name):
        self.attMod = attMod
        self.numUses = numUses
        self.name = name
    def weaponStatus(self):
        print("Weapon Name: " + self.name)
        print("Uses Left: " + str(self.numUses))
	
class HersheyKiss(Weapon):
    def __init__(self):
        Weapon.__init__(self, 1, 10, "Hershey Kiss")

class SourStraw(Weapon):
    def __init__(self):
        Weapon.__init__(self, randint(1, 2), 2, "Sour Straw")

class ChocolateBar(Weapon):
    def __init__(self):
        Weapon.__init__(self, randint(2, 3), 4, "Chocolate Bar")

class NerdBomb(Weapon):
    def __init__(self):
        Weapon.__init__(self, randint(3, 5), 1, "Nerd Bomb")

def randomWeapon():
        w = randint(1, 5)
        if w ==1:
            return HersheyKiss()
        elif w == 2:
            return SourStraw()
        elif w == 3:
            return ChocolateBar()
        else:
            return NerdBomb()
        
class NPC(Observable):
    def __init__(self, damage, hp, attackable):
        Observable.__init__(self)
        self.damage = damage
        self.hp = hp
        self.attackable = attackable

class Person(NPC):
    def __init__(self):
        NPC.__init__(self, -1, 100, False)

class Zombie(NPC):
    def __init__(self):
        NPC.__init__(self, randint(0, 11), randint(100, 201), True)

class Vampire(NPC):
    def __init__(self):
        NPC.__init__(self, randint(10, 21), randint(100, 201), True)

class Ghoul(NPC):
    def __init__(self):
        NPC.__init__(self, randint(15, 31), randint(40, 81), True)

class Werewolf(NPC):
    def __init__(self):
        NPC.__init__(self, randint(0, 40), 200, True)
        
def randomMonster():
    m = randint(1, 5)
    if m == 1:
        return Person()
    elif m == 2:
        return Zombie()
    elif m == 3:
        return Vampire()
    elif m == 4:
        return Ghoul()
    else:
        return Werewolf()
        
class Game(Observer):
    def __init__(self, player, town, row, col):
        Observer.__init__(self, "game")
        self.player = Player(player)
        self.town = Neighborhood(town, row, col)
        self.row = row
        self.col = col
        self.gameEnds = False
        
        
class Player:
    def __init__(self, name):
        self.name = name
        self.hp = randint(10000, 12600)
        self.att = randint(10, 20)
        self.inventory = []
        for i in range(1, 10):
            self.inventory.append(randomWeapon())
        
class Neighborhood:
    def __init__(self, name, row, col):
        self.name = name
        self.row = row
        self.col = col
        self.grid = []
        self.numMonsters = 0
        for i in range(0, row):
            self.grid.append([])
            for j in range(0, col):
                self.grid[i].append(House())
                self.numMonsters += self.grid[i][j].numMonsters
        for i in range(0, row):
            for j in range(0, col):
                if i - 1 >= 0:
                    self.grid[i][j].up = self.grid[i - 1][j]
                else:
                    self.grid[i][j].up = None
                if i + 1 <= row - 1:
                    self.grid[i][j].down = self.grid[i + 1][j]
                else:
                    self.grid[i][j].down = None
                if j - 1 >= 0:
                    self.grid[i][j].left = self.grid[i][j - 1]
                else:
                    self.grid[i][j].left = None
                if j + 1 <= col - 1:
                    self.grid[i][j].right = self.grid[i][j + 1]
                else:
                    self.grid[i][j].right = None
                
        
class House(Observable, Observer):
    def __init__(self):
        Observable.__init__(self)
        Observer.__init__(self, "home")
        self.monsters = []
        self.numMonsters = 0
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.hasPlayer = False
        for i in range(1, randint(0, 10)):
            self.monsters.append(randomMonster())
            if self.monsters[i - 1].attackable:
                self.numMonsters += 1
            
def attack(game, player, house, weapon):
    damage = player.att * weapon.attMod
    for mon in house.monsters:
        if mon.attackable:
            mon.hp -= damage
            if mon.hp <= 0:
                house.monsters.remove(mon)
                house.monsters.append(Person())
                game.town.numMonsters -= 1
        else:
            player.inventory.append(randomWeapon())
    for mon in house.monsters:
        player.hp -= mon.damage
    weapon.numUses -= 1
    if weapon.numUses <= 0:
        game.player.inventory.remove(weapon)
        weapon = player.inventory[randint(0, len(player.inventory) - 1)]
    cont(player, game)
    status(game)
    while game.gameEnds == False:
        takeCommand(game, house, weapon)
        
def cont(player, game):
    if player.hp <= 0:
        game.gameEnds = True
    elif game.town.numMonsters <= 0:
        game.gameEnds = True
    if game.gameEnds:
        print("Game Over!")
        sys.exit()

def move(command, game, house, weapon):
    if command == 'w':
        if house.up != None:
            house.hasPlayer == False
            house.up.hasPlayer == True
            takeCommand(game, house.up, weapon)
        else:
            print("Out of bounds")
            takeCommand(game, house, weapon)
    if command == 'a':
        if house.left != None:
            house.hasPlayer == False
            house.left.hasPlayer == True
            takeCommand(game, house.left, weapon)
        else:
            print("Out of bounds")
            takeCommand(game, house, weapon)
    if command == 's':
        if house.down != None:
            house.hasPlayer == False
            house.down.hasPlayer == True
            takeCommand(game, house.down, weapon)
        else:
            print("Out of bounds")
            takeCommand(game, house, weapon)
    if command == 'd':
        if house.right != None:
            house.hasPlayer == False
            house.right.hasPlayer == True
            takeCommand(game, house.right, weapon)
        else:
            print("Out of bounds")
            takeCommand(game, house, weapon)
        
def takeCommand(game, house, weapon):
    print("What will you do next?")
    print("Enter 'o' to see your options")
    command = input()
    if command == 'w' or command == 'a' or command == 's' or command == 'd':
        move(command, game, house, weapon)
    elif command == 'f':
        attack(game, game.player, house, weapon)
    elif command == 'i':
        for item in game.player.inventory:
            item.weaponStatus()
        takeCommand(game, house, weapon)
    elif command == 'o':
        print("Enter 'w', 'a', 's', or 'd' to move to a new house")
        print("Enter 'i' to check your inventory")
        print("Enter 'f' to battle the monsters in the current house")
        print("Enter 'q' to quit the game")
        takeCommand(game, house, weapon)
    elif command == 'q':
        sys.exit()
    else:
        print("That is not a valid option.")
        takeCommand(game, house, weapon)
        
def status(g):
    print("Player: " + g.player.name)
    print("HP: " + str(g.player.hp))
    print("Monsters: " + str(g.town.numMonsters))
    print()
        
def main():
    g = Game("Lady", "Orion", 5, 5)
    g.town.grid[0][0].hasPlayer = True
    status(g)
    takeCommand(g, g.town.grid[0][0], g.player.inventory[0])
    