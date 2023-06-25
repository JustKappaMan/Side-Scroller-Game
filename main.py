from sys import exit
from math import ceil
from pathlib import Path

import pygame as pg

from settings import *


class Sky:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.surface = pg.Surface(self.screen.get_size())
        self.surface.fill('skyblue')
        self.surface_pos = (0, 0)

    def render(self):
        self.screen.blit(self.surface, self.surface_pos)


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


class FPSCounter:
    def __init__(self, screen: pg.Surface, clock: pg.time.Clock):
        self.screen = screen
        self.clock = clock
        self.font = pg.font.SysFont('Arial', 16, bold=True)
        self.color = 'red'
        self.position = (8, 8)
        self.fps = None

    def render(self):
        self.fps = f'{int(self.clock.get_fps())}'
        self.screen.blit(self.font.render(self.fps, True, self.color), self.position)


def main():
    pg.init()
    pg.display.set_caption('Simple Game')
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()

    sky = Sky(screen)
    ground = Ground(screen, pg.image.load(Path('graphics', 'ground.png')).convert())

    ghost_surface = pg.image.load(Path('graphics', 'ghost.png')).convert_alpha()
    ghost_rect = ghost_surface.get_rect(midbottom=(screen.get_width() + 64, ground.surface_y_pos))

    fps_counter = FPSCounter(screen, clock)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    exit()

        sky.render()
        ground.render()

        ghost_rect.x -= 4
        if ghost_rect.x < -64:
            ghost_rect.x = screen.get_width() + 64
        screen.blit(ghost_surface, ghost_rect)

        fps_counter.render()

        pg.display.update()
        clock.tick(MAX_FRAMERATE)


if __name__ == '__main__':
    main()
