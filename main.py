import sys
import math
import pathlib

import pygame as pg

from settings import *


def draw_ground(screen: pg.Surface, ground_surface: pg.Surface) -> None:
    screen_width, screen_height = screen.get_size()
    ground_width, ground_height = ground_surface.get_size()

    tiles_count = math.ceil(screen_width / ground_width)

    match round(screen_height / ground_height):
        case 2:
            ground_y = screen_height - ground_height // 4
        case 3:
            ground_y = screen_height - ground_height // 2
        case _:
            ground_y = screen_height - ground_height

    for i in range(tiles_count):
        screen.blit(ground_surface, (i * ground_width, ground_y))


def main():
    pg.init()
    pg.display.set_caption(SCREEN_CAPTION)
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()

    sky_surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    sky_surface.fill('skyblue')

    ground_surface = pg.image.load(pathlib.Path('graphics', 'ground.png')).convert()
    draw_ground(screen, ground_surface)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        screen.blit(sky_surface, (0, 0))
        draw_ground(screen, ground_surface)

        pg.display.update()
        clock.tick(MAX_FRAMERATE)


if __name__ == '__main__':
    main()
