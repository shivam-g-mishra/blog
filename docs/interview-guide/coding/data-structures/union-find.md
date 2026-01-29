---
sidebar_position: 10
title: "Union-Find (Disjoint Set)"
description: >-
  Master Union-Find for coding interviews. Connected components, cycle detection,
  and optimization techniques with code in 7 languages.
keywords:
  - union find
  - disjoint set
  - connected components
  - path compression
  - union by rank
  - cycle detection

og_title: "Union-Find (Disjoint Set)"
og_description: "Track connected components with near O(1) operations. Master path compression and union by rank."
og_image: "/img/social-card.svg"

date_published: 2026-01-28
date_modified: 2026-01-28
author: shivam
reading_time: 25
content_type: explanation
---

import { LanguageSelector, TimeEstimate, ConfidenceBuilder, DifficultyBadge } from '@site/src/components/interview-guide';
import { CodeTabs } from '@site/src/components/design-patterns/CodeTabs';
import TabItem from '@theme/TabItem';

# Union-Find: Track Connected Components

The first time I encountered "dynamic connectivity"—adding edges one at a time and querying if two nodes are connected—I tried using DFS for each query. That's O(n) per query, which times out when you have thousands of queries.

**Union-Find tracks which elements belong to which groups, with near O(1) operations after optimization.**

When you see "connected components," "grouping," or "cycle detection in edges given one by one," think Union-Find.

<LanguageSelector />

<TimeEstimate
  learnTime="25-35 minutes"
  practiceTime="3-4 hours"
  masteryTime="8-10 problems"
  interviewFrequency="25%"
  difficultyRange="Medium"
  prerequisites="Graphs, Trees"
/>

---

## When to Use Union-Find

| Problem Type | Example |
|--------------|---------|
| Connected components | Network connectivity |
| Cycle detection | Does adding this edge create a cycle? |
| Dynamic connectivity | Add edges over time, query connectivity |
| Grouping | Merge accounts with same email |
| Minimum spanning tree | Kruskal's algorithm |

**Union-Find vs DFS/BFS:**
- Use Union-Find when edges are added incrementally
- Use DFS/BFS when you have the complete graph upfront

---

## Core Implementation

<CodeTabs>
<TabItem value="python" label="Python">

```python
class UnionFind:
    def __init__(self, n: int):
        """Initialize n elements, each in its own set."""
        self.parent: list[int] = list(range(n))
        self.rank: list[int] = [0] * n
        self.count: int = n  # Number of connected components
    
    def find(self, x: int) -> int:
        """
        Find root of x with path compression.
        Time: O(α(n)) ≈ O(1) amortized
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        """
        Unite sets containing x and y.
        Returns True if x and y were in different sets.
        Time: O(α(n)) ≈ O(1) amortized
        """
        px, py = self.find(x), self.find(y)
        
        if px == py:
            return False  # Already in same set
        
        # Union by rank: attach smaller tree under larger tree
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        
        self.parent[py] = px
        
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        
        self.count -= 1  # One less component
        return True
    
    def connected(self, x: int, y: int) -> bool:
        """Check if x and y are in the same set."""
        return self.find(x) == self.find(y)
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
class UnionFind {
  private parent: number[];
  private rank: number[];
  public count: number;

  constructor(n: number) {
    this.parent = Array.from({ length: n }, (_, i) => i);
    this.rank = new Array(n).fill(0);
    this.count = n;
  }

  find(x: number): number {
    if (this.parent[x] !== x) {
      this.parent[x] = this.find(this.parent[x]);
    }
    return this.parent[x];
  }

  union(x: number, y: number): boolean {
    let px = this.find(x);
    let py = this.find(y);

    if (px === py) return false;

    if (this.rank[px] < this.rank[py]) {
      [px, py] = [py, px];
    }

    this.parent[py] = px;

    if (this.rank[px] === this.rank[py]) {
      this.rank[px]++;
    }

    this.count--;
    return true;
  }

  connected(x: number, y: number): boolean {
    return this.find(x) === this.find(y);
  }
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
type UnionFind struct {
    parent []int
    rank   []int
    Count  int
}

func NewUnionFind(n int) *UnionFind {
    parent := make([]int, n)
    for i := range parent {
        parent[i] = i
    }
    return &UnionFind{
        parent: parent,
        rank:   make([]int, n),
        Count:  n,
    }
}

func (uf *UnionFind) Find(x int) int {
    if uf.parent[x] != x {
        uf.parent[x] = uf.Find(uf.parent[x])
    }
    return uf.parent[x]
}

func (uf *UnionFind) Union(x, y int) bool {
    px, py := uf.Find(x), uf.Find(y)
    
    if px == py {
        return false
    }
    
    if uf.rank[px] < uf.rank[py] {
        px, py = py, px
    }
    
    uf.parent[py] = px
    
    if uf.rank[px] == uf.rank[py] {
        uf.rank[px]++
    }
    
    uf.Count--
    return true
}

func (uf *UnionFind) Connected(x, y int) bool {
    return uf.Find(x) == uf.Find(y)
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
class UnionFind {
    private int[] parent;
    private int[] rank;
    private int count;
    
    public UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        count = n;
        
        for (int i = 0; i < n; i++) {
            parent[i] = i;
        }
    }
    
    public int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    public boolean union(int x, int y) {
        int px = find(x);
        int py = find(y);
        
        if (px == py) return false;
        
        if (rank[px] < rank[py]) {
            int temp = px;
            px = py;
            py = temp;
        }
        
        parent[py] = px;
        
        if (rank[px] == rank[py]) {
            rank[px]++;
        }
        
        count--;
        return true;
    }
    
    public boolean connected(int x, int y) {
        return find(x) == find(y);
    }
    
    public int getCount() {
        return count;
    }
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
class UnionFind {
private:
    vector<int> parent;
    vector<int> rank_;
    int count;
    
public:
    UnionFind(int n) : parent(n), rank_(n, 0), count(n) {
        iota(parent.begin(), parent.end(), 0);
    }
    
    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    
    bool unite(int x, int y) {
        int px = find(x);
        int py = find(y);
        
        if (px == py) return false;
        
        if (rank_[px] < rank_[py]) {
            swap(px, py);
        }
        
        parent[py] = px;
        
        if (rank_[px] == rank_[py]) {
            rank_[px]++;
        }
        
        count--;
        return true;
    }
    
    bool connected(int x, int y) {
        return find(x) == find(y);
    }
    
    int getCount() { return count; }
};
```

</TabItem>
<TabItem value="c" label="C">

```c
typedef struct {
    int* parent;
    int* rank;
    int count;
    int size;
} UnionFind;

UnionFind* createUnionFind(int n) {
    UnionFind* uf = (UnionFind*)malloc(sizeof(UnionFind));
    uf->parent = (int*)malloc(n * sizeof(int));
    uf->rank = (int*)calloc(n, sizeof(int));
    uf->count = n;
    uf->size = n;
    
    for (int i = 0; i < n; i++) {
        uf->parent[i] = i;
    }
    
    return uf;
}

int find(UnionFind* uf, int x) {
    if (uf->parent[x] != x) {
        uf->parent[x] = find(uf, uf->parent[x]);
    }
    return uf->parent[x];
}

bool unite(UnionFind* uf, int x, int y) {
    int px = find(uf, x);
    int py = find(uf, y);
    
    if (px == py) return false;
    
    if (uf->rank[px] < uf->rank[py]) {
        int temp = px;
        px = py;
        py = temp;
    }
    
    uf->parent[py] = px;
    
    if (uf->rank[px] == uf->rank[py]) {
        uf->rank[px]++;
    }
    
    uf->count--;
    return true;
}

bool connected(UnionFind* uf, int x, int y) {
    return find(uf, x) == find(uf, y);
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public class UnionFind {
    private int[] parent;
    private int[] rank;
    public int Count { get; private set; }
    
    public UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        Count = n;
        
        for (int i = 0; i < n; i++) {
            parent[i] = i;
        }
    }
    
    public int Find(int x) {
        if (parent[x] != x) {
            parent[x] = Find(parent[x]);
        }
        return parent[x];
    }
    
    public bool Union(int x, int y) {
        int px = Find(x);
        int py = Find(y);
        
        if (px == py) return false;
        
        if (rank[px] < rank[py]) {
            (px, py) = (py, px);
        }
        
        parent[py] = px;
        
        if (rank[px] == rank[py]) {
            rank[px]++;
        }
        
        Count--;
        return true;
    }
    
    public bool Connected(int x, int y) {
        return Find(x) == Find(y);
    }
}
```

</TabItem>
</CodeTabs>

---

## Key Optimizations

### Path Compression

Flatten the tree during `find` operations:

```
Before find(4):       After find(4):
    0                       0
    |                    /|\ \ 
    1                   1 2 3 4
    |
    2
    |
    3
    |
    4
```

### Union by Rank

Always attach smaller tree under larger tree to keep height minimal:

```
Union(small, large):
    
    large              large
                  →    / \
    small            old small
```

<ConfidenceBuilder type="remember" title="Why Both Optimizations?">

- **Path compression alone:** O(log n) amortized
- **Union by rank alone:** O(log n) amortized
- **Both together:** O(α(n)) ≈ O(1) amortized

α(n) is the inverse Ackermann function—it grows so slowly that it's effectively constant for any practical input size.

</ConfidenceBuilder>

---

## Classic Problem: Number of Connected Components

<CodeTabs>
<TabItem value="python" label="Python">

```python
def count_components(n: int, edges: list[list[int]]) -> int:
    """
    Count connected components in undirected graph.
    Time: O(E × α(n)) ≈ O(E)
    """
    uf = UnionFind(n)
    
    for u, v in edges:
        uf.union(u, v)
    
    return uf.count


# Alternative: Number of Islands using Union-Find
def num_islands_uf(grid: list[list[str]]) -> int:
    """
    Count islands in grid using Union-Find.
    """
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    
    # Count initial land cells
    land_count = sum(
        grid[r][c] == '1' 
        for r in range(rows) 
        for c in range(cols)
    )
    
    uf = UnionFind(rows * cols)
    uf.count = land_count  # Start with all land as separate islands
    
    def index(r: int, c: int) -> int:
        return r * cols + c
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                # Only check right and down to avoid double-counting
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                        uf.union(index(r, c), index(nr, nc))
    
    return uf.count
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function countComponents(n: number, edges: number[][]): number {
  const uf = new UnionFind(n);

  for (const [u, v] of edges) {
    uf.union(u, v);
  }

  return uf.count;
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public int countComponents(int n, int[][] edges) {
    UnionFind uf = new UnionFind(n);
    
    for (int[] edge : edges) {
        uf.union(edge[0], edge[1]);
    }
    
    return uf.getCount();
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func countComponents(n int, edges [][]int) int {
    uf := NewUnionFind(n)
    
    for _, edge := range edges {
        uf.Union(edge[0], edge[1])
    }
    
    return uf.Count
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
int countComponents(int n, vector<vector<int>>& edges) {
    UnionFind uf(n);
    
    for (auto& edge : edges) {
        uf.unite(edge[0], edge[1]);
    }
    
    return uf.getCount();
}
```

</TabItem>
<TabItem value="c" label="C">

```c
int countComponents(int n, int** edges, int edgesSize) {
    UnionFind* uf = createUnionFind(n);
    
    for (int i = 0; i < edgesSize; i++) {
        unite(uf, edges[i][0], edges[i][1]);
    }
    
    return uf->count;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public int CountComponents(int n, int[][] edges) {
    var uf = new UnionFind(n);
    
    foreach (var edge in edges) {
        uf.Union(edge[0], edge[1]);
    }
    
    return uf.Count;
}
```

</TabItem>
</CodeTabs>

---

## Classic Problem: Redundant Connection (Cycle Detection)

Find the edge that creates a cycle.

<CodeTabs>
<TabItem value="python" label="Python">

```python
def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    """
    Find edge that creates cycle in tree + one extra edge.
    
    Key insight: If union returns False, the edge connects
    two nodes already in the same component = cycle!
    """
    n = len(edges)
    uf = UnionFind(n + 1)  # 1-indexed nodes
    
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]  # This edge creates cycle
    
    return []
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function findRedundantConnection(edges: number[][]): number[] {
  const n = edges.length;
  const uf = new UnionFind(n + 1);

  for (const [u, v] of edges) {
    if (!uf.union(u, v)) {
      return [u, v];
    }
  }

  return [];
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public int[] findRedundantConnection(int[][] edges) {
    int n = edges.length;
    UnionFind uf = new UnionFind(n + 1);
    
    for (int[] edge : edges) {
        if (!uf.union(edge[0], edge[1])) {
            return edge;
        }
    }
    
    return new int[0];
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func findRedundantConnection(edges [][]int) []int {
    n := len(edges)
    uf := NewUnionFind(n + 1)
    
    for _, edge := range edges {
        if !uf.Union(edge[0], edge[1]) {
            return edge
        }
    }
    
    return []int{}
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
vector<int> findRedundantConnection(vector<vector<int>>& edges) {
    int n = edges.size();
    UnionFind uf(n + 1);
    
    for (auto& edge : edges) {
        if (!uf.unite(edge[0], edge[1])) {
            return edge;
        }
    }
    
    return {};
}
```

</TabItem>
<TabItem value="c" label="C">

```c
int* findRedundantConnection(int** edges, int edgesSize, int* returnSize) {
    UnionFind* uf = createUnionFind(edgesSize + 1);
    
    for (int i = 0; i < edgesSize; i++) {
        if (!unite(uf, edges[i][0], edges[i][1])) {
            int* result = (int*)malloc(2 * sizeof(int));
            result[0] = edges[i][0];
            result[1] = edges[i][1];
            *returnSize = 2;
            return result;
        }
    }
    
    *returnSize = 0;
    return NULL;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public int[] FindRedundantConnection(int[][] edges) {
    int n = edges.Length;
    var uf = new UnionFind(n + 1);
    
    foreach (var edge in edges) {
        if (!uf.Union(edge[0], edge[1])) {
            return edge;
        }
    }
    
    return Array.Empty<int>();
}
```

</TabItem>
</CodeTabs>

---

## Classic Problem: Accounts Merge

<CodeTabs>
<TabItem value="python" label="Python">

```python
def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    """
    Merge accounts that share any email.
    
    Strategy:
    1. Map emails to account indices
    2. Union accounts sharing an email
    3. Group emails by root account
    4. Format output
    """
    from collections import defaultdict
    
    n = len(accounts)
    uf = UnionFind(n)
    email_to_id: dict[str, int] = {}
    
    # Union accounts with same email
    for i, account in enumerate(accounts):
        for email in account[1:]:  # Skip name
            if email in email_to_id:
                uf.union(i, email_to_id[email])
            email_to_id[email] = i
    
    # Group emails by root account
    id_to_emails: dict[int, set[str]] = defaultdict(set)
    for email, idx in email_to_id.items():
        root = uf.find(idx)
        id_to_emails[root].add(email)
    
    # Format result: [name, sorted_emails...]
    return [
        [accounts[idx][0]] + sorted(emails)
        for idx, emails in id_to_emails.items()
    ]
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function accountsMerge(accounts: string[][]): string[][] {
  const n = accounts.length;
  const uf = new UnionFind(n);
  const emailToId = new Map<string, number>();

  for (let i = 0; i < n; i++) {
    for (let j = 1; j < accounts[i].length; j++) {
      const email = accounts[i][j];
      if (emailToId.has(email)) {
        uf.union(i, emailToId.get(email)!);
      }
      emailToId.set(email, i);
    }
  }

  const idToEmails = new Map<number, Set<string>>();
  for (const [email, idx] of emailToId) {
    const root = uf.find(idx);
    if (!idToEmails.has(root)) {
      idToEmails.set(root, new Set());
    }
    idToEmails.get(root)!.add(email);
  }

  const result: string[][] = [];
  for (const [idx, emails] of idToEmails) {
    result.push([accounts[idx][0], ...Array.from(emails).sort()]);
  }

  return result;
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public List<List<String>> accountsMerge(List<List<String>> accounts) {
    int n = accounts.size();
    UnionFind uf = new UnionFind(n);
    Map<String, Integer> emailToId = new HashMap<>();
    
    for (int i = 0; i < n; i++) {
        List<String> account = accounts.get(i);
        for (int j = 1; j < account.size(); j++) {
            String email = account.get(j);
            if (emailToId.containsKey(email)) {
                uf.union(i, emailToId.get(email));
            }
            emailToId.put(email, i);
        }
    }
    
    Map<Integer, Set<String>> idToEmails = new HashMap<>();
    for (Map.Entry<String, Integer> entry : emailToId.entrySet()) {
        int root = uf.find(entry.getValue());
        idToEmails.computeIfAbsent(root, k -> new TreeSet<>()).add(entry.getKey());
    }
    
    List<List<String>> result = new ArrayList<>();
    for (Map.Entry<Integer, Set<String>> entry : idToEmails.entrySet()) {
        List<String> merged = new ArrayList<>();
        merged.add(accounts.get(entry.getKey()).get(0));
        merged.addAll(entry.getValue());
        result.add(merged);
    }
    
    return result;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func accountsMerge(accounts [][]string) [][]string {
    n := len(accounts)
    uf := NewUnionFind(n)
    emailToId := make(map[string]int)
    
    for i, account := range accounts {
        for _, email := range account[1:] {
            if id, exists := emailToId[email]; exists {
                uf.Union(i, id)
            }
            emailToId[email] = i
        }
    }
    
    idToEmails := make(map[int]map[string]bool)
    for email, idx := range emailToId {
        root := uf.Find(idx)
        if idToEmails[root] == nil {
            idToEmails[root] = make(map[string]bool)
        }
        idToEmails[root][email] = true
    }
    
    var result [][]string
    for idx, emailSet := range idToEmails {
        emails := make([]string, 0, len(emailSet))
        for email := range emailSet {
            emails = append(emails, email)
        }
        sort.Strings(emails)
        merged := append([]string{accounts[idx][0]}, emails...)
        result = append(result, merged)
    }
    
    return result
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
vector<vector<string>> accountsMerge(vector<vector<string>>& accounts) {
    int n = accounts.size();
    UnionFind uf(n);
    unordered_map<string, int> emailToId;
    
    for (int i = 0; i < n; i++) {
        for (int j = 1; j < accounts[i].size(); j++) {
            string& email = accounts[i][j];
            if (emailToId.count(email)) {
                uf.unite(i, emailToId[email]);
            }
            emailToId[email] = i;
        }
    }
    
    unordered_map<int, set<string>> idToEmails;
    for (auto& [email, idx] : emailToId) {
        int root = uf.find(idx);
        idToEmails[root].insert(email);
    }
    
    vector<vector<string>> result;
    for (auto& [idx, emails] : idToEmails) {
        vector<string> merged = {accounts[idx][0]};
        merged.insert(merged.end(), emails.begin(), emails.end());
        result.push_back(merged);
    }
    
    return result;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public IList<IList<string>> AccountsMerge(IList<IList<string>> accounts) {
    int n = accounts.Count;
    var uf = new UnionFind(n);
    var emailToId = new Dictionary<string, int>();
    
    for (int i = 0; i < n; i++) {
        for (int j = 1; j < accounts[i].Count; j++) {
            string email = accounts[i][j];
            if (emailToId.ContainsKey(email)) {
                uf.Union(i, emailToId[email]);
            }
            emailToId[email] = i;
        }
    }
    
    var idToEmails = new Dictionary<int, SortedSet<string>>();
    foreach (var (email, idx) in emailToId) {
        int root = uf.Find(idx);
        if (!idToEmails.ContainsKey(root)) {
            idToEmails[root] = new SortedSet<string>();
        }
        idToEmails[root].Add(email);
    }
    
    var result = new List<IList<string>>();
    foreach (var (idx, emails) in idToEmails) {
        var merged = new List<string> { accounts[idx][0] };
        merged.AddRange(emails);
        result.Add(merged);
    }
    
    return result;
}
```

</TabItem>
</CodeTabs>

---

## Complexity

| Operation | Without Optimization | With Both Optimizations |
|-----------|---------------------|------------------------|
| Find | O(n) | O(α(n)) ≈ O(1) |
| Union | O(n) | O(α(n)) ≈ O(1) |
| Space | O(n) | O(n) |

α(n) = inverse Ackermann function, effectively constant for all practical purposes.

---

## 💬 How to Communicate This in Interviews

**Identifying Union-Find:**
> "This is a connectivity problem where we're adding edges over time. Union-Find gives us near O(1) operations for tracking components..."

**Explaining optimizations:**
> "I'm using path compression to flatten the tree during find, and union by rank to keep trees balanced. Together they give O(α(n)) which is effectively constant..."

**For cycle detection:**
> "When union returns false, it means both nodes are already in the same component. Adding this edge would create a cycle..."

---

## 🏋️ Practice Problems

### Warm-Up (Build Confidence)

| Problem | Difficulty | Time |
|---------|------------|------|
| [Number of Provinces](https://leetcode.com/problems/number-of-provinces/) | <DifficultyBadge level="medium" /> | 20 min |
| [Redundant Connection](https://leetcode.com/problems/redundant-connection/) | <DifficultyBadge level="medium" /> | 20 min |

### Core Practice (Must Do)

| Problem | Difficulty | Companies | Key Insight |
|---------|------------|-----------|-------------|
| [Accounts Merge](https://leetcode.com/problems/accounts-merge/) | <DifficultyBadge level="medium" /> | Meta, Google, Amazon | Group by shared element |
| [Number of Islands](https://leetcode.com/problems/number-of-islands/) | <DifficultyBadge level="medium" /> | Amazon, Google | Grid to UF (alternative) |
| [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | <DifficultyBadge level="medium" /> | Google, Amazon | Union consecutive numbers |
| [Satisfiability of Equality](https://leetcode.com/problems/satisfiability-of-equality-equations/) | <DifficultyBadge level="medium" /> | Google | Union == first |

### Challenge (For Mastery)

| Problem | Difficulty | Companies | Why It's Hard |
|---------|------------|-----------|---------------|
| [Smallest String with Swaps](https://leetcode.com/problems/smallest-string-with-swaps/) | <DifficultyBadge level="medium" /> | Amazon, Google | UF + sorting groups |
| [Making a Large Island](https://leetcode.com/problems/making-a-large-island/) | <DifficultyBadge level="hard" /> | Google, Amazon | UF + try flipping each 0 |

---

## Key Takeaways

1. **Near O(1)** with path compression + union by rank together.

2. **Track component count** by decrementing on successful union.

3. **Cycle detection:** Union returns false if already connected.

4. **Dynamic connectivity:** Better than DFS when edges arrive incrementally.

5. **Grid problems:** Map (r, c) to index r × cols + c.

<ConfidenceBuilder type="youve-got-this">

**Union-Find has a simple template.**

Once you memorize the `find` and `union` methods, the same code works for almost every problem. The creativity is in mapping the problem to Union-Find.

</ConfidenceBuilder>

---

## What's Next?

You've completed all core data structures. Continue with algorithm patterns:

**Next up:** [Backtracking Patterns](/docs/interview-guide/coding/patterns/backtracking-patterns/introduction) — Exploring All Possibilities
