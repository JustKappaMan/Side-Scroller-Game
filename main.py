import sys

import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((720, 480))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


if __name__ == '__main__':
    main()
