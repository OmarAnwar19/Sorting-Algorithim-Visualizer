# imports
import pygame
import os
import math


#! create the class for all of our global variables, and inits
class init_info:
    # initializing pygame
    pygame.init()

    # ? the init funciton for our class
    def __init__(self, width, height, lst):
        # call the function for all our global variables
        self.vars()

        # initialize our window width and height
        self.width = width
        self.height = height

        # create the pygame window using the width and height we took in
        self.WIN = pygame.display.set_mode((width, height))

        # the title and icon for the pygame window
        pygame.display.set_icon(pygame.image.load(
            os.path.join("assets", "img", "icon.png")))
        pygame.display.set_caption("Sorting Algorithim Visualization.")

        # finally, call the function to set our list
        self.set_list(lst)

    # ? the function for all of our global variables
    def vars(self):
        # global variables for colours
        self.BLACK = 0, 0, 0
        self.WHITE = 255, 255, 255
        self.GREEN = 0, 255, 0
        self.RED = 255, 0, 0

        # the gradients for our bar colours
        self.GRADIENTS = [
            (128, 128, 128),
            (160, 160, 160),
            (192, 192, 192)
        ]

        self.BG_COLOR = self.WHITE

        # global variables for fonts
        self.REG_FONT = pygame.font.SysFont("montserrat", 20)
        self.LARGE_FONT = pygame.font.SysFont("montserrat", 30, bold=True)

        # the variables for padding on the top, and sides of the bars
        self.SIDE_PAD = 100
        self.TOP_PAD = 150

        # global variable for the sort speed of the algorithim
        self.SORT_SPEED = 120

    # ? the function for setting up our list
    def set_list(self, lst):
        # we have to set up the size of each bar, according to the list
        # the bigger the list, the smaller the bars;
        # the bigger the range of the list, the shorter each bar will be

        # set a variable for the list, and its min and max values
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        # the variable for our start coordinate
        # this is the padding (100) / 2 = 50, therefore we start at x of 50
        self.start_x = self.SIDE_PAD // 2

        # the variable for the width of each bar, determined as such:
        # --> width - side_pad = overall width left in the screen
        # --> then, we divide that by the number of items in the list
        # --> this gets us a width which is equal for each bar in the list
        self.block_width = round((self.width - self.SIDE_PAD) // len(self.lst))

        # the variable for the height of each bar, determined as such:
        # --> height - top_pad = overall height left in the screen
        # --> self.max - self.min is the range of items in our list
        # --> this is all of the possible sizes for the bars in the list
        # --> then, we divide the height / items, to get the height of each item
        self.block_height = math.floor(
            (self.height - self.TOP_PAD) / (self.max_val - self.min_val))
