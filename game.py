
import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import random 

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 9
GAME_HEIGHT = 9

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True


class Character(GameElement):
    IMAGE = "Boy"
    
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
  IMAGE = "Pokeball"
  SOLID = True
  def interact(self, player):
    GAME_BOARD.draw_msg("You're dead. Sad..")
    GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
  
  def random_move(self):
    r  = random.randint(1, 4)
    if r == 1:
      random_direction = "up"
    elif r == 2:
      random_direction = "down"
    elif r == 3:
      random_direction = "left"
    elif r == 4:
      random_direction = "right"

    next_enemy_location = self.next_pos(random_direction)
    next_enemy_x = next_enemy_location[0]
    next_enemy_y = next_enemy_location[1]

    if is_position_inbounds(next_enemy_x, next_enemy_y):
        existing_el = GAME_BOARD.get_el(next_enemy_x, next_enemy_y)
        if not existing_el:
            self.move(next_enemy_x, next_enemy_y)
            return

class Pokemon(Character):
  SOLID = True

class Pikachu(Pokemon):
  IMAGE = "FancyPikachu"
  def interact(self, player):
    GAME_BOARD.draw_msg("You found me! Thanks for saving me bestie!")

class Charmander(Pokemon):
  IMAGE = "FancyCharmander"
  def interact(self, player):
    GAME_BOARD.draw_msg("Meowth and Team Rocket stole Pikachu! Ask another sophisticated pokemon for help/advice!")

class Bulbasaur(Pokemon):
  IMAGE = "FancyBulbasaur"
  def interact(self, player):
    GAME_BOARD.draw_msg("Pikachu is behind one of the doors! You need a gem. Ask a sophisticated pokemon for more info!")

class Squirtle(Pokemon):
  IMAGE = "FancySquirtle"
  def interact(self,player):
    GAME_BOARD.draw_msg("You need something orange to save Pikachu! Orange will open the door he's behind..")

class Snorlax(Pokemon):
  IMAGE = "snorlax"
  def interact(self, player):
    GAME_BOARD.draw_msg("Don't ask me. I'm not sophisticated.")
    
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
                GAME_BOARD.del_el(self.x, self.y)
                pikachu = Pikachu()
                GAME_BOARD.register(pikachu)
                GAME_BOARD.set_el(self.x, self.y, pikachu)
                GAME_BOARD.draw_msg("You've gone through the correct door and saved PikaPika!")


class Tree(GameElement):
    IMAGE = "TallTree"
    SOLID = True

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    
    # The positions we're setting each rock to
    rock_positions = [
        (6, 6), 
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
    global PLAYER1
    PLAYER1 = Enemy()
    GAME_BOARD.register(PLAYER1)
    GAME_BOARD.set_el(0, 4, PLAYER1)

    global PLAYER2
    PLAYER2 = Enemy()
    GAME_BOARD.register(PLAYER2)
    GAME_BOARD.set_el(4, 6, PLAYER2)
    print PLAYER2 

    GAME_BOARD.draw_msg("Where's Pikachu? Ask the pokemon where he be at. Be careful of the pokeballs!")

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
    GAME_BOARD.set_el(2, 4, door1)

    door2 = Door(None)
    GAME_BOARD.register(door2)
    GAME_BOARD.set_el(5, 6, door2)

    #Initialize Pokemon positions
    fancySquirtle = Squirtle()
    GAME_BOARD.register(fancySquirtle)
    GAME_BOARD.set_el(0, 6, fancySquirtle)

    fancyCharmander = Charmander()
    GAME_BOARD.register(fancyCharmander)
    GAME_BOARD.set_el(2, 3, fancyCharmander)
     
    fancyBulbasaur = Bulbasaur()
    GAME_BOARD.register(fancyBulbasaur)
    GAME_BOARD.set_el(4, 5, fancyBulbasaur)
                  
    snorlax = Snorlax()
    GAME_BOARD.register(snorlax)
    GAME_BOARD.set_el(0, 3, snorlax)

    # Initialize and register a couple of trees
    for pos in tree_positions:
        tree = Tree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(pos[0], pos[1], tree)
        # trees.append(tree)

def is_position_inbounds(x, y):
  return x >= 0 and x < GAME_WIDTH and y >= 0 and y < GAME_HEIGHT

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
        
        PLAYER1.random_move()
        PLAYER2.random_move()

        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]
       
        if not is_position_inbounds(next_x, next_y):
            GAME_BOARD.draw_msg("You can't cross into dark-lands, stay within the perimiter of our kingdom!")
            PLAYER.move(3, 3)
            return

        existing_el = GAME_BOARD.get_el(next_x, next_y)
	   
        if existing_el is None or not existing_el.SOLID:
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)

        if existing_el:
            existing_el.interact(PLAYER)

    

    
