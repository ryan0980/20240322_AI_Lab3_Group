from board_logistic import TicTacToe
from board_logistic import ScoreEvaluator


class TicTacToeAI(TicTacToe):
    def ai_move(self):
        """
        AI 使用 minimax_with_pruning 算法进行移动。
        """
        move = self.best_move()  # 使用之前讨论的 best_move 方法
        self.place_piece(*move)
        print(f"AI ('O') 在位置 {move} 放置了一个棋子。")
        self.print_board()


def human_vs_ai_game():
    game = TicTacToeAI(
        boardSize=12, target=5
    )  # 初始化一个 12x12 的五子棋游戏，获胜条件是连续5个棋子

    while True:
        # 打印当前棋盘状态
        game.print_board()

        # 人类玩家 'X' 移动
        while True:
            try:
                x, y = map(int, input("输入你的移动 (格式：x y)：").split())
                if not game.place_piece(x, y):
                    raise ValueError
                break
            except ValueError:
                print("无效的输入，请重新输入。")

        # 检查游戏状态
        status, player = game.check_status()
        if status != "Continue":
            break

        # AI 'O' 移动
        game.ai_move()

        # 再次检查游戏状态
        status, player = game.check_status()
        if status != "Continue":
            break

    # 游戏结束，打印结果
    if status == "Win":
        print(f"{'人类' if player == False else 'AI'} 获胜！")
    elif status == "Draw":
        print("游戏平局！")


if __name__ == "__main__":
    human_vs_ai_game()
