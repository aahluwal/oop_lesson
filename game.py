import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys


#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 7
GAME_HEIGHT = 7

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True


class Character(GameElement):
    IMAGE = "Horns"
    
    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []


    #Define function for next position 
    def next_pos(self, direction):
    
        #Set conditions for directions "up", etc. and returns a specific new location
        if direction == 'up':
            return (self.x, self.y - 1) 
        
        elif direction == 'down':
            return (self.x, self.y + 1)
        
        elif direction == 'right':
            return (self.x + 1, self.y)
        
        elif direction == "left":
            return (self.x - 1, self.y)

        return direction == None 

    def move(self, x, y):
        GAME_BOARD.del_el(self.x, self.y)
        GAME_BOARD.set_el( x, y, self)
      

class Enemy(Character):
  IMAGE = "Boy"

class Gem(GameElement):
    SOLID = False

class BlueGem(Gem):
    IMAGE = "BlueGem"
    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You have acquired a gem! \
                                    You have %d items in your inventory" %(len(player.inventory)))
class OrangeGem(Gem):
    IMAGE = "OrangeGem"
    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You have a key to one of the doors. Find the door out and you're safe!")
        player.move(3, 3)

class Door(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True
      
    def __init__(self, key):
      GameElement.__init__(self)
      self.key = key

    def interact(self, player):
        for item in player.inventory:
            if item == self.key:
                self.IMAGE = "DoorOpened"
                self.SOLID = False
                GAME_BOARD.draw_msg("You've gone through the correct door and are safe!")


class Tree(GameElement):
    IMAGE = "TallTree"
    SOLID = True

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    
    # The positions we're setting each rock to
    rock_positions = [
        (4, 3), 
        (3, 4),
        (3, 2),
        (2, 3)
    ]

    rocks = []

    # For every rock position, initialize, register and set each rock
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)
    rocks[-1].SOLID = False

    # Initialize and register the player Character
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(3, 3, PLAYER)

    # # Initialize and register two enemy boys that will attack character
    # global PLAYER1
    # PLAYER1 = Enemy()
    # GAME_BOARD.register(PLAYER1)
    # GAME_BOARD.set_el(1, 1, PLAYER1)

    # global PLAYER2
    # PLAYER2 = Enemy()
    # GAME_BOARD.register(PLAYER2)
    # GAME_BOARD.set_el(4, 6, PLAYER2)
    # print PLAYER2 

    GAME_BOARD.draw_msg("This is Alyssa and Dee's wicked awesome game.")

    # Initialize and register the Gem
    gem = BlueGem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 1, gem)

    # Initialize and register an orange gem
    orange_gem = OrangeGem()
    GAME_BOARD.register(orange_gem)
    GAME_BOARD.set_el(5, 4, orange_gem)

    tree_positions = [
        (2, 5),
        (5, 1),
        (6, 3),
        (2, 0)
    ]

    trees = []

    door_opens = Door(orange_gem)
    GAME_BOARD.register(door_opens)
    GAME_BOARD.set_el(0, 0, door_opens)
    
    door1 = Door(None)
    GAME_BOARD.register(door1)
    GAME_BOARD.set_el(3, 6, door1)

    door2 = Door(None)
    GAME_BOARD.register(door2)
    GAME_BOARD.set_el(5, 5, door2)

    # Initialize and register a couple of trees
    for pos in tree_positions:
        tree = Tree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(pos[0], pos[1], tree)
        # trees.append(tree)


def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = 'up'
    
    elif KEYBOARD[key.DOWN]:
        direction = 'down'
    
    elif KEYBOARD[key.RIGHT]:
        direction = 'right'
    
    elif KEYBOARD[key.LEFT]:
        direction = 'left'

  
    if direction:
        # next_enemy_location = PLAYER1.next_pos(direction)
        # next_enemy_x = next_enemy_location[0]
        # next_enemy_y = next_enemy_location[1]
        # PLAYER1.move(next_enemy_x, next_enemy_y)

        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]
        
        if not (0 <= next_x < GAME_WIDTH):
            GAME_BOARD.draw_msg("You can't cross into dark-lands, stay within the perimiter of our kingdom!")
            PLAYER.move(3, 3)
            print PLAYER
            return
        
        if not (0 <= next_y < GAME_HEIGHT):
            GAME_BOARD.draw_msg("You can't cross into dark-lands, stay within the perimiter of our kingdom!")
            PLAYER.move(3, 3)
            print PLAYER
            return

        existing_el = GAME_BOARD.get_el(next_x, next_y)
	   
        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)

        if existing_el:
           existing_el.interact(PLAYER)

    

    
