---
sidebar_position: 1
title: "Graph Traversal Patterns — BFS & DFS Mastery"
description: >-
  Master BFS and DFS for coding interviews. Level-order traversal, shortest path,
  cycle detection, and connected components.
keywords:
  - graph traversal
  - BFS
  - DFS
  - breadth first search
  - depth first search
  - shortest path
difficulty: Intermediate
estimated_time: 35 minutes
prerequisites:
  - Graphs Data Structure
  - Queues
companies: [Google, Meta, Amazon, Microsoft, Apple]
---

# Graph Traversal: BFS vs DFS

"When do I use BFS? When do I use DFS?"

This question confused me for months. I'd pick randomly and sometimes it worked, sometimes it didn't.

**The simple rule:**
- **BFS:** When you need shortest path or level-by-level processing
- **DFS:** When you need to explore all paths or detect cycles

---

## BFS: Level by Level

### The Template

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        process(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### BFS with Levels

```python
def bfs_levels(graph, start):
    visited = {start}
    queue = deque([start])
    level = 0
    
    while queue:
        level_size = len(queue)
        
        for _ in range(level_size):
            node = queue.popleft()
            process(node, level)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        level += 1
```

### When to Use BFS

| Use Case | Why BFS |
|----------|---------|
| Shortest path (unweighted) | First path found is shortest |
| Level-order traversal | Natural level progression |
| Minimum steps/moves | Each level = one step |
| Nearest neighbor | Explores closest first |

---

## DFS: Go Deep First

### Recursive Template

```python
def dfs_recursive(graph, node, visited):
    visited.add(node)
    process(node)
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)
```

### Iterative Template

```python
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    
    while stack:
        node = stack.pop()
        
        if node in visited:
            continue
        
        visited.add(node)
        process(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
```

### When to Use DFS

| Use Case | Why DFS |
|----------|---------|
| Path exists | Just need to find any path |
| Cycle detection | Track recursion stack |
| Topological sort | Finish order matters |
| Connected components | Explore entire component |
| Backtracking | Natural undo with recursion |

---

## Classic Problems

### Problem 1: Number of Islands (BFS/DFS)

```python
def num_islands(grid):
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
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

### Problem 2: Shortest Path in Binary Matrix (BFS)

```python
def shortest_path_binary_matrix(grid):
    if grid[0][0] == 1 or grid[-1][-1] == 1:
        return -1
    
    n = len(grid)
    directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    
    queue = deque([(0, 0, 1)])  # (row, col, distance)
    grid[0][0] = 1  # Mark visited
    
    while queue:
        r, c, dist = queue.popleft()
        
        if r == n - 1 and c == n - 1:
            return dist
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                grid[nr][nc] = 1
                queue.append((nr, nc, dist + 1))
    
    return -1
```

### Problem 3: Clone Graph (DFS)

```python
def clone_graph(node):
    if not node:
        return None
    
    clones = {}
    
    def dfs(node):
        if node in clones:
            return clones[node]
        
        clone = Node(node.val)
        clones[node] = clone
        
        for neighbor in node.neighbors:
            clone.neighbors.append(dfs(neighbor))
        
        return clone
    
    return dfs(node)
```

### Problem 4: Course Schedule (Cycle Detection)

```python
def can_finish(num_courses, prerequisites):
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)
    
    # 0 = unvisited, 1 = visiting, 2 = visited
    state = [0] * num_courses
    
    def has_cycle(course):
        if state[course] == 1:  # Currently visiting = cycle
            return True
        if state[course] == 2:  # Already processed
            return False
        
        state[course] = 1  # Mark as visiting
        
        for next_course in graph[course]:
            if has_cycle(next_course):
                return True
        
        state[course] = 2  # Mark as visited
        return False
    
    for course in range(num_courses):
        if has_cycle(course):
            return False
    
    return True
```

### Problem 5: Word Ladder (BFS)

```python
def ladder_length(begin_word, end_word, word_list):
    word_set = set(word_list)
    if end_word not in word_set:
        return 0
    
    queue = deque([(begin_word, 1)])
    visited = {begin_word}
    
    while queue:
        word, length = queue.popleft()
        
        if word == end_word:
            return length
        
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                next_word = word[:i] + c + word[i+1:]
                
                if next_word in word_set and next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, length + 1))
    
    return 0
```

---

## Decision Framework

```
Need shortest path/minimum steps?
├── Yes → BFS
│
Need to explore all paths or detect cycles?
├── Yes → DFS
│
Level-by-level processing?
├── Yes → BFS
│
Backtracking needed?
├── Yes → DFS (recursive)
│
Memory constrained?
├── Yes → DFS (uses less memory than BFS)
```

---

## Multi-Source BFS

Start from multiple sources simultaneously.

```python
def walls_and_gates(rooms):
    """Fill each empty room with distance to nearest gate."""
    if not rooms:
        return
    
    rows, cols = len(rooms), len(rooms[0])
    INF = 2147483647
    
    # Start BFS from all gates
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if rooms[r][c] == 0:  # Gate
                queue.append((r, c))
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while queue:
        r, c = queue.popleft()
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == INF:
                rooms[nr][nc] = rooms[r][c] + 1
                queue.append((nr, nc))
```

---

## Bidirectional BFS

Search from both ends for faster shortest path.

```python
def bidirectional_bfs(start, end, graph):
    if start == end:
        return 0
    
    front = {start}
    back = {end}
    visited = {start, end}
    steps = 0
    
    while front and back:
        steps += 1
        
        # Always expand smaller frontier
        if len(front) > len(back):
            front, back = back, front
        
        next_front = set()
        for node in front:
            for neighbor in graph[node]:
                if neighbor in back:
                    return steps
                if neighbor not in visited:
                    visited.add(neighbor)
                    next_front.add(neighbor)
        
        front = next_front
    
    return -1  # No path
```

---

## Practice Problems

### BFS Problems

| Problem | Type | Company |
|---------|------|---------|
| Number of Islands | Grid BFS | Amazon |
| Rotting Oranges | Multi-source BFS | Amazon |
| Word Ladder | State transition | Amazon, Google |
| Shortest Path Binary Matrix | Grid BFS | Meta |
| 01 Matrix | Multi-source BFS | Google |

### DFS Problems

| Problem | Type | Company |
|---------|------|---------|
| Clone Graph | Graph traversal | Meta |
| Course Schedule | Cycle detection | Amazon |
| Number of Provinces | Connected components | Amazon |
| Pacific Atlantic Water Flow | Multi-start DFS | Google |
| All Paths From Source | Path enumeration | Google |

---

## Key Takeaways

1. **BFS for shortest path** in unweighted graphs.

2. **DFS for cycle detection** and path exploration.

3. **Multi-source BFS** when starting from multiple points.

4. **Bidirectional BFS** can dramatically speed up search.

5. **Mark visited BEFORE adding to queue** to avoid duplicates.

---

## What's Next?

Topological sort for dependency ordering:

👉 [Topological Sort →](./topological-sort)
