import math


def range_sum_naive(data, left, right):
    total = 0
    for i in range(left, right + 1):
        total += data[i]
    return total


def build_prefix(data):
    prefix = [0] * (len(data) + 1)
    for i, value in enumerate(data):
        prefix[i + 1] = prefix[i] + value
    return prefix


def range_sum_prefix(prefix, left, right):
    return prefix[right + 1] - prefix[left]


class FenwickTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (self.n + 1)
        for index, value in enumerate(data):
            self.update(index, value)

    def update(self, index, delta):
        i = index + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def prefix_sum(self, index):
        i = index + 1
        result = 0
        while i > 0:
            result += self.tree[i]
            i -= i & -i
        return result

    def range_sum(self, left, right):
        if left == 0:
            return self.prefix_sum(right)
        return self.prefix_sum(right) - self.prefix_sum(left - 1)


class SegmentTree:
    neutral = 0

    def __init__(self, data):
        self.n = len(data)
        self.tree = [self.neutral] * (4 * self.n)
        self._build(data, 1, 0, self.n - 1)

    def leaf(self, value):
        return value

    def merge(self, a, b):
        return a + b

    def _build(self, data, node, start, end):
        if start == end:
            self.tree[node] = self.leaf(data[start])
            return
        mid = (start + end) // 2
        self._build(data, 2 * node, start, mid)
        self._build(data, 2 * node + 1, mid + 1, end)
        self.tree[node] = self.merge(self.tree[2 * node], self.tree[2 * node + 1])

    def query(self, left, right):
        return self._query(1, 0, self.n - 1, left, right)

    def _query(self, node, start, end, left, right):
        if right < start or end < left:
            return self.neutral
        if left <= start and end <= right:
            return self.tree[node]
        mid = (start + end) // 2
        return self.merge(
            self._query(2 * node, start, mid, left, right),
            self._query(2 * node + 1, mid + 1, end, left, right),
        )

    def update(self, index, value):
        self._update(1, 0, self.n - 1, index, value)

    def _update(self, node, start, end, index, value):
        if start == end:
            self.tree[node] = self.leaf(value)
            return
        mid = (start + end) // 2
        if index <= mid:
            self._update(2 * node, start, mid, index, value)
        else:
            self._update(2 * node + 1, mid + 1, end, index, value)
        self.tree[node] = self.merge(self.tree[2 * node], self.tree[2 * node + 1])


class StatsSegmentTree(SegmentTree):
    neutral = (0, math.inf, -math.inf)

    def leaf(self, value):
        return (value, value, value)

    def merge(self, a, b):
        return (a[0] + b[0], min(a[1], b[1]), max(a[2], b[2]))
