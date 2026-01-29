---
sidebar_position: 1
title: "Tree Traversal Patterns"
description: >-
  Master tree traversals for coding interviews. Recursive, iterative,
  level-order, and their applications.
keywords:
  - tree traversal
  - inorder preorder postorder
  - level order traversal
  - BFS DFS tree
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - Trees
companies: [All Companies]
---

# Tree Traversals: The Foundation

Every tree problem starts with traversal. Master these patterns.

---

## The Three DFS Traversals

```
        1
       / \
      2   3
     / \
    4   5

Inorder (Left, Root, Right):   4, 2, 5, 1, 3
Preorder (Root, Left, Right):  1, 2, 4, 5, 3
Postorder (Left, Right, Root): 4, 5, 2, 3, 1
```

---

## Recursive Implementations

```python
def inorder(root, result=[]):
    if root:
        inorder(root.left, result)
        result.append(root.val)
        inorder(root.right, result)
    return result

def preorder(root, result=[]):
    if root:
        result.append(root.val)
        preorder(root.left, result)
        preorder(root.right, result)
    return result

def postorder(root, result=[]):
    if root:
        postorder(root.left, result)
        postorder(root.right, result)
        result.append(root.val)
    return result
```

---

## Iterative Implementations

### Inorder (Stack)

```python
def inorder_iterative(root):
    result = []
    stack = []
    current = root
    
    while stack or current:
        while current:
            stack.append(current)
            current = current.left
        
        current = stack.pop()
        result.append(current.val)
        current = current.right
    
    return result
```

### Preorder (Stack)

```python
def preorder_iterative(root):
    if not root:
        return []
    
    result = []
    stack = [root]
    
    while stack:
        node = stack.pop()
        result.append(node.val)
        
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return result
```

### Postorder (Stack)

```python
def postorder_iterative(root):
    if not root:
        return []
    
    result = []
    stack = [root]
    
    while stack:
        node = stack.pop()
        result.append(node.val)
        
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    
    return result[::-1]  # Reverse at end
```

---

## Level Order (BFS)

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level = []
        level_size = len(queue)
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result
```

---

## When to Use Which

| Traversal | Use Case |
|-----------|----------|
| **Inorder** | BST → sorted order |
| **Preorder** | Copy tree, serialize |
| **Postorder** | Delete tree, evaluate expression |
| **Level Order** | Level by level problems, shortest path |

---

## Variations

### Zigzag Level Order

```python
def zigzag_level_order(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    left_to_right = True
    
    while queue:
        level = deque()
        for _ in range(len(queue)):
            node = queue.popleft()
            
            if left_to_right:
                level.append(node.val)
            else:
                level.appendleft(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(list(level))
        left_to_right = not left_to_right
    
    return result
```

### Vertical Order

```python
from collections import defaultdict

def vertical_order(root):
    if not root:
        return []
    
    column_table = defaultdict(list)
    queue = deque([(root, 0)])
    
    while queue:
        node, col = queue.popleft()
        column_table[col].append(node.val)
        
        if node.left:
            queue.append((node.left, col - 1))
        if node.right:
            queue.append((node.right, col + 1))
    
    return [column_table[col] for col in sorted(column_table.keys())]
```

---

## Practice Problems

| Problem | Traversal | Company |
|---------|-----------|---------|
| Inorder Traversal | Inorder | All |
| Level Order Traversal | BFS | Amazon |
| Zigzag Level Order | BFS | Meta |
| Vertical Order | BFS | Google |
| Right Side View | BFS | Amazon |

---

## Key Takeaways

1. **Inorder on BST** gives sorted order.
2. **Level order (BFS)** for level-by-level processing.
3. **Iterative versions** avoid stack overflow on deep trees.
4. **Track level size** at start of each BFS level.
