---
sidebar_position: 1
title: "Top K Elements Pattern"
description: >-
  Master Top K problems for coding interviews. K largest, K frequent,
  K closest, and heap-based solutions.
keywords:
  - top k elements
  - k largest
  - k frequent
  - heap problems
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - Heaps
companies: [Google, Amazon, Meta, Microsoft]
---

# Top K Elements: Heap Mastery

"Find top K" problems are heap classics. Use min-heap of size K for max efficiency.

---

## The Pattern

```
Need K largest? Use min-heap of size K
- Push element
- If size > K, pop smallest
- At end, heap contains K largest

Why min-heap for K largest?
- Always pop the smallest among candidates
- What remains are the K largest
```

---

## Kth Largest Element

```python
import heapq

def find_kth_largest(nums, k):
    heap = []
    
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    
    return heap[0]  # Kth largest is the smallest in heap

# One-liner using nlargest
def find_kth_largest_simple(nums, k):
    return heapq.nlargest(k, nums)[-1]
```

---

## Top K Frequent Elements

```python
from collections import Counter

def top_k_frequent(nums, k):
    count = Counter(nums)
    
    # Min-heap of (frequency, element)
    heap = []
    
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)
    
    return [num for freq, num in heap]
```

---

## K Closest Points to Origin

```python
def k_closest(points, k):
    # Max-heap (negate distance for max behavior)
    heap = []
    
    for x, y in points:
        dist = -(x * x + y * y)
        heapq.heappush(heap, (dist, x, y))
        if len(heap) > k:
            heapq.heappop(heap)
    
    return [[x, y] for dist, x, y in heap]
```

---

## Sort Characters by Frequency

```python
def frequency_sort(s):
    count = Counter(s)
    
    # Max-heap of (frequency, char)
    heap = [(-freq, char) for char, freq in count.items()]
    heapq.heapify(heap)
    
    result = []
    while heap:
        freq, char = heapq.heappop(heap)
        result.append(char * (-freq))
    
    return ''.join(result)
```

---

## K Closest Numbers in Sorted Array

```python
def find_closest_elements(arr, k, x):
    # Binary search for closest position
    left = 0
    right = len(arr) - k
    
    while left < right:
        mid = (left + right) // 2
        
        if x - arr[mid] > arr[mid + k] - x:
            left = mid + 1
        else:
            right = mid
    
    return arr[left:left + k]
```

---

## When to Use What

| Approach | Use When |
|----------|----------|
| Min-heap (size K) | K largest, general case |
| Max-heap (size K) | K smallest |
| QuickSelect | Kth element, O(n) average |
| Bucket sort | Frequency-based, bounded range |

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Kth Largest Element | Medium | Amazon |
| Top K Frequent Elements | Medium | Meta |
| K Closest Points | Medium | Meta |
| Find K Pairs with Smallest Sums | Medium | Google |
| Kth Smallest in Sorted Matrix | Medium | Amazon |

---

## Key Takeaways

1. **Min-heap of size K** for K largest elements.
2. **Counter + heap** for frequency problems.
3. **Negate values** to simulate max-heap in Python.
4. **Consider QuickSelect** for O(n) average when only need Kth.
