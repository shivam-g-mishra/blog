---
sidebar_position: 5
title: "Grid DP Pattern"
description: >-
  Master grid dynamic programming for coding interviews. Unique paths,
  minimum path sum, and dungeon game problems.
keywords:
  - grid dp
  - unique paths
  - minimum path sum
  - 2D dynamic programming
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - DP Introduction
companies: [Google, Amazon, Meta]
---

# Grid DP: 2D Dynamic Programming

Grid problems are DP classics. Navigate from top-left to bottom-right with constraints.

---

## The Pattern

```
dp[i][j] = answer for cell (i, j)
Usually depends on: dp[i-1][j], dp[i][j-1], or both
```

---

## Unique Paths

Count paths from (0,0) to (m-1,n-1), moving only right or down.

```python
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    return dp[m-1][n-1]

# Space optimized
def unique_paths_optimized(m, n):
    row = [1] * n
    
    for i in range(1, m):
        for j in range(1, n):
            row[j] += row[j-1]
    
    return row[n-1]
```

---

## Unique Paths II (with Obstacles)

```python
def unique_paths_with_obstacles(grid):
    m, n = len(grid), len(grid[0])
    
    if grid[0][0] == 1:
        return 0
    
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1
    
    # First row
    for j in range(1, n):
        dp[0][j] = dp[0][j-1] if grid[0][j] == 0 else 0
    
    # First column
    for i in range(1, m):
        dp[i][0] = dp[i-1][0] if grid[i][0] == 0 else 0
    
    # Rest of grid
    for i in range(1, m):
        for j in range(1, n):
            if grid[i][j] == 0:
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    return dp[m-1][n-1]
```

---

## Minimum Path Sum

```python
def min_path_sum(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]
    
    # First row
    for j in range(1, n):
        dp[0][j] = dp[0][j-1] + grid[0][j]
    
    # First column
    for i in range(1, m):
        dp[i][0] = dp[i-1][0] + grid[i][0]
    
    # Rest
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
    
    return dp[m-1][n-1]
```

---

## Dungeon Game

Find minimum initial health to reach bottom-right.

```python
def calculate_minimum_hp(dungeon):
    m, n = len(dungeon), len(dungeon[0])
    dp = [[float('inf')] * (n + 1) for _ in range(m + 1)]
    dp[m][n-1] = dp[m-1][n] = 1  # Need at least 1 HP
    
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            min_health = min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j]
            dp[i][j] = max(1, min_health)
    
    return dp[0][0]
```

---

## Cherry Pickup

Two people traverse grid, maximize cherries.

```python
def cherry_pickup(grid):
    n = len(grid)
    memo = {}
    
    def dp(r1, c1, r2):
        c2 = r1 + c1 - r2  # Both travel same distance
        
        if r1 >= n or c1 >= n or r2 >= n or c2 >= n:
            return float('-inf')
        if grid[r1][c1] == -1 or grid[r2][c2] == -1:
            return float('-inf')
        if r1 == n-1 and c1 == n-1:
            return grid[r1][c1]
        
        if (r1, c1, r2) in memo:
            return memo[(r1, c1, r2)]
        
        cherries = grid[r1][c1]
        if r1 != r2:  # Don't double count
            cherries += grid[r2][c2]
        
        # Both move: (down,down), (down,right), (right,down), (right,right)
        result = cherries + max(
            dp(r1+1, c1, r2+1),
            dp(r1+1, c1, r2),
            dp(r1, c1+1, r2+1),
            dp(r1, c1+1, r2)
        )
        
        memo[(r1, c1, r2)] = result
        return result
    
    return max(0, dp(0, 0, 0))
```

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Unique Paths | Medium | Google |
| Unique Paths II | Medium | Amazon |
| Minimum Path Sum | Medium | Goldman |
| Dungeon Game | Hard | Amazon |
| Cherry Pickup | Hard | Google |
| Maximal Square | Medium | Google |

---

## Key Takeaways

1. **Top-left to bottom-right** is the classic setup.
2. **Space optimization** often possible (2D → 1D).
3. **Work backwards** for problems needing end state.
4. **Two traversals** need 3D or smart state compression.
