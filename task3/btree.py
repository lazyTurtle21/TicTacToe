from modules.binary_tree import BinaryTree
from btnode import Node, Position


class LinkedBinaryTree(BinaryTree):
    """Linked representation of a binary tree structure."""

    def _validate(self, p):
        """Return associated node, if position is valid."""
        if not isinstance(p, Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:  # convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """Return Position instance for given node (or None if no node)."""
        return Position(self, node) if node is not None else None

    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    def __len__(self):
        """Return the total number of elements in the tree."""
        return self._size

    def root(self):
        """Return the root Position of the tree (or None if tree is empty)."""
        return self._make_position(self._root)

    def parent(self, p):
        """Return the Position of p's parent (or None if p is root)."""
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p):
        """Return the Position of p's left child (or None if no left child)."""
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        """Return the Position of p's right child
        (or None if no right child)."""
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        """Return the number of children of Position p."""
        node = self._validate(p)
        count = 0
        if node._left is not None:  # left child exists
            count += 1
        if node._right is not None:  # right child exists
            count += 1
        return count

    def add(self, e, p=None, mark=None):
        """Add element e at position p"""
        if not self._root:
            return self.add_root(e, mark)
        else:
            if p._node._left is None:
                return self.add_left(p, e, mark=None)
            elif p._node._right is None:
                return self.add_right(p, e, mark=None)
            else:
                raise ValueError('No free place')

    def add_root(self, e, mark=None):
        """Place element e at the root of an empty tree and return new Position.

        Raise ValueError if tree nonempty.
        """
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1
        self._root = Node(e, mark=mark)
        return self._make_position(self._root)

    def add_left(self, p, e, mark=None):
        """Create a new left child for Position p, storing element e.

        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a left child.
        """
        node = self._validate(p)
        if node._left is not None:
            raise ValueError('Left child exists')
        self._size += 1
        node._left = Node(e, node, mark=mark)  # node is its parent
        return self._make_position(node._left)

    def add_right(self, p, e, mark=None):
        """Create a new right child for Position p, storing element e.

        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a right child.
        """
        node = self._validate(p)
        if node._right is not None:
            raise ValueError('Right child exists')
        self._size += 1
        node._right = Node(e, node, mark=mark)  # node is its parent
        return self._make_position(node._right)

    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node is not None:
                s += recurse(node._right, level + 1)
                s += "| " * level
                s += str(node._element) + (node.mark
                                           if node.mark else '') + "\n"
                s += recurse(node._left, level + 1)
            return s

        return recurse(self._root, 0)

    def mark(self, p, mark):
        """Mark certain Node at position p"""
        node = self._validate(p)
        node.mark = mark

    def find_parent(self, node):
        """Find second parent of node from the start of the tree"""
        while self.parent(node) != self.root():
            node = self.parent(node)
        return node

    def _replace(self, p, e):
        """Replace the element at position p with e, and return old element."""
        node = self._validate(p)
        old = node._element
        node._element = e
        return old

    def delete(self, p):
        """Delete the node at Position p, and replace it with its child, if any.

        Return the element that had been stored at Position p.
        Raise ValueError if Position p is invalid or p has two children.
        """
        node = self._validate(p)
        print(node._left)
        if self.num_children(p) == 2:
            raise ValueError('Position has two children')
        child = node._left if node._left else node._right  # might be None
        if child is not None:
            child._parent = node._parent  # child's grandparent becomes parent
        if node is self._root:
            self._root = child  # child becomes root
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node  # convention for deprecated node
        return node._element
