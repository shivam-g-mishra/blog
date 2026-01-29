---
sidebar_position: 7
title: "Design Netflix — Video Streaming at Scale"
description: >-
  Complete system design for Netflix. Content delivery, recommendation engine,
  encoding pipeline, and global distribution.
keywords:
  - design netflix
  - video streaming
  - content delivery
  - recommendation system
  - CDN architecture
difficulty: Advanced
estimated_time: 50 minutes
prerequisites:
  - YouTube Case Study
  - CDN Concepts
companies: [Netflix, Disney+, Amazon Prime, HBO Max]
---

# Design Netflix: Entertainment at Global Scale

Netflix serves 200M+ subscribers across 190 countries. The challenge: deliver high-quality video with minimal buffering worldwide.

---

## Requirements

### Functional
- Browse and search content
- Stream video (multiple devices)
- Personalized recommendations
- Download for offline viewing
- Multiple profiles per account
- Continue watching across devices

### Non-Functional
- **Availability:** 99.99%
- **Latency:** Start playback < 2 seconds
- **Scale:** 200M subscribers, peak 15M concurrent streams
- **Quality:** Adaptive bitrate, 4K HDR support

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Apps                              │
│  (Web, iOS, Android, Smart TV, Gaming Consoles, Roku, etc.)     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     AWS / Netflix Cloud                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   API        │  │   User       │  │ Recommendation│          │
│  │   Gateway    │  │   Service    │  │   Engine      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Content    │  │   Search     │  │   Analytics  │          │
│  │   Service    │  │   Service    │  │   Service    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Open Connect CDN                             │
│  (Netflix's own CDN - deployed in ISPs worldwide)               │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│  │  OCA 1  │  │  OCA 2  │  │  OCA 3  │  │  OCA N  │           │
│  │ (ISP A) │  │ (ISP B) │  │ (ISP C) │  │ (ISP N) │           │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Content Ingestion Pipeline

```
1. Original Content (Studio Master)
   │
   ▼
2. Quality Control
   │
   ▼
3. Encoding Pipeline
   ├── Multiple resolutions (480p, 720p, 1080p, 4K)
   ├── Multiple codecs (H.264, H.265, VP9, AV1)
   ├── Multiple bitrates per resolution
   └── Audio tracks (5.1, Atmos, multiple languages)
   │
   ▼
4. Content Store (S3)
   │
   ▼
5. Open Connect CDN Distribution
   │
   ▼
6. Available for Streaming
```

### Encoding Details

```
Per-Title Encoding:
- Analyze content complexity
- Action movie: Higher bitrate for same quality
- Animated: Lower bitrate sufficient

Output per title:
- ~1200 different files
- Multiple resolutions × bitrates × codecs × audio
- Optimized for every device/network combination
```

---

## Open Connect CDN

Netflix's secret weapon: **Own CDN deployed inside ISPs**.

```
Traditional CDN:
User → ISP → Internet → CDN Edge → Content

Netflix Open Connect:
User → ISP → OCA (inside ISP) → Content

Benefits:
- Lower latency (no internet traversal)
- Lower cost for ISPs (less backbone traffic)
- Higher quality (dedicated hardware)
```

### OCA (Open Connect Appliance)

```
Hardware:
- Custom servers with 100+ TB storage
- Optimized for video delivery
- Placed directly in ISP data centers

Content Population:
- Predictive: Pre-populate likely popular content
- Reactive: Cache on first request
- Tiered: Hot content in fast storage, cold in HDD
```

---

## Playback Flow

```
1. User clicks "Play"
   │
   ▼
2. Client requests playback URL from Playback Service
   │
   ▼
3. Playback Service:
   ├── Authenticate user
   ├── Check subscription/license
   ├── Select optimal server (OCA)
   └── Generate manifest URL
   │
   ▼
4. Client fetches manifest (list of available streams)
   │
   ▼
5. Client selects initial quality based on bandwidth
   │
   ▼
6. Client starts streaming from nearest OCA
   │
   ▼
7. Continuous adaptation:
   └── Monitor bandwidth → adjust quality in real-time
```

---

## Recommendation Engine

Netflix's recommendation system drives 80% of content watched.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Recommendation Pipeline                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Data Collection                                                 │
│  ├── Viewing history                                            │
│  ├── Search queries                                             │
│  ├── Browse behavior                                            │
│  ├── Time of day                                                │
│  ├── Device type                                                │
│  └── Ratings/thumbs                                             │
│                                                                  │
│  Algorithms                                                      │
│  ├── Collaborative filtering                                    │
│  ├── Content-based filtering                                    │
│  ├── Deep learning models                                       │
│  └── A/B testing framework                                      │
│                                                                  │
│  Output                                                          │
│  ├── Personalized rows                                          │
│  ├── Personalized artwork                                       │
│  ├── Personalized previews                                      │
│  └── "Because you watched X"                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Storage

| Data Type | Storage | Why |
|-----------|---------|-----|
| User data | Cassandra | Scale, availability |
| Viewing history | Cassandra | Time-series, write-heavy |
| Content metadata | MySQL + Cassandra | Structured + scale |
| Video files | S3 + OCA | Object storage + CDN |
| Search index | Elasticsearch | Full-text search |
| Recommendations | Precomputed + cache | Low latency |

---

## Handling Scale

### Peak Traffic (15M concurrent)

```
Strategy:
1. Predictive scaling based on historical patterns
2. Content pre-positioned on OCAs
3. Fallback tiers if primary OCA overloaded
4. Graceful degradation (lower quality if needed)
```

### New Release (Stranger Things premiere)

```
Preparation:
1. Predict demand by region
2. Pre-populate content on all OCAs
3. Scale backend services
4. Monitor in real-time
5. Adjust distribution as viewing patterns emerge
```

---

## Key Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| CDN | Own (Open Connect) | Control, cost, quality |
| Encoding | Per-title optimization | Quality vs bandwidth |
| Streaming | Adaptive bitrate | Variable network conditions |
| Recommendations | Precomputed | Sub-second latency |
| Storage | Tiered | Hot/cold data optimization |

---

## Key Takeaways

1. **Own your CDN** at Netflix scale—control and cost benefits.
2. **Per-title encoding** optimizes quality for each content type.
3. **Predictive distribution** pre-positions content before demand.
4. **Recommendations drive engagement**—80% of watching is recommended.
5. **Adaptive streaming** handles variable network conditions.
