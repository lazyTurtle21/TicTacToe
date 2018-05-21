from modules.binary_tree import BinaryTree


class Node:
    """Class for storing a node."""
    __slots__ = '_element', '_parent', '_left', '_right', 'mark'

    def __init__(self, element, parent=None, left=None, right=None,
                 mark='unknown'):
        self.mark = mark
        self._element = element
        self._parent = parent
        self._left = left
        self._right = right


class Position(BinaryTree.Position):
    """An abstraction representing the location of a single element."""

    def __init__(self, container, node):
        """Constructor should not be invoked by user."""
        self._container = container
        self._node = node

    def element(self):
        """Return the element stored at this Position."""
        return self._node._element

    def mark(self):
        """Return mark of th node at this position"""
        return self._node.mark

    def __eq__(self, other):
        """Return True if other is a Position representing the same
        location."""
        return type(other) is type(self) and other._node is self._node
