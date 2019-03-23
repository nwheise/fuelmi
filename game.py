import os
import pygame
import pygameMenu


FPS = 30
SCREEN_WIDTH = 896
SCREEN_HEIGHT = 504
TEXT_SIZE = 30
BUTTON_SIZE = (100, 100)
PET_IMG_SIZE = (275, 275)


def text_to_screen(text: str, x: int, y: int, size: int, color: tuple, font_type: str):
    font = pygame.font.SysFont(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))


def main():
    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption('health pet')

    # Create global variables
    global screen, clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(color=(255, 255, 255))
    clock = pygame.time.Clock()

    # some stat
    time = 0

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

    # main loop
    running = True
    while running:
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if food_icon_button.collidepoint(mouse_pos):
                    text_to_screen(text='Clicked food!',
                       x=50,
                       y=50,
                       size=TEXT_SIZE,
                       color=(0, 0, 0),
                       font_type='Arial')
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


        time += 1 / FPS
        pygame.display.flip()
        clock.tick(FPS)


if __name__=="__main__":
    main()