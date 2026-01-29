---
sidebar_position: 2
title: "BST Operations — The Ordered Tree"
description: >-
  Master Binary Search Tree operations for coding interviews. Insert, delete,
  search, validate, and kth smallest with code in 7 languages.
keywords:
  - BST operations
  - binary search tree
  - BST insert delete
  - validate BST
  - kth smallest BST

og_title: "BST Operations — The Ordered Tree"
og_description: "BST property enables O(log n) operations. Master search, insert, delete, and common BST problems."
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

# BST Operations: The Ordered Tree

**BST Property:** Left subtree < Node < Right subtree (for all nodes).

This single property enables O(log n) search, insert, and delete—compared to O(n) for regular binary trees.

<LanguageSelector />

<TimeEstimate
  learnTime="25-35 minutes"
  practiceTime="3-4 hours"
  masteryTime="10-12 problems"
  interviewFrequency="30%"
  difficultyRange="Easy to Medium"
  prerequisites="Trees, Binary Search"
/>

---

## Core Operations

### Search

<CodeTabs>
<TabItem value="python" label="Python">

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def search_bst(root: TreeNode | None, val: int) -> TreeNode | None:
    """
    Search for a value in BST.
    Use BST property: go left if smaller, right if larger.
    Time: O(log n) average, O(n) worst (skewed tree)
    """
    if not root or root.val == val:
        return root
    
    if val < root.val:
        return search_bst(root.left, val)
    return search_bst(root.right, val)


def search_bst_iterative(root: TreeNode | None, val: int) -> TreeNode | None:
    """Iterative version - avoids stack overflow."""
    while root and root.val != val:
        if val < root.val:
            root = root.left
        else:
            root = root.right
    return root
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
class TreeNode {
  val: number;
  left: TreeNode | null;
  right: TreeNode | null;

  constructor(val = 0, left: TreeNode | null = null, right: TreeNode | null = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

function searchBST(root: TreeNode | null, val: number): TreeNode | null {
  if (!root || root.val === val) return root;

  if (val < root.val) {
    return searchBST(root.left, val);
  }
  return searchBST(root.right, val);
}

function searchBSTIterative(root: TreeNode | null, val: number): TreeNode | null {
  while (root && root.val !== val) {
    root = val < root.val ? root.left : root.right;
  }
  return root;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
type TreeNode struct {
    Val   int
    Left  *TreeNode
    Right *TreeNode
}

func searchBST(root *TreeNode, val int) *TreeNode {
    if root == nil || root.Val == val {
        return root
    }
    
    if val < root.Val {
        return searchBST(root.Left, val)
    }
    return searchBST(root.Right, val)
}

func searchBSTIterative(root *TreeNode, val int) *TreeNode {
    for root != nil && root.Val != val {
        if val < root.Val {
            root = root.Left
        } else {
            root = root.Right
        }
    }
    return root
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public TreeNode searchBST(TreeNode root, int val) {
    if (root == null || root.val == val) return root;
    
    if (val < root.val) {
        return searchBST(root.left, val);
    }
    return searchBST(root.right, val);
}

public TreeNode searchBSTIterative(TreeNode root, int val) {
    while (root != null && root.val != val) {
        root = val < root.val ? root.left : root.right;
    }
    return root;
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
TreeNode* searchBST(TreeNode* root, int val) {
    if (!root || root->val == val) return root;
    
    if (val < root->val) {
        return searchBST(root->left, val);
    }
    return searchBST(root->right, val);
}

TreeNode* searchBSTIterative(TreeNode* root, int val) {
    while (root && root->val != val) {
        root = val < root->val ? root->left : root->right;
    }
    return root;
}
```

</TabItem>
<TabItem value="c" label="C">

```c
struct TreeNode* searchBST(struct TreeNode* root, int val) {
    if (!root || root->val == val) return root;
    
    if (val < root->val) {
        return searchBST(root->left, val);
    }
    return searchBST(root->right, val);
}

struct TreeNode* searchBSTIterative(struct TreeNode* root, int val) {
    while (root && root->val != val) {
        root = val < root->val ? root->left : root->right;
    }
    return root;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public TreeNode SearchBST(TreeNode root, int val) {
    if (root == null || root.val == val) return root;
    
    if (val < root.val) {
        return SearchBST(root.left, val);
    }
    return SearchBST(root.right, val);
}

public TreeNode SearchBSTIterative(TreeNode root, int val) {
    while (root != null && root.val != val) {
        root = val < root.val ? root.left : root.right;
    }
    return root;
}
```

</TabItem>
</CodeTabs>

---

### Insert

<CodeTabs>
<TabItem value="python" label="Python">

```python
def insert_bst(root: TreeNode | None, val: int) -> TreeNode:
    """
    Insert a value into BST.
    Navigate to correct position, create new node.
    """
    if not root:
        return TreeNode(val)
    
    if val < root.val:
        root.left = insert_bst(root.left, val)
    else:
        root.right = insert_bst(root.right, val)
    
    return root


def insert_bst_iterative(root: TreeNode | None, val: int) -> TreeNode:
    """Iterative version."""
    new_node = TreeNode(val)
    
    if not root:
        return new_node
    
    current = root
    while True:
        if val < current.val:
            if not current.left:
                current.left = new_node
                break
            current = current.left
        else:
            if not current.right:
                current.right = new_node
                break
            current = current.right
    
    return root
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function insertIntoBST(root: TreeNode | null, val: number): TreeNode {
  if (!root) return new TreeNode(val);

  if (val < root.val) {
    root.left = insertIntoBST(root.left, val);
  } else {
    root.right = insertIntoBST(root.right, val);
  }

  return root;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func insertIntoBST(root *TreeNode, val int) *TreeNode {
    if root == nil {
        return &TreeNode{Val: val}
    }
    
    if val < root.Val {
        root.Left = insertIntoBST(root.Left, val)
    } else {
        root.Right = insertIntoBST(root.Right, val)
    }
    
    return root
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public TreeNode insertIntoBST(TreeNode root, int val) {
    if (root == null) return new TreeNode(val);
    
    if (val < root.val) {
        root.left = insertIntoBST(root.left, val);
    } else {
        root.right = insertIntoBST(root.right, val);
    }
    
    return root;
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
TreeNode* insertIntoBST(TreeNode* root, int val) {
    if (!root) return new TreeNode(val);
    
    if (val < root->val) {
        root->left = insertIntoBST(root->left, val);
    } else {
        root->right = insertIntoBST(root->right, val);
    }
    
    return root;
}
```

</TabItem>
<TabItem value="c" label="C">

```c
struct TreeNode* insertIntoBST(struct TreeNode* root, int val) {
    if (!root) {
        struct TreeNode* node = (struct TreeNode*)malloc(sizeof(struct TreeNode));
        node->val = val;
        node->left = node->right = NULL;
        return node;
    }
    
    if (val < root->val) {
        root->left = insertIntoBST(root->left, val);
    } else {
        root->right = insertIntoBST(root->right, val);
    }
    
    return root;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public TreeNode InsertIntoBST(TreeNode root, int val) {
    if (root == null) return new TreeNode(val);
    
    if (val < root.val) {
        root.left = InsertIntoBST(root.left, val);
    } else {
        root.right = InsertIntoBST(root.right, val);
    }
    
    return root;
}
```

</TabItem>
</CodeTabs>

---

### Delete (The Tricky One)

<CodeTabs>
<TabItem value="python" label="Python">

```python
def delete_node(root: TreeNode | None, key: int) -> TreeNode | None:
    """
    Delete a node from BST.
    
    Three cases:
    1. Node is leaf: Just remove
    2. Node has one child: Replace with child
    3. Node has two children: Replace with inorder successor
    """
    if not root:
        return None
    
    # Find the node to delete
    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        # Found the node to delete
        
        # Case 1 & 2: Zero or one child
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        
        # Case 3: Two children
        # Find inorder successor (smallest in right subtree)
        successor = root.right
        while successor.left:
            successor = successor.left
        
        # Replace value with successor's value
        root.val = successor.val
        
        # Delete the successor from right subtree
        root.right = delete_node(root.right, successor.val)
    
    return root
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function deleteNode(root: TreeNode | null, key: number): TreeNode | null {
  if (!root) return null;

  if (key < root.val) {
    root.left = deleteNode(root.left, key);
  } else if (key > root.val) {
    root.right = deleteNode(root.right, key);
  } else {
    // Found node to delete
    if (!root.left) return root.right;
    if (!root.right) return root.left;

    // Two children: find inorder successor
    let successor = root.right;
    while (successor.left) {
      successor = successor.left;
    }

    root.val = successor.val;
    root.right = deleteNode(root.right, successor.val);
  }

  return root;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func deleteNode(root *TreeNode, key int) *TreeNode {
    if root == nil {
        return nil
    }
    
    if key < root.Val {
        root.Left = deleteNode(root.Left, key)
    } else if key > root.Val {
        root.Right = deleteNode(root.Right, key)
    } else {
        if root.Left == nil {
            return root.Right
        }
        if root.Right == nil {
            return root.Left
        }
        
        successor := root.Right
        for successor.Left != nil {
            successor = successor.Left
        }
        
        root.Val = successor.Val
        root.Right = deleteNode(root.Right, successor.Val)
    }
    
    return root
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public TreeNode deleteNode(TreeNode root, int key) {
    if (root == null) return null;
    
    if (key < root.val) {
        root.left = deleteNode(root.left, key);
    } else if (key > root.val) {
        root.right = deleteNode(root.right, key);
    } else {
        if (root.left == null) return root.right;
        if (root.right == null) return root.left;
        
        TreeNode successor = root.right;
        while (successor.left != null) {
            successor = successor.left;
        }
        
        root.val = successor.val;
        root.right = deleteNode(root.right, successor.val);
    }
    
    return root;
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
TreeNode* deleteNode(TreeNode* root, int key) {
    if (!root) return nullptr;
    
    if (key < root->val) {
        root->left = deleteNode(root->left, key);
    } else if (key > root->val) {
        root->right = deleteNode(root->right, key);
    } else {
        if (!root->left) return root->right;
        if (!root->right) return root->left;
        
        TreeNode* successor = root->right;
        while (successor->left) {
            successor = successor->left;
        }
        
        root->val = successor->val;
        root->right = deleteNode(root->right, successor->val);
    }
    
    return root;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public TreeNode DeleteNode(TreeNode root, int key) {
    if (root == null) return null;
    
    if (key < root.val) {
        root.left = DeleteNode(root.left, key);
    } else if (key > root.val) {
        root.right = DeleteNode(root.right, key);
    } else {
        if (root.left == null) return root.right;
        if (root.right == null) return root.left;
        
        TreeNode successor = root.right;
        while (successor.left != null) {
            successor = successor.left;
        }
        
        root.val = successor.val;
        root.right = DeleteNode(root.right, successor.val);
    }
    
    return root;
}
```

</TabItem>
</CodeTabs>

<ConfidenceBuilder type="remember" title="Delete with Two Children">

When deleting a node with two children:
1. Find the **inorder successor** (smallest node in right subtree)
2. **Copy** the successor's value to the current node
3. **Delete** the successor from the right subtree

This maintains the BST property because the successor is greater than all left subtree nodes and less than all other right subtree nodes.

</ConfidenceBuilder>

---

## Validate BST

<CodeTabs>
<TabItem value="python" label="Python">

```python
def is_valid_bst(root: TreeNode | None) -> bool:
    """
    Check if a binary tree is a valid BST.
    
    Key insight: Each node must be within valid range.
    As we go left, max bound decreases.
    As we go right, min bound increases.
    """
    def validate(node: TreeNode | None, min_val: float, max_val: float) -> bool:
        if not node:
            return True
        
        # Node value must be strictly within bounds
        if node.val <= min_val or node.val >= max_val:
            return False
        
        # Left subtree: max becomes current node
        # Right subtree: min becomes current node
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function isValidBST(root: TreeNode | null): boolean {
  function validate(
    node: TreeNode | null,
    minVal: number,
    maxVal: number
  ): boolean {
    if (!node) return true;

    if (node.val <= minVal || node.val >= maxVal) {
      return false;
    }

    return (
      validate(node.left, minVal, node.val) &&
      validate(node.right, node.val, maxVal)
    );
  }

  return validate(root, -Infinity, Infinity);
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func isValidBST(root *TreeNode) bool {
    return validate(root, math.MinInt64, math.MaxInt64)
}

func validate(node *TreeNode, minVal, maxVal int) bool {
    if node == nil {
        return true
    }
    
    if node.Val <= minVal || node.Val >= maxVal {
        return false
    }
    
    return validate(node.Left, minVal, node.Val) &&
           validate(node.Right, node.Val, maxVal)
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public boolean isValidBST(TreeNode root) {
    return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
}

private boolean validate(TreeNode node, long minVal, long maxVal) {
    if (node == null) return true;
    
    if (node.val <= minVal || node.val >= maxVal) {
        return false;
    }
    
    return validate(node.left, minVal, node.val) &&
           validate(node.right, node.val, maxVal);
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
bool isValidBST(TreeNode* root) {
    return validate(root, LONG_MIN, LONG_MAX);
}

bool validate(TreeNode* node, long minVal, long maxVal) {
    if (!node) return true;
    
    if (node->val <= minVal || node->val >= maxVal) {
        return false;
    }
    
    return validate(node->left, minVal, node->val) &&
           validate(node->right, node->val, maxVal);
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public bool IsValidBST(TreeNode root) {
    return Validate(root, long.MinValue, long.MaxValue);
}

private bool Validate(TreeNode node, long minVal, long maxVal) {
    if (node == null) return true;
    
    if (node.val <= minVal || node.val >= maxVal) {
        return false;
    }
    
    return Validate(node.left, minVal, node.val) &&
           Validate(node.right, node.val, maxVal);
}
```

</TabItem>
</CodeTabs>

---

## Kth Smallest Element

<CodeTabs>
<TabItem value="python" label="Python">

```python
def kth_smallest(root: TreeNode | None, k: int) -> int:
    """
    Find kth smallest element in BST.
    
    Key insight: Inorder traversal visits nodes in sorted order.
    Just count until we hit k.
    
    Time: O(H + k), Space: O(H)
    """
    stack: list[TreeNode] = []
    current = root
    
    while stack or current:
        # Go to leftmost node
        while current:
            stack.append(current)
            current = current.left
        
        # Process current node (inorder)
        current = stack.pop()
        k -= 1
        
        if k == 0:
            return current.val
        
        # Move to right subtree
        current = current.right
    
    return -1  # k larger than tree size
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function kthSmallest(root: TreeNode | null, k: number): number {
  const stack: TreeNode[] = [];
  let current = root;

  while (stack.length > 0 || current) {
    while (current) {
      stack.push(current);
      current = current.left;
    }

    current = stack.pop()!;
    k--;

    if (k === 0) return current.val;

    current = current.right;
  }

  return -1;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func kthSmallest(root *TreeNode, k int) int {
    stack := []*TreeNode{}
    current := root
    
    for len(stack) > 0 || current != nil {
        for current != nil {
            stack = append(stack, current)
            current = current.Left
        }
        
        current = stack[len(stack)-1]
        stack = stack[:len(stack)-1]
        k--
        
        if k == 0 {
            return current.Val
        }
        
        current = current.Right
    }
    
    return -1
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public int kthSmallest(TreeNode root, int k) {
    Deque<TreeNode> stack = new ArrayDeque<>();
    TreeNode current = root;
    
    while (!stack.isEmpty() || current != null) {
        while (current != null) {
            stack.push(current);
            current = current.left;
        }
        
        current = stack.pop();
        k--;
        
        if (k == 0) return current.val;
        
        current = current.right;
    }
    
    return -1;
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
int kthSmallest(TreeNode* root, int k) {
    stack<TreeNode*> st;
    TreeNode* current = root;
    
    while (!st.empty() || current) {
        while (current) {
            st.push(current);
            current = current->left;
        }
        
        current = st.top();
        st.pop();
        k--;
        
        if (k == 0) return current->val;
        
        current = current->right;
    }
    
    return -1;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public int KthSmallest(TreeNode root, int k) {
    Stack<TreeNode> stack = new();
    TreeNode current = root;
    
    while (stack.Count > 0 || current != null) {
        while (current != null) {
            stack.Push(current);
            current = current.left;
        }
        
        current = stack.Pop();
        k--;
        
        if (k == 0) return current.val;
        
        current = current.right;
    }
    
    return -1;
}
```

</TabItem>
</CodeTabs>

---

## Lowest Common Ancestor in BST

<CodeTabs>
<TabItem value="python" label="Python">

```python
def lowest_common_ancestor(
    root: TreeNode | None, 
    p: TreeNode, 
    q: TreeNode
) -> TreeNode | None:
    """
    Find LCA in BST (simpler than general binary tree).
    
    Use BST property:
    - Both p and q smaller → go left
    - Both p and q larger → go right
    - Otherwise → current node is LCA
    """
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            # Split point: one on each side (or one equals root)
            return root
    
    return None
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function lowestCommonAncestor(
  root: TreeNode | null,
  p: TreeNode,
  q: TreeNode
): TreeNode | null {
  while (root) {
    if (p.val < root.val && q.val < root.val) {
      root = root.left;
    } else if (p.val > root.val && q.val > root.val) {
      root = root.right;
    } else {
      return root;
    }
  }
  return null;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func lowestCommonAncestor(root, p, q *TreeNode) *TreeNode {
    for root != nil {
        if p.Val < root.Val && q.Val < root.Val {
            root = root.Left
        } else if p.Val > root.Val && q.Val > root.Val {
            root = root.Right
        } else {
            return root
        }
    }
    return nil
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    while (root != null) {
        if (p.val < root.val && q.val < root.val) {
            root = root.left;
        } else if (p.val > root.val && q.val > root.val) {
            root = root.right;
        } else {
            return root;
        }
    }
    return null;
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    while (root) {
        if (p->val < root->val && q->val < root->val) {
            root = root->left;
        } else if (p->val > root->val && q->val > root->val) {
            root = root->right;
        } else {
            return root;
        }
    }
    return nullptr;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public TreeNode LowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    while (root != null) {
        if (p.val < root.val && q.val < root.val) {
            root = root.left;
        } else if (p.val > root.val && q.val > root.val) {
            root = root.right;
        } else {
            return root;
        }
    }
    return null;
}
```

</TabItem>
</CodeTabs>

---

## 🎯 Pattern Triggers

| Problem Clue | BST Operation |
|--------------|---------------|
| "Find value in BST" | Search (binary search logic) |
| "Add value to BST" | Insert (find correct position) |
| "Remove value from BST" | Delete (handle 3 cases) |
| "Check valid BST" | Validate (track min/max bounds) |
| "Kth smallest/largest" | Inorder traversal + count |
| "LCA in BST" | Use BST property (no parent needed) |
| "Sorted array to BST" | Divide and conquer (mid = root) |

---

## 💬 How to Communicate This in Interviews

**Using BST property:**
> "Since this is a BST, I can use the BST property—values less than node go left, greater go right—to achieve O(log n) search..."

**Delete explanation:**
> "For deleting a node with two children, I'll find the inorder successor—the smallest value in the right subtree—swap values, then delete the successor..."

**Validation approach:**
> "I'll validate by passing down min and max bounds. Each node must be greater than min and less than max..."

---

## 🏋️ Practice Problems

| Problem | Difficulty | Companies | Key Insight |
|---------|------------|-----------|-------------|
| [Search in BST](https://leetcode.com/problems/search-in-a-binary-search-tree/) | <DifficultyBadge level="easy" /> | Amazon | Binary search |
| [Insert into BST](https://leetcode.com/problems/insert-into-a-binary-search-tree/) | <DifficultyBadge level="medium" /> | Amazon, Microsoft | Find correct leaf position |
| [Delete Node in BST](https://leetcode.com/problems/delete-node-in-a-bst/) | <DifficultyBadge level="medium" /> | Google, Amazon | Three cases |
| [Validate BST](https://leetcode.com/problems/validate-binary-search-tree/) | <DifficultyBadge level="medium" /> | Amazon, Meta | Min/max bounds |
| [Kth Smallest](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | <DifficultyBadge level="medium" /> | Meta, Amazon | Inorder + count |
| [LCA of BST](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | <DifficultyBadge level="medium" /> | Google, Meta | BST property |
| [Convert Sorted Array to BST](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/) | <DifficultyBadge level="easy" /> | Microsoft | Mid = root |

---

## Key Takeaways

1. **BST property** enables O(log n) operations—left < node < right.

2. **Inorder traversal** of BST gives sorted order.

3. **Delete with two children:** Replace with inorder successor.

4. **LCA in BST** is simpler than general tree—use BST property.

5. **Validation:** Track min/max bounds at each node.

<ConfidenceBuilder type="youve-got-this">

**BST operations follow predictable patterns.**

Once you understand the BST property, all operations become intuitive: go left for smaller, right for larger. The only tricky case is delete with two children—memorize the inorder successor approach.

</ConfidenceBuilder>

---

## What's Next?

Lowest Common Ancestor variations for different tree types:

**Next up:** [LCA Patterns](/docs/interview-guide/coding/patterns/tree-patterns/lca) — Finding Common Ancestors
