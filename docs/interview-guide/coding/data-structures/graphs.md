---
sidebar_position: 7
title: "Graphs — BFS, DFS & Essential Algorithms"
description: >-
  Master graph data structures for coding interviews. Learn representations,
  BFS, DFS, topological sort, and solve classic graph problems.
keywords:
  - graph interview questions
  - BFS DFS
  - adjacency list
  - topological sort
  - shortest path
difficulty: Intermediate
estimated_time: 55 minutes
prerequisites:
  - Big-O Notation
  - Stacks & Queues
  - Trees
companies: [Google, Meta, Amazon, Microsoft, Apple]
---

# Graphs: Where Relationships Get Complex

Trees are graphs with rules: one parent, no cycles. Remove those rules, and you get graphs—the most flexible data structure for modeling relationships.

Social networks. Maps. Course prerequisites. The internet itself. All graphs.

**If a problem involves connections between entities, think graph.**

---

## Graph Representations

### 1. Adjacency List (Most Common)

```python
# Using dictionary
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# Using defaultdict for cleaner code
from collections import defaultdict
graph = defaultdict(list)
graph['A'].append('B')
graph['A'].append('C')
```

**Space:** O(V + E)
**Best for:** Sparse graphs, most interview problems

### 2. Adjacency Matrix

```python
#     A  B  C  D
# A [[0, 1, 1, 0],
# B  [1, 0, 0, 1],
# C  [1, 0, 0, 1],
# D  [0, 1, 1, 0]]

# Check edge: O(1)
has_edge = matrix[i][j] == 1
```

**Space:** O(V²)
**Best for:** Dense graphs, quick edge lookup

### 3. Edge List

```python
edges = [
    ('A', 'B'),
    ('A', 'C'),
    ('B', 'D'),
    ('C', 'D')
]
```

**Space:** O(E)
**Best for:** Simple problems, Kruskal's algorithm

---

## Building Graphs from Input

Most interview problems give edges, not a ready graph:

```python
# From edge list to adjacency list
def build_graph(edges, directed=False):
    graph = defaultdict(list)
    
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)
    
    return graph

# Example
edges = [[0, 1], [0, 2], [1, 2], [2, 3]]
graph = build_graph(edges)
# {0: [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2]}
```

---

## BFS: Breadth-First Search

**Use when:** Shortest path (unweighted), level-by-level processing

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    order = []
    
    while queue:
        node = queue.popleft()
        order.append(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return order
```

### BFS for Shortest Path

```python
def shortest_path(graph, start, end):
    if start == end:
        return 0
    
    visited = {start}
    queue = deque([(start, 0)])  # (node, distance)
    
    while queue:
        node, dist = queue.popleft()
        
        for neighbor in graph[node]:
            if neighbor == end:
                return dist + 1
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    
    return -1  # No path
```

### Multi-Source BFS

Start from multiple sources simultaneously:

```python
# Rotting Oranges - spread from all rotten oranges at once
def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    
    # Find all rotten and count fresh
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    
    if fresh == 0:
        return 0
    
    minutes = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while queue:
        minutes += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                if (0 <= nr < rows and 0 <= nc < cols and 
                    grid[nr][nc] == 1):
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
    
    return minutes - 1 if fresh == 0 else -1
```

---

## DFS: Depth-First Search

**Use when:** Exploring all paths, detecting cycles, topological sort

```python
# Recursive DFS
def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(node)
    result = [node]
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            result.extend(dfs_recursive(graph, neighbor, visited))
    
    return result

# Iterative DFS
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    order = []
    
    while stack:
        node = stack.pop()
        
        if node not in visited:
            visited.add(node)
            order.append(node)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return order
```

### DFS for Cycle Detection

```python
# Directed graph - need to track current path
def has_cycle_directed(graph, n):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    
    def dfs(node):
        color[node] = GRAY  # Currently visiting
        
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:  # Back edge = cycle
                return True
            if color[neighbor] == WHITE and dfs(neighbor):
                return True
        
        color[node] = BLACK  # Done visiting
        return False
    
    for node in range(n):
        if color[node] == WHITE and dfs(node):
            return True
    
    return False

# Undirected graph - simpler
def has_cycle_undirected(graph, n):
    visited = set()
    
    def dfs(node, parent):
        visited.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:  # Back to non-parent = cycle
                return True
        
        return False
    
    for node in range(n):
        if node not in visited and dfs(node, -1):
            return True
    
    return False
```

---

## Topological Sort

**Use when:** Order tasks with dependencies (DAG only)

```python
# Using DFS
def topological_sort(graph, n):
    visited = set()
    result = []
    
    def dfs(node):
        visited.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        
        result.append(node)  # Add after all descendants
    
    for node in range(n):
        if node not in visited:
            dfs(node)
    
    return result[::-1]  # Reverse for correct order

# Using BFS (Kahn's algorithm)
def topological_sort_bfs(graph, n):
    indegree = [0] * n
    
    # Calculate indegrees
    for node in range(n):
        for neighbor in graph[node]:
            indegree[neighbor] += 1
    
    # Start with nodes having no dependencies
    queue = deque([i for i in range(n) if indegree[i] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    return result if len(result) == n else []  # Empty if cycle
```

---

## Classic Interview Problems

### Problem 1: Number of Islands

```python
def num_islands(grid):
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or 
            grid[r][c] == '0'):
            return
        
        grid[r][c] = '0'  # Mark visited
        
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    
    return count
```

### Problem 2: Clone Graph

```python
def clone_graph(node):
    if not node:
        return None
    
    cloned = {}
    
    def dfs(n):
        if n in cloned:
            return cloned[n]
        
        copy = Node(n.val)
        cloned[n] = copy
        
        for neighbor in n.neighbors:
            copy.neighbors.append(dfs(neighbor))
        
        return copy
    
    return dfs(node)
```

### Problem 3: Course Schedule

```python
def can_finish(num_courses, prerequisites):
    graph = defaultdict(list)
    indegree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1
    
    queue = deque([i for i in range(num_courses) if indegree[i] == 0])
    completed = 0
    
    while queue:
        course = queue.popleft()
        completed += 1
        
        for next_course in graph[course]:
            indegree[next_course] -= 1
            if indegree[next_course] == 0:
                queue.append(next_course)
    
    return completed == num_courses
```

### Problem 4: Word Ladder

```python
def ladder_length(begin_word, end_word, word_list):
    word_set = set(word_list)
    if end_word not in word_set:
        return 0
    
    queue = deque([(begin_word, 1)])
    
    while queue:
        word, length = queue.popleft()
        
        if word == end_word:
            return length
        
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i+1:]
                
                if new_word in word_set:
                    word_set.remove(new_word)
                    queue.append((new_word, length + 1))
    
    return 0
```

---

## When to Use BFS vs DFS

| Use BFS | Use DFS |
|---------|---------|
| Shortest path (unweighted) | Explore all paths |
| Level-by-level processing | Detect cycles |
| Nearest neighbor | Topological sort |
| Minimum steps/moves | Connected components |

---

## Practice Problems

### Easy

| Problem | Pattern | Company |
|---------|---------|---------|
| Flood Fill | DFS/BFS | Google |
| Find if Path Exists | BFS/DFS | Meta |

### Medium

| Problem | Pattern | Company |
|---------|---------|---------|
| Number of Islands | DFS | Amazon, Google |
| Clone Graph | DFS | Meta |
| Course Schedule | Topological | Amazon |
| Pacific Atlantic Water | DFS | Google |
| Rotting Oranges | Multi-BFS | Amazon |

### Hard

| Problem | Pattern | Company |
|---------|---------|---------|
| Word Ladder | BFS | Amazon |
| Alien Dictionary | Topological | Meta |
| Shortest Path in Binary Matrix | BFS | Google |

---

## Key Takeaways

1. **Adjacency list for interviews.** O(V + E) space, handles sparse graphs well.

2. **BFS for shortest path** in unweighted graphs. Use queue.

3. **DFS for exploration** and backtracking. Use stack or recursion.

4. **Topological sort for dependencies.** Only works on DAGs.

5. **Grid problems are graphs.** Each cell connects to neighbors.

---

## What's Next?

Heaps are essential for "top K" problems and priority scheduling:

👉 [Heaps & Priority Queues →](./heaps-priority-queues)
