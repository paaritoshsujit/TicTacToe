
####################################################################
##### Implementing Tic Tac Toe using the concept of inheritance ####
####################################################################
######## Tic Tac Toe AI also created using MiniMax Algorithm #######
####################################################################

import math
import random


class Player():
    def __init__(self, letter):
        self.letter = letter        # letter is either x or o

    def get_move(self, game):
        pass


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        # The computer chooses a random valid square to play a move on
        square = random.choice(game.available_moves())
        return square


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn and. Input move (0-8) ' )

            # Validation
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')

        return val  


class GeniusComputerPlayer(Player):
    def __init__(self,letter):
        super().__init__(letter)


    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())['position']      # randomly choose one square if board is empty

        else:
            # get the square based off of the the minimax algorithm
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):   # we call it 'state' here instead of 'game' since we use only the current state of the game each time the function is called
        max_player = self.letter    # yourself!
        other_player = 'O' if player == 'X' else 'X'


        # first we check if the previous moce won the game
        # this is our base case
        if state.current_winner == other_player:
            # we need to return the position and the score, since both these things are imoportant for minimax to work
            return {'position': None,
                    'score': 1*(state.num_empty_squares()+1) if other_player == max_player else -1*(state.num_empty_squares() + 1)
                    }
        elif not state.empty_square(): # no empty squares
            return {'position': None,
                    'score': 0
                    }

        # initialize some dictionaries
        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            # step 1: make a move, try that spot
            state.make_move(possible_move, player)

            # step 2: recurse using minimax to simulate a game after making that move
            sim_score = self.minimax(state, other_player) #now we alternate players

            # step 3: undo that move (so we can repeat the same process with a different move)
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            # step 4: update the dictionaries if necessary
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score    # replace best to maximise, if better alternative is found
            
            else: 
                if sim_score['score'] < best['score']:
                    best = sim_score    # replace best to minimise, if better alternative is found


        return best