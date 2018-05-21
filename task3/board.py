import random
from btree import LinkedBinaryTree as Tree


class Board:
    """Class for Board representation"""
    def __init__(self, board, last_turn=None):
        """Create new Board"""
        self.board = board  # string
        self.opponent = self.board[last_turn] if last_turn is not None else 'O'
        self.player = 'O' if self.opponent == 'X' else 'X'
        self.tree = Tree()

    def check_win(self, board=None):
        """Checks if there is a winning combination on board"""
        if board is None:
            board = self.board
        if not self.player:
            return False
        for x in range(0, 3):
            row = {board[x * 3:][0], board[x * 3:][1], board[x * 3:][2]}
            column = {board[x], board[x + 3], board[x + 6]}
            if len(column) == 1:
                return board[x]
            if len(row) == 1:
                return board[x * 3:][0]

        diag1 = {board[0], board[4], board[8]}  # diagonals
        diag2 = {board[2], board[4], board[6]}
        if len(diag1) == 1 or len(diag2) == 1:
            return board[4]
        if board.count(self.player) + board.count(self.opponent) == 9:
            return None  # Draw
        return False

    def make_tree(self):
        """Construct a decision tree"""
        def add(position, curr_player, leaves=[]):
            board = position.element()
            winner = self.check_win(board)
            if winner:
                self.tree.mark(position, 'win' + winner)
                leaves.append(position)
                return
            poss_moves = [int(i) - 1 for i in board if i != 'O' and i != 'X']
            if not poss_moves:
                self.tree.mark(position, 'draw')
                leaves.append(position)
                return

            moves = 2 if len(poss_moves) > 1 else 1
            for i in range(moves):
                move = random.choice(poss_moves)
                poss_moves.remove(move)
                p = self.tree.add(board[:move] + curr_player
                                  + board[move + 1:], p=position)
                add(p, 'X' if curr_player == 'O' else 'O', leaves)
            return leaves

        root = self.tree.add(self.board)
        leaves = add(root, self.player)
        return leaves

    def choose_move(self):
        """Choose the best move for computer"""
        leaves = self.make_tree()
        root = self.tree.root()
        right, left = self.tree.right(root), self.tree.left(root)
        parents = {x.element(): 0 for x in [left, right] if x is not None}
        for leaf in leaves:
            parent = self.tree.find_parent(leaf).element()
            if leaf.mark() == 'win' + self.player:
                if parent == leaf.element():
                    for i in range(9):
                        if leaf.element()[i] != parent[i]:
                            return i
                parents[parent] += 1
            elif leaf.mark() == 'win' + self.opponent:
                parents[parent] -= 1

        mean = sum(parents.values()) / len(parents)  # check if all chances are
        if not all(parents[z] == mean for z in parents.keys()):  # not equal
            next_board = max(parents, key=lambda x: parents[x])
        else:
            next_board = random.choice(list(parents.keys()))
        for i in range(9):
            if self.board[i] != next_board[i]:
                return i

    def draw(self):
        """Print the game board"""
        print('\n   1 2 3')
        for i in range(3):
            print(' ' + str(i + 1), end=' ')
            for j in range(3):
                cell = self.board[i * 3:][j]
                print(cell if cell == 'O' or cell == 'X' else ' ', end=' ')
            print()
