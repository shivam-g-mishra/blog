---
sidebar_position: 3
title: "Shortest Path Algorithms"
description: >-
  Master shortest path algorithms for coding interviews. Dijkstra,
  Bellman-Ford, BFS, and when to use each.
keywords:
  - shortest path
  - dijkstra algorithm
  - bellman ford
  - graph algorithms
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - Graphs
  - BFS/DFS
companies: [Google, Amazon, Uber, Meta]
---

# Shortest Path: Finding the Way

Different algorithms for different graph types. Know when to use each.

---

## Algorithm Selection

| Graph Type | Algorithm | Time |
|------------|-----------|------|
| Unweighted | BFS | O(V + E) |
| Non-negative weights | Dijkstra | O((V+E) log V) |
| Negative weights (no neg cycle) | Bellman-Ford | O(VE) |
| All pairs | Floyd-Warshall | O(V³) |

---

## BFS (Unweighted)

```python
from collections import deque

def shortest_path_bfs(graph, start, end):
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
    
    return -1  # No path
```

---

## Dijkstra's Algorithm

```python
import heapq

def dijkstra(graph, start):
    # graph[node] = [(neighbor, weight), ...]
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

### With Path Reconstruction

```python
def dijkstra_with_path(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    
    heap = [(0, start)]
    
    while heap:
        dist, node = heapq.heappop(heap)
        
        if node == end:
            break
        
        if dist > distances[node]:
            continue
        
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = node
                heapq.heappush(heap, (new_dist, neighbor))
    
    # Reconstruct path
    path = []
    current = end
    while current:
        path.append(current)
        current = previous[current]
    
    return distances[end], path[::-1]
```

---

## Bellman-Ford (Handles Negatives)

```python
def bellman_ford(graph, n, edges, start):
    # edges = [(u, v, weight), ...]
    distances = [float('inf')] * n
    distances[start] = 0
    
    # Relax all edges V-1 times
    for _ in range(n - 1):
        for u, v, weight in edges:
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
    
    # Check for negative cycles
    for u, v, weight in edges:
        if distances[u] + weight < distances[v]:
            return None  # Negative cycle exists
    
    return distances
```

---

## Common Problems

### Network Delay Time

```python
def network_delay_time(times, n, k):
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    
    distances = dijkstra(graph, k)
    
    max_time = max(distances.values())
    return max_time if max_time < float('inf') else -1
```

### Cheapest Flights Within K Stops

```python
def find_cheapest_price(n, flights, src, dst, k):
    # BFS with level tracking (or modified Bellman-Ford)
    prices = [float('inf')] * n
    prices[src] = 0
    
    for _ in range(k + 1):
        temp = prices[:]
        for u, v, price in flights:
            if prices[u] + price < temp[v]:
                temp[v] = prices[u] + price
        prices = temp
    
    return prices[dst] if prices[dst] < float('inf') else -1
```

### Path with Minimum Effort

```python
def minimum_effort_path(heights):
    rows, cols = len(heights), len(heights[0])
    efforts = [[float('inf')] * cols for _ in range(rows)]
    efforts[0][0] = 0
    
    heap = [(0, 0, 0)]  # (effort, row, col)
    
    while heap:
        effort, r, c = heapq.heappop(heap)
        
        if r == rows - 1 and c == cols - 1:
            return effort
        
        if effort > efforts[r][c]:
            continue
        
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_effort = max(effort, abs(heights[nr][nc] - heights[r][c]))
                if new_effort < efforts[nr][nc]:
                    efforts[nr][nc] = new_effort
                    heapq.heappush(heap, (new_effort, nr, nc))
    
    return 0
```

---

## Practice Problems

| Problem | Algorithm | Company |
|---------|-----------|---------|
| Network Delay Time | Dijkstra | Google |
| Cheapest Flights K Stops | Modified BF | Amazon |
| Path with Minimum Effort | Dijkstra variant | Google |
| Shortest Path in Grid | BFS | Meta |
| Swim in Rising Water | Dijkstra | Google |

---

## Key Takeaways

1. **BFS for unweighted** graphs—simplest and fastest.
2. **Dijkstra for non-negative** weights—use priority queue.
3. **Bellman-Ford handles negatives** but is slower.
4. **Detect negative cycles** with extra Bellman-Ford iteration.
5. **Dijkstra variants** for min-max path problems.
