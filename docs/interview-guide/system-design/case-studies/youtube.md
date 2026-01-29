---
sidebar_position: 4
title: "Design YouTube — Video Streaming"
description: >-
  Complete system design for YouTube/video streaming. Upload pipeline,
  transcoding, CDN distribution, and video recommendations.
keywords:
  - design youtube
  - video streaming
  - transcoding
  - CDN
  - video platform
difficulty: Advanced
estimated_time: 50 minutes
prerequisites:
  - Building Blocks
  - Databases
companies: [Google, Netflix, TikTok, Twitch]
---

# Design YouTube: Video at Scale

YouTube serves 1 billion hours of video daily. The challenges: upload processing, adaptive streaming, and global delivery.

---

## Requirements

### Functional
- Upload videos
- Watch videos (streaming)
- Search videos
- Comments, likes, subscriptions
- Video recommendations

### Non-Functional
- **Availability:** 99.99%
- **Latency:** Start playback < 2 seconds
- **Scale:** 1B daily users, 500 hours uploaded/minute

---

## High-Level Architecture

```
┌─────────┐     ┌─────────────┐     ┌─────────────────┐
│ Clients │────▶│ API Gateway │────▶│ Video Service   │
└─────────┘     └─────────────┘     └────────┬────────┘
     │                                       │
     │          ┌────────────────────────────┼────────────────────────────┐
     │          │                            │                            │
     │          ▼                            ▼                            ▼
     │   ┌─────────────┐            ┌─────────────┐            ┌─────────────┐
     │   │Upload       │            │ Transcoding │            │ Metadata    │
     │   │Service      │            │ Service     │            │ Service     │
     │   └─────────────┘            └─────────────┘            └─────────────┘
     │          │                            │
     │          ▼                            ▼
     │   ┌─────────────┐            ┌─────────────┐
     │   │Original     │            │ Transcoded  │
     │   │Storage (S3) │            │ Storage     │
     │   └─────────────┘            └─────────────┘
     │                                       │
     │                                       ▼
     └──────────────────────────────▶ ┌─────────────┐
                                      │    CDN      │
                                      └─────────────┘
```

---

## Upload Pipeline

```
1. Client uploads video
   │
   ▼
2. Upload Service
   - Generate upload URL (presigned S3)
   - Store metadata in DB
   │
   ▼
3. Original Storage (S3)
   │
   ▼
4. Transcoding Queue (SQS/Kafka)
   │
   ▼
5. Transcoding Workers
   - Multiple resolutions (240p, 360p, 720p, 1080p, 4K)
   - Multiple formats (H.264, VP9, AV1)
   - Generate thumbnails
   │
   ▼
6. Transcoded Storage
   │
   ▼
7. CDN Push
   │
   ▼
8. Update metadata: "ready to watch"
```

---

## Adaptive Bitrate Streaming

```
Manifest file (HLS/DASH):
#EXTM3U
#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=640x360
360p/playlist.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=1400000,RESOLUTION=1280x720
720p/playlist.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1920x1080
1080p/playlist.m3u8

Client:
1. Fetch manifest
2. Measure bandwidth
3. Request appropriate quality
4. Switch dynamically as bandwidth changes
```

---

## Video Storage

```
video_id: abc123

Storage structure:
/videos/abc123/
  ├── original.mp4
  ├── 240p/
  │   ├── segment_001.ts
  │   ├── segment_002.ts
  │   └── playlist.m3u8
  ├── 360p/
  ├── 720p/
  ├── 1080p/
  └── thumbnails/
      ├── thumb_1.jpg
      └── thumb_2.jpg
```

---

## CDN Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                      Origin (S3)                            │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
   ┌─────────┐         ┌─────────┐         ┌─────────┐
   │CDN Edge │         │CDN Edge │         │CDN Edge │
   │(US-West)│         │(Europe) │         │(Asia)   │
   └─────────┘         └─────────┘         └─────────┘
        │                   │                   │
        ▼                   ▼                   ▼
     Users                Users               Users

Popular videos: Cached at edge (99% hit rate)
Long tail: Origin fetch, cache locally
```

---

## Database Schema

```sql
-- Videos
CREATE TABLE videos (
    video_id UUID PRIMARY KEY,
    user_id UUID,
    title TEXT,
    description TEXT,
    status TEXT,  -- uploading, processing, ready, failed
    duration INT,
    view_count BIGINT,
    created_at TIMESTAMP
);

-- Video URLs
CREATE TABLE video_urls (
    video_id UUID,
    resolution TEXT,
    url TEXT,
    PRIMARY KEY (video_id, resolution)
);
```

---

## Key Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Video format | HLS/DASH | Adaptive streaming |
| Storage | S3 + CDN | Scalable, global |
| Transcoding | Async workers | CPU intensive |
| Metadata | PostgreSQL | Structured queries |
| View counts | Redis + async | High throughput |

---

## Key Takeaways

1. **Async transcoding pipeline** for CPU-intensive work.
2. **Adaptive bitrate streaming** (HLS/DASH) for quality adjustment.
3. **CDN caching** is critical—most views are from cache.
4. **Segment-based storage** enables seeking and switching quality.
5. **Popular content caching** handles the long tail efficiently.
