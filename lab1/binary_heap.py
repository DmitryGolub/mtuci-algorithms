def parent(index):
    return (index - 1) // 2


def left(index):
    return 2 * index + 1


def right(index):
    return 2 * index + 2


class MinHeap:
    def __init__(self):
        self.data = []

    def _sift_up(self, index):
        while index > 0:
            p = parent(index)
            if self.data[p] <= self.data[index]:
                break
            self.data[p], self.data[index] = self.data[index], self.data[p]
            index = p

    def push(self, value):
        self.data.append(value)
        self._sift_up(len(self.data) - 1)

    def _sift_down(self, index):
        size = len(self.data)
        while True:
            l, r = left(index), right(index)
            smallest = index
            if l < size and self.data[l] < self.data[smallest]:
                smallest = l
            if r < size and self.data[r] < self.data[smallest]:
                smallest = r
            if smallest == index:
                break
            self.data[index], self.data[smallest] = self.data[smallest], self.data[index]
            index = smallest

    def pop(self):
        root = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self._sift_down(0)
        return root

    def is_valid(self):
        size = len(self.data)
        for i in range(size):
            for child in (left(i), right(i)):
                if child < size and self.data[child] < self.data[i]:
                    return False
        return True
