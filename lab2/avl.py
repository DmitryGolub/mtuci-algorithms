from bst import Node


class AVLNode(Node):
    def __init__(self, key):
        super().__init__(key)
        self.height = 0


def node_height(node):
    if node is None:
        return -1
    return node.height


def update_height(node):
    node.height = 1 + max(node_height(node.left), node_height(node.right))


def balance_factor(node):
    return node_height(node.left) - node_height(node.right)


def rotate_right(node):
    new_root = node.left
    node.left = new_root.right
    new_root.right = node
    update_height(node)
    update_height(new_root)
    return new_root


def rotate_left(node):
    new_root = node.right
    node.right = new_root.left
    new_root.left = node
    update_height(node)
    update_height(new_root)
    return new_root


def imbalance_case(node):
    balance = balance_factor(node)
    if balance > 1:
        return "LL" if balance_factor(node.left) >= 0 else "LR"
    if balance < -1:
        return "RR" if balance_factor(node.right) <= 0 else "RL"
    return None


def rebalance(node):
    case = imbalance_case(node)
    if case == "LL":
        return rotate_right(node)
    if case == "RR":
        return rotate_left(node)
    if case == "LR":
        node.left = rotate_left(node.left)
        return rotate_right(node)
    if case == "RL":
        node.right = rotate_right(node.right)
        return rotate_left(node)
    return node


def avl_insert(root, key, balance=True):
    if root is None:
        return AVLNode(key)
    if key < root.key:
        root.left = avl_insert(root.left, key, balance)
    elif key > root.key:
        root.right = avl_insert(root.right, key, balance)
    else:
        return root
    update_height(root)
    return rebalance(root) if balance else root
