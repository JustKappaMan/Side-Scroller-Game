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


class ScoreCounter:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.font = pg.font.SysFont('Arial', 16, bold=True)
        self.color = pg.color.Color('darkgreen')
        self.position = (screen.get_width() - 8, 8)
        self.start_score = 0
        self.score = None
        self.surf = None
        self.rect = None

    def render(self):
        self.score = pg.time.get_ticks() - self.start_score
        self.surf = self.font.render(f'{self.score}', True, self.color)
        self.rect = self.surf.get_rect(topright=self.position)
        self.screen.blit(self.surf, self.rect)

    def refresh(self):
        self.start_score = pg.time.get_ticks()


class GameOverScreen:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.background_color = pg.color.Color('red')
        self.font = pg.font.SysFont('Arial', 32, bold=True)
        self.font_surf = self.font.render('Game Over', True, pg.color.Color('yellow'))
        self.font_rect = self.font_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    def render(self):
        self.screen.fill(self.background_color)
        self.screen.blit(self.font_surf, self.font_rect)


def main():
    pg.init()
    pg.display.set_caption('Simple Game')
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()

    game_is_active = True

    sky = Sky(screen)
    ground = Ground(screen, pg.image.load(Path('graphics', 'ground.png')).convert())

    player_surf = pg.image.load(Path('graphics', 'player.png')).convert()
    player_rect = player_surf.get_rect(midbottom=(64, ground.surf_y_pos))
    player_gravity = 0

    enemy_surf = pg.image.load(Path('graphics', 'enemy.png')).convert()
    enemy_rect = enemy_surf.get_rect(midbottom=(screen.get_width() + 64, ground.surf_y_pos))

    fps_counter = FPSCounter(screen, clock)
    score_counter = ScoreCounter(screen)
    game_over_screen = GameOverScreen(screen)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    exit()

            if game_is_active:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE and player_rect.bottom >= ground.surf_y_pos:
                        player_gravity = -22
            else:
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    enemy_rect.x = screen.get_width() + 64
                    score_counter.refresh()
                    game_is_active = True

        if game_is_active:
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

            if enemy_rect.colliderect(player_rect):
                game_is_active = False

            fps_counter.render()
            score_counter.render()
        else:
            game_over_screen.render()

        pg.display.update()
        clock.tick(MAX_FRAMERATE)


if __name__ == '__main__':
    main()
