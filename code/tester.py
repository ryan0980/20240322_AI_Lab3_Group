from board_logistic import TicTacToe

# 创建一个3x3的游戏实例
game = TicTacToe()

# 测试放置棋子
game.place_piece(0, 0, "X")
game.place_piece(1, 1, "O")
game.place_piece(0, 0, "O")  # 尝试放置在已占用的位置
game.place_piece(3, 3, "X")

# 打印当前棋盘状态
game.print_board()


def test_tic_tac_toe():
    # 创建一个6x6的游戏，设置获胜条件为4
    game = TicTacToe(boardSize=6, target=5)

    # 模拟一系列放置棋子的操作，可能会导致获胜
    moves = [
        (0, 0, "X"),
        (1, 0, "O"),
        (0, 1, "X"),
        (1, 1, "O"),
        (0, 2, "X"),
        (1, 2, "O"),
        (0, 3, "X"),  # 这一步应该让'X'获胜
    ]

    for x, y, piece in moves:
        game.place_piece(x, y, piece)
        if game.check_win(x, y, piece):
            print(f"玩家 {piece} 获胜了！")
            game.print_board()
            return

    print("游戏继续。")


if __name__ == "__main__":
    test_tic_tac_toe()
