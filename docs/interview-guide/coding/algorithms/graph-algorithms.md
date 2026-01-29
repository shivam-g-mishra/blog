---
sidebar_position: 4
title: "Graph Algorithms"
description: >-
  Essential graph algorithms for coding interviews. BFS, DFS, Dijkstra,
  topological sort, and union-find applications.
keywords:
  - graph algorithms
  - BFS DFS
  - dijkstra
  - topological sort
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - Graphs
  - Big-O Notation
companies: [Google, Amazon, Meta, Microsoft]
---

# Graph Algorithms: The Essential Toolkit

Most graph problems boil down to a few core algorithms. Know these cold.

---

## Algorithm Selection

| Problem Type | Algorithm | Time |
|--------------|-----------|------|
| Shortest path (unweighted) | BFS | O(V + E) |
| Explore all paths | DFS | O(V + E) |
| Shortest path (weighted) | Dijkstra | O((V+E) log V) |
| Detect cycle (directed) | DFS with colors | O(V + E) |
| Detect cycle (undirected) | Union-Find | O(E α(V)) |
| Ordering with dependencies | Topological Sort | O(V + E) |
| Connected components | DFS/BFS or Union-Find | O(V + E) |
| Minimum spanning tree | Kruskal/Prim | O(E log V) |

---

## BFS (Breadth-First Search)

**Use for:** Shortest path in unweighted graph, level-order traversal.

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

def shortest_path(graph, start, end):
    queue = deque([(start, 0)])
    visited = {start}
    
    while queue:
        node, dist = queue.popleft()
        
        if node == end:
            return dist
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    
    return -1
```

---

## DFS (Depth-First Search)

**Use for:** Detecting cycles, finding all paths, exploring components.

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

def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(node)
    process(node)
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)
```

---

## Cycle Detection

### Directed Graph (3-Color DFS)

```python
def has_cycle_directed(graph, n):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n
    
    def dfs(node):
        color[node] = GRAY
        
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:  # Back edge
                return True
            if color[neighbor] == WHITE and dfs(neighbor):
                return True
        
        color[node] = BLACK
        return False
    
    for node in range(n):
        if color[node] == WHITE and dfs(node):
            return True
    
    return False
```

### Undirected Graph (Union-Find)

```python
def has_cycle_undirected(n, edges):
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    for u, v in edges:
        pu, pv = find(u), find(v)
        if pu == pv:
            return True  # Cycle found
        parent[pu] = pv
    
    return False
```

---

## Topological Sort

**Use for:** Task scheduling, build order, course prerequisites.

```python
from collections import deque

def topological_sort(n, edges):
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
    
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

## Dijkstra's Algorithm

**Use for:** Shortest path with non-negative weights.

```python
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    heap = [(0, start)]
    
    while heap:
        dist, node = heapq.heappop(heap)
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    
    return distances
```

---

## Connected Components

```python
def count_components(n, edges):
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
            return True
        return False
    
    for u, v in edges:
        union(u, v)
    
    return len(set(find(i) for i in range(n)))
```

---

## Common Problems

| Problem | Algorithm | Key Insight |
|---------|-----------|-------------|
| Number of Islands | DFS/BFS | Flood fill from each '1' |
| Course Schedule | Topological Sort | Detect cycle in DAG |
| Network Delay | Dijkstra | Shortest path to all nodes |
| Clone Graph | DFS + HashMap | Map old → new nodes |
| Word Ladder | BFS | Shortest transformation |
| Alien Dictionary | Topological Sort | Build graph from order |

---

## Key Takeaways

1. **BFS for shortest path** in unweighted graphs.
2. **DFS for exploring** all possibilities, detecting cycles.
3. **Topological sort** for dependency ordering.
4. **Dijkstra for weighted** shortest paths (no negative).
5. **Union-Find for components** and undirected cycle detection.
