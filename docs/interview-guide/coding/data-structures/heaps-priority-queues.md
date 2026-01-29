---
sidebar_position: 6
title: "Heaps & Priority Queues — Top K, Median & More"
description: >-
  Master heaps for coding interviews. Learn when to use min/max heap, solve
  top K problems, find running median, and merge sorted lists.
keywords:
  - heap interview questions
  - priority queue
  - top k elements
  - kth largest
  - running median
difficulty: Intermediate
estimated_time: 35 minutes
prerequisites:
  - Big-O Notation
  - Arrays & Strings
companies: [Google, Meta, Amazon, Microsoft, Apple]
---

# Heaps: When You Need the Min or Max Repeatedly

There's a category of problems where you need to repeatedly find the smallest or largest element. Arrays give you O(n) per query. Sorting gives you O(n log n) upfront. But heaps? O(log n) per operation, O(1) to peek.

**Whenever you see "kth largest," "top K," or "running median"—think heap.**

---

## Heap Fundamentals

A heap is a complete binary tree where each parent is smaller (min-heap) or larger (max-heap) than its children.

```
Min-Heap:           Max-Heap:
     1                  9
    / \                / \
   3   2              7   8
  / \                / \
 7   4              3   5
```

### Python's heapq (Min-Heap)

```python
import heapq

# Create heap
heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 4)
# heap is now [1, 3, 4]

# Peek minimum
min_val = heap[0]  # 1, O(1)

# Pop minimum
min_val = heapq.heappop(heap)  # 1, O(log n)

# Heapify a list
nums = [3, 1, 4, 1, 5]
heapq.heapify(nums)  # O(n)

# Push and pop in one operation
result = heapq.heappushpop(heap, 2)  # More efficient
```

### Max-Heap Trick

Python only has min-heap. For max-heap, negate values:

```python
# Max-heap using negation
max_heap = []
heapq.heappush(max_heap, -5)
heapq.heappush(max_heap, -3)
heapq.heappush(max_heap, -7)

max_val = -heapq.heappop(max_heap)  # 7
```

### Complexity

| Operation | Time |
|-----------|------|
| Push | O(log n) |
| Pop | O(log n) |
| Peek | O(1) |
| Heapify | O(n) |

---

## The Three Heap Patterns

### Pattern 1: Top K Elements

**Problem:** Find the K largest or smallest elements.

**Key insight:** Use a heap of size K.
- For K largest: use min-heap (keeps K largest, pops smallest)
- For K smallest: use max-heap (keeps K smallest, pops largest)

```python
# Kth Largest Element
def find_kth_largest(nums, k):
    # Min-heap of size k
    heap = nums[:k]
    heapq.heapify(heap)
    
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)  # Push and pop
    
    return heap[0]

# Top K Frequent Elements
def top_k_frequent(nums, k):
    count = Counter(nums)
    
    # Min-heap of (frequency, num), keep k largest frequencies
    heap = []
    
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)
    
    return [num for freq, num in heap]
```

### Pattern 2: Two Heaps (Running Median)

**Problem:** Track median as elements arrive.

**Key insight:** Keep two heaps:
- Max-heap for smaller half
- Min-heap for larger half

```python
class MedianFinder:
    def __init__(self):
        self.small = []  # Max-heap (negated)
        self.large = []  # Min-heap
    
    def addNum(self, num):
        # Add to max-heap first
        heapq.heappush(self.small, -num)
        
        # Balance: largest of small should be <= smallest of large
        if self.small and self.large and -self.small[0] > self.large[0]:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Balance sizes (small can have at most 1 more)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2
```

### Pattern 3: K-Way Merge

**Problem:** Merge K sorted lists/arrays.

**Key insight:** Keep one element from each list in heap.

```python
def merge_k_lists(lists):
    heap = []
    
    # Add first element from each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0].val, i, lst[0]))
    
    dummy = ListNode(0)
    curr = dummy
    
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    
    return dummy.next
```

---

## Classic Interview Problems

### Problem 1: K Closest Points to Origin

```python
def k_closest(points, k):
    # Max-heap of size k (negate distance)
    heap = []
    
    for x, y in points:
        dist = x*x + y*y
        
        if len(heap) < k:
            heapq.heappush(heap, (-dist, x, y))
        elif -dist > heap[0][0]:
            heapq.heapreplace(heap, (-dist, x, y))
    
    return [[x, y] for _, x, y in heap]
```

### Problem 2: Task Scheduler

```python
def least_interval(tasks, n):
    count = Counter(tasks)
    max_heap = [-c for c in count.values()]
    heapq.heapify(max_heap)
    
    time = 0
    
    while max_heap:
        cycle = []
        
        for _ in range(n + 1):
            if max_heap:
                cnt = heapq.heappop(max_heap)
                if cnt + 1 < 0:
                    cycle.append(cnt + 1)
            time += 1
            
            if not max_heap and not cycle:
                break
        
        for cnt in cycle:
            heapq.heappush(max_heap, cnt)
    
    return time
```

### Problem 3: Reorganize String

```python
def reorganize_string(s):
    count = Counter(s)
    max_heap = [(-c, char) for char, c in count.items()]
    heapq.heapify(max_heap)
    
    result = []
    prev_count, prev_char = 0, ''
    
    while max_heap:
        count, char = heapq.heappop(max_heap)
        result.append(char)
        
        # Add back previous char if still has count
        if prev_count < 0:
            heapq.heappush(max_heap, (prev_count, prev_char))
        
        prev_count, prev_char = count + 1, char
    
    result_str = ''.join(result)
    return result_str if len(result_str) == len(s) else ""
```

---

## When to Use Heap

| Signal | Use Heap |
|--------|----------|
| "Kth largest/smallest" | Min/Max heap of size K |
| "Top K" | Heap of size K |
| "Running median" | Two heaps |
| "Merge K sorted" | K-way merge |
| "Repeatedly get min/max" | Heap |
| "Schedule by priority" | Priority queue |

---

## Practice Problems

### Easy

| Problem | Pattern | Company |
|---------|---------|---------|
| Kth Largest in Stream | Min Heap | Amazon |
| Last Stone Weight | Max Heap | Google |

### Medium

| Problem | Pattern | Company |
|---------|---------|---------|
| Kth Largest Element | Top K | Meta, Amazon |
| Top K Frequent Elements | Top K | Amazon |
| K Closest Points | Top K | Meta |
| Task Scheduler | Max Heap | Meta |
| Find Median from Stream | Two Heaps | Amazon |

### Hard

| Problem | Pattern | Company |
|---------|---------|---------|
| Merge K Sorted Lists | K-Way Merge | Amazon |
| Sliding Window Median | Two Heaps | Google |
| IPO | Two Heaps | Amazon |

---

## Key Takeaways

1. **Python heapq is min-heap.** Negate values for max-heap.

2. **Top K → heap of size K.** Use opposite heap type (min for largest).

3. **Running median → two heaps.** Max-heap for small, min-heap for large.

4. **Merge K sorted → K-way merge.** One element per list in heap.

5. **O(n log k) beats O(n log n)** when k is much smaller than n.

---

## What's Next?

Now that you've mastered the core data structures, let's learn the patterns that combine them:

👉 [Two Pointers Pattern →](../patterns/array-patterns/two-pointers)
