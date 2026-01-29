---
sidebar_position: 2
title: "BST Operations Pattern"
description: >-
  Master Binary Search Tree operations for coding interviews. Insert, delete,
  search, validate, and common BST problems.
keywords:
  - BST operations
  - binary search tree
  - BST insert delete
  - validate BST
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - Trees
  - Binary Search
companies: [Google, Amazon, Meta, Microsoft]
---

# BST Operations: The Ordered Tree

BST property: Left subtree < Node < Right subtree. This enables O(log n) operations.

---

## Core Operations

### Search

```python
def search_bst(root, val):
    if not root or root.val == val:
        return root
    
    if val < root.val:
        return search_bst(root.left, val)
    return search_bst(root.right, val)
```

### Insert

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

### Delete

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

---

## Validate BST

```python
def is_valid_bst(root):
    def validate(node, min_val, max_val):
        if not node:
            return True
        
        if node.val <= min_val or node.val >= max_val:
            return False
        
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))
```

---

## Find Kth Smallest

```python
def kth_smallest(root, k):
    stack = []
    current = root
    
    while stack or current:
        while current:
            stack.append(current)
            current = current.left
        
        current = stack.pop()
        k -= 1
        if k == 0:
            return current.val
        
        current = current.right
```

---

## Lowest Common Ancestor in BST

```python
def lca_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
```

---

## Inorder Successor

```python
def inorder_successor(root, p):
    successor = None
    
    while root:
        if p.val < root.val:
            successor = root
            root = root.left
        else:
            root = root.right
    
    return successor
```

---

## Convert Sorted Array to BST

```python
def sorted_array_to_bst(nums):
    def build(left, right):
        if left > right:
            return None
        
        mid = (left + right) // 2
        node = TreeNode(nums[mid])
        node.left = build(left, mid - 1)
        node.right = build(mid + 1, right)
        
        return node
    
    return build(0, len(nums) - 1)
```

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Validate BST | Medium | Amazon |
| Kth Smallest Element | Medium | Meta |
| LCA of BST | Medium | Google |
| Convert Sorted Array to BST | Easy | Microsoft |
| Inorder Successor | Medium | Amazon |
| Delete Node in BST | Medium | Google |

---

## Key Takeaways

1. **BST property** enables O(log n) search.
2. **Inorder traversal** gives sorted order.
3. **Delete with two children:** Replace with inorder successor.
4. **LCA in BST:** Use BST property (no need for parent pointers).
