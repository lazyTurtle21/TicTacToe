import random
import time
import os

from board import Board


class TicTacToe:
    """Class for TicTacToe representation"""
    def __init__(self, player_name):
        """Create new TicTacToe game"""
        self.human = Player(player_name, 'X' if random.randint(0, 1) else 'O')
        self.field = Board('123456789')
        self.me = Player('Computer', 'X' if self.human.symbol == 'O' else 'O')

    def make_move(self, player):
        """Make one move on game board"""
        print('\n\nYour turn, ' + player.name + ' (' + player.symbol + ')')
        if player == self.human:
            move = self.player_move()
            time.sleep(1)
        else:
            move = self.field.choose_move()
        prev = self.field.board
        self.field = Board(prev[:move] + player.symbol + prev[move + 1:], move)

    def launch(self):
        """Launch TicTacToe"""
        win = False
        current_player = self.human if self.human.symbol == 'X' else self.me

        while win is False:
            os.system('cls')
            self.field.draw()
            self.make_move(current_player)
            win = self.field.check_win()
            current_player = self.human if current_player == self.me\
                else self.me
        self.field.draw()
        print(((self.human.name if current_player == self.me else self.me.name)
              + ', you won!!!') if win is not None else 'Draw, nobody won')

    def player_move(self):
        """Receive correct coordinates of move from user"""
        move = None
        while move is None:
            try:
                move = input('Input your move(e.g. 11) : ')
                if len(move) != 2 or int(move[1]) > 3 or int(move[0]) > 3:
                    raise InvalidMove('Your input numbers are out of range')

                move = 3 * int(move[0]) - (4 - int(move[1]))
                if not self.field.board[move].isdigit():
                    raise CellIsNotEmpty('Can`t make a move on non-empty cell')
                if move > 8:
                    raise IndexError('Out of range! Game field isn`t that big')
            except (InvalidMove, CellIsNotEmpty, IndexError, ValueError) as er:
                print(er)
                print(self.human.name + ', try again, don`t despair!')
                move = None
        return move


class Player:
    """Class for Player representation"""
    def __init__(self, name, symbol):
        """Create new Player"""
        self.name = name
        self.symbol = symbol


class CellIsNotEmpty(Exception):
    pass


class InvalidMove(Exception):
    pass


if __name__ == '__main__':  # play the game
    name = input('Input your name: ')
    game = TicTacToe(name if name else 'Godzilla')
    game.launch()
