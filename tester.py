from board_logistic import TicTacToe

# 创建一个3x3的游戏实例
game = TicTacToe(3)

# 测试放置棋子
game.place_piece(0, 0, "X")
game.place_piece(1, 1, "O")
game.place_piece(0, 0, "O")  # 尝试放置在已占用的位置
game.place_piece(3, 3, "X")  # 尝试放置在棋盘外的位置

# 打印当前棋盘状态
game.print_board()
