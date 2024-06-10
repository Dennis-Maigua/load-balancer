import hashlib
import bisect

class ConsistentHash:
    def __init__(self, num_slots=512, num_virtual_servers=9):
        self.num_slots = num_slots
        self.num_virtual_servers = num_virtual_servers
        self.slots = []
        self.nodes = {}

    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16) % self.num_slots

    def add_node(self, node):
        for i in range(self.num_virtual_servers):
            virtual_node_key = f"{node}-{i}"
            hash_key = self._hash(virtual_node_key)
            self.slots.append(hash_key)
            self.nodes[hash_key] = node
        self.slots.sort()

    def remove_node(self, node):
        for i in range(self.num_virtual_servers):
            virtual_node_key = f"{node}-{i}"
            hash_key = self._hash(virtual_node_key)
            self.slots.remove(hash_key)
            del self.nodes[hash_key]

    def get_node(self, key):
        hash_key = self._hash(key)
        index = bisect.bisect(self.slots, hash_key) % len(self.slots)
        return self.nodes[self.slots[index]]
