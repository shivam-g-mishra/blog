---
sidebar_position: 2
title: "7-Day Sprint — Maximum Impact Prep"
description: >-
  Interview in a week? This high-intensity roadmap covers the patterns that
  appear most frequently. Focus ruthlessly, skip the rest.
keywords:
  - 7 day interview prep
  - one week coding interview
  - fast interview preparation
  - urgent interview prep
  - interview sprint

slug: /interview-guide/roadmaps/one-week-sprint
---

import { ConfidenceBuilder, TimeEstimate, DifficultyBadge } from '@site/src/components/interview-guide';

# 7-Day Sprint: Maximum Impact Prep

**You have 7 days. Let's make them count.**

This isn't about learning everything—it's about learning what matters most. 80% of interview problems come from 20% of patterns. We're going after that 20%.

<TimeEstimate
  learnTime="4-6 hours daily"
  practiceTime="~35 hours total"
  masteryTime="6 core patterns"
  interviewFrequency="Covers ~70% of problems"
  difficultyRange="Focused, high-impact"
  prerequisites="Basic programming knowledge"
/>

---

## The Philosophy

**Ruthless prioritization.** Every hour matters. We skip:
- Rare patterns (appears in <5% of interviews)
- Advanced optimizations (good enough is good enough)
- Deep system design (unless you're senior+)
- Exotic data structures (segment trees, etc.)

**What we focus on:**
- Patterns that appear in 50%+ of interviews
- Building blocks you can adapt to variations
- Communication skills (explaining your approach)

---

## Daily Schedule Overview

| Day | Focus | Hours | Key Outcome |
|-----|-------|-------|-------------|
| 1 | Arrays: Two Pointers | 5-6h | Solve any two-pointer problem |
| 2 | Arrays: Sliding Window | 5-6h | Fixed and variable windows |
| 3 | Trees: Traversals + BFS | 5-6h | DFS patterns, level-order |
| 4 | Graphs: BFS/DFS | 5-6h | Islands, shortest path |
| 5 | Binary Search + DP Basics | 5-6h | Templates memorized |
| 6 | Mock Interviews | 4-5h | Full simulation |
| 7 | Review + Behavioral | 3-4h | Rest and consolidate |

**Total: ~35 hours**

---

## Day 1: Two Pointers

### Morning (3 hours): Learn the Patterns

**Read:** [Two Pointers Pattern](/docs/interview-guide/coding/patterns/array-patterns/two-pointers)

**The three variations:**
1. **Opposite ends:** Start from both ends, move inward
2. **Same direction:** Fast and slow pointers
3. **Two arrays:** Merge sorted, intersection

**Template to memorize:**

```python
def two_pointer_opposite(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        # Process
        if condition:
            left += 1
        else:
            right -= 1
```

### Afternoon (3 hours): Practice Problems

| Problem | Time | Difficulty |
|---------|------|------------|
| [Two Sum II (Sorted)](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | 15 min | <DifficultyBadge level="medium" /> |
| [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | 20 min | <DifficultyBadge level="medium" /> |
| [3Sum](https://leetcode.com/problems/3sum/) | 30 min | <DifficultyBadge level="medium" /> |
| [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | 30 min | <DifficultyBadge level="hard" /> |

**Goal:** Solve at least 3 of 4 without hints.

### Evening Review
- Can you explain when to use two pointers?
- Can you write the template from memory?

---

## Day 2: Sliding Window

### Morning (3 hours): Learn the Patterns

**Read:** [Sliding Window Pattern](/docs/interview-guide/coding/patterns/array-patterns/sliding-window)

**The two types:**
1. **Fixed window:** Window size is given
2. **Variable window:** Find optimal window size

**Template to memorize:**

```python
def sliding_window_variable(s):
    left = 0
    window = {}  # or other state
    result = 0
    
    for right in range(len(s)):
        # Expand: add s[right] to window
        
        while invalid_condition:
            # Contract: remove s[left] from window
            left += 1
        
        # Update result
        result = max(result, right - left + 1)
    
    return result
```

### Afternoon (3 hours): Practice Problems

| Problem | Time | Difficulty |
|---------|------|------------|
| [Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/) | 15 min | <DifficultyBadge level="easy" /> |
| [Longest Substring Without Repeating](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | 25 min | <DifficultyBadge level="medium" /> |
| [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | 35 min | <DifficultyBadge level="hard" /> |
| [Permutation in String](https://leetcode.com/problems/permutation-in-string/) | 25 min | <DifficultyBadge level="medium" /> |

**Goal:** Recognize fixed vs variable window immediately.

---

## Day 3: Trees (DFS + BFS)

### Morning (3 hours): Learn the Patterns

**Read:** [Tree Traversals](/docs/interview-guide/coding/patterns/tree-patterns/traversals)

**Must know:**
1. Inorder, Preorder, Postorder (recursive + iterative)
2. Level-order (BFS with queue)
3. DFS patterns: return value, pass value down, global variable

**Templates to memorize:**

```python
# DFS - recursive
def dfs(node):
    if not node:
        return base_case
    left = dfs(node.left)
    right = dfs(node.right)
    return combine(left, right, node.val)

# BFS - level order
def bfs(root):
    queue = deque([root])
    while queue:
        for _ in range(len(queue)):
            node = queue.popleft()
            # process node
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
```

### Afternoon (3 hours): Practice Problems

| Problem | Time | Difficulty |
|---------|------|------------|
| [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | 10 min | <DifficultyBadge level="easy" /> |
| [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | 10 min | <DifficultyBadge level="easy" /> |
| [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | 20 min | <DifficultyBadge level="medium" /> |
| [Validate BST](https://leetcode.com/problems/validate-binary-search-tree/) | 25 min | <DifficultyBadge level="medium" /> |
| [Lowest Common Ancestor](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | 25 min | <DifficultyBadge level="medium" /> |

---

## Day 4: Graphs (BFS/DFS)

### Morning (3 hours): Learn the Patterns

**Read:** [Graph Traversal](/docs/interview-guide/coding/patterns/graph-patterns/traversal)

**Must know:**
1. BFS for shortest path (unweighted)
2. DFS for exploring all paths
3. Visited set to avoid cycles
4. Grid as implicit graph

**Templates to memorize:**

```python
# BFS shortest path
def bfs(graph, start):
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        node, dist = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

# DFS on grid
def dfs(grid, i, j, visited):
    if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]):
        return
    if (i, j) in visited or grid[i][j] == 0:
        return
    visited.add((i, j))
    for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        dfs(grid, i + di, j + dj, visited)
```

### Afternoon (3 hours): Practice Problems

| Problem | Time | Difficulty |
|---------|------|------------|
| [Number of Islands](https://leetcode.com/problems/number-of-islands/) | 20 min | <DifficultyBadge level="medium" /> |
| [Clone Graph](https://leetcode.com/problems/clone-graph/) | 25 min | <DifficultyBadge level="medium" /> |
| [Course Schedule](https://leetcode.com/problems/course-schedule/) | 30 min | <DifficultyBadge level="medium" /> |
| [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | 25 min | <DifficultyBadge level="medium" /> |

---

## Day 5: Binary Search + DP Basics

### Morning (2.5 hours): Binary Search

**Read:** [Binary Search](/docs/interview-guide/coding/patterns/search-patterns/binary-search)

**Template:**

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1  # or left for insertion point
```

**Practice:**
- [Binary Search](https://leetcode.com/problems/binary-search/) (10 min)
- [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) (25 min)
- [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) (20 min)

### Afternoon (2.5 hours): DP Basics

**Read:** [DP Introduction](/docs/interview-guide/coding/patterns/dp-patterns/introduction)

**Focus on:**
1. Fibonacci pattern (climbing stairs)
2. Decision pattern (house robber)

**Practice:**
- [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) (15 min)
- [House Robber](https://leetcode.com/problems/house-robber/) (20 min)
- [Coin Change](https://leetcode.com/problems/coin-change/) (30 min)

---

## Day 6: Mock Interviews

### Morning: Coding Mocks (3 hours)

Do 2-3 full mock interviews:
- Use a timer (45 minutes per problem)
- Explain your thought process out loud
- Code without IDE autocomplete
- Practice debugging

**Resources:**
- [Pramp](https://www.pramp.com/) (free peer mocks)
- Practice with a friend
- Record yourself and review

### Afternoon: Behavioral Prep (2 hours)

**Read:** [STAR Method](/docs/interview-guide/behavioral/star-method)

**Prepare 3-5 stories:**
1. A challenging project you led
2. A time you failed and learned
3. A conflict you resolved
4. A time you went above and beyond
5. Why this company/role

**Practice saying them out loud.**

---

## Day 7: Review + Rest

### Morning: Review Weak Areas (2 hours)

- Revisit problems you struggled with
- Review templates one more time
- Practice explaining your approach

### Afternoon: Light Review + Rest (1-2 hours)

- Don't learn anything new
- Light review of notes
- **Rest your mind**—sleep is critical for performance

---

## Quick Reference Card

**Print this and review before your interview:**

### Templates

```python
# Two Pointers (opposite)
left, right = 0, len(arr) - 1
while left < right: ...

# Sliding Window
left = 0
for right in range(n):
    # expand
    while invalid: left += 1  # contract
    # update result

# BFS
queue = deque([start])
while queue:
    node = queue.popleft()
    for neighbor in graph[node]:
        queue.append(neighbor)

# DFS (recursive)
def dfs(node):
    if not node: return
    dfs(node.left)
    dfs(node.right)

# Binary Search
while left <= right:
    mid = left + (right - left) // 2
```

### Pattern Recognition

| If you see... | Think... |
|---------------|----------|
| Sorted array, find target | Binary Search |
| Subarray/substring sum | Sliding Window |
| Two sorted arrays | Two Pointers |
| Shortest path (unweighted) | BFS |
| All paths, connected components | DFS |
| Optimal substructure | DP |

---

## What to Do If You Run Out of Time

**Priorities (in order):**
1. Two Pointers + Sliding Window (Day 1-2)
2. BFS/DFS (Day 3-4)
3. Binary Search (Day 5 morning)
4. Behavioral stories (Day 6 afternoon)

**Skip if necessary:**
- DP (focus on recognizing it, not solving)
- Mock interviews (but try to do at least 1)

---

<ConfidenceBuilder type="youve-got-this">

**7 days is enough.**

You won't know everything. That's okay. Focus on the patterns that matter most, communicate clearly, and show your problem-solving process. Many successful candidates have prepared in less time than this.

Take a deep breath. You've got this.

</ConfidenceBuilder>
