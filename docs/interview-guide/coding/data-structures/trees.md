---
sidebar_position: 5
title: "Trees — Binary Trees, BSTs & Traversals"
description: >-
  Master tree data structures for coding interviews. Learn traversals, BST
  operations, recursive patterns, and solve classic tree problems.
keywords:
  - binary tree interview
  - BST interview questions
  - tree traversal
  - inorder preorder postorder
  - tree recursion
difficulty: Intermediate
estimated_time: 50 minutes
prerequisites:
  - Big-O Notation
  - Stacks & Queues
  - Recursion basics
companies: [Google, Meta, Amazon, Microsoft, Apple]
---

# Trees: The Heart of Technical Interviews

Trees appear in roughly 25% of all coding interviews. They test recursion, pointer manipulation, and your ability to think hierarchically.

When I first encountered tree problems, I struggled with the recursive nature. The breakthrough came when I stopped trying to trace through every recursive call and instead trusted the pattern: **solve for the current node, let recursion handle the rest.**

**Trees are where recursion finally makes sense.**

---

## Tree Fundamentals

### Basic Terminology

```
        1          ← Root (level 0)
       / \
      2   3        ← Level 1
     / \   \
    4   5   6      ← Level 2 (leaves)
```

- **Root:** Top node (no parent)
- **Leaf:** Node with no children
- **Height:** Longest path from root to leaf
- **Depth:** Distance from root to node
- **Binary tree:** Each node has at most 2 children

### Node Structure

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Tree Types

| Type | Property |
|------|----------|
| **Binary Tree** | Max 2 children per node |
| **Binary Search Tree** | Left < Node < Right |
| **Balanced Tree** | Height is O(log n) |
| **Complete Tree** | All levels full except last |
| **Full Tree** | Every node has 0 or 2 children |
| **Perfect Tree** | All leaves at same level |

---

## The Four Traversals

This is the foundation of all tree problems.

### 1. Inorder (Left → Node → Right)

```python
# Recursive
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

# Iterative
def inorder_iterative(root):
    result = []
    stack = []
    curr = root
    
    while curr or stack:
        # Go left as far as possible
        while curr:
            stack.append(curr)
            curr = curr.left
        
        # Process node
        curr = stack.pop()
        result.append(curr.val)
        
        # Go right
        curr = curr.right
    
    return result
```

**Key insight:** Inorder on BST gives sorted order.

### 2. Preorder (Node → Left → Right)

```python
# Recursive
def preorder(root):
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)

# Iterative
def preorder_iterative(root):
    if not root:
        return []
    
    result = []
    stack = [root]
    
    while stack:
        node = stack.pop()
        result.append(node.val)
        
        # Push right first so left is processed first
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return result
```

**Key insight:** Preorder is useful for serialization and copying trees.

### 3. Postorder (Left → Right → Node)

```python
# Recursive
def postorder(root):
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]

# Iterative (tricky - use two stacks or reverse preorder)
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
    
    return result[::-1]  # Reverse
```

**Key insight:** Postorder processes children before parent—useful for deletion.

### 4. Level Order (BFS)

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
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

**Key insight:** Level order uses queue (BFS), others use stack (DFS).

---

## The Recursive Pattern

Most tree problems follow this template:

```python
def solve(root):
    # Base case
    if not root:
        return base_value
    
    # Recursive case
    left_result = solve(root.left)
    right_result = solve(root.right)
    
    # Combine results
    return combine(root.val, left_result, right_result)
```

### Example: Maximum Depth

```python
def max_depth(root):
    if not root:
        return 0
    
    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)
    
    return 1 + max(left_depth, right_depth)
```

### Example: Same Tree

```python
def is_same_tree(p, q):
    if not p and not q:
        return True
    if not p or not q:
        return False
    
    return (p.val == q.val and 
            is_same_tree(p.left, q.left) and 
            is_same_tree(p.right, q.right))
```

---

## Binary Search Tree (BST) Operations

### Search: O(log n) average

```python
def search_bst(root, val):
    if not root:
        return None
    
    if val == root.val:
        return root
    elif val < root.val:
        return search_bst(root.left, val)
    else:
        return search_bst(root.right, val)
```

### Insert: O(log n) average

```python
def insert_bst(root, val):
    if not root:
        return TreeNode(val)
    
    if val < root.val:
        root.left = insert_bst(root.left, val)
    else:
        root.right = insert_bst(root.right, val)
    
    return root
```

### Delete: O(log n) average

```python
def delete_bst(root, key):
    if not root:
        return None
    
    if key < root.val:
        root.left = delete_bst(root.left, key)
    elif key > root.val:
        root.right = delete_bst(root.right, key)
    else:
        # Node to delete found
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        
        # Two children: replace with inorder successor
        successor = root.right
        while successor.left:
            successor = successor.left
        
        root.val = successor.val
        root.right = delete_bst(root.right, successor.val)
    
    return root
```

### Validate BST

```python
def is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):
    if not root:
        return True
    
    if root.val <= min_val or root.val >= max_val:
        return False
    
    return (is_valid_bst(root.left, min_val, root.val) and
            is_valid_bst(root.right, root.val, max_val))
```

---

## Classic Interview Problems

### Problem 1: Lowest Common Ancestor

```python
# For BST
def lca_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root

# For Binary Tree
def lca_bt(root, p, q):
    if not root or root == p or root == q:
        return root
    
    left = lca_bt(root.left, p, q)
    right = lca_bt(root.right, p, q)
    
    if left and right:
        return root
    return left or right
```

### Problem 2: Path Sum

```python
def has_path_sum(root, target):
    if not root:
        return False
    
    if not root.left and not root.right:
        return root.val == target
    
    remaining = target - root.val
    return (has_path_sum(root.left, remaining) or 
            has_path_sum(root.right, remaining))
```

### Problem 3: Invert Binary Tree

```python
def invert_tree(root):
    if not root:
        return None
    
    # Swap children
    root.left, root.right = root.right, root.left
    
    # Recurse
    invert_tree(root.left)
    invert_tree(root.right)
    
    return root
```

### Problem 4: Serialize and Deserialize

```python
class Codec:
    def serialize(self, root):
        if not root:
            return "null"
        
        return f"{root.val},{self.serialize(root.left)},{self.serialize(root.right)}"
    
    def deserialize(self, data):
        def helper(nodes):
            val = next(nodes)
            if val == "null":
                return None
            
            node = TreeNode(int(val))
            node.left = helper(nodes)
            node.right = helper(nodes)
            return node
        
        return helper(iter(data.split(",")))
```

### Problem 5: Diameter of Binary Tree

```python
def diameter_of_binary_tree(root):
    diameter = 0
    
    def depth(node):
        nonlocal diameter
        if not node:
            return 0
        
        left_depth = depth(node.left)
        right_depth = depth(node.right)
        
        # Diameter through this node
        diameter = max(diameter, left_depth + right_depth)
        
        return 1 + max(left_depth, right_depth)
    
    depth(root)
    return diameter
```

---

## Common Patterns Summary

| Pattern | When to Use | Template |
|---------|-------------|----------|
| **Recursive DFS** | Most tree problems | `solve(root.left) + solve(root.right)` |
| **Level order BFS** | Level-by-level processing | Queue with level size |
| **Path tracking** | Find paths, path sum | Pass state down recursively |
| **BST property** | Sorted operations | Go left if smaller, right if larger |
| **Boundary conditions** | Validate BST | Pass min/max bounds |

---

## Practice Problems

### Easy

| Problem | Pattern | Company |
|---------|---------|---------|
| Maximum Depth | Recursive | Google, Amazon |
| Same Tree | Recursive | Meta |
| Invert Binary Tree | Recursive | Google |
| Path Sum | DFS | Amazon |
| Symmetric Tree | Recursive/BFS | Meta |

### Medium

| Problem | Pattern | Company |
|---------|---------|---------|
| Validate BST | Boundary | Amazon |
| Lowest Common Ancestor | Recursive | Meta, Google |
| Binary Tree Level Order | BFS | Amazon |
| Construct from Preorder/Inorder | Recursive | Google |
| Kth Smallest in BST | Inorder | Amazon |

### Hard

| Problem | Pattern | Company |
|---------|---------|---------|
| Serialize/Deserialize | Preorder | Meta, Google |
| Binary Tree Max Path Sum | DFS | Meta |
| Recover BST | Inorder | Amazon |

---

## Interview Tips

1. **Trust the recursion.** Solve for current node, let recursion handle subtrees.

2. **Draw the tree.** Visualize before coding.

3. **Know all four traversals** and when to use each.

4. **BST = sorted order.** Use inorder to get sorted elements.

5. **Consider iterative** when asked—shows depth of knowledge.

---

## Key Takeaways

1. **Four traversals:** Inorder, Preorder, Postorder, Level order. Know them cold.

2. **Recursive pattern:** Base case → recurse left/right → combine results.

3. **BST property:** Left subtree < node < right subtree. Use for efficient search.

4. **DFS uses stack, BFS uses queue.** Choose based on problem requirements.

5. **Inorder on BST = sorted order.** This unlocks many problems.

---

## What's Next?

Graphs generalize trees—multiple paths, cycles, and more complex relationships:

👉 [Graphs →](./graphs)
