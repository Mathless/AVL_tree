# Node class
class Node:
    def __init__(self, val=None):
        self.val = val
        self._left = None
        self._right = None
        self._height = 0
        self._balance = 0  # good: {-1, 0, 1}

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def height(self):
        return self._height

    @property
    def balance(self):
        return self._balance

    def _update(self):
        if self.left:
            l = self.left._height
        else:
            l = -1
        if self.right:
            r = self.right._height
        else:
            r = -1

        self._height = 1 + max(l, r)
        self._balance = r - l

    @left.setter
    def left(self, node):
        self._left = node
        self._update()

    @right.setter
    def right(self, node):
        self._right = node
        self._update()

    # Function for printing binary tree,
    # source: https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.val
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.val
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.val
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.val
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


class Tree:

    def __init__(self):
        self.node = None

    #        a   = h
    #      /
    #    b       = h + {1, 2}
    #   /
    # c          = h + 2
    def _ll(self, root):
        t = root.left  # t = b
        root.left = t.right  # a.l = t.r
        t.right = root  # t.r = a

        return t

    # a         = h
    #  \
    #   b       = h + {1, 2}
    #    \
    #     c     = h + 2
    def _rr(self, root):
        t = root.right  # t = b
        root.right = t.left  # a.r = b.l
        t.left = root  # t.l = a
        return t

    #        a   = h
    #      /
    #    b       = h + {1, 2}
    #    \
    #     c      = h + 2
    def _lr(self, root):
        root.left = self._rr(root.left)
        return self._ll(root)

    # a         = h
    #  \
    #   b       = h + {1, 2}
    #   /
    # c         = h + 2
    def _rl(self, root):
        root.right = self._ll(root.right)
        return self._rr(root)

    def _rebalance(self, root):
        if root.balance > 1:
            if root.right.balance >= 0:
                root = self._rr(root)
            else:
                root = self._rl(root)

        elif root.balance < -1:
            if root.right.balance <= 0:
                root = self._ll(root)
            else:
                root = self._lr(root)
        return root

    def _add(self, root, element):
        if not root:  # Creating new Node
            return Node(element)
        if element < root.val:
            root.left = self._add(root.left, element)
        else:
            root.right = self._add(root.right, element)
        return self._rebalance(root)  # We go down and when we go up we balance the tree

    def add(self, element):
        self.node = self._add(self.node, element)

    def _search(self, element, node):
        if node == None:
            return False
        if node.val == element:
            return True
        if element >= node.val:
            return self._search(element, node.right)
        else:
            return self._search(element, node.left)

    def search(self, element):
        if self.node is None:
            return False
        if self.node.val == element:
            return True
        return self._search(element, self.node)

    def _inorder(self, root):
        if root:
            self._inorder(root.left)
            self.inorder_list.append(root.val)
            self._inorder(root.right)

    def inorder(self):
        self.inorder_list = []
        self._inorder(self.node)
        return self.inorder_list

    def postorder(self):
        return self.inorder()[::-1]


if __name__ == "__main__":
    tree = Tree()
    tree.add(1)
    tree.add(2)
    for j in range(3, 10):
        tree.add(j)
        tree.node.display()
    for j in range(3, 10):
        tree.add(j)
        tree.node.display()
    print(tree.inorder())
    print(tree.postorder())
