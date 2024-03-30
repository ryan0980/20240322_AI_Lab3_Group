from games import *
from Apicall import *


def play_tictactoe(h=12, v=12, k=6):
    # Initialize the game
    # Assume there is already a game created by API
    # rule: team_id1 will make the first move and takes 'O'
    # rule: team_id2 will make the second move and takes 'X'
    # rule: The board position start from 0

    global board
    game = TicTacToe(h, v, k)
    state = game.initial
    move_count = 0
    # Assume AI can play both O and X
    player_1 = 'O'
    player_2 = 'X'
    team_id1 = '1412'
    team_id2 = '1399'
    game_id = '4742'

    # Function to print the board
    def print_board(state):
        for x in range(1, h + 1):
            for y in range(1, v + 1):
                print(state.board.get((x, y), '-'), end=' ')
            print()

    def getNextMover():
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

    # Main game loop
    while True:
        next_mover = team_id1
        if move_count == 0:
            print("player_1's move (O):")
        else:
            next_mover = getNextMover()
            if next_mover == team_id1:
                # To do: set next Mover
                state.to_move = player_1
                print("player_1's move:")
            else:
                if next_mover == team_id2:
                    state.to_move = player_2
                    print("player_2's move:")
                else:
                    print("Can not get valid next Mover")
                    return
        move = alpha_beta_player(game, state)
        move_count += 1
        # make Move
        post = POST()
        post.makeMove(next_mover, game_id, move)
        print(post.payload)
        res = requests.request("POST", url=post.url, headers=post.headers, data=post.payload)
        print(res.text)
        # Update the state with the move
        state = game.result(state, move)

        # To do : update the board by using the board return by API
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
        for row in board:
            print(row)
        # Print the board
        print_board(state)

        # Check for terminal state
        if game.terminal_test(state):
            if state.utility > 0:
                print("player_1 wins!")
            elif state.utility < 0:
                print("player_2 win!")
            else:
                print("It's a draw!")
            break


if __name__ == "__main__":
    play_tictactoe()
