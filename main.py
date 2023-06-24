from sys import exit
from math import ceil
from pathlib import Path

import pygame as pg

from settings import *


class Ground:
    def __init__(self, screen: pg.Surface, surface: pg.Surface):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()

        self.surface = surface
        self.surface_width, self.surface_height = self.surface.get_size()

        match round(self.screen_height / self.surface_height):
            case 2:
                self.surface_y_pos = self.screen_height - self.surface_height // 4
            case 3:
                self.surface_y_pos = self.screen_height - self.surface_height // 2
            case _:
                self.surface_y_pos = self.screen_height - self.surface_height

        self.surfaces_count = ceil(self.screen_width / self.surface_width)

    def render(self):
        for i in range(self.surfaces_count):
            self.screen.blit(self.surface, (i * self.surface_width, self.surface_y_pos))


def main():
    pg.init()
    pg.display.set_caption('Simple Game')
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()

    font = pg.font.Font(Path('graphics', 'fonts', 'Pixeltype.ttf'), 32)
    font_surface = font.render('Simple Game', False, 'black')
    font_rect = font_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))

    sky_surface = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    sky_surface.fill('skyblue')

    ground = Ground(screen, pg.image.load(Path('graphics', 'ground.png')).convert())

    ghost_surface = pg.image.load(Path('graphics', 'ghost.png')).convert_alpha()
    ghost_rect = ghost_surface.get_rect(midbottom=(600, ground.surface_y_pos))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        screen.blit(sky_surface, (0, 0))
        ground.render()
        screen.blit(font_surface, font_rect)

        ghost_rect.x -= 4
        if ghost_rect.x < -64:
            ghost_rect.x = 800
        screen.blit(ghost_surface, ghost_rect)

        pg.display.update()
        clock.tick(MAX_FRAMERATE)


if __name__ == '__main__':
    main()
