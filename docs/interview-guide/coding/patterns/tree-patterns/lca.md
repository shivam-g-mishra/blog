---
sidebar_position: 2
title: "Lowest Common Ancestor (LCA)"
description: >-
  Master LCA problems for coding interviews. Binary tree LCA, BST LCA,
  and with parent pointers.
keywords:
  - lowest common ancestor
  - LCA
  - binary tree
  - BST
  - tree problems
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - Tree Traversal
companies: [Google, Meta, Amazon, Microsoft]
---

# Lowest Common Ancestor: Find the Meeting Point

LCA is the deepest node that is an ancestor of both given nodes.

---

## Binary Tree LCA

```python
def lca_binary_tree(root, p, q):
    if not root or root == p or root == q:
        return root
    
    left = lca_binary_tree(root.left, p, q)
    right = lca_binary_tree(root.right, p, q)
    
    if left and right:
        return root  # p and q on different sides
    
    return left or right
```

---

## BST LCA (Optimized)

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

## With Parent Pointers

```python
def lca_with_parent(p, q):
    ancestors = set()
    
    while p:
        ancestors.add(p)
        p = p.parent
    
    while q:
        if q in ancestors:
            return q
        q = q.parent
    
    return None
```

---

## Practice Problems

| Problem | Variation | Company |
|---------|-----------|---------|
| LCA of Binary Tree | Standard | Meta |
| LCA of BST | BST optimized | Amazon |
| LCA III | May not exist | Google |
| LCA with Parent | Two pointers | Meta |
