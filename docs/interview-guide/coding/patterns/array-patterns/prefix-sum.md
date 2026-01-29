---
sidebar_position: 3
title: "Prefix Sum Pattern — Range Queries Made Easy"
description: >-
  Master the prefix sum technique for coding interviews. O(1) range queries,
  subarray sum problems, and 2D matrix applications.
keywords:
  - prefix sum
  - cumulative sum
  - range sum query
  - subarray sum
  - coding patterns
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - Arrays & Strings
  - Hash Tables
companies: [Google, Meta, Amazon, Microsoft]
---

# Prefix Sum: O(1) Range Queries

The first time I saw "find the number of subarrays with sum equal to K," I tried every possible subarray. O(n²) at best.

Then I learned prefix sum + hash map. Same problem, O(n). 

**Prefix sum turns range queries from O(n) to O(1).**

---

## The Core Idea

Precompute cumulative sums so any range sum is just subtraction:

```python
# Array:      [1, 2, 3, 4, 5]
# Prefix:  [0, 1, 3, 6, 10, 15]
#              ↑  ↑
# Sum of arr[1:4] = prefix[4] - prefix[1] = 10 - 1 = 9

def build_prefix_sum(arr):
    prefix = [0] * (len(arr) + 1)
    for i in range(len(arr)):
        prefix[i + 1] = prefix[i] + arr[i]
    return prefix

def range_sum(prefix, left, right):
    return prefix[right + 1] - prefix[left]
```

---

## Pattern 1: Range Sum Query

**Problem:** Multiple queries for sum of elements in range [i, j]

```python
class NumArray:
    def __init__(self, nums):
        self.prefix = [0]
        for num in nums:
            self.prefix.append(self.prefix[-1] + num)
    
    def sum_range(self, left, right):
        return self.prefix[right + 1] - self.prefix[left]

# Build: O(n), Query: O(1)
```

---

## Pattern 2: Subarray Sum Equals K

**The most important prefix sum pattern.** Combine with hash map.

```python
def subarray_sum(nums, k):
    count = 0
    prefix_sum = 0
    prefix_counts = {0: 1}  # Sum 0 occurs once (empty prefix)
    
    for num in nums:
        prefix_sum += num
        
        # If prefix_sum - k exists, we found subarrays ending here
        if prefix_sum - k in prefix_counts:
            count += prefix_counts[prefix_sum - k]
        
        prefix_counts[prefix_sum] = prefix_counts.get(prefix_sum, 0) + 1
    
    return count
```

**Why it works:** If `prefix[j] - prefix[i] = k`, then `sum(arr[i+1:j+1]) = k`.

---

## Pattern 3: 2D Prefix Sum (Matrix)

```python
class NumMatrix:
    def __init__(self, matrix):
        if not matrix:
            return
        
        rows, cols = len(matrix), len(matrix[0])
        self.prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
        
        for r in range(rows):
            for c in range(cols):
                self.prefix[r + 1][c + 1] = (
                    matrix[r][c] +
                    self.prefix[r][c + 1] +
                    self.prefix[r + 1][c] -
                    self.prefix[r][c]
                )
    
    def sum_region(self, r1, c1, r2, c2):
        return (
            self.prefix[r2 + 1][c2 + 1] -
            self.prefix[r1][c2 + 1] -
            self.prefix[r2 + 1][c1] +
            self.prefix[r1][c1]
        )
```

---

## Classic Problems

### Problem 1: Contiguous Array (Equal 0s and 1s)

```python
def find_max_length(nums):
    # Treat 0 as -1, find longest subarray with sum 0
    prefix_sum = 0
    first_occurrence = {0: -1}
    max_length = 0
    
    for i, num in enumerate(nums):
        prefix_sum += 1 if num == 1 else -1
        
        if prefix_sum in first_occurrence:
            max_length = max(max_length, i - first_occurrence[prefix_sum])
        else:
            first_occurrence[prefix_sum] = i
    
    return max_length
```

### Problem 2: Product of Array Except Self

```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    
    # Left products
    left = 1
    for i in range(n):
        result[i] = left
        left *= nums[i]
    
    # Right products
    right = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right
        right *= nums[i]
    
    return result
```

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Range Sum Query | Easy | Google |
| Subarray Sum Equals K | Medium | Meta, Google |
| Contiguous Array | Medium | Meta |
| Product Except Self | Medium | Amazon |
| Range Sum Query 2D | Medium | Google |

---

## Key Takeaways

1. **Prefix sum = O(n) precompute, O(1) queries.**

2. **Subarray sum K = prefix sum + hash map.** The combo is powerful.

3. **Works for 2D matrices** with inclusion-exclusion principle.

4. **Transform problems:** Equal 0s/1s becomes sum = 0 with transformation.

---

## What's Next?

Binary search is essential for sorted data problems:

👉 [Binary Search Pattern →](../search-patterns/binary-search)
