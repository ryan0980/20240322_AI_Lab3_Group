from games import *
def play_tictactoe(h=12, v=12, k=6):
    # Initialize the game
    game = TicTacToe(h, v, k)
    state = game.initial
    
    # Define player types
    ai_player = 'X'
    human_player = 'O'

    # Function to print the board
    def print_board(state):
        for x in range(1, h+1):
            for y in range(1, v+1):
                print(state.board.get((x, y), '-'), end=' ')
            print()
    
    # Main game loop
    while True:
        if state.to_move == ai_player:
            print("AI's move (X):")
            move = alpha_beta_player(game, state)
        else:
            print("Your move (O): Enter 'x y'")
            valid_move = False
            while not valid_move:
                try:
                    x, y = map(int, input().split())
                    if (x, y) in state.moves:
                        move = (x, y)
                        valid_move = True
                    else:
                        print("Invalid move. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter two integers separated by a space.")
        
        # Update the state with the move
        state = game.result(state, move)
        
        # Print the board
        print_board(state)
        
        # Check for terminal state
        if game.terminal_test(state):
            if state.utility > 0:
                print("AI wins!")
            elif state.utility < 0:
                print("You win!")
            else:
                print("It's a draw!")
            break

# Example usage:
play_tictactoe()
