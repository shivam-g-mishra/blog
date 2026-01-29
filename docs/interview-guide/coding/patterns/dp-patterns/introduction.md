---
sidebar_position: 1
title: "Dynamic Programming — The Complete Guide"
description: >-
  Master dynamic programming for coding interviews. Learn to identify DP problems,
  choose between top-down and bottom-up, and solve classic patterns.
keywords:
  - dynamic programming
  - DP interview
  - memoization
  - tabulation
  - optimal substructure
difficulty: Advanced
estimated_time: 45 minutes
prerequisites:
  - Recursion
  - Arrays
companies: [Google, Meta, Amazon, Microsoft, Apple]
---

# Dynamic Programming: The Pattern Behind the Magic

I used to think DP was about memorizing solutions. Fibonacci, knapsack, longest common subsequence—learn the code, move on.

Then I failed three DP problems in a row in real interviews. I knew the classic solutions, but the problems were slightly different.

**The breakthrough:** DP isn't about memorizing solutions. It's about recognizing when a problem has overlapping subproblems and optimal substructure.

---

## When to Use DP

A problem is DP if it has:

1. **Optimal Substructure:** The optimal solution contains optimal solutions to subproblems
2. **Overlapping Subproblems:** Same subproblems are solved multiple times

**Common signals:**
- "Find minimum/maximum..."
- "Count the number of ways..."
- "Is it possible to..."
- "Find the longest/shortest..."
- "Find all combinations that..."

---

## The Two Approaches

### Top-Down (Memoization)

Start with the main problem, recursively solve subproblems, cache results.

```python
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]
```

**Pros:** Natural recursive thinking, only computes needed subproblems
**Cons:** Recursion overhead, possible stack overflow

### Bottom-Up (Tabulation)

Build solution from smallest subproblems up.

```python
def fib_tab(n):
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]
```

**Pros:** No recursion overhead, usually faster
**Cons:** Must solve all subproblems, need to determine order

---

## The DP Framework

```python
def solve_dp(input):
    # 1. DEFINE STATE
    # What information do I need to represent a subproblem?
    # dp[i] = answer for subproblem i
    
    # 2. IDENTIFY BASE CASE
    # What are the smallest subproblems I can solve directly?
    
    # 3. FIND RECURRENCE RELATION
    # How does dp[i] relate to smaller subproblems?
    # dp[i] = f(dp[i-1], dp[i-2], ...)
    
    # 4. DETERMINE ORDER
    # In what order should I solve subproblems?
    
    # 5. RETURN FINAL ANSWER
    # Which state gives me the answer?
```

---

## The Five DP Patterns

### 1. Linear DP (1D Array)

**State:** `dp[i]` = answer considering elements 0 to i

```python
# Climbing Stairs
def climb_stairs(n):
    if n <= 2:
        return n
    
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]
```

### 2. Grid DP (2D Pathfinding)

**State:** `dp[i][j]` = answer at position (i, j)

```python
# Unique Paths
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    
    return dp[m - 1][n - 1]
```

### 3. String DP (Two Sequences)

**State:** `dp[i][j]` = answer for first i chars of s1 and first j chars of s2

```python
# Longest Common Subsequence
def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]
```

### 4. Decision DP (Take/Skip)

**State:** `dp[i]` = best answer considering items 0 to i

```python
# House Robber
def rob(nums):
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    
    for i in range(2, len(nums)):
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
    
    return dp[-1]
```

### 5. Interval DP

**State:** `dp[i][j]` = answer for interval [i, j]

```python
# Longest Palindromic Subsequence
def longest_palindrome_subseq(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    
    for i in range(n):
        dp[i][i] = 1
    
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    
    return dp[0][n - 1]
```

---

## Space Optimization

Many DP problems only need previous row/values:

```python
# Fibonacci: O(n) space → O(1) space
def fib_optimized(n):
    if n <= 1:
        return n
    
    prev2, prev1 = 0, 1
    
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    
    return prev1
```

---

## Practice Problems by Pattern

### Linear DP

| Problem | Company |
|---------|---------|
| Climbing Stairs | Google |
| House Robber | Amazon |
| Maximum Subarray | Meta |
| Coin Change | Amazon |
| Decode Ways | Meta |

### Grid DP

| Problem | Company |
|---------|---------|
| Unique Paths | Google |
| Minimum Path Sum | Amazon |
| Triangle | Microsoft |
| Dungeon Game | Google |

### String DP

| Problem | Company |
|---------|---------|
| Longest Common Subsequence | Google |
| Edit Distance | Amazon |
| Longest Palindromic Substring | Meta |
| Word Break | Amazon |

---

## Key Takeaways

1. **Recognize the signals:** "minimum," "maximum," "count ways," "is possible"

2. **Define state clearly.** What information represents a subproblem?

3. **Find the recurrence.** How does current state relate to previous?

4. **Start with memoization** if recursion is natural, convert to tabulation if needed.

5. **Optimize space** by keeping only what's needed.

---

## What's Next?

Learn the specific Knapsack pattern for selection problems:

👉 [Knapsack Pattern →](./knapsack)
