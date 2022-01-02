import copy
from ast import literal_eval
from aoc_utils import read_lines_lazy

EXPLODE_DEPTH = 4
SPLIT_VALUE = 10


class TreeNode:
    parent = None
    children = None
    siblings = None
    depth = 0

    def __init__(self, parent, init_list):
        self.parent = parent
        self.__set_children(init_list)

    def __set_children(self, children_list):
        if not isinstance(children_list, list):
            self.children = children_list
        else:
            if all(map(lambda x: isinstance(x, TreeNode), children_list)):
                self.children = copy.deepcopy(children_list)
                for i in range(len(self.children)):
                    self.children[i].parent = self
                self.__update_depth()
            else:
                self.__update_depth()
                self.children = list(map(lambda x: TreeNode(self, x), children_list))

            for i in range(len(self.children)):
                self.children[i].siblings = [self.children[0:i], self.children[i+1:]]

    def __update_depth(self):
        self.depth = 0 if self.parent is None else self.parent.depth + 1
        if not self.is_leaf():
            for child in self.children:
                child.__update_depth()

    def is_leaf(self):  # Regular numbers are leaves
        return not isinstance(self.children, list)

    def is_root(self):
        return self.parent is None

    def has_only_leaves(self):
        return not self.is_leaf() and all(map(lambda x: x.is_leaf(), self.children))

    def get_root(self):
        return self if self.is_root() else self.parent.get_root()

    def get_left_sibling(self, recursive=False):
        if self.is_root():
            return None
        if self.siblings[0]:
            return self.siblings[0][-1]
        if not recursive:
            return None
        return self.parent.get_left_sibling(recursive)

    def get_right_sibling(self, recursive=False):
        if self.is_root():
            return None
        if self.siblings[1]:
            return self.siblings[1][0]
        if not recursive:
            return None
        return self.parent.get_right_sibling(recursive)

    def get_leftmost_leaf(self):
        return self if self.is_leaf() else self.children[0].get_leftmost_leaf()

    def get_rightmost_leaf(self):
        return self if self.is_leaf() else self.children[-1].get_rightmost_leaf()

    def get_nearest_left_leaf(self):
        subtree = self.get_left_sibling(True)
        return subtree.get_rightmost_leaf() if subtree is not None else None

    def get_nearest_right_leaf(self):
        subtree = self.get_right_sibling(True)
        return subtree.get_leftmost_leaf() if subtree is not None else None

    def can_explode(self):
        global EXPLODE_DEPTH
        return self.depth >= EXPLODE_DEPTH and self.has_only_leaves()

    def can_split(self):
        global SPLIT_VALUE
        return self.is_leaf() and int(self.children) >= SPLIT_VALUE

    def explode(self):
        did_explode = False
        if self.can_explode():
            left_value = int(self.children[0].children)
            right_value = int(self.children[-1].children)
            self.children = 0

            left = self.get_nearest_left_leaf()
            right = self.get_nearest_right_leaf()

            if left is not None:
                left.children += left_value
            if right is not None:
                right.children += right_value
            # print("EXP", self.get_root())
            did_explode = True
        elif not self.is_leaf():
            # Explode all
            for child in self.children:
                if child.explode():
                    did_explode = True
        return did_explode

    def split(self):
        if self.can_split():
            left_value = int(self.children) // 2
            right_value = int(self.children) - left_value
            self.__set_children([left_value, right_value])
            # print("SPL", self.get_root())
            return True

        if not self.is_leaf():
            # Split first child only (because explode has higher priority)
            for child in self.children:
                if child.split():
                    return True

        return False

    def reduce(self):
        e = s = True
        while e or s:
            e = self.explode()
            s = self.split()

    def get_magnitude(self):
        if self.is_leaf():
            return int(self.children)
        return 3 * self.children[0].get_magnitude() + 2 * self.children[-1].get_magnitude()

    def __add__(self, other):
        return TreeNode(None, [self, other])

    def __str__(self):
        if self.is_leaf():
            return str(self.children)
        return '[' + ','.join(list(map(str, self.children))) + ']'


# Load the values
VALUES = list(map(lambda x: TreeNode(None, literal_eval(x)), read_lines_lazy('day18.txt')))

# Sum them & print magnitude
agg = VALUES[0]
for i in range(1, len(VALUES)):
    agg = agg + VALUES[i]
    agg.reduce()
print("Part 1:", agg.get_magnitude())

# Check all the sums & find the maximal magnitude
max_magnitude = 0
for i in range(len(VALUES)):
    for j in range(len(VALUES)):
        x = VALUES[i] + VALUES[j]
        y = VALUES[j] + VALUES[i]
        x.reduce()
        y.reduce()
        mag = max(x.get_magnitude(), y.get_magnitude())
        if mag > max_magnitude:
            max_magnitude = mag
print("Part 2:", max_magnitude)


