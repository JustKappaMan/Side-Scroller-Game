from sys import exit
from math import ceil
from pathlib import Path

import pygame

from settings import *


def tile_background(screen: pygame.display, image: pygame.Surface) -> None:
    screen_width, screen_height = screen.get_size()
    image_width, image_height = image.get_size()

    x_tiles_count = ceil(screen_width / image_width)
    y_tiles_count = ceil(screen_height / image_height)

    for x in range(x_tiles_count):
        for y in range(y_tiles_count):
            screen.blit(image, (x * image_width, y * image_height))


def main():
    pygame.init()
    pygame.display.set_caption('Simple Game')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    grass_surface = pygame.image.load(Path('graphics', 'grass.png'))
    tile_background(screen, grass_surface)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(FRAMERATE_LIMIT)


if __name__ == '__main__':
    main()
