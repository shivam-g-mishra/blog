---
sidebar_position: 2
title: "Linked Lists — Pointers, Patterns & Problems"
description: >-
  Master linked lists for coding interviews. Learn pointer manipulation, 
  fast-slow technique, reversal patterns, and solve classic problems.
keywords:
  - linked list interview
  - singly linked list
  - doubly linked list
  - fast slow pointers
  - reverse linked list
difficulty: Intermediate
estimated_time: 40 minutes
prerequisites:
  - Big-O Notation
  - Arrays & Strings
companies: [Google, Meta, Amazon, Microsoft, Apple]
---

# Linked Lists: Master Pointer Manipulation

In my first Amazon interview, I was asked to reverse a linked list. I'd done it a hundred times on LeetCode. But when I tried to write it on the whiteboard, my mind went blank.

The problem wasn't that I hadn't practiced. It was that I'd memorized code instead of understanding the pointer dance.

**Linked list problems aren't about data structures—they're about pointer manipulation.** Once you understand how pointers move, every linked list problem becomes manageable.

---

## Why Linked Lists Matter in Interviews

Interviewers love linked lists because they test:

1. **Pointer manipulation** — Can you track multiple references?
2. **Edge case handling** — Empty list, single node, cycles
3. **In-place algorithms** — O(1) space constraints
4. **Visualization** — Can you draw what's happening?

**The key insight: Linked list problems are really pointer puzzles.**

---

## Linked List Fundamentals

### Node Structure

```python
# Singly Linked List
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Doubly Linked List
class DoublyListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next
```

### Arrays vs Linked Lists

| Operation | Array | Linked List |
|-----------|-------|-------------|
| Access by index | O(1) | O(n) |
| Insert at beginning | O(n) | O(1) |
| Insert at end | O(1) amortized | O(1) with tail pointer |
| Insert in middle | O(n) | O(1) after finding position |
| Delete | O(n) | O(1) after finding position |
| Memory | Contiguous | Scattered |

**When to use linked lists:**
- Frequent insertions/deletions at beginning
- Don't need random access
- Don't know size in advance
- Need to implement stacks, queues, LRU cache

---

## The Three Essential Patterns

### Pattern 1: Fast and Slow Pointers

**Use when:** Finding middle, detecting cycles, finding nth from end

```python
# Find middle of linked list
def find_middle(head):
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next        # Move 1 step
        fast = fast.next.next   # Move 2 steps
    
    return slow  # slow is at middle when fast reaches end
```

**Why it works:** When fast pointer reaches the end (traveling 2x speed), slow pointer is at the middle.

```python
# Detect cycle
def has_cycle(head):
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:  # They meet = cycle exists
            return True
    
    return False

# Find cycle start (Floyd's algorithm)
def detect_cycle_start(head):
    slow = fast = head
    
    # Phase 1: Detect cycle
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle
    
    # Phase 2: Find start
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow  # Start of cycle
```

### Pattern 2: In-Place Reversal

**Use when:** Reversing entire list or portions

```python
# Reverse entire list
def reverse_list(head):
    prev = None
    curr = head
    
    while curr:
        next_temp = curr.next  # Save next
        curr.next = prev       # Reverse pointer
        prev = curr            # Move prev forward
        curr = next_temp       # Move curr forward
    
    return prev  # New head

# Visualizing the reversal:
# 1 -> 2 -> 3 -> None
# 
# Step 1: prev=None, curr=1
#         1 -> None, prev=1, curr=2
# 
# Step 2: prev=1, curr=2
#         2 -> 1 -> None, prev=2, curr=3
# 
# Step 3: prev=2, curr=3
#         3 -> 2 -> 1 -> None, prev=3, curr=None
# 
# Return prev (3)
```

```python
# Reverse between positions m and n
def reverse_between(head, m, n):
    if not head or m == n:
        return head
    
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    
    # Move to position before m
    for _ in range(m - 1):
        prev = prev.next
    
    # Reverse from m to n
    curr = prev.next
    for _ in range(n - m):
        next_node = curr.next
        curr.next = next_node.next
        next_node.next = prev.next
        prev.next = next_node
    
    return dummy.next
```

### Pattern 3: Dummy Head

**Use when:** The head might change, or handling edge cases

```python
# Merge two sorted lists
def merge_two_lists(l1, l2):
    dummy = ListNode(0)  # Dummy head simplifies logic
    curr = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    
    curr.next = l1 or l2  # Attach remaining
    
    return dummy.next  # Skip dummy
```

**Why use dummy head:**
- No special case for empty list
- No special case for inserting at head
- Cleaner code, fewer edge cases

---

## Classic Interview Problems

### Problem 1: Remove Nth Node From End

```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0)
    dummy.next = head
    
    # Use two pointers n nodes apart
    first = dummy
    second = dummy
    
    # Advance first by n+1 steps
    for _ in range(n + 1):
        first = first.next
    
    # Move both until first reaches end
    while first:
        first = first.next
        second = second.next
    
    # second is now at node before the one to remove
    second.next = second.next.next
    
    return dummy.next
```

### Problem 2: Palindrome Linked List

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
    second_half = reverse_list(slow.next)
    
    # Compare halves
    first_half = head
    while second_half:
        if first_half.val != second_half.val:
            return False
        first_half = first_half.next
        second_half = second_half.next
    
    return True
```

### Problem 3: Add Two Numbers

```python
def add_two_numbers(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    carry = 0
    
    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        
        total = val1 + val2 + carry
        carry = total // 10
        curr.next = ListNode(total % 10)
        curr = curr.next
        
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    
    return dummy.next
```

### Problem 4: Reorder List

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
    second = reverse_list(slow.next)
    slow.next = None  # Cut the list
    
    # Merge alternating
    first = head
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2
```

### Problem 5: Copy List with Random Pointer

```python
def copy_random_list(head):
    if not head:
        return None
    
    # Step 1: Create interleaved copies
    curr = head
    while curr:
        copy = Node(curr.val)
        copy.next = curr.next
        curr.next = copy
        curr = copy.next
    
    # Step 2: Set random pointers
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next
        curr = curr.next.next
    
    # Step 3: Separate lists
    dummy = Node(0)
    copy_curr = dummy
    curr = head
    
    while curr:
        copy_curr.next = curr.next
        curr.next = curr.next.next
        copy_curr = copy_curr.next
        curr = curr.next
    
    return dummy.next
```

---

## Common Mistakes

### 1. Losing Reference to Nodes

```python
# Wrong - loses the list
curr.next = curr.next.next  # Lost the node in between!

# Right - save reference first
temp = curr.next
curr.next = curr.next.next
# temp still available if needed
```

### 2. Forgetting Null Checks

```python
# Wrong - crashes on empty list
def get_second(head):
    return head.next.val  # NullPointerException if head is None!

# Right
def get_second(head):
    if not head or not head.next:
        return None
    return head.next.val
```

### 3. Infinite Loops with Cycles

```python
# Wrong - infinite loop if cycle exists
while curr:
    curr = curr.next  # Never ends!

# Right - use fast-slow to detect cycle first
```

---

## Edge Cases Checklist

Always test:
- [ ] Empty list (`head = None`)
- [ ] Single node
- [ ] Two nodes
- [ ] Odd vs even length
- [ ] Cycle present
- [ ] Operation at head
- [ ] Operation at tail

---

## Practice Problems

### Easy

| Problem | Pattern | Company |
|---------|---------|---------|
| Reverse Linked List | Reversal | Google, Amazon |
| Merge Two Sorted Lists | Dummy Head | Meta, Microsoft |
| Linked List Cycle | Fast-Slow | Amazon, Apple |
| Remove Duplicates | Two Pointers | Google |
| Middle of Linked List | Fast-Slow | Amazon |

### Medium

| Problem | Pattern | Company |
|---------|---------|---------|
| Add Two Numbers | Dummy Head | Amazon, Meta |
| Remove Nth From End | Two Pointers | Meta, Google |
| Reorder List | Multiple Patterns | Amazon |
| Sort List | Merge Sort | Microsoft |
| Palindrome Linked List | Fast-Slow + Reverse | Meta |

### Hard

| Problem | Pattern | Company |
|---------|---------|---------|
| Merge k Sorted Lists | Heap + Merge | Google, Amazon |
| Reverse Nodes in k-Group | Complex Reversal | Meta |
| Copy List with Random | Hash Map / Interleave | Amazon |

---

## Interview Tips

1. **Draw it out** — Always sketch the list and show pointer movements.

2. **Use a dummy head** — Simplifies edge cases for head operations.

3. **Save references before modifying** — Don't lose nodes.

4. **Check null before accessing** — `curr and curr.next` before `curr.next.val`.

5. **Consider fast-slow first** — It solves middle, cycle, and nth-from-end.

---

## Key Takeaways

1. **Three patterns cover 90% of problems:** Fast-slow, reversal, dummy head.

2. **Think in terms of pointers,** not data. Visualize the connections.

3. **Dummy head eliminates edge cases** for operations that might change the head.

4. **Fast-slow is magical** — middle, cycle detection, nth from end.

5. **Always handle null** — empty list, single node, etc.

---

## What's Next?

Stacks and queues are often implemented with linked lists and appear in many interview problems:

👉 [Stacks & Queues →](./stacks-queues)
