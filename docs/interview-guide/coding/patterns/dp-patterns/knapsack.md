---
sidebar_position: 2
title: "Knapsack Pattern — Selection Problems"
description: >-
  Master the 0/1 Knapsack pattern for coding interviews. Subset sum, partition
  problems, and bounded knapsack variations.
keywords:
  - knapsack problem
  - 0/1 knapsack
  - subset sum
  - partition equal subset
  - dynamic programming
difficulty: Advanced
estimated_time: 35 minutes
prerequisites:
  - DP Introduction
companies: [Google, Amazon, Microsoft, Apple]
---

# Knapsack: The Selection Pattern

"Given items with weights and values, maximize value without exceeding capacity."

That's the classic knapsack. But the pattern appears in disguise everywhere:

- "Can you partition array into two equal sums?"
- "How many ways to make change for amount K?"
- "What's the minimum number of coins?"

**Knapsack is about selecting items with constraints.**

---

## The Core Pattern

### 0/1 Knapsack

Each item can be taken once or not at all.

```python
def knapsack_01(weights, values, capacity):
    n = len(weights)
    # dp[i][w] = max value using first i items with capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item i
            dp[i][w] = dp[i - 1][w]
            
            # Take item i (if it fits)
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    dp[i][w],
                    dp[i - 1][w - weights[i - 1]] + values[i - 1]
                )
    
    return dp[n][capacity]
```

**Space Optimized (1D):**

```python
def knapsack_01_optimized(weights, values, capacity):
    dp = [0] * (capacity + 1)
    
    for i in range(len(weights)):
        # Traverse backward to avoid using same item twice
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]
```

---

## Knapsack Variations

### 1. Unbounded Knapsack

Each item can be used unlimited times.

```python
def knapsack_unbounded(weights, values, capacity):
    dp = [0] * (capacity + 1)
    
    for w in range(1, capacity + 1):
        for i in range(len(weights)):
            if weights[i] <= w:
                dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]
```

### 2. Bounded Knapsack

Each item has a limited quantity.

```python
def knapsack_bounded(weights, values, quantities, capacity):
    dp = [0] * (capacity + 1)
    
    for i in range(len(weights)):
        for _ in range(quantities[i]):  # Use item up to quantity times
            for w in range(capacity, weights[i] - 1, -1):
                dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]
```

---

## Classic Problems

### Problem 1: Subset Sum

"Can we select items to get exactly target sum?"

```python
def can_partition(nums, target):
    dp = [False] * (target + 1)
    dp[0] = True  # Empty subset sums to 0
    
    for num in nums:
        for s in range(target, num - 1, -1):
            dp[s] = dp[s] or dp[s - num]
    
    return dp[target]
```

### Problem 2: Partition Equal Subset Sum

"Can array be partitioned into two equal sums?"

```python
def can_partition_equal(nums):
    total = sum(nums)
    
    # Can't split odd sum equally
    if total % 2 != 0:
        return False
    
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    
    for num in nums:
        for s in range(target, num - 1, -1):
            dp[s] = dp[s] or dp[s - num]
    
    return dp[target]
```

### Problem 3: Coin Change (Minimum Coins)

"Minimum coins to make amount."

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] = min(dp[a], dp[a - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1
```

### Problem 4: Coin Change 2 (Count Ways)

"Number of ways to make amount."

```python
def coin_change_ways(coins, amount):
    dp = [0] * (amount + 1)
    dp[0] = 1  # One way to make 0
    
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]
    
    return dp[amount]
```

### Problem 5: Target Sum

"Assign + or - to reach target sum."

```python
def find_target_sum_ways(nums, target):
    total = sum(nums)
    
    # Need (total + target) to be even for valid partition
    if (total + target) % 2 != 0 or abs(target) > total:
        return 0
    
    # Find subset with sum = (total + target) / 2
    subset_sum = (total + target) // 2
    
    dp = [0] * (subset_sum + 1)
    dp[0] = 1
    
    for num in nums:
        for s in range(subset_sum, num - 1, -1):
            dp[s] += dp[s - num]
    
    return dp[subset_sum]
```

---

## Pattern Recognition

| Problem Type | Knapsack Variation |
|--------------|-------------------|
| Select items once | 0/1 Knapsack |
| Unlimited selection | Unbounded Knapsack |
| Limited quantities | Bounded Knapsack |
| Exactly K items | Add dimension |
| Count ways | Sum instead of max |
| Check possible | Boolean DP |

---

## Key Insights

### 1. Direction of Inner Loop

```python
# 0/1 Knapsack: Backward (each item once)
for w in range(capacity, weight - 1, -1):

# Unbounded: Forward (item can repeat)
for w in range(weight, capacity + 1):
```

### 2. Subset Sum Transformation

Many problems reduce to subset sum:
- Partition equal → subset sum = total/2
- Target sum → subset sum = (total + target)/2

### 3. Base Cases

```python
# Minimum problems: dp[0] = 0, rest = infinity
# Count problems: dp[0] = 1, rest = 0
# Boolean problems: dp[0] = True, rest = False
```

---

## Practice Problems

| Problem | Type | Company |
|---------|------|---------|
| 0/1 Knapsack | Classic | Amazon |
| Partition Equal Subset | Subset Sum | Meta |
| Target Sum | Counting | Google |
| Coin Change | Unbounded Min | Amazon |
| Coin Change 2 | Unbounded Count | Google |
| Last Stone Weight II | Partition | Google |
| Ones and Zeroes | Multi-dimensional | Google |

---

## Key Takeaways

1. **Backward loop for 0/1**, forward for unbounded.

2. **Transform problems** to subset sum when possible.

3. **Space optimization** from O(n×W) to O(W).

4. **Count vs Minimize:** Different recurrence relations.

---

## What's Next?

Grid DP for pathfinding and matrix problems:

👉 [Grid DP Pattern →](./grid-dp)
