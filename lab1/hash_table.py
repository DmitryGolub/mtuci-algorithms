class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.buckets = [[] for _ in range(size)]
        self.count = 0

    def _bucket_index(self, key):
        return hash(key) % self.size

    def set(self, key, value):
        bucket = self.buckets[self._bucket_index(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.count += 1

    def get(self, key):
        bucket = self.buckets[self._bucket_index(key)]
        for existing_key, value in bucket:
            if existing_key == key:
                return value
        return None

    def remove(self, key):
        bucket = self.buckets[self._bucket_index(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                del bucket[i]
                self.count -= 1
                return True
        return False

    @property
    def load_factor(self):
        return self.count / self.size

    def collision_count(self):
        return sum(len(bucket) - 1 for bucket in self.buckets if bucket)

    def max_chain_length(self):
        return max(len(bucket) for bucket in self.buckets)
