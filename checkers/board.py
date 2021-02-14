from .const import *
from .piece import Piece

STARTING_ROWS = 3


class Board:
    def __init__(self):
        self.board = []
        self.red_count = self.white_count = STARTING_ROWS * COLS // 2
        self.red_kings = self.white_kings = 0
        self.set_pieces()

    @staticmethod
    def _draw_squares(win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    @staticmethod
    def _is_legal_field(row, col):
        return row % 2 != col % 2

    def set_pieces(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if self._is_legal_field(row, col):
                    if row < STARTING_ROWS:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row >= ROWS - STARTING_ROWS:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(None)
                else:
                    self.board[row].append(None)

    def draw(self, window):
        self._draw_squares(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    piece.draw(window)

    def evaluate(self, color):
        evaluation = self.white_count - self.red_count + (self.white_kings * 0.5 - self.red_kings * 0.5)
        if color == WHITE:
            return evaluation
        else:
            return -evaluation

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece is not None and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col] = None
        self.board[row][col] = piece
        piece.move(row, col)

        if not piece.is_king and (row == ROWS - 1 or row == 0):
            if piece.color == RED:
                self.red_kings += 1
            else:
                self.white_kings += 1
            piece.set_king()

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_valid_moves(self, piece):
        moves = {}
        row = piece.row
        col = piece.col

        if piece.direction == Dir.Up or piece.is_king:
            moves.update(self._traverse(row, col, -1, piece.color, Dir.Left))
            moves.update(self._traverse(row, col, -1, piece.color, Dir.Right))
        if piece.direction == Dir.Down or piece.is_king:
            moves.update(self._traverse(row, col, 1, piece.color, Dir.Left))
            moves.update(self._traverse(row, col, 1, piece.color, Dir.Right))

        return moves

    def _traverse(self, row, col, step, color, direction, skipped=None):
        if skipped is None:
            skipped = []
        moves = {}
        last_skipped = []

        start_row = row + step

        for r in range(start_row, start_row + 2 * step, step):
            if direction == Dir.Left:
                col -= 1
            else:
                col += 1

            if r < 0 or r >= ROWS or col < 0 or col >= COLS:
                break

            current_square = self.board[r][col]
            if current_square is None:
                if not skipped and r == start_row:
                    moves[(r, col)] = []

                if last_skipped:
                    moves[(r, col)] = last_skipped + skipped
                    skipped += last_skipped
                    moves.update(self._traverse(r, col, step, color, Dir.Left, skipped))
                    moves.update(self._traverse(r, col, step, color, Dir.Right, skipped))
                break
            elif current_square.color == color:
                break
            else:
                last_skipped = [current_square]

        return moves

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = None
            if piece is not None:
                if piece.color == RED:
                    self.red_count -= 1
                else:
                    self.white_count -= 1

    def winner(self):
        if self.red_count <= 0:
            return WHITE
        elif self.white_count <= 0:
            return RED
        return None
