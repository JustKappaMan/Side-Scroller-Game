from sys import exit
from math import ceil
from pathlib import Path
from random import randint, choice

import pygame as pg

from settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, initial_position: tuple[int, int]):
        super().__init__()
        self.image = pg.image.load(Path('graphics', 'player.png')).convert()
        self.rect = self.image.get_rect(midbottom=initial_position)
        self.initial_position = initial_position

        self.gravity = 0
        self.jump_gravity = -22

        self.jump_sounds = (pg.mixer.Sound(Path('audio', 'jump1.ogg')),
                            pg.mixer.Sound(Path('audio', 'jump2.ogg')),
                            pg.mixer.Sound(Path('audio', 'jump3.ogg')))
        for sound in self.jump_sounds:
            sound.set_volume(0.5)

    def handle_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and self.rect.bottom >= self.initial_position[1]:
            self.gravity = self.jump_gravity
            choice(self.jump_sounds).play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= self.initial_position[1]:
            self.rect.bottom = self.initial_position[1]

    def update(self):
        self.handle_input()
        self.apply_gravity()


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 5
        if randint(0, 2):
            self.image = pg.image.load(Path('graphics', 'running_enemy.png')).convert()
            self.rect = self.image.get_rect(midbottom=(
                randint(game.screen.get_width() + 256, game.screen.get_width() + 512), game.ground.surf_y_pos))
        else:
            self.image = pg.image.load(Path('graphics', 'flying_enemy.png')).convert()
            self.rect = self.image.get_rect(midbottom=(
                randint(game.screen.get_width() + 256, game.screen.get_width() + 512), game.ground.surf_y_pos - 64))

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
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.surf = pg.image.load(Path('graphics', 'ground.png')).convert()
        self.surfs_count = ceil(screen.get_width() / self.surf.get_width())

        match round(screen.get_height() / self.surf.get_height()):
            case 2:
                self.surf_y_pos = screen.get_height() - self.surf.get_height() // 4
            case 3:
                self.surf_y_pos = screen.get_height() - self.surf.get_height() // 2
            case _:
                self.surf_y_pos = screen.get_height() - self.surf.get_height()

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


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Simple Game')
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()

        self.background_music = pg.mixer.Sound(Path('audio', 'soundtrack.ogg'))
        self.background_music.set_volume(0.5)
        self.background_music.play(loops=-1)

        self.start_screen = StartScreen(self.screen)
        self.game_over_screen = GameOverScreen(self.screen)

        self.sky = Sky(self.screen)
        self.ground = Ground(self.screen)

        self.fps_counter = FPSCounter(self.screen, self.clock)
        self.score_counter = ScoreCounter(self.screen)

        self.player = pg.sprite.GroupSingle()
        # noinspection PyTypeChecker
        self.player.add(Player((64, self.ground.surf_y_pos)))

        self.enemies = pg.sprite.Group()
        self.enemy_timer = pg.USEREVENT + 1
        pg.time.set_timer(self.enemy_timer, 1800)

        self.is_active = False

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    exit()

                if self.is_active:
                    if event.type == self.enemy_timer:
                        # noinspection PyTypeChecker
                        self.enemies.add(Enemy())
                else:
                    if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                        self.score_counter.refresh()
                        self.is_active = True

            if self.is_active:
                self.sky.render()
                self.ground.render()
                self.fps_counter.render()
                self.score_counter.render()

                self.player.draw(self.screen)
                self.player.update()

                self.enemies.draw(self.screen)
                self.enemies.update()

                if pg.sprite.spritecollide(self.player.sprite, self.enemies, False):
                    self.enemies.empty()
                    self.is_active = False
            else:
                if self.score_counter.current_score == 0:
                    self.start_screen.render()
                else:
                    self.game_over_screen.render()

            pg.display.update()
            self.clock.tick(MAX_FRAMERATE)


if __name__ == '__main__':
    game = Game()
    game.run()
