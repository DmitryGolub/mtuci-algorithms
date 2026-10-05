from bst import height, inorder, insert, search
from range_queries import FenwickTree, StatsSegmentTree, build_prefix, range_sum_prefix


class Sensor:
    def __init__(self, sensor_id, name, measurements=None):
        self.sensor_id = sensor_id
        self.name = name
        self.measurements = list(measurements) if measurements else []


class SensorRegistry:
    def __init__(self):
        self.root = None
        self.count = 0

    def add(self, sensor):
        self.root = insert(self.root, sensor.sensor_id, sensor)
        self.count += 1

    def find(self, sensor_id):
        node, visited = search(self.root, sensor_id)
        return (node.value if node else None), visited

    def sorted_ids(self):
        return inorder(self.root)

    def height(self):
        return height(self.root)


class MeasurementAnalyzer:
    def __init__(self, measurements):
        self.values = list(measurements)
        self.prefix = build_prefix(self.values)
        self.fenwick = FenwickTree(self.values)
        self.segment = StatsSegmentTree(self.values)

    def sum_prefix(self, left, right):
        return range_sum_prefix(self.prefix, left, right)

    def sum_fenwick(self, left, right):
        return self.fenwick.range_sum(left, right)

    def stats(self, left, right):
        return self.segment.query(left, right)

    def update(self, index, value):
        delta = value - self.values[index]
        self.values[index] = value
        self.fenwick.update(index, delta)
        self.segment.update(index, value)
        self.prefix = build_prefix(self.values)
