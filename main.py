import sys

import pygame as pg

from settings import *


def main():
    pg.init()
    pg.display.set_caption(SCREEN_CAPTION)
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        pg.display.update()
        clock.tick(MAX_FRAMERATE)


if __name__ == '__main__':
    main()
