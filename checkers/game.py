import pygame

from .board import Board
from .const import RED, WHITE, BLUE, SQUARE_SIZE


class Game:
    def __init__(self, win):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.win = win
        self.valid_moves = {}

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def select(self, row, col):
        if self.selected is not None:
            moved = self._move(row, col)
            if not moved:
                self.selected = None
                self.valid_moves = {}
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece is not None and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece is None and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def winner(self):
        return self.board.winner()

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()
