---
sidebar_position: 1
title: "Fast & Slow Pointers Pattern"
description: >-
  Master the fast and slow pointer technique for linked list problems.
  Cycle detection, middle element, and more.
keywords:
  - fast slow pointers
  - tortoise hare
  - cycle detection
  - linked list middle
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - Linked Lists
companies: [Google, Amazon, Meta, Microsoft]
---

# Fast & Slow Pointers: The Tortoise and Hare

Two pointers moving at different speeds solve many linked list problems elegantly.

---

## The Pattern

```
Slow pointer: moves 1 step
Fast pointer: moves 2 steps

Key insight: 
- If there's a cycle, they will meet
- When fast reaches end, slow is at middle
```

---

## Detect Cycle

```python
def has_cycle(head):
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            return True
    
    return False
```

---

## Find Cycle Start

```python
def detect_cycle(head):
    slow = fast = head
    
    # Phase 1: Find meeting point
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            break
    else:
        return None  # No cycle
    
    # Phase 2: Find cycle start
    # Distance from head to cycle start = 
    # Distance from meeting point to cycle start
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow
```

**Why this works:**

```
Let:
- F = distance from head to cycle start
- C = cycle length
- X = distance from cycle start to meeting point

When they meet:
slow traveled: F + X
fast traveled: F + X + n*C (for some n >= 1)

Since fast travels 2x speed:
2(F + X) = F + X + n*C
F + X = n*C
F = n*C - X

This means: distance from head = distance from meeting point to cycle start
```

---

## Find Middle of List

```python
def find_middle(head):
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow  # Middle (or second middle if even length)

# For first middle in even length:
def find_first_middle(head):
    slow = fast = head
    
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow
```

---

## Check Palindrome

```python
def is_palindrome(head):
    if not head or not head.next:
        return True
    
    # Find middle
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    # Reverse second half
    second_half = reverse(slow.next)
    
    # Compare
    first_half = head
    while second_half:
        if first_half.val != second_half.val:
            return False
        first_half = first_half.next
        second_half = second_half.next
    
    return True

def reverse(head):
    prev = None
    while head:
        next_node = head.next
        head.next = prev
        prev = head
        head = next_node
    return prev
```

---

## Reorder List

Convert `1→2→3→4→5` to `1→5→2→4→3`.

```python
def reorder_list(head):
    if not head or not head.next:
        return
    
    # Find middle
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    # Reverse second half
    second = reverse(slow.next)
    slow.next = None  # Cut the list
    
    # Merge alternating
    first = head
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2
```

---

## Happy Number

Detect cycle in number transformation.

```python
def is_happy(n):
    def get_next(num):
        total = 0
        while num > 0:
            digit = num % 10
            total += digit * digit
            num //= 10
        return total
    
    slow = fast = n
    
    while True:
        slow = get_next(slow)
        fast = get_next(get_next(fast))
        
        if fast == 1:
            return True
        if slow == fast:
            return False
```

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Linked List Cycle | Easy | Amazon |
| Linked List Cycle II | Medium | Microsoft |
| Middle of Linked List | Easy | Meta |
| Palindrome Linked List | Easy | Meta |
| Reorder List | Medium | Amazon |
| Happy Number | Easy | Google |

---

## Key Takeaways

1. **Cycle detection:** Fast catches slow if cycle exists.
2. **Find middle:** When fast reaches end, slow is at middle.
3. **Cycle start:** Math proves the reset-and-walk trick works.
4. **Pattern applies beyond lists:** Any repeating function (Happy Number).
