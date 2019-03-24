import os
import pygame
import pygameMenu

# Define some constant values
FPS = 30

SCREEN_WIDTH = 896
SCREEN_HEIGHT = 504
STATUS_BAR_WIDTH = 208
STATUS_BAR_HEIGHT = 50
TEXT_SIZE = 30
BUTTON_SIZE = (100, 100)
PET_IMG_SIZE = (275, 275)

BACKGROUND_COLOR = (255, 255, 255)
MENU_BACKGROUND_COLOR = (0, 240, 255)

NUMBER_SELECTORS = [(str(i), i) for i in range(10)]
MINUTES_SELECTORS = [(str(i*10), i*10) for i in range(10)]
FOODS = ['Fruits', 'Vegetables', 'Water', 'Junk']

# Define the primary stats
nutrition = {'Fruits': 30, 'Vegetables': 60, 'Water': 40, 'Junk': 0}
activity_level = 60
sleep_level = 35


def text_to_screen(text: str, x: int, y: int, size: int, color: tuple, font_type: str):
    '''
    A simple function for blitting text on the screen
    '''
    font = pygame.font.SysFont(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))


def menu_background():
    '''
    Function to fill the background when a menu pops up
    '''
    screen.fill(MENU_BACKGROUND_COLOR)


def render_progress_bar(stat_name: str, value: int, x: int, y: int):
    '''
    Display a progress bar, which varies in color depending on percentage. The
    stat name is displayed on the bar and the percentage as a number is displayed
    to the right.
    '''
    if value > 66:
        bar_color = (0, 180, 0)
    elif value > 33:
        bar_color = (255, 165, 0)
    else:
        bar_color = (255, 0, 0)

    # Display the percent number
    percent_text = f'{int(value)}%'
    text_to_screen(text=percent_text,
                   x= x + STATUS_BAR_WIDTH + 20,
                   y= y + (STATUS_BAR_HEIGHT - TEXT_SIZE) // 2,
                   size=TEXT_SIZE,
                   color=(0, 0, 0),
                   font_type='consolas')

    # Draw the bar itself
    pygame.draw.rect(screen, (0, 0, 0), (x, y, STATUS_BAR_WIDTH, STATUS_BAR_HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255), (x + 2, y + 2, STATUS_BAR_WIDTH - 4, STATUS_BAR_HEIGHT - 4))
    pygame.draw.rect(screen, bar_color, (x + 4, y + 4, (STATUS_BAR_WIDTH // 100) * value, STATUS_BAR_HEIGHT - 8))

    # Write a label on the bar
    text_to_screen(text=stat_name,
                   x= x + 20,
                   y= y + (STATUS_BAR_HEIGHT - TEXT_SIZE) // 2,
                   size=TEXT_SIZE,
                   color=(0, 0, 0),
                   font_type='consolas')


def update_nutrition(change: int, **kwargs):
    '''
    Update nutrition, specifically by what type of food was eaten and the
    number of servings.
    '''
    global nutrition

    key = kwargs['food_type']
    if key == 'Water':
        nutrition[key] += change*10
    else:
        nutrition[key] += change*20

    if nutrition[key] > 100:
        nutrition[key] = 100


def calculate_nutrition():
    '''
    Calculate a nutrition score in [0, 100] by weighting each food type score
    '''
    return 0.25 * nutrition['Fruits'] + \
           0.25 * nutrition['Vegetables'] + \
           0.5 * nutrition['Water'] - \
           0.5 * nutrition['Junk']


def update_sleep(change: int):
    '''
    Increase sleep level based on hours slept.
    '''
    global sleep_level

    if 0 < change < 3:
        sleep_level += 20
    elif change < 5:
        sleep_level += 50
    elif change < 7:
        sleep_level += 80
    else:
        sleep_level = 100

    if sleep_level > 100:
        sleep_level = 100


def update_activity(change: int):
    '''
    Increase activity level based on minutes active
    '''
    global activity_level

    activity_level += change
    if activity_level > 100:
        activity_level = 100


def decrease_stats():
    '''
    Decrease all stats (nutrition, activity, and sleep)
    '''
    global nutrition, activity_level, sleep_level

    for key in nutrition:
        nutrition[key] -= 5
        if nutrition[key] < 0:
            nutrition[key] = 0

    activity_level -= 5    
    if activity_level < 0:
        activity_level = 0

    sleep_level -= 5
    if sleep_level < 0:
        sleep_level = 0


def create_food_menu():
    '''
    Create and return a TextMenu for selecting what has been eaten.
    '''
    food_menu = pygameMenu.TextMenu(surface=screen,
                                    bgfun=menu_background,
                                    enabled=False,
                                    font=pygameMenu.fonts.FONT_NEVIS,
                                    menu_alpha=90,
                                    onclose=pygameMenu.locals.PYGAME_MENU_CLOSE,
                                    title='Eat',
                                    title_offsety=5,
                                    window_height=SCREEN_HEIGHT,
                                    window_width=SCREEN_WIDTH)
    for m in FOODS:
        food_menu.add_selector(title=m,
                               values=NUMBER_SELECTORS,
                               onchange=None,
                               onreturn=update_nutrition,
                               food_type=m)

    return food_menu


def create_sleep_menu():
    '''
    Create and return a TextMenu for how many hours slept
    '''
    sleep_menu = pygameMenu.TextMenu(surface=screen,
                                     bgfun=menu_background,
                                     enabled=False,
                                     font=pygameMenu.fonts.FONT_NEVIS,
                                     menu_alpha=90,
                                     onclose=pygameMenu.locals.PYGAME_MENU_CLOSE,
                                     title='Sleep',
                                     title_offsety=5,
                                     window_height=SCREEN_HEIGHT,
                                     window_width=SCREEN_WIDTH)
    sleep_menu.add_selector(title='Hours Slept',
                            values=NUMBER_SELECTORS,
                            onchange=None,
                            onreturn=update_sleep)

    return sleep_menu


def create_activity_menu():
    '''
    Create and return a TextMenu for how many hours slept
    '''
    activity_menu = pygameMenu.TextMenu(surface=screen,
                                        bgfun=menu_background,
                                        enabled=False,
                                        font=pygameMenu.fonts.FONT_NEVIS,
                                        menu_alpha=90,
                                        onclose=pygameMenu.locals.PYGAME_MENU_CLOSE,
                                        title='Exercise',
                                        title_offsety=5,
                                        window_height=SCREEN_HEIGHT,
                                        window_width=SCREEN_WIDTH)
    activity_menu.add_selector(title='Active Minutes',
                               values=MINUTES_SELECTORS,
                               onchange=None,
                               onreturn=update_activity)

    return activity_menu


def main():
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption('FuelMi')

    # Create global variables
    global screen, clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(color=BACKGROUND_COLOR)
    clock = pygame.time.Clock()

    # get icons for buttons
    food_icon = pygame.image.load(os.path.join('images', 'food_icon.png'))
    food_icon = pygame.transform.scale(food_icon, BUTTON_SIZE)
    activity_icon = pygame.image.load(os.path.join('images', 'activity_icon.png'))
    activity_icon = pygame.transform.scale(activity_icon, BUTTON_SIZE)
    sleep_icon = pygame.image.load(os.path.join('images', 'sleep_icon.png'))
    sleep_icon = pygame.transform.scale(sleep_icon, BUTTON_SIZE)

    # get images
    normal_image = pygame.image.load(os.path.join('images', 'pogchamp.png'))
    normal_image = pygame.transform.scale(normal_image, PET_IMG_SIZE)
    tired_image = pygame.image.load(os.path.join('images', 'residentsleeper.png'))
    tired_image = pygame.transform.scale(tired_image, PET_IMG_SIZE)
    hungry_image = pygame.image.load(os.path.join('images', 'babyrage.png'))
    hungry_image = pygame.transform.scale(hungry_image, PET_IMG_SIZE)
    low_activity_image = pygame.image.load(os.path.join('images', 'kappa.jpg'))
    low_activity_image = pygame.transform.scale(low_activity_image, PET_IMG_SIZE)

    # create menus
    food_menu = create_food_menu()
    sleep_menu = create_sleep_menu()
    activity_menu = create_activity_menu()

    # main loop
    frame = 0
    running = True
    while running:
        # Paint background
        screen.fill(BACKGROUND_COLOR)

        # Progress bars
        nutrition_summary = calculate_nutrition()
        render_progress_bar(stat_name='nutrition', value=nutrition_summary, x=450, y=100)
        render_progress_bar(stat_name='activity', value=activity_level, x=450, y=175)
        render_progress_bar(stat_name='sleep', value=sleep_level, x=450, y=250)

        # Draw buttons
        food_icon_button = screen.blit(food_icon,
                                       (SCREEN_WIDTH // 5, 3.5 * (SCREEN_HEIGHT // 5)))
        activity_icon_button = screen.blit(activity_icon,
                                           (2 * SCREEN_WIDTH // 5, 3.5 * (SCREEN_HEIGHT // 5)))
        sleep_icon_button = screen.blit(sleep_icon,
                                        (3 * SCREEN_WIDTH // 5, 3.5 * (SCREEN_HEIGHT // 5)))

        # Draw the image
        image_position = (125, 75)
        if sleep_level < 33:
            screen.blit(tired_image, image_position)
        elif nutrition_summary < 33:
            screen.blit(hungry_image, image_position)
        elif activity_level < 33:
            screen.blit(low_activity_image, image_position)
        else:
            screen.blit(normal_image, image_position)

        # Handle events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if food_icon_button.collidepoint(mouse_pos):
                    food_menu.enable()
                    food_menu.mainloop(events)
                elif activity_icon_button.collidepoint(mouse_pos):
                    activity_menu.enable()
                    activity_menu.mainloop(events)
                elif sleep_icon_button.collidepoint(mouse_pos):
                    sleep_menu.enable()
                    sleep_menu.mainloop(events)

        frame += FPS
        if frame % 9000 == 0:
            decrease_stats()

        pygame.display.update()
        clock.tick(FPS)


if __name__=="__main__":
    main()