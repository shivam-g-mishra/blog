---
sidebar_position: 4
title: "Kadane's Algorithm Pattern"
description: >-
  Master Kadane's algorithm for coding interviews. Maximum subarray,
  variations, and related problems.
keywords:
  - kadane algorithm
  - maximum subarray
  - subarray sum
  - dynamic programming
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - Arrays
companies: [Amazon, Google, Meta, Microsoft]
---

# Kadane's Algorithm: Maximum Subarray

Kadane's algorithm finds the maximum sum contiguous subarray in O(n).

---

## The Core Algorithm

```python
def max_subarray(nums):
    max_sum = nums[0]
    current_sum = nums[0]
    
    for i in range(1, len(nums)):
        # Either extend current subarray or start new
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example: [-2, 1, -3, 4, -1, 2, 1, -5, 4]
# Maximum subarray: [4, -1, 2, 1] → Sum = 6
```

---

## The Intuition

```
At each position, we ask:
"Should I extend the previous subarray or start fresh?"

If current_sum + nums[i] < nums[i]:
  → Previous subarray is dragging us down
  → Start fresh from nums[i]
  
If current_sum + nums[i] >= nums[i]:
  → Previous subarray is helping or neutral
  → Extend it
```

---

## Finding the Subarray Indices

```python
def max_subarray_with_indices(nums):
    max_sum = nums[0]
    current_sum = nums[0]
    
    start = end = 0
    temp_start = 0
    
    for i in range(1, len(nums)):
        if nums[i] > current_sum + nums[i]:
            current_sum = nums[i]
            temp_start = i
        else:
            current_sum = current_sum + nums[i]
        
        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i
    
    return max_sum, start, end
```

---

## Variations

### Maximum Circular Subarray

```python
def max_subarray_circular(nums):
    # Case 1: Max subarray doesn't wrap
    max_kadane = kadane_max(nums)
    
    # Case 2: Max subarray wraps around
    # = Total sum - Minimum subarray
    total = sum(nums)
    min_kadane = kadane_min(nums)
    
    # Handle all negative case
    if total == min_kadane:
        return max_kadane
    
    return max(max_kadane, total - min_kadane)

def kadane_max(nums):
    max_sum = current = nums[0]
    for num in nums[1:]:
        current = max(num, current + num)
        max_sum = max(max_sum, current)
    return max_sum

def kadane_min(nums):
    min_sum = current = nums[0]
    for num in nums[1:]:
        current = min(num, current + num)
        min_sum = min(min_sum, current)
    return min_sum
```

### Maximum Product Subarray

```python
def max_product(nums):
    max_prod = min_prod = result = nums[0]
    
    for i in range(1, len(nums)):
        num = nums[i]
        
        # Swap if negative (min becomes max)
        if num < 0:
            max_prod, min_prod = min_prod, max_prod
        
        max_prod = max(num, max_prod * num)
        min_prod = min(num, min_prod * num)
        
        result = max(result, max_prod)
    
    return result
```

### Maximum Sum with No Adjacent Elements

```python
def max_sum_no_adjacent(nums):
    if not nums:
        return 0
    if len(nums) == 1:
        return max(0, nums[0])
    
    # prev2 = max sum ending 2 positions back
    # prev1 = max sum ending 1 position back
    prev2 = max(0, nums[0])
    prev1 = max(prev2, nums[1])
    
    for i in range(2, len(nums)):
        current = max(prev1, prev2 + nums[i])
        prev2 = prev1
        prev1 = current
    
    return prev1
```

---

## 2D Kadane: Maximum Rectangle Sum

```python
def max_rectangle_sum(matrix):
    if not matrix:
        return 0
    
    rows, cols = len(matrix), len(matrix[0])
    max_sum = float('-inf')
    
    for left in range(cols):
        temp = [0] * rows
        
        for right in range(left, cols):
            # Add current column to temp
            for i in range(rows):
                temp[i] += matrix[i][right]
            
            # Apply Kadane on temp
            current_max = kadane_max(temp)
            max_sum = max(max_sum, current_max)
    
    return max_sum
```

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Maximum Subarray | Medium | Amazon |
| Maximum Circular Subarray | Medium | Google |
| Maximum Product Subarray | Medium | Amazon |
| House Robber | Medium | All |
| Maximum Rectangle | Hard | Google |

---

## Key Takeaways

1. **Core insight:** Extend or start fresh at each position.
2. **O(n) time, O(1) space** for basic version.
3. **Track min and max** for product variant (negatives flip).
4. **Circular variant:** Use total - min_subarray.
5. **2D extension:** Apply 1D Kadane to column sums.
