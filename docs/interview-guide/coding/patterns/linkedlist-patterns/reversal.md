---
sidebar_position: 2
title: "Linked List Reversal Pattern"
description: >-
  Master linked list reversal for coding interviews. Full reversal,
  partial reversal, k-group reversal, and variations.
keywords:
  - linked list reversal
  - reverse linked list
  - k group reversal
  - iterative recursive
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - Linked Lists
companies: [Google, Amazon, Meta, Microsoft]
---

# Linked List Reversal: The Core Pattern

Reversal is fundamental to many linked list problems. Master iterative and recursive approaches.

---

## Basic Reversal (Iterative)

```python
def reverse_list(head):
    prev = None
    current = head
    
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    
    return prev
```

### Visualization

```
Initial: 1 → 2 → 3 → 4 → None

Step 1: prev=None, curr=1
        None ← 1   2 → 3 → 4
        
Step 2: prev=1, curr=2
        None ← 1 ← 2   3 → 4
        
Step 3: prev=2, curr=3
        None ← 1 ← 2 ← 3   4
        
Step 4: prev=3, curr=4
        None ← 1 ← 2 ← 3 ← 4

Result: 4 → 3 → 2 → 1 → None
```

---

## Basic Reversal (Recursive)

```python
def reverse_list_recursive(head):
    if not head or not head.next:
        return head
    
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    
    return new_head
```

---

## Reverse Between Positions

Reverse nodes from position left to right.

```python
def reverse_between(head, left, right):
    if not head or left == right:
        return head
    
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    
    # Move prev to node before left
    for _ in range(left - 1):
        prev = prev.next
    
    # Start reversal
    current = prev.next
    
    for _ in range(right - left):
        next_node = current.next
        current.next = next_node.next
        next_node.next = prev.next
        prev.next = next_node
    
    return dummy.next
```

### Visualization

```
Reverse 2 to 4 in: 1 → 2 → 3 → 4 → 5

prev = 1, current = 2

Iteration 1: Move 3 after 1
1 → 3 → 2 → 4 → 5

Iteration 2: Move 4 after 1
1 → 4 → 3 → 2 → 5

Result: 1 → 4 → 3 → 2 → 5
```

---

## Reverse in K-Groups

```python
def reverse_k_group(head, k):
    # Check if we have k nodes
    count = 0
    current = head
    while current and count < k:
        current = current.next
        count += 1
    
    if count < k:
        return head  # Not enough nodes
    
    # Reverse k nodes
    prev = None
    current = head
    for _ in range(k):
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    
    # Recursively reverse rest
    head.next = reverse_k_group(current, k)
    
    return prev
```

---

## Swap Nodes in Pairs

```python
def swap_pairs(head):
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    
    while prev.next and prev.next.next:
        first = prev.next
        second = prev.next.next
        
        # Swap
        first.next = second.next
        second.next = first
        prev.next = second
        
        prev = first
    
    return dummy.next
```

---

## Reverse Alternating K Nodes

```python
def reverse_alternating_k(head, k):
    current = head
    prev = None
    is_reverse = True
    
    while current:
        if is_reverse:
            # Reverse k nodes
            tail = current
            prev_section = prev
            
            count = 0
            while current and count < k:
                next_node = current.next
                current.next = prev
                prev = current
                current = next_node
                count += 1
            
            if prev_section:
                prev_section.next = prev
            else:
                head = prev
            tail.next = current
            prev = tail
        else:
            # Skip k nodes
            count = 0
            while current and count < k:
                prev = current
                current = current.next
                count += 1
        
        is_reverse = not is_reverse
    
    return head
```

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Reverse Linked List | Easy | All |
| Reverse Linked List II | Medium | Amazon |
| Reverse Nodes in k-Group | Hard | Meta |
| Swap Nodes in Pairs | Medium | Google |
| Reverse Alternating K | Medium | Microsoft |

---

## Key Takeaways

1. **Three pointers:** prev, current, next for iterative reversal.
2. **Dummy node** simplifies edge cases.
3. **K-group reversal** = check count + reverse + recurse.
4. **Draw it out** before coding—reversal is error-prone.
