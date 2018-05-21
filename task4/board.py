import random

from anytree import Node, find


class Board:
    """Class for Board representation"""
    def __init__(self, board, last_turn=None):
        """Create new Board"""
        self.board = board  # string
        self.opponent = self.board[last_turn] if last_turn is not None else 'O'
        self.player = 'O' if self.opponent == 'X' else 'X'
        self.root = None

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
            board = position.name
            winner = self.check_win(board)
            if winner:
                position.mark = 'win' + winner
                leaves.append(position)
                return
            poss_moves = [int(i) - 1 for i in board if i != 'O' and i != 'X']
            if not poss_moves:
                position.mark = 'draw'
                leaves.append(position)
                return

            for i in range(len(poss_moves)):
                move = poss_moves[i]
                next_board = board[:move] + curr_player + board[move + 1:]
                # TO DO: check if board is already in a tree
                # if not find(self.root, filter_=lambda x: x.name == board):
                p = Node(next_board, parent=position, mark=None)
                add(p, 'X' if curr_player == 'O' else 'O', leaves)
            return leaves

        self.root = Node(self.board, mark=None)
        leaves = add(self.root, self.player)
        return leaves

    def choose_move(self):
        """Choose the best move for computer"""
        leaves = self.make_tree()
        parents = {x.name: 0 for x in self.root.children}
        for leaf in leaves:
            parent = self.find_parent(leaf).name
            if leaf.mark == 'win' + self.player:
                if parent == leaf.name:
                    for i in range(9):
                        if leaf.name[i] != parent[i]:
                            return i
                parents[parent] += 1
            elif leaf.mark == 'win' + self.opponent:
                parents[parent] -= 1

        mean = sum(parents.values()) / len(parents)  # check if all chances are
        if not all(parents[z] == mean for z in parents.keys()):  # not equal
            next_board = max(parents, key=lambda x: parents[x])
        else:
            next_board = random.choice(list(parents.keys()))
        for i in range(9):
            if self.board[i] != next_board[i]:
                return i

    def find_parent(self, node):
        """Find second parent of node from the start of the tree"""
        while node.parent != self.root:
            node = node.parent
        return node

    def draw(self):
        """Print the game board"""
        print('\n   1 2 3')
        for i in range(3):
            print(' ' + str(i + 1), end=' ')
            for j in range(3):
                cell = self.board[i * 3:][j]
                print(cell if cell == 'O' or cell == 'X' else ' ', end=' ')
            print()
