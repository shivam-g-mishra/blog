---
sidebar_position: 2
title: "Merge K Sorted Pattern"
description: >-
  Master merging K sorted lists/arrays for coding interviews. Heap-based
  merge, linked list merge, and optimization techniques.
keywords:
  - merge k sorted
  - merge k lists
  - k-way merge
  - heap merge
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - Heaps
  - Linked Lists
companies: [Google, Amazon, Meta, Microsoft]
---

# Merge K Sorted: K-Way Merge

Merging K sorted lists is a classic heap problem. The heap tracks the smallest element from each list.

---

## The Pattern

```
K sorted lists, heap tracks heads

Lists: [1,4,5], [1,3,4], [2,6]

Heap: [1, 1, 2]  (heads of each list)
Pop 1, push 4 → [1, 2, 4]
Pop 1, push 3 → [2, 3, 4]
Pop 2, push 6 → [3, 4, 6]
...
```

---

## Merge K Sorted Lists

```python
import heapq

def merge_k_lists(lists):
    heap = []
    
    # Add head of each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst.val, i, lst))
    
    dummy = ListNode()
    current = dummy
    
    while heap:
        val, i, node = heapq.heappop(heap)
        current.next = node
        current = current.next
        
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    
    return dummy.next
```

**Complexity:** O(N log K) where N = total elements, K = number of lists

---

## Merge K Sorted Arrays

```python
def merge_k_arrays(arrays):
    heap = []
    
    # (value, array_index, element_index)
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(heap, (arr[0], i, 0))
    
    result = []
    
    while heap:
        val, arr_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        
        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, arr_idx, elem_idx + 1))
    
    return result
```

---

## Smallest Range Covering K Lists

Find smallest range that includes at least one number from each list.

```python
def smallest_range(nums):
    heap = []
    current_max = float('-inf')
    
    # Initialize with first element of each list
    for i, lst in enumerate(nums):
        heapq.heappush(heap, (lst[0], i, 0))
        current_max = max(current_max, lst[0])
    
    result = [float('-inf'), float('inf')]
    
    while True:
        current_min, list_idx, elem_idx = heapq.heappop(heap)
        
        # Update result if this range is smaller
        if current_max - current_min < result[1] - result[0]:
            result = [current_min, current_max]
        
        # Try to expand from this list
        if elem_idx + 1 == len(nums[list_idx]):
            break  # Can't continue, one list exhausted
        
        next_val = nums[list_idx][elem_idx + 1]
        heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
        current_max = max(current_max, next_val)
    
    return result
```

---

## Kth Smallest in Sorted Matrix

Matrix where each row and column is sorted.

```python
def kth_smallest_matrix(matrix, k):
    n = len(matrix)
    heap = [(matrix[0][0], 0, 0)]
    visited = {(0, 0)}
    
    for _ in range(k):
        val, row, col = heapq.heappop(heap)
        
        # Add right neighbor
        if col + 1 < n and (row, col + 1) not in visited:
            heapq.heappush(heap, (matrix[row][col + 1], row, col + 1))
            visited.add((row, col + 1))
        
        # Add bottom neighbor
        if row + 1 < n and (row + 1, col) not in visited:
            heapq.heappush(heap, (matrix[row + 1][col], row + 1, col))
            visited.add((row + 1, col))
    
    return val
```

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Merge K Sorted Lists | Hard | Amazon |
| Kth Smallest in Sorted Matrix | Medium | Google |
| Smallest Range | Hard | Google |
| Find K Pairs with Smallest Sums | Medium | Amazon |
| Merge Sorted Array | Easy | Meta |

---

## Key Takeaways

1. **Heap size = K** (number of lists), not total elements.
2. **Store (value, list_id, index)** to track position.
3. **O(N log K)** beats O(N log N) naive sort.
4. **Works for any sorted sequences:** lists, arrays, iterators.
