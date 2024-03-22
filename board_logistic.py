class TicTacToe:
    def __init__(self, n):
        """
        初始化一个n*n的棋盘。
        """
        self.board = [["0" for _ in range(n)] for _ in range(n)]
        self.size = n

    def place_piece(self, x, y, piece):
        """
        在棋盘上放置一个棋子。
        """
        if 0 <= x < self.size and 0 <= y < self.size:
            if self.board[x][y] == "0":
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
