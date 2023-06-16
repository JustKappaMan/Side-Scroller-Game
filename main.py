from sys import exit
from math import ceil
from pathlib import Path
from random import randint

import pygame as pg

from settings import *


def tile_background(screen: pg.display, image: pg.Surface) -> None:
    screen_width, screen_height = screen.get_size()
    image_width, image_height = image.get_size()

    x_tiles_count = ceil(screen_width / image_width)
    y_tiles_count = ceil(screen_height / image_height)

    for x in range(x_tiles_count):
        for y in range(y_tiles_count):
            screen.blit(image, (x * image_width, y * image_height))


def place_image_randomly(screen: pg.display, image: pg.Surface) -> None:
    screen_width, screen_height = screen.get_size()
    image_width, image_height = image.get_size()

    screen.blit(image, (
        randint(SCREEN_PADDING, screen_width - SCREEN_PADDING - image_width // 2),
        randint(SCREEN_PADDING, screen_height - SCREEN_PADDING - image_height // 2)
    ))


def main():
    pg.init()
    pg.display.set_caption('Simple Game')
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()

    grass = pg.image.load(Path('graphics', 'grass.png'))
    tile_background(screen, grass)

    cherry = pg.transform.scale(pg.image.load(Path('graphics', 'cherry.png')), (50, 50))
    place_image_randomly(screen, cherry)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    place_image_randomly(screen, cherry)
                    print('Randomly placing another cherry')

        pg.display.update()
        clock.tick(FRAMERATE_LIMIT)

if __name__ == '__main__':
    main()
