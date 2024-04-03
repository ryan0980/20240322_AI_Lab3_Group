class TicTacToe:
    def __init__(self, boardSize=12, target=6):
        """
        初始化一个n*n的棋盘。
        O (True) 代表最大玩家, X (False) 代表最小玩家。
        """
        self.board = [[None for _ in range(boardSize)] for _ in range(boardSize)]
        self.boardSize = boardSize
        self.target = target
        self.max_step = 2
        # self.max_step = self.calculate_max_step()  # 树中的最大步数
        self.is_max_player = True  # 开始时默认为 True，即 O (最大玩家) 先行

    def calculate_max_step(self):
        # 基于棋盘大小动态计算 max_step
        if self.boardSize <= 3:
            return 9  # 对于 3x3 的棋盘，最大步数可以是全部格子
        elif self.boardSize <= 5:
            return 4  # 对于较小的棋盘，深度可以设置得较深
        elif self.boardSize <= 8:
            return 3  # 中等大小的棋盘，减少深度
        else:
            return 2  # 对于较大的棋盘，只搜索几层

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

    def evaluate_move(self, x, y):
        """
        评估在 (x, y) 位置放置棋子后的评分。
        """
        self.place_piece(x, y)
        score = self.minimax_with_pruning(
            0, False, float("-inf"), float("inf")
        )  # 假设接下来是对手的回合
        self.remove_piece(x, y)
        return score

    def print_board_with_scores(self):
        """
        打印棋盘，并在每个空位旁边显示评分。
        """
        print("棋盘及评分：")
        alpha = float("-inf")
        beta = float("inf")
        for x in range(self.boardSize):
            row_str = ""
            for y in range(self.boardSize):
                if self.board[x][y] is None:  # 空位显示评分
                    score = self.evaluate_move(x, y)
                    row_str += f"[{score:2}] "
                else:  # 非空位显示棋子
                    piece = "O" if self.board[x][y] else "X"
                    row_str += f" {piece}  "
            print(row_str)

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

    def step_taken(self):
        """
        返回当前已放置的棋子数量。
        """
        return sum(1 for row in self.board for cell in row if cell is not None)

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
        以固定宽度打印棋盘，并在行和列索引旁添加边框，以改善视觉呈现。
        """
        col_width = 3  # 每个格子的固定宽度
        border = "+" + ("-" * col_width + "+") * self.boardSize

        # 打印列索引
        col_header = " " * (col_width + 1) + " ".join(
            f"{i:^{col_width}}" for i in range(self.boardSize)
        )
        print(col_header)
        print(border)

        # 打印棋盘行，包括行号
        for i, row in enumerate(self.board):
            row_str = (
                "|"
                + "|".join(
                    " O " if cell is True else " X " if cell is False else "   "
                    for cell in row
                )
                + "|"
            )
            print(f"{i:^{col_width}}{row_str}")
            print(border)

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
        moves = []
        center = self.boardSize // 2
        for layer in range(center + 1):
            for x in range(
                max(0, center - layer), min(self.boardSize, center + layer + 1)
            ):
                for y in range(
                    max(0, center - layer), min(self.boardSize, center + layer + 1)
                ):
                    if (
                        x == center - layer
                        or x == center + layer
                        or y == center - layer
                        or y == center + layer
                    ) and self.board[x][
                        y
                    ] is None:  # 确保使用有效的索引访问棋盘
                        moves.append((x, y))
        return moves

    def set_board(self, input_board):
        self.board = input_board
        self.check_next_move_player()

    def check_next_move_player(self):
        o_count = 0
        x_count = 0
        for row in self.board:
            for cell in row:
                if cell is True:
                    o_count += 1
                elif cell is False:
                    x_count += 1

        # 如果 'O' 的数量等于 'X' 的数量，下一个玩家是 'O' (True)
        # 否则，下一个玩家是 'X' (False)
        self.is_max_player = o_count == x_count

    def best_move(self):
        if self.step_taken() == 0:
            return (self.boardSize // 2, self.boardSize // 2)
        # 首先检查 AI 自己是否有立即获胜的走法
        win_move = self.search_win_move(True if self.is_max_player else False)
        if win_move:
            return win_move

        # 然后检查对手是否有立即获胜的走法，如果有，阻止对手获胜
        opponent_win_move = self.search_win_move(False if self.is_max_player else True)
        if opponent_win_move:
            return opponent_win_move

        # 如果没有立即获胜的走法，使用 minimax 算法寻找最佳走法
        best_score = float("-inf") if self.is_max_player else float("inf")
        best_move = None
        alpha = float("-inf")
        beta = float("inf")

        for move in self.generate_moves():
            x, y = move
            self.place_piece(x, y)  # 模拟执行这个走法
            score = self.minimax_with_pruning(
                0, not self.is_max_player, alpha, beta
            )  # 使用带有剪枝的minimax
            self.remove_piece(x, y)  # 撤销这个走法

            if self.is_max_player and score > best_score:
                best_score = score
                best_move = move
                alpha = max(alpha, score)
            elif not self.is_max_player and score < best_score:
                best_score = score
                best_move = move
                beta = min(beta, score)

            if beta <= alpha:
                break

        return best_move if best_move is not None else self.generate_moves()[0]

    def minimax(self, depth, is_max_player):
        status, player = self.check_status()
        if status == "Win":
            return (1 if player == True else -1) * (self.max_step - depth)
        elif status == "Draw":
            return 0
        if depth == self.max_step:
            evaluator = ScoreEvaluator(self.board, self.target)
            return evaluator.evaluate_score(self.is_max_player)

        if is_max_player:
            maxEval = float("-inf")
            for move in self.generate_moves():
                x, y = move
                self.place_piece(x, y)
                eval = self.minimax(depth + 1, False)
                self.remove_piece(x, y)
                maxEval = max(maxEval, eval)
            return maxEval
        else:
            minEval = float("inf")
            for move in self.generate_moves():
                x, y = move
                self.place_piece(x, y)
                eval = self.minimax(depth + 1, True)
                self.remove_piece(x, y)
                minEval = min(minEval, eval)
            return minEval

    def minimax_with_pruning(
        self, depth, is_max_player, alpha=float("-inf"), beta=float("inf")
    ):
        status, player = self.check_status()
        if status == "Win":
            return (1 if player == True else -1) * (self.max_step - depth)
        elif status == "Draw":
            return 0
        if depth == self.max_step:
            evaluator = ScoreEvaluator(self.board, self.target)
            return evaluator.evaluate_score(self.is_max_player)

        if is_max_player:
            maxEval = float("-inf")
            for move in self.generate_moves():
                x, y = move
                self.place_piece(x, y)
                eval = self.minimax_with_pruning(depth + 1, False, alpha, beta)
                self.remove_piece(x, y)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float("inf")
            for move in self.generate_moves():
                x, y = move
                self.place_piece(x, y)
                eval = self.minimax_with_pruning(depth + 1, True, alpha, beta)
                self.remove_piece(x, y)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval


class ScoreEvaluator:
    def __init__(self, board, target=6):
        self.board = board
        self.boardSize = len(board)
        self.target = target

    def evaluate_score(self, piece):
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        evaluated_positions = set()

        for x in range(self.boardSize):
            for y in range(self.boardSize):
                if (x, y) in evaluated_positions or self.board[x][y] != piece:
                    continue  # 跳过已评分或非目标棋子的位置

                for dx, dy in directions:
                    # 只评分一次每个方向上的连续棋子
                    if (x - dx, y - dy) not in evaluated_positions:
                        score += self.evaluate_direction(x, y, dx, dy, piece)
                        evaluated_positions.add((x, y))

        if not piece:
            score = -score  # 如果是 "X"，取负分

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
            score = float("inf")  # 达到或超过获胜条件
        elif blocked == 0:
            score = 10**consecutive  # 无阻塞，得分为连续棋子数的指数
        elif blocked == 1:
            score = 5**consecutive  # 单边阻塞，降低得分

        return score
