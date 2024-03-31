from board_logistic import TicTacToe
from board_logistic import ScoreEvaluator


def test_best_move():
    game = TicTacToe(boardSize=3, target=3)  # 创建一个3x3的棋盘，获胜条件是连续3个棋子

    # 设置一个棋局，其中 'O' (True) 是下一步行棋方，并且处于获胜的边缘
    game.set_board([[True, False, None], [None, False, True], [None, None, None]])
    print("初始棋盘:")
    game.print_board()

    # 检查最佳移动
    x, y = game.best_move()
    print(f"最佳走法是在位置 ({x}, {y})")

    # 根据最佳走法放置棋子，并打印棋盘状态
    game.place_piece(x, y)
    print("执行最佳走法后的棋盘:")
    game.print_board()

    # 检查游戏状态
    status, player = game.check_status()
    if status == "Win":
        print(f"玩家 {'O' if player else 'X'} 获胜!")
    elif status == "Draw":
        print("游戏平局!")
    else:
        print("游戏继续.")


if __name__ == "__main__":
    test_best_move()
