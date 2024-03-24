# Basic arcade program
# Displays a white window with a blue circle in the middle

# Imports
import arcade

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Welcome to Arcade"
RADIUS = 150

COLUMN_SPACING = 20
ROW_SPACING = 20
LEFT_MARGIN = 110
BOTTOM_MARGIN = 110
NUMBER_COUNT = 9

WIDTH = 40
HEIGHT = 40
MARGIN = 5

NUMBERS_LIST = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

LINE_COUNT =20
ROW_1 = 0
ROW_2 = 1
ROW_3 = 2
ROW_4 = 3
ROW_5 = 4
ROW_6 = 5
ROW_7 = 6
ROW_8 = 7
ROW_9 = 8

COLUMN_1  = 9
COLUMN_2 = 10
COLUMN_3 = 11
COLUMN_4 = 12
COLUMN_5 = 13
COLUMN_6 = 14
COLUMN_7 = 15
COLUMN_8 = 16
COLUMN_9 = 17

DIAGONAL_1 = 18
DIAGONAL_2 = 19


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")
        self.number_list = None

        self.list_list = None
        self.number_sprite = None
        self.held_number = None
        self.held_number_original_position = None
        self.grid_list = None
        self.piles = None
        self.start_list = None
        self.array = None
        arcade.set_background_color(arcade.color.WHITE)


    def setup(self):
        """ Set up the game and initialize the variables. """
        # Sprite lists
        self.number_list = arcade.SpriteList()
        self.list_list: arcade.SpriteList = arcade.SpriteList()
        self.held_number = []
        self.held_number_original_position = []
        self.grid_list: arcade.SpriteList = arcade.SpriteList()
        self.start_list: arcade.SpriteList = arcade.SpriteList()
        self.piles = [[] for _ in range(LINE_COUNT)]
        self.list_list = []
        self.array = [[1,0,3,0,5,0,7,8,0],
                      [0,5,0,7,0,9,1,2,3],
                      [7,8,0,1,0,3,0,5,6],
                      [2,3,4,5,0,0,0,9,1],
                      [5,0,0,8,9,1,2,0,0],
                      [8,9,0,2,3,0,5,0,7],
                      [3,0,5,6,0,0,9,1,2],
                      [0,7,0,9,1,2,3,0,5],
                      [9,0,2,3,4,0,6,7,8]]

        for row in range(9):    
            for column in range(9): 
                grid = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.BLACK)
                grid.position = 200, 200
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                grid.center_x = x
                grid.center_y = y
                self.grid_list.append(grid)

        for row in range(9):    
            for column in range(9): 
                start = row + 1
                picName = str(self.array[row][column]) + '.png' 
                number = arcade.Sprite(picName, .5)
                # number = arcade.SpriteSolidColor(20, 20, arcade.color.WHITE)
                #number = arcade.draw_text("1", 20, 20, arcade.color.WHITE)
                number.position = 200, 200
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                number.center_x = x
                number.center_y = y
        
                self.start_list.append(number)
        


        x = 100
        for i in NUMBERS_LIST:
            x += 50
            picName = i + '.png' 
            number = arcade.Sprite(picName, .5)
            number.center_x = x
            number.center_y = 500
            self.number_list.append(number)



            
    def pull_to_top(self, number: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.number_list.remove(number)
        self.number_list.append(number)
    def on_mouse_press(self, x, y, button, key_modifiers):
    
    # Get list of cards we've clicked on
        numbers = arcade.get_sprites_at_point((x, y), self.number_list)
    # Have we clicked on a card?
        if len(numbers) > 0:
        # Might be a stack of cards, get the top one
            primary_number = numbers[-1]
        # All other cases, grab the face-up card we are clicking on
            self.held_number = [primary_number]
        # Save the position
            self.held_number_original_position = [self.held_number[0].position]
        # Put on top in drawing order
            self.pull_to_top(self.held_number[0])


    def remove_card_from_pile(self, number):
        """ Remove card from whatever pile it was in. """
        for pile in self.piles:
            if number in pile:
                pile.remove(number)
                break
    def get_pile_for_card(self, number):
        
        for index, pile in enumerate(self.piles):
            if number in pile:
                print(index)
                return index
            
    def move_card_to_new_pile(self, number, pile_index):
        """ Move the card to a new pile """
        self.remove_card_from_pile(number)
        self.piles[pile_index].append(number)
                
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # If we are holding cards, move them with the mouse
        for number in self.held_number:
            number.center_x += dx
            number.center_y += dy
    def on_mouse_release(self, x: float, y: float, button: int,
                     modifiers: int):
    
    # If we don't have any cards, who cares
        if len(self.held_number) == 0:
            return
        
         # Find the closest pile, in case we are in contact with more than one
        grid, distance = arcade.get_closest_sprite(self.held_number[0], self.grid_list)
        reset_position = True

        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_number[0], grid):

            grid_index = self.grid_list.index(grid)

            # For each held card, move it to the pile we dropped on
            for i, dropped_number in enumerate(self.held_number):
                # Move cards to proper position
                dropped_number.position = grid.center_x, grid.center_y

            # Success, don't reset position of cards
            reset_position = False

        # for index, pile in enumerate(self.piles):
        #     if number in pile:
        # #         reset_position = True
        # card_index = self.piles[pile_index]
        # for i in self.piles[pile_index]:
        #     print(i)
        #     if self.held_number == i:
        #         reset_position = True
        #     else: reset_position = False

            # Release on top play pile? And only one card held?
        if reset_position:
            # Where-ever we were dropped, it wasn't valid. Reset the each card's position
            # to its original spot.
            for grid_index, number in enumerate(self.held_number):
                number.position = self.held_number_original_position[grid_index]
    # We are no longer holding cards
        self.held_number = []

    def on_draw(self):

        arcade.start_render()
        self.grid_list.draw()
        self.number_list.draw()
        self.start_list.draw()

       



def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()