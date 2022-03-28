from player import RandomComputerPlayer, HumanPlayer, GeniusComputerPlayer
import time


class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]            # We make use of a singe list to represent a 3 by 3 board
        self.current_winner = None                      # To keep Track of the Winner

    def print_board(self):
        for row in [self.board[i*3: (i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():     # We use this function to show which numbers correspond to which spot on the board, eg 0 | 1 | 2
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    
    def available_moves(self):
        # moves = []
        # for (i, spot) in enumerate (self.board):       # ['x', 'x', 'o'] --> [(0,'x'), (1, 'x'), (2, 'o')]
        #     if spot == ' ':
        #         moves.append(i)
        # return moves

        return [ i for i, spot in enumerate(self.board) if spot == ' ']  # Condensed form of the above code, through list comprehension

    def empty_square(self):
        return (' ' in self.board)      # Checks if the board has any empty squares, returns True or False

    def num_empty_squares(self):
        return self.board.count(' ')    # Returns number of empty sqaures in the board

    def make_move(self, square, letter):    # Function to actually make a move on the board
        if self.board[square] == ' ':
            self.board[square] = letter
            # check for win condition right after move is made
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # win condition is 3 in a row, horizontal, vertical or diagonal

        # first we check row
        row_index = square // 3
        row = self.board[row_index * 3 : (row_index + 1)*3]
        if all ([spot == letter for spot in row]):
            return True

        # now we check columns
        col_index = square % 3
        col = [self.board[col_index + i*3] for i in range(3)]
        if all ([spot == letter for spot in col]):
            return True
        
        # lastly, we check the two diagonals
        # keep in mind that we only need to check for this condition only if the square in mind lies on the diagonal
        # The condition for this is that the square must lie on an even spot, ie 0, 2, 4, 6 or 8
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
            
        # if all these checks fail, the game is not yet won by either player
        return False


def play(game, x_player, o_player, print_game = True):  # 'game' is an object of class TicTacToe
    #returns the winner of the game(either x or o), or None if its a tie
    
    if print_game:
        game.print_board_nums()

    letter = 'X'        # Starting letter

    # now we iterate while the game has empty squares, ignoring the win condition, since we'll put a break statement when that occurs
    while game.empty_square():
        # get the move from the appropriate player
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        # we need to actually perform a move based on the square we just got
        if game.make_move(square, letter):
            if print_game:
                print(letter + ' makes a move to square {}'.format(square))
                game.print_board()
                print('')   # just an empty line

        # right after the move is made, we need to check if someone won the game
        if game.current_winner:
            if print_game:
                print(letter + ' wins!!')
            return letter

        # after the move is made, we need to give the next player his turn
        letter = 'O' if letter =='X' else 'X'

        # adding a small pause between moves\
        if print_game == True:
            time.sleep(0.8)

    
    if print_game:
        print('It\'s a tie!')



if __name__ == '__main__':
    x_wins = o_wins = ties = 0

    for _ in range(1000):
        x_player = RandomComputerPlayer('X')
        o_player = GeniusComputerPlayer('O')

        tictactoe = TicTacToe()
        result = play(tictactoe, x_player, o_player, print_game = False)

        if result =='X':
            x_wins += 1
        elif result == 'O':
            o_wins += 1
        else:
            ties += 1

    print('At the end of a 1000 iterations, we observe that X wins {} times, O wins {} times, and they tie {} times'.format(x_wins, o_wins, ties))