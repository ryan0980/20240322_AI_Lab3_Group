from board_logistic import TicTacToe
from board_logistic import ScoreEvaluator
import time


class TicTacToeAI(TicTacToe):
    def ai_move(self, is_max_player):
        self.is_max_player = is_max_player  # 设置当前玩家
        start_time = time.time()
        move = self.best_move()  # 基于当前棋盘状态，找到最佳移动
        # self.print_board_with_scores()
        self.place_piece(*move)  # 在棋盘上放置棋子
        end_time = time.time()
        print(
            f"AI ('{'O' if is_max_player else 'X'}') at {move} time use: {end_time - start_time:.2f} s"
        )
        self.print_board()


def ai_vs_ai_game():
    game = TicTacToeAI(boardSize=20, target=10)

    print("game start, ai vs ai")
    current_player = True  # True 代表 "O" 玩家开始

    while True:
        game.ai_move(current_player)  # 当前 AI 玩家移动

        status, player = game.check_status()  # 检查游戏状态
        if status != "Continue":
            break

        current_player = not current_player  # 切换玩家

    # 游戏结束，打印结果
    if status == "Win":
        print(f"AI ('{'O' if player else 'X'}') win")
    elif status == "Draw":
        print("draw")


if __name__ == "__main__":
    ai_vs_ai_game()
