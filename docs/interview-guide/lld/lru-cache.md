---
sidebar_position: 4
title: "Design LRU Cache"
description: >-
  Complete LLD for LRU Cache. Hash map + doubly linked list implementation
  with O(1) operations.
keywords:
  - LRU cache design
  - LRU cache implementation
  - cache eviction
  - doubly linked list
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - Hash Tables
  - Linked Lists
companies: [Amazon, Google, Meta, Microsoft]
---

# Design LRU Cache

LRU Cache is both a coding problem and a design problem. It tests data structure knowledge and implementation skill.

---

## Requirements

- `get(key)`: Return value if exists, else -1
- `put(key, value)`: Insert or update. Evict LRU if at capacity.
- Both operations must be O(1)

---

## The Insight

**Hash Map alone:** O(1) access, but can't track order
**Linked List alone:** Tracks order, but O(n) access

**Hash Map + Doubly Linked List:** O(1) for both!

```
Hash Map: key → Node (for O(1) lookup)
DLL: Maintains recency order (for O(1) eviction)

Most Recent ←→ Node ←→ Node ←→ ... ←→ Least Recent
    HEAD                                    TAIL
```

---

## Implementation

```python
class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        
        # Dummy head and tail for easier edge case handling
        self.head = Node()  # Most recently used
        self.tail = Node()  # Least recently used
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_to_head(self, node: Node):
        """Add node right after head (most recent)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node: Node):
        """Remove node from its current position."""
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _move_to_head(self, node: Node):
        """Move existing node to head (mark as most recent)."""
        self._remove_node(node)
        self._add_to_head(node)
    
    def _remove_tail(self) -> Node:
        """Remove and return the least recently used node."""
        node = self.tail.prev
        self._remove_node(node)
        return node
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._move_to_head(node)  # Mark as recently used
        return node.value
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update existing
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # Add new
            node = Node(key, value)
            self.cache[key] = node
            self._add_to_head(node)
            
            if len(self.cache) > self.capacity:
                # Evict LRU
                lru = self._remove_tail()
                del self.cache[lru.key]
```

---

## Visualization

```
Initial state (capacity=3):
HEAD ←→ TAIL

After put(1, 'A'):
HEAD ←→ [1:A] ←→ TAIL

After put(2, 'B'):
HEAD ←→ [2:B] ←→ [1:A] ←→ TAIL

After put(3, 'C'):
HEAD ←→ [3:C] ←→ [2:B] ←→ [1:A] ←→ TAIL

After get(1):  # Move 1 to front
HEAD ←→ [1:A] ←→ [3:C] ←→ [2:B] ←→ TAIL

After put(4, 'D'):  # Capacity exceeded, evict LRU (2)
HEAD ←→ [4:D] ←→ [1:A] ←→ [3:C] ←→ TAIL
```

---

## Complexity

| Operation | Time | Space |
|-----------|------|-------|
| get | O(1) | - |
| put | O(1) | - |
| Overall | - | O(capacity) |

---

## Using OrderedDict (Simpler)

Python's OrderedDict handles the complexity internally:

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # Mark as recently used
        return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove oldest
```

---

## Follow-up Questions

### Thread-Safe LRU

```python
import threading

class ThreadSafeLRUCache(LRUCache):
    def __init__(self, capacity):
        super().__init__(capacity)
        self.lock = threading.Lock()
    
    def get(self, key):
        with self.lock:
            return super().get(key)
    
    def put(self, key, value):
        with self.lock:
            super().put(key, value)
```

### TTL-Based Eviction

```python
class LRUCacheWithTTL:
    def __init__(self, capacity, ttl_seconds):
        self.capacity = capacity
        self.ttl = ttl_seconds
        self.cache = OrderedDict()
        self.timestamps = {}
    
    def get(self, key):
        if key not in self.cache:
            return -1
        if time.time() - self.timestamps[key] > self.ttl:
            del self.cache[key]
            del self.timestamps[key]
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]
```

---

## Key Takeaways

1. **Hash Map + DLL** enables O(1) for both access and eviction.
2. **Dummy nodes** simplify edge cases (empty list, single element).
3. **OrderedDict** provides a simpler implementation in Python.
4. **Know both versions** for interviews.
