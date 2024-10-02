from math import inf as infinity
from random import choice
import platform
import time
from os import system

h_name_change = ''
h_name = ''
HUMAN = -1
COMP = +1
gamemode = ''
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def reset_to_0(the_array):
    for i, e in enumerate(the_array):
        if isinstance(e, list):
            reset_to_0(e)
        else:
            the_array[i] = 0


def evaluate(state):
    """
    Function to heuristic evaluation of state.
    :param state: the state of the current board
    :return: +1 if the computer wins (max); -1 if the human wins (min); 0 draw
    """
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    """
    This function test if the human or computer wins
    :param state: the state of the current board
    :return: True if the human or computer wins
    """
    return wins(state, HUMAN) or wins(state, COMP)

def empty_cells(state):
    """
    Each empty cell will be added into cells' list
    :param state: the state of the current board
    :return: a list of empty cells
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    """
    A move is valid if the chosen cell is empty
    :param x: X coordinate
    :param y: Y coordinate
    :return: True if the board[x][y] is empty
    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """
    Set the move on board, if the coordinates are valid
    :param x: X coordinate
    :param y: Y coordinate
    :param player: the current player
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    """
    AI function that choice the best move
    :param state: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9),
    but never nine in this case (see iaturn() function)
    :param player: a human or a computer
    :return: a list with [the best row, best col, best score]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):
    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def render1():
    exp_board = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9'],
    ]

    str_line = '---------------'

    print('\n' + str_line)
    for row in exp_board:
        for cell in row:
            print(f'| {cell} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    """
    It calls the minimax function if the depth < 9,
    else it choices a random coordinate.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean()
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)


def human_turn(c_choice, h_choice, human_name):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    # clean()
    # print(human_name + f'\'s turn [{h_choice}]')

    if gamemode == "pvp":
        if human_name == "Player 1":
            print(human_name + f'\'s turn [{h_choice}]')
        elif human_name == "Player 2":
            print(human_name + f'\'s turn [{c_choice}]')
    elif gamemode == "pvc":
        print(human_name + f'\'s turn [{h_choice}]')    

    render1()
    render(board, c_choice, h_choice)

    while move < 1 or move > 9:
        try:
            print("Refer to the number on the first table for cell positions")
            move = int(input('Use your numpad (1..9) to choose position: '))
            coord = moves[move]

            if gamemode == "pvp":

                if human_name == "Player 1":
                    player_symbol = -1
                elif human_name == "Player 2":
                    player_symbol = 1

            elif gamemode == "pvc":
                player_symbol = HUMAN if h_choice == 'X' else COMP            

           # player_symbol = HUMAN if h_choice == 'X' else COMP
            can_move = set_move(coord[0], coord[1], player_symbol)

            if not can_move:
                print('Move not allowed')  # Prints out an error message when the move is not allowed
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Invalid Input')
            exit()
        except (KeyError, ValueError):
            print('Invalid Input')

def choose_mode():
    while True:
        choice = input("Choose gamemode:\n1. Player vs Computer\n2. Player vs Player\nEnter your choice (1 or 2): ")
        global gamemode        

        if choice == '1':
            gamemode = 'pvc'
            return '1', 'X', 'O'  # Assuming the computer always plays with 'O'
        elif choice == '2':
            gamemode = 'pvp'
            return '2', 'X', 'O'  # Set designated symbols for both players (Player 1 is X and Player 2 is O)
        else:
            print("Invalid choice. Please enter '1' or '2'.")

def player_vs_player():
    reset_to_0(board)
    h_choice1 = 'X'
    h_choice2 = 'O'

    clean()
    print("Player 1, you are 'O'.")
    print("Player 2, you are 'X'. Let's start the game!\n")
    
    current_player = HUMAN  # Start with player 1
    
    # Main loop for Player vs Player
    while len(empty_cells(board)) > 0 and not game_over(board):
    # clean()
    #    render(board, h_choice2, h_choice1)

        if current_player == HUMAN:
            # print("\nPlayer 1's turn:")
            human_turn(h_choice1, h_choice2, "Player 1")
        else:
            # print("\nPlayer 2's turn:")
            human_turn(h_choice1, h_choice2, "Player 2")

        current_player *= -1  # Switch players for the next turn
                
    # Game over message
    if wins(board, HUMAN):
        clean()
        render(board, h_choice1, h_choice2)
        print('Congratulations, Player 1, YOU WIN!')
    elif wins(board, COMP):
        clean()
        render(board, h_choice1, h_choice2)
        print('Congratulations, Player 2, YOU WIN!')
    else:
        clean()
        render(board, h_choice1, h_choice2)
        print("It's a DRAW!")

def main():
    clean()
    repeat = True
    global h_name_change
    h_name_change = 'N'

    print("----------------------------------------------------")
    print("|                 Tic Tac Toe                      |")
    print("----------------------------------------------------")
    print("This is a tic-tac-toe game.\n")
    print("1. The user will need to choose a gamemode.")
    print("1. The player will be required to input a name if they are playing against a computer.")
    print("2. The player will then choose where to put their symbol in a grid of 3x3.")
    print("3. The player and computer will take turn.")
    print("4. This process will repeat until 3 symbols are lined up or if the grid is full.")
    print("5. The first one to line up 3 symbols wins the game. If both fail to do so, then it's a draw.\n")

    print("Example of winning positions:\n")

    print("Diagonal:")
    print("---------------")
    print("|   ||   || X |")
    print("---------------")
    print("|   || X ||   |")
    print("---------------")
    print("| X ||   ||   |")
    print("---------------\n")

    print("Horizontal:")
    print("---------------")
    print("|   ||   ||   |")
    print("---------------")
    print("| X || X || X |")
    print("---------------")
    print("|   ||   ||   |")
    print("---------------\n")

    print("Vertical:")
    print("---------------")
    print("|   || X ||   |")
    print("---------------")
    print("|   || X ||   |")
    print("---------------")
    print("|   || X ||   |")
    print("---------------\n")


    game_mode, player1_choice, player2_choice = choose_mode()

    # Main loop to determine to repeat the game
    while repeat:
        # ... (previous code)
        if game_mode == '2':
            Flag = False
            player_vs_player()

        else:
            reset_to_0(board)
            h_name_confirmation = ''
            h_choice = ''
            c_choice = ''
            first = ''  # if human first 
            Flag = False

            if (h_name_change == 'N'):
                # Lets the user input their player name
                while h_name_confirmation != 'Y':
                    try:
                        h_name_confirmation = ''
                        print('')
                        global h_name
                        h_name = input('What is your player name?\nPlayer name: ')
                        print('')
                        while h_name_confirmation != 'N' and h_name_confirmation != 'Y':
                            h_name_confirmation = input(
                                'Do you want to be called \'' + h_name + '\'?[y/n]\nSelection: ').upper()
                            if (h_name_confirmation != 'N' and h_name_confirmation != 'Y'):
                                print("Invalid Input. Please choose 'y' or 'n'\n")
                    except (EOFError, KeyboardInterrupt):
                        print('Invalid Input')
                        exit()
                    except (KeyError, ValueError):
                        print('Invalid Input')
                h_name_change = ''

            # Human chooses X or O to play
            if game_mode == '1':
                h_choice = player1_choice
                c_choice = player2_choice
            else:
                h_choice = player1_choice

            # Setting computer's choice
            if h_choice == 'X':
                c_choice = 'O'
            else:
                c_choice = 'X'

            # Human may starts first
        
            while first != 'Y' and first != 'N':
                # Prompts user to choose who to start first
                print('')
                first = input('Do you want to start first?[y/n]: ').upper()
                if first == 'Y' or first == 'N':
                    break
                else:
                    print("Invalid Input. Please choose 'y' or 'n'")

            # Main loop of this game
            while len(empty_cells(board)) > 0 and not game_over(board):
                if first == 'N':
                    ai_turn(c_choice, h_choice)
                    if game_over(board):
                        break

                human_turn(c_choice, h_choice, h_name)
                if game_over(board):
                    break

                if first == 'Y':
                    ai_turn(c_choice, h_choice)


            # Game over message
            if wins(board, HUMAN):
                clean()
                print(f'Human turn [{h_choice}]')
                render(board, c_choice, h_choice)
                print('Congratulations, YOU WIN!')
            elif wins(board, COMP):
                clean()
                print(f'Computer turn [{c_choice}]')
                render(board, c_choice, h_choice)
                print('Oh man, YOU LOSE!')
            else:
                clean()
                render(board, c_choice, h_choice)
                print('Yay, it\'s a DRAW!')

        # Prompts user to see if the game should be played again
        while Flag == False:
            cont = input("Do you want to play again? [y/n]: ").upper()
            if cont == 'Y':
                Flag = True
                if gamemode == 'pvp':
                    break
                elif gamemode == 'pvc':
                    h_name_change = ''
                    while h_name_change != 'N' and h_name_change != 'Y':
                        h_name_change = input('\nAre you still playing as ' + h_name + '? [y/n]\nSelection: ').upper()
                        if (h_name_change != 'N' and h_name_change != 'Y'):
                            print("Invalid Input. Please choose 'y' or 'n'.")
                    break
            elif cont == 'N':
                Flag = True
                repeat = False
                break
            else:
                Flag = False
                print("Invalid Input. Please choose 'y' or 'n'")

    exit()


if __name__ == '__main__':
    main()