from copy import deepcopy

RED = (255, 0, 0)
WHITE = (255, 255, 255)


def simulate_move(piece, move, board, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            moves.append(new_board)

    return moves


def minimax(board, depth, max_player, ai_color, player_color):
    if depth == 0 or board.winner() is not None:
        return board.evaluate(ai_color), board

    if max_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(board, ai_color):
            evaluation = minimax(move, depth - 1, False, ai_color, player_color)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move

        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(board, player_color):
            evaluation = minimax(move, depth - 1, True, ai_color, player_color)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move

        return min_eval, best_move
