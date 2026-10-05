class Node:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


def insert(root, key, value=None):
    if root is None:
        return Node(key, value)
    current = root
    while True:
        if key == current.key:
            current.value = value
            return root
        if key < current.key:
            if current.left is None:
                current.left = Node(key, value)
                return root
            current = current.left
        else:
            if current.right is None:
                current.right = Node(key, value)
                return root
            current = current.right


def build_bst(keys):
    root = None
    for key in keys:
        root = insert(root, key)
    return root


def search(root, key):
    current = root
    visited = 0
    while current is not None:
        visited += 1
        if key == current.key:
            return current, visited
        if key < current.key:
            current = current.left
        else:
            current = current.right
    return None, visited


def preorder(root):
    if root is None:
        return []
    return [root.key] + preorder(root.left) + preorder(root.right)


def inorder(root):
    if root is None:
        return []
    return inorder(root.left) + [root.key] + inorder(root.right)


def postorder(root):
    if root is None:
        return []
    return postorder(root.left) + postorder(root.right) + [root.key]


def find_min(root):
    current = root
    while current.left is not None:
        current = current.left
    return current


def delete(root, key):
    if root is None:
        return None
    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        successor = find_min(root.right)
        root.key = successor.key
        root.value = successor.value
        root.right = delete(root.right, successor.key)
    return root


def height(root):
    if root is None:
        return -1
    return 1 + max(height(root.left), height(root.right))
