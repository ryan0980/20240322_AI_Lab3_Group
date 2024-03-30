class TicTacToe:
    def __init__(self, boardSize=12, target=6):
        """
        初始化一个n*n的棋盘。
        O (True) 代表最大玩家, X (False) 代表最小玩家。
        """
        self.board = [[None for _ in range(boardSize)] for _ in range(boardSize)]
        self.boardSize = boardSize
        self.target = target
        self.max_step = 100  # 树中的最大步数
        self.is_max_player = True  # 开始时默认为 True，即 O (最大玩家) 先行

    def check_status(self):
        """
        返回当前棋盘的状态。
        如果有玩家获胜，则返回获胜信息；否则，检查是否平局或游戏是否继续。
        """
        # 遍历棋盘检查是否有玩家获胜
        for x in range(self.boardSize):
            for y in range(self.boardSize):
                piece = self.board[x][y]
                if piece is not None and self.check_win(x, y, piece):
                    # 如果找到获胜的玩家，返回游戏结束和获胜玩家
                    return "Win", piece

        # 如果没有玩家获胜，检查是否平局或游戏是否继续
        if self.is_draw():
            # 如果棋盘已满，表示平局
            return "Draw", None
        else:
            # 否则游戏继续
            return "Continue", None

    def is_draw(self):
        """
        检查棋盘是否已满，即是否平局。
        棋盘上的每个位置非None表示有棋子放置，如果所有位置都被放置了棋子，则为平局。
        """
        return all(
            self.board[x][y] is not None  # 更新条件检查为非None，表示位置被占用
            for x in range(self.boardSize)
            for y in range(self.boardSize)
        )

    def check_win(self, x, y, piece):
        """
        检查在给定位置放置一个棋子后是否获胜。
        piece 参数应为 True 或 False，分别代表两个玩家。
        返回布尔值：如果放置后导致获胜，则为 True；否则为 False。

        参数:
        - x, y: 放置棋子的位置坐标。
        - piece: 放置的棋子，True 代表 "O"，False 代表 "X"。
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 水平，垂直，两个对角线
        for dx, dy in directions:
            count = 1  # 包括当前放置的棋子
            # 检查一个方向上的连续相同棋子
            for step in range(1, self.target):
                nx, ny = x + dx * step, y + dy * step
                if (
                    0 <= nx < self.boardSize
                    and 0 <= ny < self.boardSize
                    and self.board[nx][ny] == piece
                ):
                    count += 1
                else:
                    break
            # 检查相反方向上的连续相同棋子
            for step in range(1, self.target):
                nx, ny = x - dx * step, y - dy * step
                if (
                    0 <= nx < self.boardSize
                    and 0 <= ny < self.boardSize
                    and self.board[nx][ny] == piece
                ):
                    count += 1
                else:
                    break
            # 如果连续相同棋子的数量达到了target，则当前玩家获胜
            if count >= self.target:
                return True
        return False

    def print_board(self):
        """
        打印当前棋盘的状态。
        将 True 显示为 "O"，False 显示为 "X"，None 显示为 "-"。
        """
        for row in self.board:
            print(
                " ".join(
                    [
                        "O" if cell is True else "X" if cell is False else "-"
                        for cell in row
                    ]
                )
            )

    def place_piece(self, x, y):
        """
        根据当前玩家在棋盘上放置一个棋子。
        如果当前位置为空（None），则放置棋子并切换玩家。
        成功放置棋子返回True，否则返回False。
        """
        if 0 <= x < self.boardSize and 0 <= y < self.boardSize:
            if self.board[x][y] is None:  # 检查位置是否为空
                self.board[x][y] = self.is_max_player  # True 代表 "O"，False 代表 "X"
                self.is_max_player = not self.is_max_player  # 切换玩家
                return True
            else:
                print("这个位置已经被占用了。")
                return False
        else:
            print("坐标超出棋盘范围。")
            return False

    def remove_piece(self, x, y):
        """
        从棋盘上移除一个棋子，这被视为一次回合操作。
        成功移除棋子并切换玩家返回True，否则返回False。
        """
        if 0 <= x < self.boardSize and 0 <= y < self.boardSize:
            if self.board[x][y] is not None:  # 如果该位置上有棋子
                self.board[x][y] = None  # 移除棋子，即将该位置重置为 None
                self.is_max_player = not self.is_max_player  # 切换玩家
                return True
            else:
                print("该位置上没有棋子。")
                return False
        else:
            print("坐标超出棋盘范围。")
            return False

    def search_win_move(self, is_max_player):
        """
        检查是否存在立即获胜的走法。
        is_max_player: 布尔值，表示当前是否为最大玩家（True代表"O"，False代表"X"）。
        返回获胜移动的坐标(x, y)，如果没有立即获胜的走法，则返回None。
        """
        original_player = self.is_max_player  # 保存当前玩家状态

        for x in range(self.boardSize):
            for y in range(self.boardSize):
                if self.board[x][y] is None:  # 空位
                    self.is_max_player = is_max_player  # 设置当前玩家状态以模拟放置棋子
                    self.place_piece(x, y)  # 模拟放置棋子
                    if self.check_win(x, y, is_max_player):  # 检查是否获胜
                        self.remove_piece(x, y)  # 撤销模拟的移动
                        self.is_max_player = original_player  # 恢复原来的玩家状态
                        return (x, y)  # 返回获胜移动
                    self.remove_piece(x, y)  # 撤销模拟的移动
                    self.is_max_player = original_player  # 恢复原来的玩家状态

        self.is_max_player = original_player  # 确保在方法结束时恢复原来的玩家状态
        return None

    def generate_moves(self):
        """
        从棋盘中心向外生成所有可能的下一步走法。
        只包括当前为空（None）的位置。
        """
        moves = []
        center = self.boardSize // 2
        for layer in range(center + 1):
            for x in range(center - layer, center + layer + 1):
                for y in range(center - layer, center + layer + 1):
                    if (
                        x == center - layer
                        or x == center + layer
                        or y == center - layer
                        or y == center + layer
                    ) and self.board[x][
                        y
                    ] is None:  # 检查位置是否为空
                        moves.append((x, y))
        return moves

    def best_move(self):
        """
        使用 minimax 算法来确定最佳走法。这个方法首先生成所有可能的走法，
        然后对每一个可能的走法调用 minimax 方法来评估它的得分。基于 minimax
        算法的返回值，选择最佳的走法。如果当前玩家是最大玩家（self.is_max_player
        为 True），则选择得分最高的走法；如果当前玩家是最小玩家，则选择得分最低的走法。

        返回值是一个元组 (x, y)，代表棋盘上的坐标，是当前玩家应该执行的最佳走法。
        如果没有可行的走法，返回最靠近中心的步
        """
        best_score = float("-inf") if self.is_max_player else float("inf")
        best_move = self.generate_moves()[0]
        for move in self.generate_moves():
            x, y = move
            self.place_piece(x, y)  # 模拟执行这个走法
            score = self.minimax(0, not self.is_max_player)  # 评估这个走法
            self.remove_piece(x, y)  # 撤销这个走法
            if (self.is_max_player and score > best_score) or (
                not self.is_max_player and score < best_score
            ):
                best_score = score
                best_move = move
        return best_move


class ScoreEvaluator:
    def __init__(self, board, target=6):
        self.board = board
        self.boardSize = len(board)
        self.target = target

    def evaluate_score(self, piece):
        """
        评估棋局得分。
        piece: True 或 False，表示要评估哪方的得分（True代表"O"，False代表"X"）。
        """
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 水平、垂直、两个对角线方向

        for x in range(self.boardSize):
            for y in range(self.boardSize):
                if self.board[x][y] == piece:
                    for dx, dy in directions:
                        score += self.evaluate_direction(x, y, dx, dy, piece)

        return score

    def evaluate_direction(self, x, y, dx, dy, piece):
        """
        在给定方向上评估得分。
        """
        consecutive = 1
        blocked = 0
        score = 0

        # 前进方向
        nx, ny = x + dx, y + dy
        while (
            0 <= nx < self.boardSize
            and 0 <= ny < self.boardSize
            and self.board[nx][ny] == piece
        ):
            consecutive += 1
            nx += dx
            ny += dy

        # 检查前进方向是否被阻塞
        if not (
            0 <= nx < self.boardSize
            and 0 <= ny < self.boardSize
            and self.board[nx][ny] is None
        ):
            blocked += 1

        # 后退方向
        nx, ny = x - dx, y - dy
        while (
            0 <= nx < self.boardSize
            and 0 <= ny < self.boardSize
            and self.board[nx][ny] == piece
        ):
            consecutive += 1
            nx -= dx
            ny -= dy

        # 检查后退方向是否被阻塞
        if not (
            0 <= nx < self.boardSize
            and 0 <= ny < self.boardSize
            and self.board[nx][ny] is None
        ):
            blocked += 1

        # 根据连续棋子和阻塞情况计算得分
        if consecutive >= self.target:
            return float("inf")  # 达到或超过获胜条件
        elif blocked == 0:
            score = 10**consecutive  # 无阻塞，得分为连续棋子数的指数
        elif blocked == 1:
            score = 5**consecutive  # 单边阻塞，降低得分

        return score
