import pygame as pg


class FPSCounter:
    def __init__(self, screen: pg.Surface, clock: pg.time.Clock):
        self.screen = screen
        self.clock = clock
        self.font = pg.font.SysFont("Arial", 16, bold=True)
        self.color = pg.color.Color("red")
        self.position = (screen.get_width() - 8, 8)
        self.fps = None
        self.surf = None
        self.rect = None

    def render(self):
        self.fps = f"{int(self.clock.get_fps())}"
        self.surf = self.font.render(self.fps, True, self.color)
        self.rect = self.surf.get_rect(topright=self.position)
        self.screen.blit(self.surf, self.rect)


class ScoreCounter:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.font = pg.font.SysFont("Arial", 16, bold=True)
        self.color = pg.color.Color("darkgreen")
        self.position = (8, 8)
        self.start_score = 0
        self.current_score = 0
        self.score_divisor = 100
        self.surf = None
        self.rect = None

    def render(self):
        self.current_score = pg.time.get_ticks() // self.score_divisor - self.start_score
        self.surf = self.font.render(f"Score: {self.current_score}", True, self.color)
        self.rect = self.surf.get_rect(topleft=self.position)
        self.screen.blit(self.surf, self.rect)

    def refresh(self):
        self.start_score = pg.time.get_ticks() // self.score_divisor
