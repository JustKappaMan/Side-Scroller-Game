import sys

import pygame as pg


def main():
    pg.init()
    screen = pg.display.set_mode((720, 480))
    pg.display.set_caption('Simple Game')
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        pg.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
