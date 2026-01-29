---
sidebar_position: 3
title: "Recursion & Backtracking"
description: >-
  Master recursion patterns for coding interviews. Base cases, recursive
  thinking, and common pitfalls.
keywords:
  - recursion
  - backtracking
  - recursive algorithms
  - interview preparation
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - Big-O Notation
companies: [All Companies]
---

# Recursion: Think in Subproblems

Recursion is about breaking a problem into smaller identical subproblems.

---

## The Recursion Template

```python
def solve(problem):
    # 1. Base case(s)
    if is_base_case(problem):
        return base_result
    
    # 2. Recursive case
    smaller_problem = reduce(problem)
    sub_result = solve(smaller_problem)
    
    # 3. Combine results
    return combine(sub_result)
```

---

## Classic Examples

### Factorial

```python
def factorial(n):
    if n <= 1:           # Base case
        return 1
    return n * factorial(n - 1)  # Reduce and combine
```

### Fibonacci (Naive)

```python
def fib(n):
    if n <= 1:           # Base cases
        return n
    return fib(n - 1) + fib(n - 2)  # Two subproblems
```

### Fibonacci (Memoized)

```python
def fib(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]
```

---

## Tree Recursion

```python
def tree_height(root):
    if not root:
        return 0
    
    left_height = tree_height(root.left)
    right_height = tree_height(root.right)
    
    return 1 + max(left_height, right_height)

def inorder(root, result=[]):
    if root:
        inorder(root.left, result)
        result.append(root.val)
        inorder(root.right, result)
    return result
```

---

## Backtracking Template

```python
def backtrack(path, choices):
    if is_solution(path):
        result.append(path[:])
        return
    
    for choice in choices:
        if is_valid(choice, path):
            path.append(choice)      # Make choice
            backtrack(path, choices)  # Explore
            path.pop()               # Undo choice
```

### Permutations

```python
def permutations(nums):
    result = []
    
    def backtrack(path, remaining):
        if not remaining:
            result.append(path[:])
            return
        
        for i in range(len(remaining)):
            path.append(remaining[i])
            backtrack(path, remaining[:i] + remaining[i+1:])
            path.pop()
    
    backtrack([], nums)
    return result
```

### Combinations

```python
def combinations(n, k):
    result = []
    
    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(1, [])
    return result
```

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Missing base case | Always define when to stop |
| Wrong base case | Test with smallest inputs |
| Not reducing problem | Each call must get closer to base |
| Stack overflow | Add memoization or convert to iterative |
| Modifying shared state | Pass copies or undo changes |

---

## Tail Recursion

```python
# Not tail recursive (has pending operation)
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)  # Multiply AFTER return

# Tail recursive (no pending operation)
def factorial_tail(n, acc=1):
    if n <= 1:
        return acc
    return factorial_tail(n - 1, n * acc)  # Nothing after return
```

---

## When to Use Recursion

| Good Fit | Bad Fit |
|----------|---------|
| Tree/graph traversal | Simple iteration |
| Divide and conquer | When stack depth is huge |
| Backtracking problems | Performance-critical code |
| Problems with recursive structure | When iterative is clearer |

---

## Key Takeaways

1. **Always define base case first.**
2. **Each recursive call must reduce the problem.**
3. **Use memoization for overlapping subproblems.**
4. **Backtracking = recursion + undo choices.**
5. **Convert to iterative if stack overflow is a concern.**
