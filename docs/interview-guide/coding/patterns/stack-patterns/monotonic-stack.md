---
sidebar_position: 1
title: "Monotonic Stack Pattern"
description: >-
  Master monotonic stack for coding interviews. Next greater element,
  daily temperatures, largest rectangle, and stock span problems.
keywords:
  - monotonic stack
  - next greater element
  - daily temperatures
  - largest rectangle histogram
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - Stacks
companies: [Amazon, Google, Meta, Microsoft]
---

# Monotonic Stack: Next Greater/Smaller

A monotonic stack maintains elements in sorted order, enabling O(n) solutions for "next greater/smaller" problems.

---

## The Pattern

```
Problem: Find next greater element for each position

Array: [4, 2, 1, 5, 3]

For each element, we need:
4 → 5 (first greater to right)
2 → 5
1 → 5
5 → -1 (none)
3 → -1
```

---

## Next Greater Element

```python
def next_greater_element(nums):
    n = len(nums)
    result = [-1] * n
    stack = []  # Indices of elements waiting for next greater
    
    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)
    
    return result

# nums = [4, 2, 1, 5, 3]
# returns [5, 5, 5, -1, -1]
```

---

## Daily Temperatures

How many days until warmer temperature?

```python
def daily_temperatures(temperatures):
    n = len(temperatures)
    result = [0] * n
    stack = []  # Indices
    
    for i in range(n):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            idx = stack.pop()
            result[idx] = i - idx
        stack.append(i)
    
    return result

# [73, 74, 75, 71, 69, 72, 76, 73]
# returns [1, 1, 4, 2, 1, 1, 0, 0]
```

---

## Stock Span

Days since price was higher.

```python
def stock_span(prices):
    n = len(prices)
    spans = [0] * n
    stack = []  # (index, price)
    
    for i, price in enumerate(prices):
        span = 1
        
        while stack and stack[-1][1] <= price:
            span += stack.pop()[0]
        
        stack.append((span, price))
        spans[i] = span
    
    return spans
```

---

## Largest Rectangle in Histogram

Classic hard problem using monotonic stack.

```python
def largest_rectangle_area(heights):
    stack = []  # (index, height)
    max_area = 0
    
    for i, h in enumerate(heights):
        start = i
        
        while stack and stack[-1][1] > h:
            idx, height = stack.pop()
            max_area = max(max_area, height * (i - idx))
            start = idx
        
        stack.append((start, h))
    
    # Process remaining in stack
    for idx, height in stack:
        max_area = max(max_area, height * (len(heights) - idx))
    
    return max_area
```

---

## Trapping Rain Water

```python
def trap(height):
    stack = []
    water = 0
    
    for i, h in enumerate(height):
        while stack and h > height[stack[-1]]:
            bottom = height[stack.pop()]
            
            if not stack:
                break
            
            left = stack[-1]
            width = i - left - 1
            bounded_height = min(h, height[left]) - bottom
            water += width * bounded_height
        
        stack.append(i)
    
    return water
```

---

## When to Use

| Clue | Pattern |
|------|---------|
| "Next greater/smaller" | Monotonic stack |
| "Previous greater/smaller" | Monotonic stack (iterate backwards) |
| "Span" problems | Monotonic stack |
| Rectangle/histogram | Monotonic stack |

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Next Greater Element | Easy | Amazon |
| Daily Temperatures | Medium | Google |
| Largest Rectangle in Histogram | Hard | Amazon |
| Trapping Rain Water | Hard | Google |
| Stock Span | Medium | Goldman |
| Maximal Rectangle | Hard | Meta |

---

## Key Takeaways

1. **Monotonic stack** solves "next greater/smaller" in O(n).
2. **Store indices** to calculate distances.
3. **Process while popping** to handle elements found their answer.
4. **Handle remaining elements** after the loop.
