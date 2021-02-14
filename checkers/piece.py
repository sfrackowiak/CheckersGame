import pygame

from .const import RED, SQUARE_SIZE, GREY, CROWN, Dir


class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.is_king = False

        if self.color == RED:
            self.direction = Dir.Up
        else:
            self.direction = Dir.Down

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def set_king(self):
        self.is_king = True

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.is_king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def __repr__(self):
        return str(self.color)
