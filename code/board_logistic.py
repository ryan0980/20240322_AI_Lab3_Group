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

    def print_board(self):
        """
        打印当前棋盘的状态。
        """
        for row in self.board:
            print(row)
