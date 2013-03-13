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


class Gem(GameElement):
    IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        
        if self.IMAGE == "BlueGem":
            player.inventory.append(self)
            GAME_BOARD.draw_msg("You have acquired a gem! \
                                    You have %d items in your inventory" %(len(player.inventory)))

        elif self.IMAGE == "OrangeGem":
            GAME_BOARD.del_el(player.x, player.y)
            GAME_BOARD.set_el(3, 3, player)

class OrangeGem(Gem):
    IMAGE = "OrangeGem"

class Tree(GameElement):
    IMAGE = "TallTree"
    SOLID = True

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    
    # The positions we're setting each rock to
    rock_positions = [
        (2, 1), 
        (1, 2),
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

    for rock in rocks:
        print rock

    # Initialize and register the player Character
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(3, 3, PLAYER)
    print PLAYER

    GAME_BOARD.draw_msg("This is Alyssa and Dee's wicked awesome game.")

    # Initialize and register the Gem
    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 1, gem)

    # Initialize and register an orange gem
    orange_gem = OrangeGem()
    GAME_BOARD.register(orange_gem)
    GAME_BOARD.set_el(5, 4, orange_gem)

    tree_positions = [
        (4, 3),
        (5, 1),
        (6, 3),
        (2, 0)
    ]

    trees = []

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
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        existing_el = GAME_BOARD.get_el(next_x, next_y)

        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)

        if existing_el:
            existing_el.interact(PLAYER)