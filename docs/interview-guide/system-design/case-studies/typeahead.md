---
sidebar_position: 14
title: "Design Typeahead / Autocomplete"
description: >-
  Complete system design for typeahead/autocomplete. Trie-based suggestions,
  ranking, and real-time updates.
keywords:
  - typeahead design
  - autocomplete system
  - search suggestions
  - trie system design
difficulty: Intermediate
estimated_time: 35 minutes
prerequisites:
  - Tries
  - Caching
companies: [Google, Amazon, Meta, LinkedIn]
---

# Design Typeahead: Instant Suggestions

Typeahead provides instant search suggestions as users type. The challenge: sub-100ms latency at scale.

---

## Requirements

### Functional
- Return top suggestions as user types
- Rank by popularity/relevance
- Support prefix matching
- Update suggestions based on new data

### Non-Functional
- **Latency:** < 100ms
- **Scale:** Billions of queries/day
- **Availability:** 99.99%

---

## High-Level Architecture

```
┌─────────────┐     ┌─────────────────────────────────────────────┐
│   Client    │────▶│            Load Balancer                    │
└─────────────┘     └──────────────────┬──────────────────────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
                    ▼                  ▼                  ▼
             ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
             │  Suggestion │    │  Suggestion │    │  Suggestion │
             │   Server 1  │    │   Server 2  │    │   Server N  │
             └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
                    │                  │                  │
                    └──────────────────┼──────────────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │  Trie Storage   │
                              │  (Distributed)  │
                              └─────────────────┘
```

---

## Data Structure: Trie

```
Example: Storing "tree", "trie", "try", "trip"

         root
          │
          t
          │
          r
         /│\
        e i y
        │ │
        e p (trip)
        │
       (tree, trie)

Each node stores:
- Children map
- Top N suggestions at this prefix
- Frequency/weight for ranking
```

### Trie Node

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.top_suggestions = []  # Pre-computed top K
        self.is_end = False

class Trie:
    def __init__(self, k=10):
        self.root = TrieNode()
        self.k = k  # Top K suggestions per node
    
    def insert(self, word, weight):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            self._update_suggestions(node, word, weight)
        node.is_end = True
    
    def _update_suggestions(self, node, word, weight):
        # Keep top K by weight
        node.top_suggestions.append((word, weight))
        node.top_suggestions.sort(key=lambda x: -x[1])
        node.top_suggestions = node.top_suggestions[:self.k]
    
    def get_suggestions(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return [word for word, _ in node.top_suggestions]
```

---

## Ranking Suggestions

```
Ranking factors:
1. Query frequency (how often searched)
2. Recency (recent > old)
3. User context (location, history)
4. Trending boost
5. Personalization

Simple scoring:
score = frequency * recency_decay * context_boost

Where:
recency_decay = e^(-λ * age_days)
```

---

## Data Collection Pipeline

```
User Query → Kafka → Aggregator → Trie Builder

1. User searches "python tutorial"
2. Log sent to Kafka
3. Aggregator counts queries (hourly/daily)
4. Periodic job rebuilds trie with new weights
5. New trie deployed to servers
```

---

## Scaling Strategies

### Partition by Prefix

```
Server 1: a-g
Server 2: h-n
Server 3: o-z

Query "hello" → Server 2

Pros: Simple routing
Cons: Uneven distribution (more 's' words than 'x')
```

### Replicate Everything

```
Each server has complete trie

Pros: Simple, any server handles any query
Cons: Memory intensive, update complexity
```

### Hybrid Approach

```
- Hot prefixes (a, th, wh, etc.) on all servers
- Cold prefixes partitioned
- Cache popular queries
```

---

## Caching

```
Multi-level caching:

1. Browser cache (immediate repeat queries)
2. CDN cache (popular queries)
3. Server-side cache (Redis)
   - Key: prefix
   - Value: top suggestions
   - TTL: 1 hour

Cache hit rates can exceed 90%
```

---

## Real-Time Updates

```
For trending topics:

1. Detect trending queries (sudden frequency spike)
2. Fast-path injection into trie
3. Boost trending score temporarily

Example: Breaking news event
- Query "earthquake california" spikes
- Inject into suggestions within minutes
- Decay boost over hours
```

---

## Key Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Data structure | Trie | Prefix matching efficient |
| Pre-compute | Top K per node | O(1) query time |
| Updates | Periodic batch | Simplicity, consistency |
| Caching | Multi-level | 90%+ hit rate |
| Ranking | Weighted | Frequency + recency |

---

## Key Takeaways

1. **Pre-compute suggestions** at each trie node.
2. **Cache aggressively**—most queries repeat.
3. **Batch updates** for simplicity.
4. **Fast path for trending** content.
5. **Trade storage for latency** (store suggestions at each node).
