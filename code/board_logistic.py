class TicTacToe:
    def __init__(self, boardSize=12, target=6):
        """
        初始化一个n*n的棋盘。
        """
        self.board = [["-" for _ in range(boardSize)] for _ in range(boardSize)]
        self.boardSize = boardSize
        self.target = target

    def place_piece(self, x, y, piece):
        """
        在棋盘上放置一个棋子。
        """
        if 0 <= x < self.boardSize and 0 <= y < self.boardSize:
            if self.board[x][y] == "-":
                self.board[x][y] = piece
                return True  # 成功放置棋子
            else:
                print("这个位置已经被占用了。")
                return False  # 位置已被占用，放置失败
        else:
            print("坐标超出棋盘范围。")
            return False  # 坐标超出范围，放置失败

    def is_draw(self):
        """
        检查棋盘是否已满，即是否平局。
        """
        return all(
            self.board[x][y] != "-"
            for x in range(self.boardSize)
            for y in range(self.boardSize)
        )

    def print_board(self):
        """
        打印当前棋盘的状态。
        """
        for row in self.board:
            print(row)

    def generate_moves(self):
        """
        生成所有可能的下一步走法。empty blank
        """
        moves = []
        for x in range(self.boardSize):
            for y in range(self.boardSize):
                if self.board[x][y] == "-":
                    moves.append((x, y))
        return moves

    def best_move(self):
        best_score = float("-inf")
        best_move = set()
        for move in self.generate_moves():
            score = self.minimax(move)
            if score >= best_score:
                best_score = score
                best_move.add(move)
        return best_move

    def minimax(self):
        pass

    def check_win(self, x, y, piece):
        """
        check if win after piece is placed, return bool
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
