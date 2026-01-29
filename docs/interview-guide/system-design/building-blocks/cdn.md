---
sidebar_position: 4
title: "CDN — Content Delivery Networks"
description: >-
  Master CDN concepts for system design interviews. Edge caching, cache
  invalidation, and CDN architecture.
keywords:
  - CDN
  - content delivery network
  - edge caching
  - static content
  - CloudFront
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - Caching
companies: [All Companies]
---

# CDN: Content at the Edge

CDNs serve content from servers closest to users, reducing latency dramatically.

---

## How CDNs Work

```
Without CDN:
User (Tokyo) → Origin Server (US) → Response
Latency: ~200ms

With CDN:
User (Tokyo) → Edge Server (Tokyo) → Response
Latency: ~20ms (if cached)
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Origin Server                            │
│                    (Your application server)                     │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
        ┌─────────┐     ┌─────────┐     ┌─────────┐
        │  Edge   │     │  Edge   │     │  Edge   │
        │  (US)   │     │ (Europe)│     │ (Asia)  │
        └─────────┘     └─────────┘     └─────────┘
              │               │               │
              ▼               ▼               ▼
          US Users       EU Users        Asia Users
```

---

## What to Cache on CDN

| Cache | Don't Cache |
|-------|-------------|
| Static files (JS, CSS, images) | Personalized content |
| Fonts | User-specific data |
| Video/audio files | Real-time data |
| API responses (sometimes) | Sensitive information |
| HTML (with care) | Frequently changing data |

---

## Cache Control Headers

```
# Cache for 1 year (static assets with hash)
Cache-Control: public, max-age=31536000, immutable

# Cache for 1 hour, revalidate after
Cache-Control: public, max-age=3600, must-revalidate

# Don't cache
Cache-Control: no-store

# Private (browser only, not CDN)
Cache-Control: private, max-age=3600
```

---

## Cache Invalidation

```
Methods:

1. TTL-based: Content expires after time
   Cache-Control: max-age=3600

2. Cache busting: Change URL on update
   /static/app.abc123.js → /static/app.def456.js

3. Purge API: Explicitly invalidate
   POST /cdn/purge {"path": "/images/*"}

4. Versioning: Include version in URL
   /v2/api/users
```

---

## CDN Providers

| Provider | Strengths |
|----------|-----------|
| **CloudFront** | AWS integration |
| **Cloudflare** | DDoS protection, free tier |
| **Akamai** | Enterprise, largest network |
| **Fastly** | Real-time purging |
| **Google Cloud CDN** | GCP integration |

---

## Interview Tips

### When to Mention CDN

- Static content delivery
- Global user base
- High read traffic
- Media streaming
- Reducing origin load

### Design Considerations

```
1. Cache hit ratio: Higher = better
2. TTL strategy: Balance freshness vs efficiency
3. Cache invalidation: How to update content?
4. Origin shield: Protect origin from thundering herd
5. Cost: Pay per GB transferred
```

---

## Key Takeaways

1. **CDN reduces latency** by serving from edge.
2. **Cache static content** aggressively with long TTL.
3. **Cache busting** via URL hashing for updates.
4. **Consider cache invalidation** strategy upfront.
5. **Origin shield** protects origin from cache misses.
