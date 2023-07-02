from sys import exit
from math import ceil
from pathlib import Path
from random import randint, choice

import pygame as pg

from settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, position: tuple[int, int]):
        super().__init__()
        self.image = pg.image.load(Path('graphics', 'player.png')).convert()
        self.rect = self.image.get_rect(midbottom=position)
        self.gravity = 0
        self.jump_gravity = -22
        self.initial_position = position

    def handle_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and self.rect.bottom >= self.initial_position[1]:
            self.gravity = self.jump_gravity

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= self.initial_position[1]:
            self.rect.bottom = self.initial_position[1]

    def update(self):
        self.handle_input()
        self.apply_gravity()


class Enemy(pg.sprite.Sprite):
    def __init__(self, surf_y_pos: int, screen_width: int):
        super().__init__()
        self.speed = 4
        self.kind = choice(('running', 'flying'))
        match self.kind:
            case 'running':
                self.image = pg.image.load(Path('graphics', 'running_enemy.png')).convert()
                self.rect = self.image.get_rect(midbottom=(
                    randint(screen_width + 256, screen_width + 512), surf_y_pos))
            case 'flying':
                self.image = pg.image.load(Path('graphics', 'flying_enemy.png')).convert()
                self.rect = self.image.get_rect(midbottom=(
                    randint(screen_width + 256, screen_width + 512), surf_y_pos - 64))

    def update(self):
        self.rect.x -= self.speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -self.rect.width:
            self.kill()


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
        self.surf = surf
        self.surfs_count = ceil(screen.get_width() / surf.get_width())

        match round(screen.get_height() / self.surf.get_height()):
            case 2:
                self.surf_y_pos = screen.get_height() - surf.get_height() // 4
            case 3:
                self.surf_y_pos = screen.get_height() - surf.get_height() // 2
            case _:
                self.surf_y_pos = screen.get_height() - surf.get_height()

    def render(self):
        for i in range(self.surfs_count):
            self.screen.blit(self.surf, (i * self.surf.get_width(), self.surf_y_pos))


class FPSCounter:
    def __init__(self, screen: pg.Surface, clock: pg.time.Clock):
        self.screen = screen
        self.clock = clock
        self.font = pg.font.SysFont('Arial', 16, bold=True)
        self.color = pg.color.Color('red')
        self.position = (screen.get_width() - 8, 8)
        self.fps = None
        self.surf = None
        self.rect = None

    def render(self):
        self.fps = f'{int(self.clock.get_fps())}'
        self.surf = self.font.render(self.fps, True, self.color)
        self.rect = self.surf.get_rect(topright=self.position)
        self.screen.blit(self.surf, self.rect)


class ScoreCounter:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.font = pg.font.SysFont('Arial', 16, bold=True)
        self.color = pg.color.Color('darkgreen')
        self.position = (8, 8)
        self.start_score = 0
        self.current_score = 0
        self.score_divisor = 100
        self.surf = None
        self.rect = None

    def render(self):
        self.current_score = pg.time.get_ticks() // self.score_divisor - self.start_score
        self.surf = self.font.render(f'Score: {self.current_score}', True, self.color)
        self.rect = self.surf.get_rect(topleft=self.position)
        self.screen.blit(self.surf, self.rect)

    def refresh(self):
        self.start_score = pg.time.get_ticks() // self.score_divisor


class StartScreen:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.background_color = pg.color.Color('darkgreen')
        self.font = pg.font.SysFont('Arial', 32, bold=True)
        self.font_surf = self.font.render('Press Space to run', True, pg.color.Color('yellow'))
        self.font_rect = self.font_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    def render(self):
        self.screen.fill(self.background_color)
        self.screen.blit(self.font_surf, self.font_rect)


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

    sky = Sky(screen)
    ground = Ground(screen, pg.image.load(Path('graphics', 'ground.png')).convert())

    fps_counter = FPSCounter(screen, clock)
    score_counter = ScoreCounter(screen)
    start_screen = StartScreen(screen)
    game_over_screen = GameOverScreen(screen)

    player_group = pg.sprite.GroupSingle()
    player_group.add(Player((64, ground.surf_y_pos)))

    enemies_group = pg.sprite.Group()
    enemy_timer = pg.USEREVENT + 1
    pg.time.set_timer(enemy_timer, 1800)

    game_is_active = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                exit()

            if game_is_active:
                if event.type == enemy_timer:
                    enemies_group.add(Enemy(ground.surf_y_pos, screen.get_width()))
            else:
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    score_counter.refresh()
                    game_is_active = True

        if game_is_active:
            sky.render()
            ground.render()
            fps_counter.render()
            score_counter.render()

            player_group.draw(screen)
            player_group.update()

            enemies_group.draw(screen)
            enemies_group.update()

            if pg.sprite.spritecollide(player_group.sprite, enemies_group, False):
                enemies_group.empty()
                game_is_active = False
        else:
            if score_counter.current_score == 0:
                start_screen.render()
            else:
                game_over_screen.render()

        pg.display.update()
        clock.tick(MAX_FRAMERATE)


if __name__ == '__main__':
    main()
