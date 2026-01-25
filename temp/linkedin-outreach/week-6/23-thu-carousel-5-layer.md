# Post #23: The 5-Layer Architecture
**Week 6 | Thursday | 7:00 AM PT**
**Format:** Carousel (PDF upload)
**Blog Link:** Scalable Architecture

---

## CAPTION (Copy everything below the line)

---

How we handle millions of events per second.

Our 5-layer observability architecture ⬇️

---
#Observability #Architecture #DevOps #Scale

💡 Full breakdown in comments

---

## FIRST COMMENT (Post within 60 seconds)

📚 Complete architecture documentation:

https://blog.shivam.info/blog/scalable-observability-architecture?utm_source=linkedin&utm_medium=social&utm_campaign=week6

Comment "ARCH" for the direct link!

---

## CAROUSEL SLIDES (Create in Canva - 1080x1350px)

### Slide 1 (Cover)
```
THE 5-LAYER
OBSERVABILITY ARCHITECTURE

Handling millions of events/sec
at 90% cost reduction

[Swipe →]
```

### Slide 2
```
LAYER 1: COLLECTION

OpenTelemetry SDK in every app
     ↓
Local OTel Collector (sidecar)

Unified collection.
One SDK for everything.
```

### Slide 3
```
LAYER 2: AGGREGATION

Regional OTel Collectors
• Batch and compress
• Sample intelligently
• Add metadata
• Route by type

Reduce volume before it leaves the region.
```

### Slide 4
```
LAYER 3: BUFFERING

Kafka Cluster
• Absorb traffic spikes
• Enable replay
• Decouple producers/consumers
• Zero data loss

The reliability backbone.
```

### Slide 5
```
LAYER 4: STORAGE

Metrics → Prometheus/Mimir
Logs → Loki
Traces → Tempo/Jaeger

Object storage (S3/MinIO) for
long-term, cheap retention.
```

### Slide 6
```
LAYER 5: VISUALIZATION

Grafana
• Unified dashboards
• Cross-data-source queries
• Alerting
• Explore mode

One UI for everything.
```

### Slide 7
```
THE FLOW:

App → Collector → Kafka → Storage → Grafana

Each layer adds:
• Reliability
• Scalability
• Flexibility

But also complexity.
```

### Slide 8 (CTA)
```
DON'T START HERE.

This is where we ended up.
Not where we started.

Start with single-node.
Scale when you need to.

Full guide: Comment "ARCH"

blog.shivam.info
```
