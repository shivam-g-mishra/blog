---
sidebar_position: 1
title: "Two Pointers Pattern — Complete Guide"
description: >-
  Master the two pointers technique for coding interviews. Learn the three
  variations, recognize when to use it, and solve classic problems.
keywords:
  - two pointers technique
  - two pointers pattern
  - coding interview patterns
  - array two pointers
  - opposite pointers
difficulty: Beginner
estimated_time: 30 minutes
prerequisites:
  - Big-O Notation
  - Arrays & Strings
companies: [Google, Meta, Amazon, Microsoft, Apple]
---

# Two Pointers: The First Pattern to Master

If there's one pattern that appears more than any other in coding interviews, it's two pointers. It's elegant, efficient, and once you recognize it, problems that seemed hard become obvious.

**Two pointers turns O(n²) brute force into O(n) elegance.**

---

## The Core Idea

Instead of nested loops, use two indices that move based on conditions:

```python
# Brute force: O(n²)
for i in range(n):
    for j in range(i + 1, n):
        if condition(arr[i], arr[j]):
            return result

# Two pointers: O(n)
left, right = 0, n - 1
while left < right:
    if condition(arr[left], arr[right]):
        return result
    # Move one pointer based on logic
```

---

## The Three Variations

### 1. Opposite Direction (Most Common)

Start from both ends, move toward middle.

```python
def two_sum_sorted(numbers, target):
    left, right = 0, len(numbers) - 1
    
    while left < right:
        current_sum = numbers[left] + numbers[right]
        
        if current_sum == target:
            return [left + 1, right + 1]
        elif current_sum < target:
            left += 1   # Need larger sum
        else:
            right -= 1  # Need smaller sum
    
    return []
```

**Use when:**
- Array is sorted
- Finding pairs that satisfy a condition
- Comparing elements from both ends

### 2. Same Direction (Fast-Slow)

Both pointers move in same direction at different speeds or conditions.

```python
def remove_duplicates(nums):
    if not nums:
        return 0
    
    write = 1  # Slow pointer - where to write
    
    for read in range(1, len(nums)):  # Fast pointer - what to read
        if nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write += 1
    
    return write
```

**Use when:**
- Removing elements in-place
- Partitioning array
- Finding cycle in linked list

### 3. Sliding Window Variant

Two pointers defining a window that expands and contracts.

```python
def min_subarray_len(target, nums):
    left = 0
    current_sum = 0
    min_length = float('inf')
    
    for right in range(len(nums)):
        current_sum += nums[right]
        
        while current_sum >= target:
            min_length = min(min_length, right - left + 1)
            current_sum -= nums[left]
            left += 1
    
    return min_length if min_length != float('inf') else 0
```

**Use when:**
- Finding subarray with property
- Variable-size window
- Optimizing within constraint

---

## Pattern Recognition

| Problem Type | Two Pointer Approach |
|--------------|---------------------|
| "Find pair with sum X" (sorted) | Opposite ends |
| "Remove duplicates in-place" | Same direction |
| "Reverse array/string" | Opposite ends |
| "Palindrome check" | Opposite ends |
| "Container with most water" | Opposite ends |
| "3Sum / 4Sum" | Sort + opposite ends |
| "Move zeros" | Same direction |
| "Merge sorted arrays" | Same direction |

---

## Classic Problems

### Problem 1: Container With Most Water

```python
def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        width = right - left
        h = min(height[left], height[right])
        max_water = max(max_water, width * h)
        
        # Move the shorter line (might find taller)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_water
```

**Why it works:** Moving the shorter line might find a taller one. Moving the taller line can only decrease width with same or smaller height.

### Problem 2: 3Sum

```python
def three_sum(nums):
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicates
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        target = -nums[i]
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            current_sum = nums[left] + nums[right]
            
            if current_sum == target:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    
    return result
```

### Problem 3: Trapping Rain Water

```python
def trap(height):
    if not height:
        return 0
    
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    
    return water
```

### Problem 4: Move Zeroes

```python
def move_zeroes(nums):
    write = 0
    
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1
```

### Problem 5: Valid Palindrome

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    
    while left < right:
        # Skip non-alphanumeric
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True
```

---

## Practice Problems

### Easy

| Problem | Variation | Company |
|---------|-----------|---------|
| Two Sum II | Opposite | Google, Amazon |
| Valid Palindrome | Opposite | Meta |
| Reverse String | Opposite | Apple |
| Move Zeroes | Same Direction | Meta |
| Merge Sorted Array | Same Direction | Microsoft |

### Medium

| Problem | Variation | Company |
|---------|-----------|---------|
| 3Sum | Sort + Opposite | Google, Meta |
| Container With Most Water | Opposite | Amazon |
| Sort Colors | Same Direction | Microsoft |
| Remove Duplicates II | Same Direction | Google |

### Hard

| Problem | Variation | Company |
|---------|-----------|---------|
| Trapping Rain Water | Opposite | Google, Amazon |
| 4Sum | Sort + Opposite | Meta |

---

## Common Mistakes

1. **Forgetting to sort** — Opposite direction usually needs sorted array
2. **Infinite loop** — Always ensure pointers move toward each other
3. **Off-by-one** — Be careful with `<` vs `<=` in while condition
4. **Missing duplicates** — Skip duplicates in problems asking for unique results

---

## Key Takeaways

1. **Sort first** for opposite-direction problems on unsorted arrays.

2. **Move the "losing" pointer** — In water container, move shorter side.

3. **Same direction for in-place** — Read pointer explores, write pointer marks position.

4. **Recognize the pattern** — "Find pair," "sorted array," "in-place" = two pointers.

---

## What's Next?

The sliding window pattern builds on two pointers for subarray problems:

👉 [Sliding Window Pattern →](./sliding-window)
