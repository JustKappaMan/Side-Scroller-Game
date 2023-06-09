import sys

import pygame

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480


def main():
    pygame.init()
    pygame.display.set_caption('Simple Game')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
