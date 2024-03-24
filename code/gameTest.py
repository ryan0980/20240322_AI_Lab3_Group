import requests
import json
from Apicall import GET, POST


def is_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def is_board_full(board):
    return all(all(cell != '-' for cell in row) for row in board)


def evaluate_board(board):
    if is_winner(board, 'O'):
        return 1
    if is_winner(board, 'X'):
        return -1
    if is_board_full(board):
        return 0
    return None


def minimax(board, depth, is_maximizing):
    result = evaluate_board(board)
    if result is not None:
        return result

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = '-'
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = '-'
                    best_score = min(best_score, score)
        return best_score


def find_best_move(board):
    best_score = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            print(i)
            print(j)
            print(board)
            if board[i][j] == '-':
                board[i][j] = 'O'
                score = minimax(board, 1, False)
                board[i][j] = '-'
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move


# Initialize the board
board = [['-', '-', '-'],
         ['-', '-', '-'],
         ['-', '-', '-']]


#在 3x3棋盘上进行一步最优操作的测试
if __name__ == "__main__":
    getop = GET()
    getop.getBoardString('4688')
    response = requests.request("GET", url=getop.url, headers=getop.headers)
    print(response.text)
    # Use the getBoardString API here to get the board state
    if response.text:
        responseJson = json.loads(response.text)
        board_string = responseJson["output"].strip()
        # Split the board string by newline character to get each row of the board
        rows = board_string.split('\n')
        board = [list(row) for row in rows]
    for row in board:
        print(row)

    # # Check if the game is over
    # if evaluate_board(board) is not None:
    #     break

    # Make the best move
    best_move = find_best_move(board)
    move_str = str(best_move[0] + 1) + ',' + str(best_move[1] + 1)
    print(move_str)
    # Use the makeMove API here to make the move
    # Execute the makeMove API call here
    post_test = POST()
    post_test.makeMove('1412', '4688', move_str)
    print(post_test.payload)
    response = requests.request("POST", url=post_test.url, headers=post_test.headers, data=post_test.payload)
    print(response.text)
    # Update the board with the move
    board[best_move[0]][best_move[1]] = 'O'