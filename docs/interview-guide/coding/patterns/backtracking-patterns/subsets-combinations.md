---
sidebar_position: 2
title: "Subsets & Combinations Pattern"
description: >-
  Master subsets and combinations for coding interviews. Generate all subsets,
  combinations, permutations with backtracking.
keywords:
  - subsets
  - combinations
  - permutations
  - backtracking
  - power set
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - Backtracking Introduction
companies: [Google, Amazon, Meta, Microsoft]
---

# Subsets & Combinations: Generate Everything

Classic backtracking problems. Know the templates.

---

## Subsets (Power Set)

Generate all 2^n subsets.

```python
def subsets(nums):
    result = []
    
    def backtrack(start, current):
        result.append(current[:])  # Add current subset
        
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()
    
    backtrack(0, [])
    return result

# [1, 2, 3] → [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]
```

### Subsets with Duplicates

```python
def subsets_with_dup(nums):
    nums.sort()  # Important: sort first
    result = []
    
    def backtrack(start, current):
        result.append(current[:])
        
        for i in range(start, len(nums)):
            # Skip duplicates
            if i > start and nums[i] == nums[i - 1]:
                continue
            
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()
    
    backtrack(0, [])
    return result
```

---

## Combinations

Choose k elements from n.

```python
def combine(n, k):
    result = []
    
    def backtrack(start, current):
        if len(current) == k:
            result.append(current[:])
            return
        
        # Optimization: don't continue if not enough elements left
        remaining = k - len(current)
        for i in range(start, n - remaining + 2):
            current.append(i)
            backtrack(i + 1, current)
            current.pop()
    
    backtrack(1, [])
    return result

# combine(4, 2) → [[1,2], [1,3], [1,4], [2,3], [2,4], [3,4]]
```

---

## Combination Sum

Find combinations that sum to target.

```python
def combination_sum(candidates, target):
    result = []
    
    def backtrack(start, current, remaining):
        if remaining == 0:
            result.append(current[:])
            return
        
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                continue
            
            current.append(candidates[i])
            # Same element can be used again: pass i, not i+1
            backtrack(i, current, remaining - candidates[i])
            current.pop()
    
    backtrack(0, [], target)
    return result
```

### Combination Sum II (Each Number Once)

```python
def combination_sum2(candidates, target):
    candidates.sort()
    result = []
    
    def backtrack(start, current, remaining):
        if remaining == 0:
            result.append(current[:])
            return
        
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            
            # Skip duplicates
            if i > start and candidates[i] == candidates[i - 1]:
                continue
            
            current.append(candidates[i])
            backtrack(i + 1, current, remaining - candidates[i])
            current.pop()
    
    backtrack(0, [], target)
    return result
```

---

## Permutations

Generate all n! permutations.

```python
def permute(nums):
    result = []
    
    def backtrack(current, remaining):
        if not remaining:
            result.append(current[:])
            return
        
        for i in range(len(remaining)):
            current.append(remaining[i])
            backtrack(current, remaining[:i] + remaining[i+1:])
            current.pop()
    
    backtrack([], nums)
    return result

# Alternative with swap
def permute_swap(nums):
    result = []
    
    def backtrack(start):
        if start == len(nums):
            result.append(nums[:])
            return
        
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]
    
    backtrack(0)
    return result
```

### Permutations with Duplicates

```python
def permute_unique(nums):
    nums.sort()
    result = []
    used = [False] * len(nums)
    
    def backtrack(current):
        if len(current) == len(nums):
            result.append(current[:])
            return
        
        for i in range(len(nums)):
            if used[i]:
                continue
            # Skip duplicate if previous same element wasn't used
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue
            
            used[i] = True
            current.append(nums[i])
            backtrack(current)
            current.pop()
            used[i] = False
    
    backtrack([])
    return result
```

---

## Template Summary

```python
# Subsets: Add at every node
def subsets_template(nums):
    def backtrack(start, current):
        result.append(current[:])  # Add here
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()

# Combinations: Add only when size = k
def combinations_template(n, k):
    def backtrack(start, current):
        if len(current) == k:
            result.append(current[:])  # Add only when complete
            return
        for i in range(start, n + 1):
            current.append(i)
            backtrack(i + 1, current)
            current.pop()

# Permutations: Add when all elements used
def permutations_template(nums):
    def backtrack(current, remaining):
        if not remaining:
            result.append(current[:])  # Add when empty
            return
        for i in range(len(remaining)):
            current.append(remaining[i])
            backtrack(current, remaining[:i] + remaining[i+1:])
            current.pop()
```

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Subsets | Medium | Meta |
| Subsets II | Medium | Amazon |
| Combinations | Medium | Google |
| Combination Sum | Medium | Amazon |
| Permutations | Medium | Microsoft |
| Permutations II | Medium | Google |

---

## Key Takeaways

1. **Subsets:** Add result at every node.
2. **Combinations:** Add only when size equals k.
3. **Permutations:** Use all elements exactly once.
4. **Handle duplicates:** Sort + skip consecutive same elements.
