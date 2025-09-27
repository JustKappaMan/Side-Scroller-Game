import pygame as pg


class StartScreen:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.background_color = pg.color.Color("darkgreen")
        self.font = pg.font.SysFont("Arial", 32, bold=True)
        self.font_surf = self.font.render("Press S to start", True, pg.color.Color("yellow"))
        self.font_rect = self.font_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    def render(self):
        self.screen.fill(self.background_color)
        self.screen.blit(self.font_surf, self.font_rect)


class GameOverScreen:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.background_color = pg.color.Color("red")
        self.font = pg.font.SysFont("Arial", 32, bold=True)
        self.font_surf = self.font.render("Press S to restart", True, pg.color.Color("yellow"))
        self.font_rect = self.font_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    def render(self):
        self.screen.fill(self.background_color)
        self.screen.blit(self.font_surf, self.font_rect)
