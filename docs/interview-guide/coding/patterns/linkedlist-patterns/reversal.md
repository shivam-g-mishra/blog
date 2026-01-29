---
sidebar_position: 2
title: "Linked List Reversal — The Core Pattern"
description: >-
  Master linked list reversal for coding interviews. Full reversal,
  partial reversal, k-group reversal with code in 7 languages.
keywords:
  - linked list reversal
  - reverse linked list
  - k group reversal
  - swap pairs
  - iterative recursive

og_title: "Linked List Reversal — The Core Pattern"
og_description: "Reversal is fundamental to many linked list problems. Master iterative and recursive approaches with full code examples."
og_image: "/img/social-card.svg"

date_published: 2026-01-28
date_modified: 2026-01-28
author: shivam
reading_time: 30
content_type: explanation
---

import { LanguageSelector, TimeEstimate, ConfidenceBuilder, DifficultyBadge } from '@site/src/components/interview-guide';
import { CodeTabs } from '@site/src/components/design-patterns/CodeTabs';
import TabItem from '@theme/TabItem';

# Linked List Reversal: The Core Pattern

Reversal is fundamental to many linked list problems. Master both iterative and recursive approaches—interviewers often ask for both.

<LanguageSelector />

<TimeEstimate
  learnTime="25-30 minutes"
  practiceTime="3-4 hours"
  masteryTime="6-8 problems"
  interviewFrequency="25%"
  difficultyRange="Easy to Hard"
  prerequisites="Linked Lists"
/>

---

## Visualization

```
Initial:  1 → 2 → 3 → 4 → None
          ↑   ↑   ↑   ↑
          prev curr next (moving)

Step 1:   None ← 1   2 → 3 → 4
               prev curr

Step 2:   None ← 1 ← 2   3 → 4
                    prev curr

Step 3:   None ← 1 ← 2 ← 3   4
                         prev curr

Step 4:   None ← 1 ← 2 ← 3 ← 4
                              prev

Result:   4 → 3 → 2 → 1 → None
```

---

## Basic Reversal (Iterative)

<CodeTabs>
<TabItem value="python" label="Python">

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_list(head: ListNode | None) -> ListNode | None:
    """
    Reverse a linked list iteratively.
    Time: O(n), Space: O(1)
    
    Key: Use three pointers - prev, current, next
    At each step: save next, reverse link, advance all pointers
    """
    prev = None
    current = head
    
    while current:
        next_node = current.next  # Save next
        current.next = prev       # Reverse link
        prev = current            # Advance prev
        current = next_node       # Advance current
    
    return prev  # New head
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
class ListNode {
  val: number;
  next: ListNode | null;
  constructor(val = 0, next: ListNode | null = null) {
    this.val = val;
    this.next = next;
  }
}

function reverseList(head: ListNode | null): ListNode | null {
  let prev: ListNode | null = null;
  let current = head;

  while (current) {
    const nextNode = current.next;
    current.next = prev;
    prev = current;
    current = nextNode;
  }

  return prev;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
type ListNode struct {
    Val  int
    Next *ListNode
}

func reverseList(head *ListNode) *ListNode {
    var prev *ListNode = nil
    current := head
    
    for current != nil {
        nextNode := current.Next
        current.Next = prev
        prev = current
        current = nextNode
    }
    
    return prev
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public ListNode reverseList(ListNode head) {
    ListNode prev = null;
    ListNode current = head;
    
    while (current != null) {
        ListNode nextNode = current.next;
        current.next = prev;
        prev = current;
        current = nextNode;
    }
    
    return prev;
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
ListNode* reverseList(ListNode* head) {
    ListNode* prev = nullptr;
    ListNode* current = head;
    
    while (current) {
        ListNode* nextNode = current->next;
        current->next = prev;
        prev = current;
        current = nextNode;
    }
    
    return prev;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public ListNode ReverseList(ListNode head) {
    ListNode prev = null;
    ListNode current = head;
    
    while (current != null) {
        ListNode nextNode = current.next;
        current.next = prev;
        prev = current;
        current = nextNode;
    }
    
    return prev;
}
```

</TabItem>
</CodeTabs>

---

## Basic Reversal (Recursive)

<CodeTabs>
<TabItem value="python" label="Python">

```python
def reverse_list_recursive(head: ListNode | None) -> ListNode | None:
    """
    Reverse a linked list recursively.
    Time: O(n), Space: O(n) - call stack
    
    Base case: empty or single node → return as is
    Recursive: reverse rest, then fix pointers
    """
    # Base case
    if not head or not head.next:
        return head
    
    # Reverse the rest of the list
    new_head = reverse_list_recursive(head.next)
    
    # Fix pointers
    # head.next is now the LAST node of reversed sublist
    head.next.next = head  # Make it point back to head
    head.next = None       # Head is now last, points to None
    
    return new_head


# Trace for [1, 2, 3]:
# reverse(1) → reverse(2) → reverse(3) returns 3
# reverse(2): new_head=3, 2.next(3).next = 2, 2.next = None
#             List: 3 → 2 → None
# reverse(1): new_head=3, 1.next(2).next = 1, 1.next = None
#             List: 3 → 2 → 1 → None
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function reverseListRecursive(head: ListNode | null): ListNode | null {
  if (!head || !head.next) return head;

  const newHead = reverseListRecursive(head.next);

  head.next.next = head;
  head.next = null;

  return newHead;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func reverseListRecursive(head *ListNode) *ListNode {
    if head == nil || head.Next == nil {
        return head
    }
    
    newHead := reverseListRecursive(head.Next)
    
    head.Next.Next = head
    head.Next = nil
    
    return newHead
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public ListNode reverseListRecursive(ListNode head) {
    if (head == null || head.next == null) return head;
    
    ListNode newHead = reverseListRecursive(head.next);
    
    head.next.next = head;
    head.next = null;
    
    return newHead;
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
ListNode* reverseListRecursive(ListNode* head) {
    if (!head || !head->next) return head;
    
    ListNode* newHead = reverseListRecursive(head->next);
    
    head->next->next = head;
    head->next = nullptr;
    
    return newHead;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public ListNode ReverseListRecursive(ListNode head) {
    if (head == null || head.next == null) return head;
    
    ListNode newHead = ReverseListRecursive(head.next);
    
    head.next.next = head;
    head.next = null;
    
    return newHead;
}
```

</TabItem>
</CodeTabs>

---

## Reverse Between Positions

Reverse only nodes from position `left` to `right` (1-indexed).

<CodeTabs>
<TabItem value="python" label="Python">

```python
def reverse_between(head: ListNode | None, left: int, right: int) -> ListNode | None:
    """
    Reverse nodes between positions left and right (1-indexed).
    Example: 1→2→3→4→5, left=2, right=4 → 1→4→3→2→5
    
    Time: O(n), Space: O(1)
    """
    if not head or left == right:
        return head
    
    # Use dummy node to handle edge case where left=1
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    
    # Move prev to node BEFORE left position
    for _ in range(left - 1):
        prev = prev.next
    
    # current is at position left (first node to reverse)
    current = prev.next
    
    # Reverse nodes from left to right
    # We do (right - left) reversals
    for _ in range(right - left):
        # Remove next_node from its position
        next_node = current.next
        current.next = next_node.next
        
        # Insert next_node right after prev
        next_node.next = prev.next
        prev.next = next_node
    
    return dummy.next


# Visualization for 1→2→3→4→5, left=2, right=4:
# prev=1, current=2
#
# Iteration 1: Move 3 after 1
# 1→3→2→4→5 (3 inserted after prev)
#
# Iteration 2: Move 4 after 1
# 1→4→3→2→5 (4 inserted after prev)
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function reverseBetween(head: ListNode | null, left: number, right: number): ListNode | null {
  if (!head || left === right) return head;

  const dummy = new ListNode(0, head);
  let prev: ListNode = dummy;

  for (let i = 0; i < left - 1; i++) {
    prev = prev.next!;
  }

  let current = prev.next!;

  for (let i = 0; i < right - left; i++) {
    const nextNode = current.next!;
    current.next = nextNode.next;
    nextNode.next = prev.next;
    prev.next = nextNode;
  }

  return dummy.next;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func reverseBetween(head *ListNode, left int, right int) *ListNode {
    if head == nil || left == right {
        return head
    }
    
    dummy := &ListNode{Next: head}
    prev := dummy
    
    for i := 0; i < left-1; i++ {
        prev = prev.Next
    }
    
    current := prev.Next
    
    for i := 0; i < right-left; i++ {
        nextNode := current.Next
        current.Next = nextNode.Next
        nextNode.Next = prev.Next
        prev.Next = nextNode
    }
    
    return dummy.Next
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public ListNode reverseBetween(ListNode head, int left, int right) {
    if (head == null || left == right) return head;
    
    ListNode dummy = new ListNode(0);
    dummy.next = head;
    ListNode prev = dummy;
    
    for (int i = 0; i < left - 1; i++) {
        prev = prev.next;
    }
    
    ListNode current = prev.next;
    
    for (int i = 0; i < right - left; i++) {
        ListNode nextNode = current.next;
        current.next = nextNode.next;
        nextNode.next = prev.next;
        prev.next = nextNode;
    }
    
    return dummy.next;
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
ListNode* reverseBetween(ListNode* head, int left, int right) {
    if (!head || left == right) return head;
    
    ListNode dummy(0);
    dummy.next = head;
    ListNode* prev = &dummy;
    
    for (int i = 0; i < left - 1; i++) {
        prev = prev->next;
    }
    
    ListNode* current = prev->next;
    
    for (int i = 0; i < right - left; i++) {
        ListNode* nextNode = current->next;
        current->next = nextNode->next;
        nextNode->next = prev->next;
        prev->next = nextNode;
    }
    
    return dummy.next;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public ListNode ReverseBetween(ListNode head, int left, int right) {
    if (head == null || left == right) return head;
    
    ListNode dummy = new ListNode(0) { next = head };
    ListNode prev = dummy;
    
    for (int i = 0; i < left - 1; i++) {
        prev = prev.next;
    }
    
    ListNode current = prev.next;
    
    for (int i = 0; i < right - left; i++) {
        ListNode nextNode = current.next;
        current.next = nextNode.next;
        nextNode.next = prev.next;
        prev.next = nextNode;
    }
    
    return dummy.next;
}
```

</TabItem>
</CodeTabs>

---

## Reverse Nodes in K-Groups

<CodeTabs>
<TabItem value="python" label="Python">

```python
def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    """
    Reverse list in groups of k nodes.
    If remaining nodes < k, leave them as is.
    
    Example: 1→2→3→4→5, k=2 → 2→1→4→3→5
    
    Time: O(n), Space: O(1) iterative / O(n/k) recursive
    """
    # First check if we have k nodes
    count = 0
    current = head
    while current and count < k:
        current = current.next
        count += 1
    
    if count < k:
        return head  # Not enough nodes, return as is
    
    # Reverse k nodes
    prev = None
    current = head
    for _ in range(k):
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    
    # head is now the tail of this reversed group
    # Connect it to the result of reversing the rest
    head.next = reverse_k_group(current, k)
    
    return prev  # New head of this group
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function reverseKGroup(head: ListNode | null, k: number): ListNode | null {
  // Count k nodes
  let count = 0;
  let current = head;
  while (current && count < k) {
    current = current.next;
    count++;
  }

  if (count < k) return head;

  // Reverse k nodes
  let prev: ListNode | null = null;
  current = head;
  for (let i = 0; i < k; i++) {
    const nextNode = current!.next;
    current!.next = prev;
    prev = current;
    current = nextNode;
  }

  // Connect to reversed rest
  head!.next = reverseKGroup(current, k);

  return prev;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func reverseKGroup(head *ListNode, k int) *ListNode {
    // Count k nodes
    count := 0
    current := head
    for current != nil && count < k {
        current = current.Next
        count++
    }
    
    if count < k {
        return head
    }
    
    // Reverse k nodes
    var prev *ListNode = nil
    current = head
    for i := 0; i < k; i++ {
        nextNode := current.Next
        current.Next = prev
        prev = current
        current = nextNode
    }
    
    // Connect to reversed rest
    head.Next = reverseKGroup(current, k)
    
    return prev
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public ListNode reverseKGroup(ListNode head, int k) {
    // Count k nodes
    int count = 0;
    ListNode current = head;
    while (current != null && count < k) {
        current = current.next;
        count++;
    }
    
    if (count < k) return head;
    
    // Reverse k nodes
    ListNode prev = null;
    current = head;
    for (int i = 0; i < k; i++) {
        ListNode nextNode = current.next;
        current.next = prev;
        prev = current;
        current = nextNode;
    }
    
    // Connect to reversed rest
    head.next = reverseKGroup(current, k);
    
    return prev;
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
ListNode* reverseKGroup(ListNode* head, int k) {
    // Count k nodes
    int count = 0;
    ListNode* current = head;
    while (current && count < k) {
        current = current->next;
        count++;
    }
    
    if (count < k) return head;
    
    // Reverse k nodes
    ListNode* prev = nullptr;
    current = head;
    for (int i = 0; i < k; i++) {
        ListNode* nextNode = current->next;
        current->next = prev;
        prev = current;
        current = nextNode;
    }
    
    // Connect to reversed rest
    head->next = reverseKGroup(current, k);
    
    return prev;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public ListNode ReverseKGroup(ListNode head, int k) {
    // Count k nodes
    int count = 0;
    ListNode current = head;
    while (current != null && count < k) {
        current = current.next;
        count++;
    }
    
    if (count < k) return head;
    
    // Reverse k nodes
    ListNode prev = null;
    current = head;
    for (int i = 0; i < k; i++) {
        ListNode nextNode = current.next;
        current.next = prev;
        prev = current;
        current = nextNode;
    }
    
    // Connect to reversed rest
    head.next = ReverseKGroup(current, k);
    
    return prev;
}
```

</TabItem>
</CodeTabs>

---

## 🎯 Pattern Triggers

| Problem Clue | Approach |
|--------------|----------|
| "Reverse linked list" | Basic iterative/recursive |
| "Reverse between positions" | Dummy node + insertion technique |
| "Reverse in k-groups" | Count + reverse + recurse |
| "Swap pairs" | K-group with k=2 |
| "Palindrome list" | Find middle + reverse second half |

---

## 💬 How to Communicate

**Explaining iterative reversal:**
> "I'll use three pointers: prev, current, and next. At each step, I save the next node, reverse the current link to point to prev, then advance all pointers. When current becomes null, prev is the new head..."

**Explaining the dummy node:**
> "I use a dummy node before the head to simplify edge cases. This way, even if I need to reverse starting from position 1, I always have a 'prev' node to work with..."

---

## 🏋️ Practice Problems

| Problem | Difficulty | Variant |
|---------|------------|---------|
| [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | <DifficultyBadge level="easy" /> | Basic |
| [Reverse Linked List II](https://leetcode.com/problems/reverse-linked-list-ii/) | <DifficultyBadge level="medium" /> | Between positions |
| [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) | <DifficultyBadge level="hard" /> | K-group |
| [Swap Nodes in Pairs](https://leetcode.com/problems/swap-nodes-in-pairs/) | <DifficultyBadge level="medium" /> | K=2 |
| [Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/) | <DifficultyBadge level="easy" /> | With reversal |

---

## Key Takeaways

1. **Three pointers:** prev, current, next for iterative reversal.

2. **Dummy node** simplifies edge cases (reversing from position 1).

3. **K-group reversal:** Check count → reverse → recurse.

4. **Draw it out!** Reversal is error-prone; visualize pointer changes.

5. **Know both** iterative (O(1) space) and recursive (cleaner code).

<ConfidenceBuilder type="youve-got-this">

**Reversal is about redirecting pointers.**

Save the next node, flip the current link, advance. That's the entire pattern. Everything else is variations on when and where to apply it.

</ConfidenceBuilder>

---

## What's Next?

More linked list patterns:

**See also:** [Fast & Slow Pointers](/docs/interview-guide/coding/patterns/linkedlist-patterns/fast-slow) — Cycle Detection and Middle Finding
