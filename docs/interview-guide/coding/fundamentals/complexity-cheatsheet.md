---
sidebar_position: 5
title: "Complexity Cheat Sheet"
description: >-
  Quick reference for time and space complexity of common data structures
  and algorithms. Print this and memorize it.
keywords:
  - time complexity
  - space complexity
  - big o cheat sheet
  - algorithm complexity
difficulty: Beginner
estimated_time: 10 minutes
prerequisites: []
companies: [All Companies]
---

# Complexity Cheat Sheet

Print this. Memorize this. Reference this before every interview.

---

## Data Structure Operations

### Arrays

| Operation | Time | Notes |
|-----------|------|-------|
| Access by index | O(1) | |
| Search (unsorted) | O(n) | |
| Search (sorted) | O(log n) | Binary search |
| Insert at end | O(1) | Amortized |
| Insert at middle | O(n) | Shift elements |
| Delete at end | O(1) | |
| Delete at middle | O(n) | Shift elements |

### Linked List

| Operation | Time | Notes |
|-----------|------|-------|
| Access by index | O(n) | |
| Search | O(n) | |
| Insert at head | O(1) | |
| Insert at tail | O(1) | With tail pointer |
| Insert at middle | O(n) | O(1) if have reference |
| Delete | O(n) | O(1) if have reference |

### Hash Table

| Operation | Average | Worst |
|-----------|---------|-------|
| Insert | O(1) | O(n) |
| Delete | O(1) | O(n) |
| Search | O(1) | O(n) |

### Binary Search Tree (Balanced)

| Operation | Average | Worst (unbalanced) |
|-----------|---------|-------------------|
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| Search | O(log n) | O(n) |

### Heap

| Operation | Time |
|-----------|------|
| Insert | O(log n) |
| Delete max/min | O(log n) |
| Get max/min | O(1) |
| Heapify array | O(n) |

### Stack / Queue

| Operation | Time |
|-----------|------|
| Push/Enqueue | O(1) |
| Pop/Dequeue | O(1) |
| Peek | O(1) |

---

## Sorting Algorithms

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes |
| Radix Sort | O(nk) | O(nk) | O(nk) | O(n+k) | Yes |

---

## Graph Algorithms

| Algorithm | Time | Space |
|-----------|------|-------|
| BFS | O(V + E) | O(V) |
| DFS | O(V + E) | O(V) |
| Dijkstra | O((V + E) log V) | O(V) |
| Bellman-Ford | O(VE) | O(V) |
| Floyd-Warshall | O(V³) | O(V²) |
| Topological Sort | O(V + E) | O(V) |
| Kruskal's MST | O(E log E) | O(V) |
| Prim's MST | O((V + E) log V) | O(V) |

---

## Common Patterns

| Pattern | Typical Complexity |
|---------|-------------------|
| Two Pointers | O(n) |
| Sliding Window | O(n) |
| Binary Search | O(log n) |
| BFS/DFS | O(V + E) |
| Dynamic Programming | O(n²) or O(n × m) |
| Backtracking | O(2ⁿ) or O(n!) |
| Divide & Conquer | O(n log n) |

---

## Space Complexity Rules

| What | Space |
|------|-------|
| Primitives | O(1) |
| Array of size n | O(n) |
| 2D array n×m | O(n × m) |
| Hash map with n entries | O(n) |
| Recursive call stack | O(depth) |
| Graph adjacency list | O(V + E) |
| Graph adjacency matrix | O(V²) |

---

## Quick Reference

```
O(1)       - Hash table lookup, array access
O(log n)   - Binary search, balanced tree ops
O(n)       - Linear scan, two pointers
O(n log n) - Efficient sorting (merge, quick, heap)
O(n²)      - Nested loops, naive DP
O(2ⁿ)      - Subsets, combinations
O(n!)      - Permutations
```

---

## Interview Tips

1. **Always state complexity** after solving.
2. **Time AND space** - mention both.
3. **Average vs worst case** - know when they differ.
4. **Can you do better?** - always ask yourself.
