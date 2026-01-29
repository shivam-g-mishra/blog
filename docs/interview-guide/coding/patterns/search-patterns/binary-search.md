---
sidebar_position: 1
title: "Binary Search Pattern — Beyond Simple Search"
description: >-
  Master binary search for coding interviews. Classic search, boundary finding,
  search on answer, and rotated array problems.
keywords:
  - binary search
  - binary search template
  - search rotated array
  - first position
  - coding patterns
difficulty: Intermediate
estimated_time: 35 minutes
prerequisites:
  - Arrays & Strings
  - Big-O Notation
companies: [Google, Meta, Amazon, Microsoft, Apple]
---

# Binary Search: More Than Just Finding Elements

Most people think binary search is simple: find an element in a sorted array. But in interviews, it's rarely that straightforward.

"Find the minimum in rotated sorted array." "Find first position of element." "Find the smallest divisor given a threshold."

**Binary search is a technique for eliminating half the search space each step.**

---

## The Three Templates

### Template 1: Classic Binary Search

```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

**Use when:** Finding exact element, answer exists or doesn't.

### Template 2: Find First/Last Position (Boundary)

```python
def find_first(nums, target):
    left, right = 0, len(nums) - 1
    result = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            result = mid
            right = mid - 1  # Keep searching left
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result

def find_last(nums, target):
    left, right = 0, len(nums) - 1
    result = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            result = mid
            left = mid + 1  # Keep searching right
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result
```

**Use when:** Finding boundary positions, first/last occurrence.

### Template 3: Search on Answer

```python
def search_on_answer(nums, condition):
    left, right = min_possible, max_possible
    
    while left < right:
        mid = left + (right - left) // 2
        
        if condition(mid):
            right = mid  # Answer could be mid or smaller
        else:
            left = mid + 1  # Answer must be larger
    
    return left
```

**Use when:** Finding minimum/maximum value that satisfies condition.

---

## Classic Problems

### Problem 1: Search in Rotated Sorted Array

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

### Problem 2: Find Minimum in Rotated Sorted Array

```python
def find_min(nums):
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] > nums[right]:
            left = mid + 1  # Min is in right half
        else:
            right = mid  # Min could be mid or left
    
    return nums[left]
```

### Problem 3: Koko Eating Bananas (Search on Answer)

```python
def min_eating_speed(piles, h):
    def can_finish(speed):
        hours = sum((pile + speed - 1) // speed for pile in piles)
        return hours <= h
    
    left, right = 1, max(piles)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if can_finish(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

### Problem 4: Find Peak Element

```python
def find_peak_element(nums):
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] > nums[mid + 1]:
            right = mid  # Peak is at mid or left
        else:
            left = mid + 1  # Peak is in right half
    
    return left
```

### Problem 5: Search a 2D Matrix

```python
def search_matrix(matrix, target):
    if not matrix:
        return False
    
    rows, cols = len(matrix), len(matrix[0])
    left, right = 0, rows * cols - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        row, col = mid // cols, mid % cols
        val = matrix[row][col]
        
        if val == target:
            return True
        elif val < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return False
```

---

## Pattern Recognition

| Problem Type | Template |
|--------------|----------|
| Find exact element | Classic |
| First/last position | Boundary |
| Minimum satisfying condition | Search on answer |
| Rotated array | Modified classic |
| Find peak | Compare with neighbor |
| Matrix as 1D array | Index conversion |

---

## Common Mistakes

1. **Infinite loop:** Wrong update (`left = mid` without `+1`)
2. **Off-by-one:** `left <= right` vs `left < right`
3. **Integer overflow:** Use `left + (right - left) // 2`
4. **Wrong half:** Ensure you eliminate the correct half

---

## Practice Problems

### Easy

| Problem | Type | Company |
|---------|------|---------|
| Binary Search | Classic | Google |
| First Bad Version | Boundary | Meta |
| Search Insert Position | Boundary | Amazon |

### Medium

| Problem | Type | Company |
|---------|------|---------|
| Search in Rotated Array | Modified | Meta, Amazon |
| Find Minimum Rotated | Modified | Google |
| Find Peak Element | Compare Neighbor | Meta |
| Koko Eating Bananas | Search Answer | Google |
| Capacity to Ship | Search Answer | Amazon |

### Hard

| Problem | Type | Company |
|---------|------|---------|
| Median of Two Sorted | Binary Search | Google, Amazon |
| Split Array Largest Sum | Search Answer | Google |

---

## Key Takeaways

1. **Three templates** cover most problems: classic, boundary, search-on-answer.

2. **Eliminate half each step** — that's the core principle.

3. **Search on answer** is powerful for optimization problems.

4. **Always check loop termination** — `left <= right` vs `left < right`.

5. **Sorted or monotonic** property is required.

---

## What's Next?

Dynamic Programming patterns for optimal substructure problems:

👉 [DP Patterns →](../dp-patterns/knapsack)
