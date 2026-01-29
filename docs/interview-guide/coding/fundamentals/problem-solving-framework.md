---
sidebar_position: 3
title: "Problem-Solving Framework for Coding Interviews"
description: >-
  A step-by-step framework (UMPIRE) for approaching any coding interview problem.
  Never freeze up or go blank in an interview again.
keywords:
  - coding interview framework
  - problem solving steps
  - UMPIRE method
  - technical interview approach
  - how to solve coding problems
difficulty: Beginner
estimated_time: 20 minutes
prerequisites:
  - Big-O Notation
  - Choosing Data Structures
companies: [All]
---

# The Problem-Solving Framework: Never Freeze Up Again

You know that feeling. The interviewer shares their screen, and there it is: a problem you've never seen before. Your mind goes blank. You stare at the screen. Seconds feel like minutes.

I've been there. In my first Google interview, I spent 10 minutes in silence, trying to think of the "perfect" approach. The interviewer eventually asked, "Would you like to talk through your thinking?"

I'd wasted a third of the interview saying nothing.

**The fix isn't knowing more algorithms. It's having a repeatable process.**

Here's the framework that got me through 12 technical interview loops: **UMPIRE**.

---

## The UMPIRE Framework

```
U - Understand the problem
M - Match to known patterns
P - Plan your approach
I - Implement the code
R - Review and test
E - Evaluate complexity
```

Let's break down each step.

---

## U — Understand the Problem

**Spend 3-5 minutes here. Most mistakes happen because you solved the wrong problem.**

### Ask Clarifying Questions

Never start coding without understanding:

**Input:**
- What's the input type? (array, string, tree, graph?)
- What's the size range? (affects acceptable complexity)
- Can input be empty? Negative? Duplicates?
- Is the input sorted? Unique?

**Output:**
- What should I return? (value, index, boolean, modified input?)
- What if there's no valid answer?
- Should I return one solution or all solutions?

**Constraints:**
- What are the size limits?
- Are there time/space requirements?
- Any special restrictions?

### Work Through Examples

Don't just use the given examples. Create your own:

```
Given: nums = [2, 7, 11, 15], target = 9
Expected: [0, 1]

My examples:
- Empty array: [] → what should I return?
- Single element: [5], target = 5 → valid?
- No solution: [1, 2, 3], target = 10 → return what?
- Duplicates: [3, 3], target = 6 → which indices?
- Negative numbers: [-1, 2], target = 1 → works?
```

**Say this out loud:** "Let me make sure I understand. Given [restate problem], I need to return [expected output]. Is that correct?"

---

## M — Match to Known Patterns

**Look for signals that point to specific patterns.**

| If you see... | Think about... |
|---------------|----------------|
| "Sorted array" | Binary search |
| "Find pair/triplet that..." | Two pointers, hash map |
| "Subarray/substring with property" | Sliding window |
| "Tree traversal" | BFS, DFS, recursion |
| "Graph connectivity" | BFS, DFS, Union-Find |
| "Shortest path" | BFS (unweighted), Dijkstra (weighted) |
| "Top K / Kth largest" | Heap |
| "All combinations/permutations" | Backtracking |
| "Optimal substructure + overlapping" | Dynamic programming |
| "Parentheses matching" | Stack |

**Say this out loud:** "This reminds me of [pattern] because [reason]."

---

## P — Plan Your Approach

**Don't code yet. Plan first.**

### Talk Through the Approach

1. **Describe your strategy in plain English**
   - "I'm going to use a hash map to store values I've seen..."
   
2. **Walk through an example**
   - "With [2, 7, 11, 15] and target 9: First I see 2, I need 7..."

3. **Identify edge cases now**
   - "I need to handle empty arrays and no-solution cases"

4. **State expected complexity**
   - "This should be O(n) time and O(n) space"

### Get Buy-In

Before coding, ask: "Does this approach sound reasonable? Should I start implementing?"

This does two things:
- Confirms you're on the right track
- Shows you're collaborative (a signal interviewers look for)

---

## I — Implement the Code

**Now—and only now—start coding.**

### Write Clean Code

```python
# Good: Clear variable names, logical structure
def two_sum(nums, target):
    seen = {}  # value -> index
    
    for index, num in enumerate(nums):
        complement = target - num
        
        if complement in seen:
            return [seen[complement], index]
        
        seen[num] = index
    
    return []  # No solution found

# Bad: Cryptic names, unclear logic
def f(n, t):
    d = {}
    for i, x in enumerate(n):
        if t - x in d:
            return [d[t - x], i]
        d[x] = i
```

### Talk While You Code

**Don't go silent.** Explain what you're doing:

- "I'm initializing a hash map to store values I've seen"
- "Now I'm iterating through the array"
- "Here I'm checking if the complement exists"

This shows your thinking process—even if you make a mistake, the interviewer sees your logic.

### Write Incrementally

Don't try to write the entire solution at once:

1. Write the function signature
2. Handle the main logic
3. Add edge case handling
4. Clean up and optimize

---

## R — Review and Test

**Never say "I'm done" without testing.**

### Trace Through Manually

Pick an example and trace through your code line by line:

```python
def two_sum(nums, target):
    seen = {}
    for index, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], index]
        seen[num] = index
    return []

# Trace: nums = [2, 7, 11], target = 9
# index=0, num=2: complement=7, not in {}, seen={2:0}
# index=1, num=7: complement=2, 2 in {2:0}! return [0, 1] ✓
```

### Test Edge Cases

Always test:
- Empty input
- Single element
- No valid answer
- All same elements
- Very large/small values

### Look for Common Bugs

- Off-by-one errors (`<` vs `<=`)
- Forgetting to update loop variables
- Missing return statement
- Wrong operator (= vs ==)
- Integer overflow (in some languages)

---

## E — Evaluate Complexity

**Always state complexity before the interviewer asks.**

### Time Complexity

- Count operations relative to input size
- Nested loops? Probably O(n²) or O(n × m)
- Hash map operations? Usually O(1)
- Sorting? O(n log n)
- Recursion? Count calls × work per call

### Space Complexity

- Extra data structures? Count their size
- Recursion? Count max stack depth
- In-place modification? O(1)

**Say this out loud:** "This solution is O(n) time because we iterate through the array once, and O(n) space because we store up to n elements in the hash map."

---

## Putting It All Together

Let's walk through a complete example:

### Problem: Two Sum
Given an array of integers nums and an integer target, return indices of the two numbers that add up to target.

### U — Understand
- Input: array of integers, integer target
- Output: indices (not values) of two numbers
- Can I use the same element twice? (Ask!)
- What if no solution exists?
- Are there always exactly two numbers that work?

### M — Match
- Need to find pairs → Hash map or two pointers
- Array is unsorted → Hash map is O(n)
- "Find pair that sums to target" → Classic hash map pattern

### P — Plan
"I'll use a hash map to store each number and its index as I iterate. For each number, I'll check if its complement (target - num) exists in the map. If it does, I've found my pair."

Time: O(n), Space: O(n)

### I — Implement
```python
def two_sum(nums, target):
    seen = {}
    
    for index, num in enumerate(nums):
        complement = target - num
        
        if complement in seen:
            return [seen[complement], index]
        
        seen[num] = index
    
    return []
```

### R — Review
Trace through [2, 7, 11, 15], target = 9:
- i=0: complement=7, not in {}, add 2:0
- i=1: complement=2, found at index 0! Return [0, 1] ✓

Test edge cases:
- Empty array → returns []
- No solution → returns []
- Single element → returns []

### E — Evaluate
"O(n) time because we iterate once. O(n) space for the hash map."

---

## Common Mistakes to Avoid

### 1. Jumping to Code Too Fast
The #1 mistake. Spend time understanding before coding.

### 2. Going Silent
Talk through your thinking. Silence looks like confusion.

### 3. Not Testing
Always trace through at least one example manually.

### 4. Ignoring Edge Cases
Empty, single element, no solution—test them all.

### 5. Not Stating Complexity
Don't wait to be asked. Volunteer it.

### 6. Refusing Hints
Hints aren't failure. They're collaboration. Take them gracefully.

---

## Key Takeaways

1. **Have a process.** UMPIRE gives you steps to follow when your mind goes blank.

2. **Talk out loud.** The interview is about your process, not just the answer.

3. **Understand before coding.** 5 minutes of clarification saves 15 minutes of rewriting.

4. **Test your code.** Never say "I'm done" without tracing through an example.

5. **State complexity explicitly.** Show you understand the efficiency of your solution.

---

## What's Next?

Now that you have a framework, let's look at the specific data structures you'll need to master:

👉 [Arrays & Strings →](../data-structures/arrays-strings)
