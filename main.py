from sys import exit
from pathlib import Path

import pygame

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480
FRAMERATE_LIMIT = 60


def main():
    pygame.init()
    pygame.display.set_caption('Simple Game')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    background_surface = pygame.image.load(Path('graphics', 'grass.png'))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(background_surface, (0, 0))

        pygame.display.update()
        clock.tick(FRAMERATE_LIMIT)


if __name__ == '__main__':
    main()
