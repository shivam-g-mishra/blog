---
sidebar_position: 2
title: "Coding Interview Mock"
description: >-
  Complete coding interview mock with timing, hints, and evaluation.
  Practice like a real interview.
keywords:
  - coding mock interview
  - practice interview
  - coding interview
difficulty: Intermediate
estimated_time: 45 minutes
prerequisites:
  - Data Structures
  - Patterns
companies: [All Companies]
---

# Coding Interview Mock

Practice a realistic 45-minute coding interview. Set a timer and work through this.

---

## Format

```
0:00 - 0:05  Problem understanding, clarifying questions
0:05 - 0:10  Approach discussion
0:10 - 0:35  Implementation
0:35 - 0:40  Testing
0:40 - 0:45  Complexity analysis, follow-ups
```

---

## Problem 1: Medium (25 minutes)

### Merge Intervals

**Given** an array of intervals where `intervals[i] = [start, end]`, merge all overlapping intervals.

**Example:**
```
Input: [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
```

---

### Hints (reveal progressively)

<details>
<summary>Hint 1 (after 3 min stuck)</summary>

What if you sort the intervals first? By what criteria?

</details>

<details>
<summary>Hint 2 (after 5 min stuck)</summary>

Sort by start time. Then iterate and check if current overlaps with previous.

</details>

<details>
<summary>Hint 3 (after 8 min stuck)</summary>

Two intervals overlap if `current.start <= previous.end`. Merge by taking `max(previous.end, current.end)`.

</details>

---

### Expected Solution

```python
def merge(intervals):
    if not intervals:
        return []
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    result = [intervals[0]]
    
    for current in intervals[1:]:
        last = result[-1]
        
        if current[0] <= last[1]:  # Overlapping
            last[1] = max(last[1], current[1])
        else:
            result.append(current)
    
    return result
```

**Complexity:** O(n log n) time, O(n) space

---

### Evaluation Criteria

| Criteria | Points | Notes |
|----------|--------|-------|
| Clarified edge cases | 10 | Empty input, single interval |
| Correct approach | 20 | Sorting + linear scan |
| Clean code | 20 | Variable names, structure |
| Bug-free | 20 | Handles overlaps correctly |
| Complexity analysis | 15 | Time and space |
| Test cases | 15 | Edge cases covered |

---

## Problem 2: Medium-Hard (20 minutes)

### LRU Cache

Design a data structure that supports `get` and `put` in O(1) time.

- `get(key)`: Return value if key exists, else -1
- `put(key, value)`: Insert or update. If at capacity, evict least recently used.

**Example:**
```
LRUCache cache = new LRUCache(2);
cache.put(1, 1);
cache.put(2, 2);
cache.get(1);       // returns 1
cache.put(3, 3);    // evicts key 2
cache.get(2);       // returns -1
```

---

### Hints

<details>
<summary>Hint 1</summary>

You need O(1) lookup AND O(1) removal. What data structures give you each?

</details>

<details>
<summary>Hint 2</summary>

HashMap for O(1) lookup. Doubly linked list for O(1) removal and insertion.

</details>

<details>
<summary>Hint 3</summary>

Keep most recently used at head, least recently used at tail. HashMap stores key → node mapping.

</details>

---

### Expected Solution

```python
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = Node()  # Dummy head
        self.tail = Node()  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.val
        return -1
    
    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        
        node = Node(key, value)
        self._add(node)
        self.cache[key] = node
        
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
    
    def _add(self, node):
        # Add to head (most recent)
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
    
    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
```

---

## Self-Evaluation Rubric

After completing both problems, score yourself:

| Category | Excellent (A) | Good (B) | Needs Work (C) |
|----------|---------------|----------|----------------|
| **Problem Understanding** | Asked good clarifying questions | Some questions | Jumped to coding |
| **Approach** | Optimal solution quickly | Got there with hints | Needed significant help |
| **Coding** | Clean, bug-free first try | Minor bugs fixed quickly | Major bugs or messy |
| **Communication** | Explained clearly throughout | Mostly communicated | Coded silently |
| **Testing** | Comprehensive test cases | Basic testing | No testing |
| **Time Management** | Finished with time to spare | Just finished | Ran out of time |

---

## Follow-Up Questions

Be prepared for:

**Merge Intervals:**
- How would you insert a new interval into already merged list?
- What if intervals are streaming in real-time?

**LRU Cache:**
- How would you make this thread-safe?
- Design LFU (Least Frequently Used) cache instead.

---

## Key Takeaways

1. **Always clarify** before coding.
2. **State your approach** before implementing.
3. **Test with examples** as you code.
4. **Think out loud**—silence is your enemy.
5. **Practice with timer** to simulate pressure.
