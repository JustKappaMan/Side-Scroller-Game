from sys import exit
from math import ceil
from pathlib import Path

import pygame as pg

from settings import *


class Sky:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.surf = pg.Surface(screen.get_size())
        self.surf.fill(pg.color.Color('skyblue'))
        self.surf_pos = (0, 0)

    def render(self):
        self.screen.blit(self.surf, self.surf_pos)


class Ground:
    def __init__(self, screen: pg.Surface, surf: pg.Surface):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        self.surf = surf
        self.surf_width, self.surf_height = surf.get_size()

        match round(self.screen_height / self.surf_height):
            case 2:
                self.surf_y_pos = self.screen_height - self.surf_height // 4
            case 3:
                self.surf_y_pos = self.screen_height - self.surf_height // 2
            case _:
                self.surf_y_pos = self.screen_height - self.surf_height

        self.surfs_count = ceil(self.screen_width / self.surf_width)

    def render(self):
        for i in range(self.surfs_count):
            self.screen.blit(self.surf, (i * self.surf_width, self.surf_y_pos))


class FPSCounter:
    def __init__(self, screen: pg.Surface, clock: pg.time.Clock):
        self.screen = screen
        self.clock = clock
        self.font = pg.font.SysFont('Arial', 16, bold=True)
        self.color = pg.color.Color('red')
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

    player_surf = pg.image.load(Path('graphics', 'player.png')).convert()
    player_rect = player_surf.get_rect(midbottom=(64, ground.surf_y_pos))
    player_gravity = 0

    enemy_surf = pg.image.load(Path('graphics', 'enemy.png')).convert()
    enemy_rect = enemy_surf.get_rect(midbottom=(screen.get_width() + 64, ground.surf_y_pos))

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
                if event.key == pg.K_SPACE:
                    player_gravity = -20

        sky.render()
        ground.render()

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= ground.surf_y_pos:
            player_rect.bottom = ground.surf_y_pos
        screen.blit(player_surf, player_rect)

        enemy_rect.x -= 4
        if enemy_rect.x < -64:
            enemy_rect.x = screen.get_width() + 64
        screen.blit(enemy_surf, enemy_rect)

        fps_counter.render()

        pg.display.update()
        clock.tick(MAX_FRAMERATE)


if __name__ == '__main__':
    main()
