from board_logistic import TicTacToe
from board_logistic import ScoreEvaluator
import time

from Apicall import *


class TicTacToeAI(TicTacToe):

    def ai_move(self, is_max_player):
        self.is_max_player = is_max_player  # 设置当前玩家
        start_time = time.time()
        move = self.best_move()  # 基于当前棋盘状态，找到最佳移动
        # self.print_board_with_scores()
        self.place_piece(*move)  # 在棋盘上放置棋子
        end_time = time.time()
        print(
            f"AI ('{'O' if is_max_player else 'X'}') 在位置 {move} 放置了一个棋子。用时: {end_time - start_time:.2f} 秒"
        )
        self.print_board()
        return move

    def getNextMover(self):
        getop = GET()
        getop.getMoves(game_id, 1)
        response = requests.request("GET", url=getop.url, headers=getop.headers)
        responseJson = json.loads(response.text)
        team_id = responseJson["moves"][0]["teamId"]
        print("last Move Team: " + team_id)
        if team_id == team_id1:
            return team_id2
        else:
            if team_id == team_id2:
                return team_id1
            else:
                return "Invalid Mover"

    def getBoardbyAPI(self):
        getop = GET()
        getop.getBoardString(game_id)
        res = requests.request("GET", url=getop.url, headers=getop.headers)
        print(res.text)
        # Use the getBoardString API here to get the board state
        if res.text:
            responseJson = json.loads(res.text)
            board_string = responseJson["output"].strip()
            # Split the board string by newline character to get each row of the board
            rows = board_string.split('\n')
            board = [list(row) for row in rows]
        input_board = [[True if cell == 'O' else False if cell == 'X' else None for cell in row] for row in board]
        return input_board


def ai_vs_ai_game():
    global board
    global team_id1
    global team_id2
    global game_id
    team_id1 = '1417'
    team_id2 = '1399'
    game_id = '5177'
    game = TicTacToeAI(boardSize=5, target=4)

    print("游戏开始，AI 对战 AI。")
    current_player = True  # True 代表 "O" 玩家开始

    while True:
        input_board = game.getBoardbyAPI()
        game.set_board(input_board)
        game.print_board()
        move = game.ai_move(current_player)  # 当前 AI 玩家移动
        move = ','.join(str(i) for i in move)
        current_player = (game.getNextMover() == team_id1)
        if current_player:
            teamid = team_id1
            continue
        else:
            teamid = team_id2

        post = POST()
        post.makeMove(teamid, game_id, move)
        print(post.payload)
        res = requests.request("POST", url=post.url, headers=post.headers, data=post.payload)
        print(res.text)
        status, player = game.check_status()  # 检查游戏状态
        if status != "Continue":
            break


    # 游戏结束，打印结果
    if status == "Win":
        print(f"AI ('{'O' if player else 'X'}') 获胜！")
    elif status == "Draw":
        print("游戏平局！")


if __name__ == "__main__":
    ai_vs_ai_game()
