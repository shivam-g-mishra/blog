---
sidebar_position: 1
title: "Sorting Algorithms"
description: >-
  Master sorting algorithms for coding interviews. Quick sort, merge sort,
  counting sort, and when to use each.
keywords:
  - sorting algorithms
  - quick sort
  - merge sort
  - interview preparation
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - Big-O Notation
  - Arrays
companies: [All Companies]
---

# Sorting Algorithms: Know When to Use Each

You rarely implement sorting from scratch in interviews, but understanding the algorithms helps you choose the right approach and analyze complexity.

---

## Comparison at a Glance

| Algorithm | Time (Best) | Time (Avg) | Time (Worst) | Space | Stable? |
|-----------|-------------|------------|--------------|-------|---------|
| **Quick Sort** | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| **Heap Sort** | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| **Counting Sort** | O(n + k) | O(n + k) | O(n + k) | O(k) | Yes |
| **Bucket Sort** | O(n + k) | O(n + k) | O(n²) | O(n) | Yes |

---

## Quick Sort

**Best for:** General-purpose, in-place sorting.

```python
def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)
    
    return arr

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

**Key insight:** Partition around a pivot. Elements smaller go left, larger go right.

---

## Merge Sort

**Best for:** Guaranteed O(n log n), stable sorting, linked lists.

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Key insight:** Divide, recursively sort, merge sorted halves.

---

## Heap Sort

**Best for:** In-place, guaranteed O(n log n), no extra space.

```python
def heap_sort(arr):
    n = len(arr)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Extract elements
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    
    return arr

def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
```

---

## Counting Sort

**Best for:** Small range of integers (k is small).

```python
def counting_sort(arr):
    if not arr:
        return arr
    
    min_val, max_val = min(arr), max(arr)
    range_size = max_val - min_val + 1
    
    count = [0] * range_size
    output = [0] * len(arr)
    
    # Count occurrences
    for num in arr:
        count[num - min_val] += 1
    
    # Cumulative count
    for i in range(1, range_size):
        count[i] += count[i - 1]
    
    # Build output (reverse for stability)
    for num in reversed(arr):
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1
    
    return output
```

**Key insight:** O(n + k) when range k is small. Not comparison-based.

---

## When to Use What

| Scenario | Best Choice | Why |
|----------|-------------|-----|
| General purpose | Quick Sort | Fast average case, in-place |
| Need stability | Merge Sort | Preserves relative order |
| Limited memory | Heap Sort | O(1) extra space |
| Small integer range | Counting Sort | O(n + k) linear time |
| Nearly sorted | Insertion Sort | O(n) best case |
| Linked list | Merge Sort | No random access needed |

---

## Interview Applications

| Problem | Sorting Insight |
|---------|-----------------|
| **K-th Largest** | Quick Select (partition) |
| **Merge Intervals** | Sort by start |
| **Meeting Rooms** | Sort by start/end |
| **Top K Frequent** | Bucket sort by frequency |
| **Sort Colors** | Dutch National Flag (3-way partition) |

---

## Key Takeaways

1. **Quick Sort** for general use—fast average case.
2. **Merge Sort** when stability matters or for linked lists.
3. **Counting/Bucket Sort** when range is limited.
4. **Know partitioning**—it's the basis of Quick Select.
5. **In interviews**, often use `sorted()` but know the complexity.
