from board_logistic import TicTacToe


def test_place_and_remove_piece():
    game = TicTacToe(boardSize=3, target=3)
    game.place_piece(1, 1)  # "O" 放置在中间
    passed = game.board[1][1] == True
    game.remove_piece(1, 1)  # 移除刚才放置的棋子
    passed &= game.board[1][1] is None
    return passed


def test_is_draw():
    game = TicTacToe(boardSize=3, target=3)
    for x in range(3):
        for y in range(3):
            game.place_piece(x, y)
    return game.is_draw()


def test_check_win():
    game = TicTacToe(boardSize=3, target=3)
    game.place_piece(0, 0)  # "O"
    game.place_piece(1, 0)  # "X"
    game.place_piece(0, 1)  # "O"
    game.place_piece(1, 1)  # "X"
    game.place_piece(0, 2)  # "O" 获胜
    return game.check_win(0, 2, True)


def test_search_win_move():
    game = TicTacToe(boardSize=3, target=3)
    game.place_piece(0, 0)  # "O"
    game.place_piece(1, 1)  # "X"
    game.place_piece(0, 1)  # "O"
    win_move = game.search_win_move(True)  # "O" 寻找获胜走法
    return win_move == (0, 2)


def test_generate_moves():
    game = TicTacToe(boardSize=3, target=3)
    game.place_piece(1, 1)  # 中心放置一个棋子
    moves = game.generate_moves()
    return len(moves) == 8  # 除中心外，应有8个可能的走法


def run_tests():
    print(
        f"Test place and remove piece: {'True' if test_place_and_remove_piece() else 'False'}"
    )
    print(f"Test is draw: {'True' if test_is_draw() else 'False'}")
    print(f"Test check win: {'True' if test_check_win() else 'False'}")
    print(f"Test search win move: {'True' if test_search_win_move() else 'False'}")
    print(f"Test generate moves: {'True' if test_generate_moves() else 'False'}")


if __name__ == "__main__":
    run_tests()
