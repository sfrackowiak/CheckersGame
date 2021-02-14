import time

import pygame

from checkers.const import WIDTH, HEIGHT, SQUARE_SIZE, WHITE, RED, DEPTH
from checkers.game import Game
from minimax.algorithm import minimax

FPS = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def print_end_message(is_winner):
    if is_winner:
        print('You won')
    else:
        print('You lost')


def main():
    clock = pygame.time.Clock()
    game = Game(WINDOW)
    play_with_ai = True
    ai_vs_ai = False
    ai_color = WHITE
    player_color = RED

    while True:
        clock.tick(FPS)
        game.update()

        if play_with_ai and game.turn == ai_color:
            new_board = minimax(game.get_board(), DEPTH, True, ai_color, player_color)[1]
            if new_board is None:
                is_player_winner = True
                break
            game.ai_move(new_board)
            if ai_vs_ai:
                time.sleep(1)

        if ai_vs_ai and game.turn != ai_color:
            new_board = minimax(game.get_board(), DEPTH, True, player_color, ai_color)[1]
            if new_board is None:
                is_player_winner = False
                break
            game.ai_move(new_board)
            time.sleep(1)

        if game.winner() is not None:
            is_player_winner = game.winner() != ai_color
            break

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
            if event.type == pygame.QUIT:
                pygame.quit()

    print_end_message(is_player_winner)
    pygame.quit()


main()
