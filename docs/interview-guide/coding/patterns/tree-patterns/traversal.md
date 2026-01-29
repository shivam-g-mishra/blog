---
sidebar_position: 1
title: "Tree Traversal Patterns"
description: >-
  Master tree traversal for coding interviews. Inorder, preorder, postorder,
  level-order, and iterative approaches.
keywords:
  - tree traversal
  - inorder
  - preorder
  - postorder
  - level order
  - BFS DFS tree
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - Trees Data Structure
companies: [Google, Meta, Amazon, Microsoft]
---

# Tree Traversal: Four Ways to Walk a Tree

Every tree problem starts with traversal. Master these four patterns.

---

## The Four Traversals

```
        1
       / \
      2   3
     / \
    4   5

Inorder (L-Root-R):   4, 2, 5, 1, 3  (BST: sorted order)
Preorder (Root-L-R):  1, 2, 4, 5, 3  (copy tree, serialize)
Postorder (L-R-Root): 4, 5, 2, 3, 1  (delete tree, evaluate)
Level-order:          1, 2, 3, 4, 5  (BFS, level problems)
```

---

## Recursive Implementations

```python
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

def preorder(root):
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)

def postorder(root):
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]
```

---

## Iterative Implementations

### Inorder (Stack)

```python
def inorder_iterative(root):
    result, stack = [], []
    current = root
    
    while current or stack:
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
    
    result, stack = [], [root]
    
    while stack:
        node = stack.pop()
        result.append(node.val)
        
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return result
```

### Level Order (Queue)

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level = []
        for _ in range(len(queue)):
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
| **Inorder** | BST sorted order, validate BST |
| **Preorder** | Serialize tree, copy tree |
| **Postorder** | Delete tree, evaluate expression |
| **Level-order** | Level-based problems, BFS |

---

## Practice Problems

| Problem | Traversal | Company |
|---------|-----------|---------|
| Binary Tree Inorder | Inorder | Amazon |
| Validate BST | Inorder | Meta |
| Serialize Tree | Preorder | Google |
| Max Depth | Postorder/Level | Amazon |
| Level Order Traversal | Level | Meta |
| Zigzag Level Order | Level | Amazon |
