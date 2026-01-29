---
sidebar_position: 2
title: "Problem-Solving Approach"
description: >-
  Structured approach to solving coding problems in interviews. From
  understanding to optimization with the UMPIRE method.
keywords:
  - problem solving
  - coding approach
  - UMPIRE method
  - interview strategy
difficulty: Beginner
estimated_time: 15 minutes
prerequisites: []
companies: [All Companies]
---

# Problem-Solving: The UMPIRE Method

Don't just start coding. Follow a structured approach every time.

---

## UMPIRE Framework

| Step | Action | Time |
|------|--------|------|
| **U**nderstand | Clarify the problem | 2 min |
| **M**atch | Identify patterns/data structures | 2 min |
| **P**lan | Outline your approach | 3 min |
| **I**mplement | Write the code | 15 min |
| **R**eview | Test with examples | 3 min |
| **E**valuate | Analyze complexity, optimize | 2 min |

---

## U: Understand

**Before anything else:**

```
□ Restate the problem in your own words
□ Clarify inputs and outputs
□ Ask about constraints (size, range, type)
□ Identify edge cases
□ Work through a simple example
```

**Example:**
```
"So I need to find two numbers in this array that add up to 
the target. The array has n integers, and I should return 
their indices. Can there be duplicates? Can the array be 
empty? Is there always a valid solution?"
```

---

## M: Match

**Recognize patterns:**

| If you see... | Think... |
|---------------|----------|
| Sorted array | Binary search, two pointers |
| Find/count elements | Hash map |
| Optimal substructure | Dynamic programming |
| All possibilities | Backtracking |
| Level-by-level | BFS |
| Tree structure | DFS, recursion |
| K largest/smallest | Heap |
| Intervals | Sort + scan |

---

## P: Plan

**Outline before coding:**

```
"My plan:
1. Create a hash map to store seen numbers
2. Iterate through array once
3. For each number, check if complement exists
4. Return indices if found

Edge cases:
- Empty array → return []
- Single element → return []
- No valid pair → based on problem definition"
```

---

## I: Implement

**Code with intention:**

- Write clean, readable code
- Use meaningful variable names
- Add brief comments for complex logic
- Don't optimize prematurely

```python
def two_sum(nums, target):
    # Map: number → index
    seen = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        
        if complement in seen:
            return [seen[complement], i]
        
        seen[num] = i
    
    return []  # No solution found
```

---

## R: Review

**Test your code:**

```
"Let me trace through:

Input: nums = [2, 7, 11, 15], target = 9

i=0, num=2:
  complement = 7
  7 not in seen
  seen = {2: 0}

i=1, num=7:
  complement = 2
  2 in seen! seen[2] = 0
  return [0, 1] ✓"
```

**Check edge cases:**
- Empty input
- Single element
- Duplicates
- Negative numbers

---

## E: Evaluate

**Analyze and improve:**

```
"Time: O(n) - single pass through array
Space: O(n) - hash map storing up to n elements

Is there room to optimize?
- Already optimal for time
- Can't reduce space without sacrificing time
- Trade-off is appropriate"
```

---

## When You're Stuck

1. **Simplify:** Solve a smaller version first
2. **Brute force:** Start with obvious solution, then optimize
3. **Visualize:** Draw it out
4. **Work backwards:** Start from desired output
5. **Ask for hints:** Better than silence

---

## Key Takeaways

1. **Never skip understanding.** Rushing causes bugs.
2. **Pattern matching accelerates solutions.** Build this skill.
3. **Plan before coding.** 5 minutes planning saves 15 minutes debugging.
4. **Test thoroughly.** Walk through your code with examples.
5. **Know your complexity.** Always state time and space.
