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


class Sprite:
    def __init__(self, screen: pg.display, filepath: Path):
        self.screen = screen
        self.image = pg.image.load(filepath)
        self.x_position = None
        self.y_position = None

    def set_position(self, x_position: int, y_position: int):
        screen_width, screen_height = self.screen.get_size()
        image_width, image_height = self.image.get_size()

        min_x_position = SCREEN_PADDING
        max_x_position = screen_width - SCREEN_PADDING - image_width // 2

        if x_position < min_x_position or x_position > max_x_position:
            raise ValueError(f'{x_position=}, correct values are {min_x_position}...{max_x_position}')

        min_y_position = SCREEN_PADDING
        max_y_position = screen_height - SCREEN_PADDING - image_height // 2

        if y_position < min_y_position or y_position > max_y_position:
            raise ValueError(f'{y_position=}, correct values are {min_y_position}...{max_y_position}')

        self.x_position, self.y_position = x_position, y_position
        self.draw()

    def set_random_position(self):
        screen_width, screen_height = self.screen.get_size()
        image_width, image_height = self.image.get_size()

        self.x_position = randint(SCREEN_PADDING, screen_width - SCREEN_PADDING - image_width // 2)
        self.y_position = randint(SCREEN_PADDING, screen_height - SCREEN_PADDING - image_height // 2)
        self.draw()

    def draw(self):
        self.screen.blit(self.image, (self.x_position, self.y_position))


def main():
    pg.init()
    pg.display.set_caption('Simple Game')
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()

    grass = pg.image.load(Path('graphics', 'grass.png'))
    tile_background(screen, grass)

    cherry = Sprite(screen, Path('graphics', 'cherry.png'))
    cherry.set_random_position()

    ghost = Sprite(screen, Path('graphics', 'ghost.png'))
    ghost.set_random_position()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            keys = pg.key.get_pressed()

            if keys[pg.K_w]:
                tile_background(screen, grass)
                cherry.draw()
                ghost.set_position(ghost.x_position, ghost.y_position - 4)
            if keys[pg.K_a]:
                tile_background(screen, grass)
                cherry.draw()
                ghost.set_position(ghost.x_position - 4, ghost.y_position)
            if keys[pg.K_s]:
                tile_background(screen, grass)
                cherry.draw()
                ghost.set_position(ghost.x_position, ghost.y_position + 4)
            if keys[pg.K_d]:
                tile_background(screen, grass)
                cherry.draw()
                ghost.set_position(ghost.x_position + 4, ghost.y_position)

        pg.display.update()
        clock.tick(FRAMERATE_LIMIT)


if __name__ == '__main__':
    main()
