---
sidebar_position: 2
title: "Topological Sort Pattern"
description: >-
  Master topological sorting for coding interviews. Course schedule,
  build order, and dependency resolution problems.
keywords:
  - topological sort
  - course schedule
  - dependency order
  - DAG
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - Graphs
  - BFS/DFS
companies: [Google, Amazon, Meta, Microsoft]
---

# Topological Sort: Order Dependencies

Topological sort orders vertices in a DAG so that for every edge u→v, u comes before v.

---

## When to Use

```
Keywords that suggest topological sort:
- "ordering"
- "dependency"
- "prerequisites"
- "build order"
- "schedule"
```

---

## Kahn's Algorithm (BFS)

```python
from collections import deque, defaultdict

def topological_sort_bfs(num_nodes, edges):
    # Build graph and count in-degrees
    graph = defaultdict(list)
    in_degree = [0] * num_nodes
    
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
    
    # Start with nodes having no dependencies
    queue = deque([i for i in range(num_nodes) if in_degree[i] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check for cycle
    if len(result) != num_nodes:
        return []  # Cycle exists
    
    return result
```

---

## DFS Approach

```python
def topological_sort_dfs(num_nodes, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
    
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * num_nodes
    result = []
    has_cycle = False
    
    def dfs(node):
        nonlocal has_cycle
        if has_cycle:
            return
        
        color[node] = GRAY
        
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                has_cycle = True
                return
            if color[neighbor] == WHITE:
                dfs(neighbor)
        
        color[node] = BLACK
        result.append(node)
    
    for node in range(num_nodes):
        if color[node] == WHITE:
            dfs(node)
    
    if has_cycle:
        return []
    
    return result[::-1]
```

---

## Course Schedule

Can you finish all courses given prerequisites?

```python
def can_finish(num_courses, prerequisites):
    graph = defaultdict(list)
    in_degree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    count = 0
    
    while queue:
        course = queue.popleft()
        count += 1
        
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    return count == num_courses
```

---

## Course Schedule II

Return order to take courses.

```python
def find_order(num_courses, prerequisites):
    graph = defaultdict(list)
    in_degree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    order = []
    
    while queue:
        course = queue.popleft()
        order.append(course)
        
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    return order if len(order) == num_courses else []
```

---

## Alien Dictionary

Derive order of letters from sorted alien words.

```python
def alien_order(words):
    # Build graph from adjacent word pairs
    graph = defaultdict(set)
    in_degree = {c: 0 for word in words for c in word}
    
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        
        # Check for invalid case: "abc" before "ab"
        if len(w1) > len(w2) and w1[:len(w2)] == w2:
            return ""
        
        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                if c2 not in graph[c1]:
                    graph[c1].add(c2)
                    in_degree[c2] += 1
                break
    
    # Topological sort
    queue = deque([c for c in in_degree if in_degree[c] == 0])
    result = []
    
    while queue:
        c = queue.popleft()
        result.append(c)
        
        for neighbor in graph[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(result) != len(in_degree):
        return ""  # Cycle
    
    return "".join(result)
```

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Course Schedule | Medium | Amazon |
| Course Schedule II | Medium | Google |
| Alien Dictionary | Hard | Meta |
| Minimum Height Trees | Medium | Google |
| Sequence Reconstruction | Medium | Google |

---

## Key Takeaways

1. **BFS (Kahn's)** is often simpler for interviews.
2. **Cycle detection** is built-in (count != total nodes).
3. **Build graph** from dependency pairs first.
4. **In-degree tracking** is the key insight.
