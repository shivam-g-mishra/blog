---
sidebar_position: 10
title: "Union-Find (Disjoint Set)"
description: >-
  Master Union-Find for coding interviews. Connected components, cycle detection,
  and optimization techniques.
keywords:
  - union find
  - disjoint set
  - connected components
  - path compression
  - union by rank
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - Graphs
  - Trees
companies: [Google, Amazon, Meta, Microsoft]
---

# Union-Find: Track Connected Components

Union-Find tracks which elements belong to which groups, with near O(1) operations.

---

## When to Use

| Problem Type | Example |
|--------------|---------|
| Connected components | Network connectivity |
| Cycle detection | Graph has cycle? |
| Dynamic connectivity | Add edges over time |
| Grouping | Accounts merge |

---

## Basic Implementation

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # Already connected
        
        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        
        return True
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

---

## Key Optimizations

### Path Compression

```
Before find(4):
    0
    |
    1
    |
    2
    |
    3
    |
    4

After find(4):
      0
   /|\ \ 
  1 2 3 4
```

### Union by Rank

Always attach smaller tree under larger tree:
```
Union(small, large):
    large          large
               →   / \
    small        small old
```

---

## Classic Problems

### Number of Islands

```python
def num_islands(grid):
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    uf = UnionFind(rows * cols)
    count = sum(grid[r][c] == '1' for r in range(rows) for c in range(cols))
    
    def index(r, c):
        return r * cols + c
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                        if uf.union(index(r, c), index(nr, nc)):
                            count -= 1
    
    return count
```

### Accounts Merge

```python
def accounts_merge(accounts):
    uf = UnionFind(len(accounts))
    email_to_id = {}
    
    # Union accounts with same email
    for i, account in enumerate(accounts):
        for email in account[1:]:
            if email in email_to_id:
                uf.union(i, email_to_id[email])
            email_to_id[email] = i
    
    # Group emails by root account
    id_to_emails = defaultdict(set)
    for email, id in email_to_id.items():
        root = uf.find(id)
        id_to_emails[root].add(email)
    
    # Format result
    return [[accounts[id][0]] + sorted(emails) 
            for id, emails in id_to_emails.items()]
```

### Redundant Connection (Find cycle edge)

```python
def find_redundant_connection(edges):
    n = len(edges)
    uf = UnionFind(n + 1)
    
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]  # This edge creates cycle
    
    return []
```

---

## Complexity

| Operation | Without Opt | With Opt |
|-----------|-------------|----------|
| Find | O(n) | O(α(n)) ≈ O(1) |
| Union | O(n) | O(α(n)) ≈ O(1) |
| Space | O(n) | O(n) |

α(n) = inverse Ackermann function, effectively constant.

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Number of Islands | Medium | Amazon |
| Accounts Merge | Medium | Meta |
| Redundant Connection | Medium | Google |
| Longest Consecutive Sequence | Medium | Google |
| Number of Provinces | Medium | Microsoft |

---

## Key Takeaways

1. **Near O(1)** with path compression + union by rank.
2. **Track component count** by decrementing on successful union.
3. **Cycle detection:** Union returns false if already connected.
4. **Better than DFS** for dynamic connectivity.
