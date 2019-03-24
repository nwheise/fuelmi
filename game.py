import os
import pygame
import pygameMenu


FPS = 30
SCREEN_WIDTH = 896
SCREEN_HEIGHT = 504
TEXT_SIZE = 30
BUTTON_SIZE = (100, 100)
PET_IMG_SIZE = (275, 275)
BACKGROUND_COLOR = (255, 255, 255)
MENU_BACKGROUND_COLOR = (0, 240, 255)
NUMBER_SELECTORS = [(str(i), i) for i in range(10)]
STATUS_BAR_WIDTH = 208
STATUS_BAR_HEIGHT = 50

nutrition_level = 60
activity_level = 90
sleep_level = 30


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
    if value > 66:
        bar_color = (0, 180, 0)
    elif value > 33:
        bar_color = (255, 165, 0)
    else:
        bar_color = (255, 0, 0)

    percent_text = f'{value:2d}%'
    text_to_screen(text=percent_text,
                   x= x + STATUS_BAR_WIDTH + 20,
                   y= y + (STATUS_BAR_HEIGHT - TEXT_SIZE) // 2,
                   size=TEXT_SIZE,
                   color=(0, 0, 0),
                   font_type='consolas')

    pygame.draw.rect(screen, (0, 0, 0), (x, y, STATUS_BAR_WIDTH, STATUS_BAR_HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255), (x + 2, y + 2, STATUS_BAR_WIDTH - 4, STATUS_BAR_HEIGHT - 4))
    pygame.draw.rect(screen, bar_color, (x + 4, y + 4, (STATUS_BAR_WIDTH // 100) * value, STATUS_BAR_HEIGHT - 8))

    text_to_screen(text=stat_name,
                   x= x + 20,
                   y= y + (STATUS_BAR_HEIGHT - TEXT_SIZE) // 2,
                   size=TEXT_SIZE,
                   color=(0, 0, 0),
                   font_type='consolas')


def update_nutrition(change: int):
    global nutrition_level
    nutrition_level += change


def decrease_stats():
    global nutrition_level, activity_level, sleep_level
    nutrition_level -= 5
    activity_level -= 5
    sleep_level -= 5

def main():
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption('health pet')

    # Create global variables
    global screen, clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(color=BACKGROUND_COLOR)
    clock = pygame.time.Clock()

    # get icons
    food_icon = pygame.image.load(os.path.join('images', 'food_icon.png'))
    food_icon = pygame.transform.scale(food_icon, BUTTON_SIZE)
    activity_icon = pygame.image.load(os.path.join('images', 'activity_icon.png'))
    activity_icon = pygame.transform.scale(activity_icon, BUTTON_SIZE)
    sleep_icon = pygame.image.load(os.path.join('images', 'sleep_icon.png'))
    sleep_icon = pygame.transform.scale(sleep_icon, BUTTON_SIZE)

    # get image
    pet_image = pygame.image.load(os.path.join('images', 'tamagotchi.png'))
    pet_image = pygame.transform.scale(pet_image, PET_IMG_SIZE)

    # Menu
    FOOD = ['Fruits', 'Vegetables', 'Grains']
    food_menu = pygameMenu.TextMenu(surface=screen,
                                    bgfun=menu_background,
                                    enabled=False,
                                    font=pygameMenu.fonts.FONT_NEVIS,
                                    menu_alpha=90,
                                    onclose=pygameMenu.locals.PYGAME_MENU_CLOSE,
                                    title='Feed',
                                    title_offsety=5,
                                    window_height=SCREEN_HEIGHT,
                                    window_width=SCREEN_WIDTH)
    for m in FOOD:
        food_menu.add_selector(title=m,
                               values=NUMBER_SELECTORS,
                               onchange=None,
                               onreturn=update_nutrition)
    food_menu.add_option('Close', pygameMenu.locals.PYGAME_MENU_CLOSE)

    # main loop
    frame = 0
    running = True
    while running:
        # Paint background
        screen.fill(BACKGROUND_COLOR)

        # Progress bars
        render_progress_bar(stat_name='nutrition', value=nutrition_level, x=500, y=100)
        render_progress_bar(stat_name='activity', value=activity_level, x=500, y=175)
        render_progress_bar(stat_name='sleep', value=sleep_level, x=500, y=250)

        # Draw a button
        food_icon_button = screen.blit(food_icon,
                                       (SCREEN_WIDTH // 5, 3.5 * (SCREEN_HEIGHT // 5)))
        activity_icon_button = screen.blit(activity_icon,
                                           (2 * SCREEN_WIDTH // 5, 3.5 * (SCREEN_HEIGHT // 5)))
        sleep_icon_button = screen.blit(sleep_icon,
                                        (3 * SCREEN_WIDTH // 5, 3.5 * (SCREEN_HEIGHT // 5)))

        # Draw the image
        screen.blit(pet_image, (100, 50))

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
                    text_to_screen(text='Clicked activity!',
                       x=50,
                       y=100,
                       size=TEXT_SIZE,
                       color=(0, 0, 0),
                       font_type='Arial')
                elif sleep_icon_button.collidepoint(mouse_pos):
                    text_to_screen(text='Clicked sleep!',
                       x=50,
                       y=150,
                       size=TEXT_SIZE,
                       color=(0, 0, 0),
                       font_type='Arial')

        frame += FPS
        if frame % 9000 == 0:
            decrease_stats()

        pygame.display.update()
        clock.tick(FPS)


if __name__=="__main__":
    main()