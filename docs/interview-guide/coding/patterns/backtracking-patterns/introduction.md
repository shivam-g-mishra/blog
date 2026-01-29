---
sidebar_position: 1
title: "Backtracking Pattern — Systematic Search"
description: >-
  Master backtracking for coding interviews. Subsets, permutations, combinations,
  and constraint satisfaction problems.
keywords:
  - backtracking
  - recursion
  - subsets
  - permutations
  - combinations
  - N-Queens
difficulty: Advanced
estimated_time: 40 minutes
prerequisites:
  - Recursion
  - Trees
companies: [Google, Meta, Amazon, Microsoft]
---

# Backtracking: Explore All Possibilities

When I first saw "generate all permutations," I had no idea where to start. How do you systematically explore every possibility?

**Backtracking is controlled recursion with a pattern:**

1. Make a choice
2. Explore with that choice
3. Undo the choice (backtrack)
4. Make the next choice

---

## The Template

```python
def backtrack(path, choices):
    # Base case: found a solution
    if is_solution(path):
        result.append(path.copy())  # Important: copy!
        return
    
    for choice in choices:
        # Pruning: skip invalid choices
        if not is_valid(choice, path):
            continue
        
        # Make choice
        path.append(choice)
        
        # Explore
        backtrack(path, remaining_choices)
        
        # Undo choice (backtrack)
        path.pop()
```

---

## The Three Classic Problems

### 1. Subsets (All Combinations)

Generate all 2^n subsets of a set.

```python
def subsets(nums):
    result = []
    
    def backtrack(start, path):
        result.append(path.copy())  # Every path is a valid subset
        
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)  # Move forward, no duplicates
            path.pop()
    
    backtrack(0, [])
    return result

# subsets([1,2,3]) → [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]
```

**Decision tree:**
```
                    []
           /        |        \
         [1]       [2]       [3]
        /   \       |
     [1,2]  [1,3]  [2,3]
       |
    [1,2,3]
```

### 2. Permutations (All Orderings)

Generate all n! orderings.

```python
def permutations(nums):
    result = []
    
    def backtrack(path, remaining):
        if not remaining:
            result.append(path.copy())
            return
        
        for i in range(len(remaining)):
            path.append(remaining[i])
            backtrack(path, remaining[:i] + remaining[i+1:])
            path.pop()
    
    backtrack([], nums)
    return result

# Alternative using swap
def permutations_swap(nums):
    result = []
    
    def backtrack(start):
        if start == len(nums):
            result.append(nums.copy())
            return
        
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]  # Swap
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]  # Undo swap
    
    backtrack(0)
    return result
```

### 3. Combinations (Choose K)

Generate all ways to choose k elements.

```python
def combinations(n, k):
    result = []
    
    def backtrack(start, path):
        if len(path) == k:
            result.append(path.copy())
            return
        
        # Pruning: need k-len(path) more elements
        # Can't pick from fewer than that
        for i in range(start, n - (k - len(path)) + 2):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(1, [])
    return result
```

---

## Handling Duplicates

When input has duplicates, avoid duplicate solutions.

```python
def subsets_with_duplicates(nums):
    nums.sort()  # Sort first!
    result = []
    
    def backtrack(start, path):
        result.append(path.copy())
        
        for i in range(start, len(nums)):
            # Skip duplicates at same level
            if i > start and nums[i] == nums[i - 1]:
                continue
            
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(0, [])
    return result

# [1,2,2] → [[], [1], [1,2], [1,2,2], [2], [2,2]]
# Without duplicate check: [[], [1], [1,2], [1,2,2], [1,2], [2], [2,2], [2]]
```

---

## Classic Problems

### N-Queens

Place N queens on NxN board with no attacks.

```python
def solve_n_queens(n):
    result = []
    
    def is_valid(board, row, col):
        # Check column
        for i in range(row):
            if board[i] == col:
                return False
        
        # Check diagonals
        for i in range(row):
            if abs(board[i] - col) == abs(i - row):
                return False
        
        return True
    
    def backtrack(row, board):
        if row == n:
            result.append(board.copy())
            return
        
        for col in range(n):
            if is_valid(board, row, col):
                board.append(col)
                backtrack(row + 1, board)
                board.pop()
    
    backtrack(0, [])
    return result
```

### Word Search

Find if word exists in grid.

```python
def exist(board, word):
    rows, cols = len(board), len(board[0])
    
    def backtrack(r, c, idx):
        if idx == len(word):
            return True
        
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            board[r][c] != word[idx]):
            return False
        
        # Mark as visited
        temp = board[r][c]
        board[r][c] = '#'
        
        # Explore 4 directions
        found = (backtrack(r + 1, c, idx + 1) or
                 backtrack(r - 1, c, idx + 1) or
                 backtrack(r, c + 1, idx + 1) or
                 backtrack(r, c - 1, idx + 1))
        
        # Restore
        board[r][c] = temp
        
        return found
    
    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
    
    return False
```

### Generate Parentheses

Generate all valid combinations of n pairs.

```python
def generate_parentheses(n):
    result = []
    
    def backtrack(path, open_count, close_count):
        if len(path) == 2 * n:
            result.append(''.join(path))
            return
        
        if open_count < n:
            path.append('(')
            backtrack(path, open_count + 1, close_count)
            path.pop()
        
        if close_count < open_count:
            path.append(')')
            backtrack(path, open_count, close_count + 1)
            path.pop()
    
    backtrack([], 0, 0)
    return result
```

### Sudoku Solver

```python
def solve_sudoku(board):
    def is_valid(row, col, num):
        # Check row
        if num in board[row]:
            return False
        
        # Check column
        for r in range(9):
            if board[r][col] == num:
                return False
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if board[r][c] == num:
                    return False
        
        return True
    
    def backtrack():
        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    for num in '123456789':
                        if is_valid(r, c, num):
                            board[r][c] = num
                            if backtrack():
                                return True
                            board[r][c] = '.'
                    return False
        return True
    
    backtrack()
```

---

## Pattern Recognition

| Problem Type | Key Insight |
|--------------|-------------|
| **Subsets** | Include/exclude each element |
| **Permutations** | All orderings, use swap |
| **Combinations** | Choose k, maintain order |
| **Partitioning** | Split into groups |
| **Grid search** | 4/8 directional moves |
| **Constraint satisfaction** | Check validity before placing |

---

## Optimization Tips

### 1. Prune Early

```python
# Instead of checking validity at the end
if not is_valid(path):
    return

# Check before making choice
if is_valid(choice):
    make_choice(choice)
    backtrack()
    undo_choice()
```

### 2. Avoid Copies

```python
# Slow: creates new list each time
backtrack(path + [choice])

# Fast: modify in place
path.append(choice)
backtrack(path)
path.pop()
```

### 3. Use Sets for Fast Lookup

```python
# N-Queens optimization
cols = set()
diag1 = set()  # row - col
diag2 = set()  # row + col

def is_valid(row, col):
    return col not in cols and (row - col) not in diag1 and (row + col) not in diag2
```

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Subsets | Medium | Meta, Google |
| Subsets II | Medium | Amazon |
| Permutations | Medium | Google |
| Permutations II | Medium | Meta |
| Combinations | Medium | Amazon |
| Combination Sum | Medium | Google, Meta |
| N-Queens | Hard | Amazon |
| Word Search | Medium | Meta |
| Sudoku Solver | Hard | Google |
| Generate Parentheses | Medium | Amazon |

---

## Key Takeaways

1. **Three steps:** Make choice, explore, undo choice.

2. **Subsets vs Permutations:** Subsets move forward (i+1), permutations use all remaining.

3. **Handle duplicates:** Sort first, skip same elements at same level.

4. **Prune early** to avoid exploring invalid branches.

5. **Remember to copy** when adding to results.

---

## What's Next?

Graph patterns for traversal and connectivity:

👉 [Graph Patterns →](../graph-patterns/traversal)
