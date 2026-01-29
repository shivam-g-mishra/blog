---
sidebar_position: 11
title: "Design Search Engine"
description: >-
  Complete system design for a web search engine. Crawling, indexing,
  ranking, and query processing at scale.
keywords:
  - design search engine
  - web crawler
  - inverted index
  - pagerank
  - search architecture
difficulty: Advanced
estimated_time: 50 minutes
prerequisites:
  - Building Blocks
  - Databases
companies: [Google, Microsoft, Amazon]
---

# Design a Web Search Engine

Building a search engine like Google is one of the most complex system design challenges. Let's break it down.

---

## Requirements

### Functional
- Crawl the web
- Index pages
- Search by keywords
- Rank results by relevance
- Handle billions of queries daily

### Non-Functional
- **Latency:** < 200ms query response
- **Scale:** Billions of pages indexed
- **Freshness:** New content indexed within hours
- **Availability:** 99.99%

---

## High-Level Architecture

```
                              ┌─────────────────┐
                              │   Web Pages     │
                              │  (The Internet) │
                              └────────┬────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Crawling System                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   URL        │  │   Crawler    │  │   Content    │          │
│  │   Frontier   │──▶│   Workers    │──▶│   Store      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Indexing System                           │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Parser     │  │   Index      │  │   Inverted   │          │
│  │   (Extract)  │──▶│   Builder    │──▶│   Index      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Query System                             │
├─────────────────────────────────────────────────────────────────┤
│  User Query                                                      │
│      │                                                           │
│      ▼                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Query      │  │   Index      │  │   Ranking    │          │
│  │   Parser     │──▶│   Lookup     │──▶│   (PageRank) │──▶ Results│
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Web Crawler

### Architecture

```
URL Frontier (Priority Queue)
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│  DNS Resolver → Fetch Page → Parse HTML → Extract URLs          │
└─────────────────────────────────────────────────────────────────┘
       │                              │
       ▼                              ▼
  Store Content                 Add to Frontier
                               (after dedup)
```

### Key Considerations

```
Politeness:
- Respect robots.txt
- Rate limit per domain
- Random delays between requests

Prioritization:
- PageRank score
- Freshness requirements
- Domain importance

Deduplication:
- URL normalization
- Content fingerprinting (simhash)
```

---

## Inverted Index

```
Forward Index:
Doc1: "the quick brown fox"
Doc2: "the lazy dog"
Doc3: "quick brown dog"

Inverted Index:
"the"   → [Doc1, Doc2]
"quick" → [Doc1, Doc3]
"brown" → [Doc1, Doc3]
"fox"   → [Doc1]
"lazy"  → [Doc2]
"dog"   → [Doc2, Doc3]

With positions (for phrase queries):
"quick" → [Doc1:pos2, Doc3:pos1]
```

### Index Structure

```
┌──────────────────────────────────────────────────────────────┐
│  Term Dictionary (In-memory)                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Term → (DocFreq, Pointer to Posting List)              │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Posting Lists (On-disk, compressed)                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ [DocID, TermFreq, Positions]...                        │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## Ranking Algorithm

### TF-IDF (Term Frequency - Inverse Document Frequency)

```
TF = (Term count in doc) / (Total terms in doc)
IDF = log(Total docs / Docs containing term)

Score = TF × IDF
```

### PageRank

```
PageRank models: "A page is important if important pages link to it"

PR(A) = (1-d) + d × Σ(PR(Ti)/C(Ti))

Where:
- d = damping factor (0.85)
- Ti = pages linking to A
- C(Ti) = outbound links from Ti
```

### Modern Ranking (Simplified)

```
Signals:
1. Content relevance (TF-IDF, BM25)
2. Link analysis (PageRank)
3. User signals (click-through rate)
4. Freshness
5. Page quality
6. Personalization
7. Location
8. Device type
```

---

## Query Processing

```
Query: "quick brown fox"

1. Parse & Tokenize
   ["quick", "brown", "fox"]

2. Index Lookup
   quick → [Doc1, Doc3, Doc7, Doc12...]
   brown → [Doc1, Doc3, Doc5...]
   fox   → [Doc1, Doc8...]

3. Intersection
   [Doc1] (appears in all)

4. Scoring
   Score each document

5. Ranking
   Sort by score

6. Return Top K
   [Doc1, Doc3, Doc7...]
```

---

## Scaling

### Sharding the Index

```
By Document (Horizontal):
Shard 1: Docs 0-1M
Shard 2: Docs 1M-2M
...

Query broadcasts to all shards, merge results

By Term (Vertical):
Shard 1: Terms A-M
Shard 2: Terms N-Z

Query routes to relevant shards
```

### Replication

```
Each shard has multiple replicas
- Read scalability
- Fault tolerance
```

---

## Key Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Index storage | SSDs | Fast random access |
| Compression | Yes | Reduce I/O |
| Caching | Query cache | Repeated queries |
| Sharding | By document | Parallel scoring |
| Ranking | Multi-signal | Quality results |

---

## Key Takeaways

1. **Crawling is distributed** with politeness constraints.
2. **Inverted index** enables fast keyword lookup.
3. **Ranking combines multiple signals** (content, links, user behavior).
4. **Sharding by document** enables parallel query processing.
5. **Caching** is critical for common queries.
