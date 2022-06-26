# imports
import random
import pygame

# import our init class
from classes.init import init_info


#! the function for generating our starting list
# takes in a number for our list, then a min and max, generates list between
def gen_start_list(n, min_val, max_val):
    # create an empty list
    lst = []

    # loop over the range n
    for i in range(n):
        # create a random value between the min_val and max_val
        val = random.randint(min_val, max_val)
        # add that value to our list
        lst.append(val)

    # finally, return the list after loop is completed
    return lst


#! functions for drawing things to the screen
# the function for drawing our window
def draw_window(info, algo_name, ascending):
    # first, fill the window with white
    info.WIN.fill(info.BG_COLOR)

    # first thing for outputting text, is to create the text object
    sorting_txt = info.LARGE_FONT.render(
        # for the string, we output the algo name, and the a ternary for ascending or descending
        f"{algo_name}: {'ASCENDING' if ascending else 'DESCENDING'}", 1, info.GREEN)
    # now, we can display the text to the WIN (pygame window):
    # we display it at coords: ((width / 2) - (text_width / 2), 5)
    # --> this displays it at x coord of the middle of the screen, and padded 5  down for y
    info.WIN.blit(sorting_txt, (info.width / 2 -
                  sorting_txt.get_width() / 2, 5))

    # same as above, but for the control text
    controls_txt = info.REG_FONT.render(
        "R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, info.BLACK)
    info.WIN.blit(controls_txt, (info.width / 2 -
                  controls_txt.get_width() / 2, 45))

    # same as above, but for the sorting algo text
    sorting_txt = info.REG_FONT.render(
        "I - Insertion Sort | B - Bubble Sort", 1, info.BLACK)
    info.WIN.blit(sorting_txt, (info.width / 2 -
                  sorting_txt.get_width() / 2, 75))

    # then, call the function to draw our list
    draw_list(info)

    # update the pygame display
    pygame.display.update()


# the function for drawing our list
def draw_list(info, color_pos={}, clear_bg=False):
    # to draw list, we have to determine the height of each item in the list,
    # and the x coordinate of each item in the list on the screen
    # --> then, we draw a rectangle with the information above

    # if the variable for clear_bg = True, that means we have to draw over the
    if clear_bg:
        # create a new rectangle with x,y, width, and height as such, to cover the entire sorting area:
        # x = half of the side padding = (100/2) = 50 for the x coord
        # y = the top padding = 100 = 100 pixels down for the y coord
        # width = the width - side_padding = width of the list area
        # height = the height - top_padding = height of the list area
        clear_rect = pygame.Rect(info.SIDE_PAD // 2, info.TOP_PAD,
                                 info.width - info.SIDE_PAD, info.height - info.TOP_PAD)
        # then, we draw the rectangle
        pygame.draw.rect(info.WIN, info.BG_COLOR, clear_rect)

    # * see docs/enumerate for info on enumerate

    # loop over each item in the list, getting the val, and the index i
    for i, val in enumerate(info.lst):
        # calculate the x position of the block, equal to:
        # --> the start x, + (the index times the block width)
        # --> each time the index increases, this means x is shifted block_width units right
        x = info.start_x + (i * info.block_width)

        # val - info.min_val gives how much larger than the min_val the current list item is
        # --> returns this as a value between the min, and max of the values in the array
        # then, we multiply this value by the height of each block, giving us height of current block
        # lastly, we subtract this from the height of the screen,
        # --> this gives us a y coordinate down from the top, which is where we start drawing from
        y = info.height - ((val - info.min_val) * info.block_height)

        # decide the colors by dividing the index by 3
        # --> this always return 0, 1, or 2,
        #   --> therefore will assign a color to the block randomly from the gradients
        color = info.GRADIENTS[i % 3]

        # if the current index is currentley being sorted (in color positions)
        if i in color_pos:
            # then we set the color of the current block to the one for sorting (red or green)
            color = color_pos[i]

        # now that we have all of the info, create a rectangle
        # we use x, y, and the info.block_width and info.height to create it
        block = pygame.Rect(x, y, info.block_width, info.height)

        # then, we can draw the rectangle to the screen (takes in: (window, color, rect_to_draw))
        pygame.draw.rect(info.WIN, color, block)

    # if the clear screen var is True, update the screen with the cleared rectangle
    if clear_bg:
        # manually update the screen, to make sure the clear rectangle overlays
        pygame.display.update()


#! sorting algorithim functions
# the function for our bubble sort algorithim
# since we yield a value, this is actually a generator
def bubble_sort(info, ascending=True):
    # get our list from the info object
    lst = info.lst
    # get the size of our list
    size = len(lst)

    # outer loop, to sort the first element size-1 times
    for i in range(size-1):
        # sort the elements
        for j in range(size - 1 - i):
            # get the element at index j, and the one after it (index j+1)
            num1 = lst[j]
            num2 = lst[j+1]

            # if ascending:
            # if the first element is greater than the second, swap them
            # OR
            # if descendin:
            # if the first element is less than the second, swap them
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                # both are swapped in the same way
                lst[j], lst[j+1] = lst[j+1], lst[j]

                # how the drawing works, is that we re-draw the mid-sort list after each swap
                # but, before we can do this, we have to draw a big white rectangle over the
                # current area where the list is drawn, so that we dont have overlap
                # so, in draw_list(), we draw a big block starting from the x and y after the padding,
                # and as big as the width and hieght - padding, to cover the entire area
                # then, we draw the list mid-sort, it won't have any issues with layering
                draw_list(info, {j: info.GREEN, j+1: info.RED}, True)

                # yield is in a generator, where after the current logic block (if...),
                # it pauses execution, and returns a value

                # this is useful because it means the function pauses in between each swap
                # --> this means we can use our controls in the middle of a sort
                yield True

    return lst


# function/generator for insertion sort
def insertion_sort(info, ascending=True):
    # get our list from the info object
    lst = info.lst
    # get the size of our list
    size = len(lst)

    # set up the first loop, from index 1, until the end (index 0 isnt checked in insertion sort)
    for i in range(1, size):
        # set the current element as the list at index i
        curr = lst[i]

        # while the loop is true
        while True:
            # there are two conditionals depending on if ascending or descending

            # the line for ascending:
            # so, if index i is not 0 (we havnt reaced end of loop), and the previous element is
            # greater than the current one (so we need to swap them), and ascenidng=True
            asc_sort = i > 0 and lst[i-1] > curr and ascending

            # the line for decending, same as above, except checks that current is larger than previous,
            # and that ascending is false
            desc_sort = i > 0 and lst[i-1] < curr and not ascending

            # if neither of these conditions are true, exit the loop (we are done sorting)
            if not asc_sort and not desc_sort:
                break

            # swap the elements
            lst[i] = lst[i-1]
            # decrement i, so that we check the second last element in the array, then third last, etc...
            i = i-1
            # change curr, so that it is the new element at list index i
            lst[i] = curr

            # finally, draw the list
            draw_list(info, {i-1: info.GREEN, i: info.RED}, True)

            # as with the bubble sort function, this is actually a generator, so we yield True
            # this allows us to pause in the middle of execution, or reset, etc..
            yield True


#! the main function for running the app
def run():
    # create the variables for our list creation
    list_n = 50
    min_val = 0
    max_val = 100

    # call the function to create our list, and assign it to var
    start_lst = gen_start_list(list_n, min_val, max_val)

    # instantiate our init_info class, using our list generated above
    info = init_info(800, 600, start_lst)

    # variables for run time (?sorting, ?ascending/descending)
    sorting = False
    # if ascending == True, then ascending order, if false then descending order
    ascending = True

    # variable for the current sorting algorithim
    curr_algo = bubble_sort
    # variable for the name of the current sorting algorithim, by default is bubble sort
    curr_algo_name = "Bubble Sort"
    # variable for the generator of the current sorting algorithim
    curr_algo_gen = None

    # create the pygame clock to regulate app run speed
    clock = pygame.time.Clock()

    # while the app is running
    while True:
        # tick the clock at 60 fps (run app at 60fps)
        clock.tick(info.SORT_SPEED)

        # get the next yield item in the generator
        # this will generate through each item in the list, until no more remain
        # each item will be sorted accordingly, until no items remain,
        # at that point, StopIterationException will be returned, and sorting is over
        # so in action, we first check if the algorithim is running (sorting = True)
        if sorting:
            # if so, we try to get the next object of the generator
            try:
                # if it works, the generator will start sorting the next element in the list
                next(curr_algo_gen)
            # if there is a StopIteration exception, we catch it
            except StopIteration:
                # then, we set sorting to false
                sorting = False
        # if the sorting variable is true, it will end up sorting during the generator,
        # otherwise, we have to manually output the window
        else:
            # output the pygame display by calling the draw_window function
            draw_window(info, curr_algo_name, ascending)

        # loop over each event that is triggered
        for event in pygame.event.get():
            # if the event type is quit (user pressed x)
            if event.type == pygame.QUIT:
                # quit the pygame program
                pygame.quit()

            # if the event is a keydown (user presses a key)
            if event.type == pygame.KEYDOWN:
                # if the user presses the r key (to reset)
                if event.key == pygame.K_r:
                    # generate a new list
                    lst = gen_start_list(list_n, min_val, max_val)
                    # then, set the list in our info class to the new one
                    info.set_list(lst)
                    # the next time the window is redrawn, this will be the new list

                    # finally, set the variable for sorting = False
                    sorting = False

                # if the user presses the space bar (to start sorting),
                # AND, the sorting variable is false (algorithim is not already running)
                if event.key == pygame.K_SPACE and not sorting:
                    # set the variable for sorting as true
                    sorting = True
                    # create the generator object, passing in info, and ascending
                    curr_algo_gen = curr_algo(info, ascending)

                # if the user presses the a key (sort by ascending),
                # AND, the sorting variable is false (algorithim is not already running)
                if event.key == pygame.K_a and not sorting:
                    # set the variable for ascending = True, so we sort in ascending order
                    ascending = True

                # if the user presses the d key (sort by descending),
                # AND, the sorting variable is false (algorithim is not already running)
                if event.key == pygame.K_d and not sorting:
                    # set the variable for ascending = False, so we sort in descending order
                    ascending = False

                # if the user presses the i key (insertion sort),
                # AND, the sorting variable is false (algorithim is not already running)
                if event.key == pygame.K_i and not sorting:
                    # change the current sorting algorithim
                    curr_algo = insertion_sort
                    # change the name of the current sorting algorithim
                    curr_algo_name = "Insertion Sort"

                # if the user presses the b key (bubble sort),
                # AND, the sorting variable is false (algorithim is not already running)
                if event.key == pygame.K_d and not sorting:
                    # change the current sorting algorithim
                    curr_algo = insertion_sort
                    # change the name of the current sorting algorithim
                    curr_algo_name = "Insertion Sort"
