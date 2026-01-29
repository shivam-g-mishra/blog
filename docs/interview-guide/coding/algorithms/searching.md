---
sidebar_position: 2
title: "Searching Algorithms"
description: >-
  Master searching algorithms for coding interviews. Binary search,
  exponential search, and search variations.
keywords:
  - searching algorithms
  - binary search
  - linear search
  - interview preparation
difficulty: Intermediate
estimated_time: 15 minutes
prerequisites:
  - Big-O Notation
  - Arrays
companies: [All Companies]
---

# Searching Algorithms: Finding Elements Efficiently

Searching is fundamental. Know when O(n) is unavoidable and when you can do better.

---

## Comparison at a Glance

| Algorithm | Time | Space | Requirement |
|-----------|------|-------|-------------|
| **Linear Search** | O(n) | O(1) | None |
| **Binary Search** | O(log n) | O(1) | Sorted array |
| **Hash Lookup** | O(1) avg | O(n) | Hash table |
| **Exponential Search** | O(log n) | O(1) | Sorted, unbounded |

---

## Linear Search

**When to use:** Unsorted data, small arrays, one-time search.

```python
def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1
```

**Key insight:** Sometimes O(n) is the best you can do. Don't over-optimize.

---

## Binary Search

**When to use:** Sorted array, repeated searches, finding boundaries.

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

### Finding Boundaries

```python
def find_left_boundary(arr, target):
    """First occurrence of target"""
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left if left < len(arr) and arr[left] == target else -1

def find_right_boundary(arr, target):
    """Last occurrence of target"""
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    
    return left - 1 if left > 0 and arr[left - 1] == target else -1
```

---

## Exponential Search

**When to use:** Unbounded/infinite arrays, unknown size.

```python
def exponential_search(arr, target):
    if arr[0] == target:
        return 0
    
    # Find range
    bound = 1
    while bound < len(arr) and arr[bound] < target:
        bound *= 2
    
    # Binary search in range
    left = bound // 2
    right = min(bound, len(arr) - 1)
    
    return binary_search_range(arr, target, left, right)
```

---

## Search in Rotated Array

```python
def search_rotated(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        
        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1
```

---

## 2D Matrix Search

```python
def search_matrix(matrix, target):
    """Matrix where rows and columns are sorted"""
    if not matrix:
        return False
    
    rows, cols = len(matrix), len(matrix[0])
    row, col = 0, cols - 1
    
    while row < rows and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] > target:
            col -= 1
        else:
            row += 1
    
    return False
```

---

## Interview Applications

| Problem | Search Type |
|---------|-------------|
| **Find in sorted array** | Binary search |
| **First/last occurrence** | Boundary search |
| **Search in rotated** | Modified binary search |
| **Find peak** | Binary search on condition |
| **Sqrt(x)** | Binary search on answer |
| **Kth smallest in matrix** | Binary search on value |

---

## Key Takeaways

1. **Binary search requires sorted data** or monotonic property.
2. **Boundary templates** for first/last occurrence.
3. **Binary search on answer** for optimization problems.
4. **2D search** from top-right or bottom-left corner.
5. **Know when linear is fine**—don't force binary search.
