---
slug: scalable-observability-architecture
title: "Designing Scalable Observability: A Five-Layer Architecture for Enterprise Workloads"
authors: [shivam]
tags: [observability, opentelemetry, kafka, kubernetes, architecture, tempo, mimir, loki, enterprise]
description: A deep dive into scalable observability architecture - five-layer design with Kafka buffering, intelligent sampling, object storage backends, and production deployment patterns for enterprise workloads.
image: /img/scalable-observability.png
---

A deep dive into scalable observability architecture—the five-layer design pattern that handles millions of events per second while reducing costs by 90% compared to commercial alternatives.

<!-- truncate -->

This is **Part 3** of our observability series:
1. [Fundamentals](../observability-fundamentals-architects-guide) — Core concepts and architecture
2. [Single-Node Setup](../single-node-observability-setup) — Practical deployment guide
3. **Scalable Architecture** (this article) — Enterprise patterns

## The Cost That Started It All

This architecture was born from a real problem. We built a system center agent—a Go application collecting metadata from 5,000+ data center nodes. For monitoring, we chose a well-known commercial platform.

The first invoice? **$150,000 for a single month.**

At $25/node for infrastructure monitoring plus $12/node for APM, the annual cost would exceed **$1.5 million**—just to observe our own infrastructure.

That's when we decided to build something different.

## When You Need to Scale

The [single-node setup](../single-node-observability-setup) handles most workloads, but you need more when:

| Trigger | Why It Matters |
|---------|----------------|
| >50K events/second sustained | Single-node throughput limit |
| 99.9%+ uptime for observability | Can't have SPOF |
| Multi-region deployment | Latency-sensitive collection |
| Compliance requirements | Zero data loss mandate |
| Query performance degrading | Storage/compute separation needed |

**Signs you're approaching single-node limits:**
- Collector queue consistently > 5,000 items
- Memory usage > 80% of limits
- Query latency increasing in Grafana
- "Dropped spans" alerts firing

## The Design Philosophy

Before diving into components, let me explain the principles guiding this architecture:

### 1. Decouple Ingestion from Processing

In single-node, the Collector exports directly to backends. If Jaeger is slow, the Collector slows down.

The scalable architecture introduces **Kafka** between ingestion and processing. Collectors accept data at full speed regardless of backend health. Data is durably stored until processors are ready.

### 2. Scale Components Independently

Different bottlenecks require different solutions:
- CPU-bound on processing? Add processors.
- Network-bound on ingestion? Add gateways.
- Storage-bound? Add object storage capacity.

### 3. Accept Graceful Degradation

Total failure should be rare. Partial degradation—slower queries, some sampling, delayed processing—is an acceptable trade-off for resilience.

### 4. Optimize for the Common Case

Most telemetry isn't interesting. Most traces succeed. Most logs are routine. Optimize for high-volume, low-value data while ensuring high-value data (errors, anomalies) is always preserved.

## The Architecture at a Glance

One sentence:

> **Applications send telemetry to gateway collectors, which buffer it in Kafka, where processor collectors consume it, apply sampling and enrichment, and write to specialized storage backends that Grafana queries.**

Visual representation:

```
Applications → Gateways → Kafka → Processors → Storage → Grafana
                 ↑                    ↑           ↑
              (scale)             (sample)    (cheap S3)
```

## The Five-Layer Architecture

```
                               YOUR APPLICATIONS
                     (Instrumented with OpenTelemetry SDKs)
                                     │
                                     │ OTLP Protocol
                                     ▼
    ┌───────────────────────────────────────────────────────────────────┐
    │                       LAYER 1: INGESTION                          │
    │                                                                   │
    │                    ┌─────────────────┐                            │
    │                    │  Load Balancer  │  HAProxy, NGINX, or        │
    │                    │   (Port 4317)   │  cloud LB                  │
    │                    └────────┬────────┘                            │
    │                             │                                     │
    │          ┌──────────────────┼──────────────────┐                  │
    │          ▼                  ▼                  ▼                  │
    │       ┌──────┐          ┌──────┐          ┌──────┐                │
    │       │ GW 1 │          │ GW 2 │          │ GW N │                │
    │       │      │          │      │          │      │                │
    │       └──┬───┘          └──┬───┘          └──┬───┘                │
    │          │                 │                 │   OTel Collector    │
    │          │                 │                 │   (Gateway mode)    │
    │          │                 │                 │   Stateless         │
    └──────────┼─────────────────┼─────────────────┼────────────────────┘
               │                 │                 │
               └─────────────────┼─────────────────┘
                                 │
                                 ▼
    ┌───────────────────────────────────────────────────────────────────┐
    │                       LAYER 2: BUFFERING                          │
    │                                                                   │
    │                ┌────────────────────────────┐                     │
    │                │        Apache Kafka        │                     │
    │                │                            │                     │
    │                │  Topics:                   │                     │
    │                │  • otlp-traces   (12 part) │                     │
    │                │  • otlp-metrics  (12 part) │                     │
    │                │  • otlp-logs     (12 part) │                     │
    │                │                            │                     │
    │                │  Replicated, durable       │                     │
    │                │  24-hour retention         │                     │
    │                └────────────────────────────┘                     │
    │                                                                   │
    │    Why Kafka?                                                     │
    │    • Decouples ingestion from processing                          │
    │    • Survives backend outages                                     │
    │    • Enables replay for reprocessing                              │
    │    • Horizontal scaling via partitions                            │
    └─────────────────────────────┬─────────────────────────────────────┘
                                  │
                                  ▼
    ┌───────────────────────────────────────────────────────────────────┐
    │                       LAYER 3: PROCESSING                         │
    │                                                                   │
    │          ┌──────────────────┼──────────────────┐                  │
    │          ▼                  ▼                  ▼                  │
    │       ┌──────┐          ┌──────┐          ┌──────┐                │
    │       │ P 1  │          │ P 2  │          │ P N  │                │
    │       │ ┌──┐ │          │ ┌──┐ │          │ ┌──┐ │                │
    │       │ │TML│ │          │ │TML│ │          │ │TML│ │                │
    │       │ └──┘ │          │ └──┘ │          │ └──┘ │                │
    │       └──────┘          └──────┘          └──────┘                │
    │                                                                   │
    │    OTel Collector (Processor mode) handles:                       │
    │    • Tail-based sampling (keep errors, sample success)            │
    │    • Filtering (drop health checks, noise)                        │
    │    • Enrichment (add K8s labels, environment)                     │
    │    • Batching (efficient writes)                                  │
    └─────────────────────────────┬─────────────────────────────────────┘
                                  │
                                  ▼
    ┌───────────────────────────────────────────────────────────────────┐
    │                        LAYER 4: STORAGE                           │
    │                                                                   │
    │       ┌─────────────┐   ┌─────────────┐   ┌─────────────┐         │
    │       │   Tempo     │   │   Mimir     │   │    Loki     │         │
    │       │  (Traces)   │   │  (Metrics)  │   │   (Logs)    │         │
    │       │             │   │             │   │             │         │
    │       │  TraceQL    │   │  PromQL     │   │  LogQL      │         │
    │       └──────┬──────┘   └──────┬──────┘   └──────┬──────┘         │
    │              │                 │                 │                │
    │              └─────────────────┼─────────────────┘                │
    │                                │                                  │
    │                                ▼                                  │
    │                ┌────────────────────────────┐                     │
    │                │      Object Storage        │                     │
    │                │     (S3 / MinIO / GCS)     │                     │
    │                │                            │                     │
    │                │  • Eleven 9s durability    │                     │
    │                │  • ~$0.02/GB/month         │                     │
    │                │  • Unlimited capacity      │                     │
    │                └────────────────────────────┘                     │
    └─────────────────────────────┬─────────────────────────────────────┘
                                  │
                                  ▼
    ┌───────────────────────────────────────────────────────────────────┐
    │                     LAYER 5: VISUALIZATION                        │
    │                                                                   │
    │                ┌────────────────────────────┐                     │
    │                │         Grafana            │                     │
    │                │    (HA with PostgreSQL)    │                     │
    │                │                            │                     │
    │                │  • Unified dashboards      │                     │
    │                │  • Trace-log correlation   │                     │
    │                │  • Alerting                │                     │
    │                └────────────────────────────┘                     │
    └───────────────────────────────────────────────────────────────────┘
```

## Layer Deep Dives

### Layer 1: Ingestion (The Front Door)

Gateway Collectors are OpenTelemetry Collectors configured for one job: accept telemetry fast and get it into Kafka reliably.

```yaml
# Gateway collector config (simplified)
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317

processors:
  batch:
    timeout: 200ms
    send_batch_size: 8192

exporters:
  kafka:
    brokers: ["kafka-0:9092", "kafka-1:9092", "kafka-2:9092"]
    topic: otlp-traces
    encoding: otlp_proto

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [kafka]
```

**Key characteristics:**
- **Stateless**: No data stored beyond in-flight batches
- **Fast**: Minimal processing, just validation and batching
- **Scalable**: Add instances behind load balancer

### Layer 2: Buffering (The Shock Absorber)

Kafka provides the durability and decoupling that makes this architecture reliable.

**Why Kafka specifically?**

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| Redis Streams | Simple, low latency | Limited durability | Good for small scale |
| RabbitMQ | Feature-rich | Not built for this throughput | Not suitable |
| Apache Pulsar | Modern, cloud-native | Smaller community | Viable alternative |
| **Apache Kafka** | Proven at scale, durable | Operational complexity | **Our choice** |

**Topic design:**
- `otlp-traces` — Trace spans (12 partitions)
- `otlp-metrics` — Metric data (12 partitions)
- `otlp-logs` — Log records (12 partitions)

**Why 12 partitions?** Partitions enable parallel processing. 12 is a good starting point—divisible by 2, 3, 4, and 6 for flexible consumer scaling.

**Retention:** 24 hours. This provides a buffer for downstream outages without excessive storage.

### Layer 3: Processing (The Smart Filter)

This is where intelligence happens. Processor collectors consume from Kafka and apply transformations.

**Critical function: Tail-based sampling**

```yaml
processors:
  tail_sampling:
    decision_wait: 10s
    num_traces: 100000
    policies:
      # Keep all errors
      - name: keep-errors
        type: status_code
        status_code:
          status_codes: [ERROR]
      
      # Keep slow traces
      - name: keep-slow
        type: latency
        latency:
          threshold_ms: 1000
      
      # Sample the rest
      - name: sample-remainder
        type: probabilistic
        probabilistic:
          sampling_percentage: 10
```

**Impact of sampling:**

```
Input: 100,000 traces
├── 500 contain errors → Keep all (0.5%)
├── 2,000 are slow (>1s) → Keep all (2%)
└── 97,500 normal → Keep 9,750 (10% sample)

Output: ~12,250 traces (87.75% reduction)

What you lose: Random successful, fast traces
What you keep: Everything you'd actually investigate
```

### Layer 4: Storage (The Long-Term Memory)

Each signal has different access patterns, so we use optimized backends.

**Tempo for Traces**

Why Tempo over Jaeger for scalable deployments?
- **Object storage native**: No Cassandra/Elasticsearch to manage
- **Cost efficient**: S3 is dramatically cheaper than database storage
- **TraceQL**: Powerful query language

**Mimir for Metrics**

Why Mimir over Prometheus?
- **Horizontal scaling**: Prometheus is single-node; Mimir distributes
- **Object storage**: Unlimited retention at S3 prices
- **100% PromQL compatible**: Existing queries work unchanged

**Loki for Logs**

Why Loki over Elasticsearch?
- **Index only labels**: Not every word in every log
- **Storage**: ~3x raw log size vs. 10x+ for Elasticsearch
- **Operational simplicity**: Far fewer moving parts

**The Object Storage Secret**

All three backends write to object storage (S3, MinIO, GCS):
- **Cost**: ~$0.02/GB/month vs. $0.10+ for block storage
- **Durability**: 99.999999999% (eleven nines)
- **Capacity**: Unlimited—just keep adding data

## Technology Selection Rationale

### Single-Node vs. Scalable Backend Choices

| Component | Single-Node | Scalable | Why the Change |
|-----------|-------------|----------|----------------|
| Traces | Jaeger (Badger) | Tempo (S3) | Horizontal scale, object storage |
| Metrics | Prometheus | Mimir | HA, unlimited retention |
| Logs | Loki | Loki (S3) | Same, just add object storage |
| Buffer | None | Kafka | Decoupling, durability |

### Why Not Just Scale Prometheus?

Prometheus is fundamentally single-node. Options like Thanos and Cortex add complexity. Mimir is designed from the ground up for horizontal scaling while maintaining full PromQL compatibility.

## Cost Analysis

### Self-Hosted vs. Commercial

| Scale | Self-Hosted | Commercial | Annual Savings |
|-------|-------------|------------|----------------|
| Small (500 hosts) | ~$300/mo | ~$25K/mo | ~$300K |
| Medium (2K hosts) | ~$2K/mo | ~$80K/mo | ~$936K |
| Enterprise (5K+) | ~$15K/mo | ~$150K/mo | ~$1.6M |

### Infrastructure Costs Breakdown (Medium Scale)

| Component | Instances | Spec | Monthly Cost |
|-----------|-----------|------|--------------|
| Gateway Collectors | 3 | 4 CPU, 8GB | $150 |
| Kafka | 3 | 4 CPU, 16GB, 500GB SSD | $450 |
| Processors | 6 | 4 CPU, 8GB | $300 |
| Storage Backends | 3 | 8 CPU, 32GB | $600 |
| Grafana | 2 | 2 CPU, 4GB | $80 |
| Object Storage | - | 10TB | $200 |
| **Total** | | | **~$1,800/mo** |

### The Hidden Cost: Operations

Self-hosting isn't free. Budget for:

| Activity | Time Investment |
|----------|-----------------|
| Initial setup | 2-4 weeks |
| Ongoing maintenance | 0.5-1.0 FTE |
| Incident response | Variable |
| Upgrades/patches | Monthly |

**When to stay commercial:**
- Team < 10 engineers
- No Kubernetes/infrastructure expertise
- Observability isn't core competency
- Budget isn't a constraint

**When to self-host:**
- Budget constrained relative to scale
- Have infrastructure expertise
- Data sovereignty requirements
- Want unlimited customization

## Implementation Paths

### Docker Compose (Phase 2)

For teams not on Kubernetes, the scalable architecture runs in Docker Compose:

```bash
cd docs/scalable/configs/docker
docker compose -f docker-compose-scalable.yaml up -d

# Scale collectors
docker compose up -d --scale otel-gateway=3 --scale otel-processor=6
```

### Kubernetes (Phase 3)

For production Kubernetes deployments:

```bash
cd docs/scalable/configs/kubernetes

# Prerequisites
kubectl create namespace kafka
kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka'

# Deploy stack
kubectl apply -f namespace.yaml
kubectl apply -f minio.yaml
kubectl apply -f kafka-cluster.yaml
# ... see implementation guide for full order
```

### Terraform + AWS (Phase 4)

For infrastructure-as-code deployments:

```bash
cd docs/scalable/configs/terraform
terraform init
terraform plan -var-file=production.tfvars
terraform apply
```

## Common Mistakes to Avoid

From our production experience:

### 1. Over-engineering from Day One

**Mistake**: Building the full five-layer architecture for 1,000 events/second.

**Reality**: Single-node handles 50K events/second. Start simple.

### 2. Keeping All Traces

**Mistake**: "We might need them!"

**Reality**: 90% of traces are successful, normal-latency requests you'll never look at. Sample aggressively.

### 3. Underestimating Kafka Operations

**Mistake**: "Kafka is just a message queue."

**Reality**: Kafka requires operational expertise. Plan for broker failures, partition rebalancing, and consumer lag monitoring.

### 4. Ignoring the Collector

**Mistake**: Focusing on backends while running a single, under-resourced Collector.

**Reality**: The Collector is your first line of defense. Give it resources and redundancy.

### 5. Not Testing Failure Modes

**Mistake**: Only testing the happy path.

**Reality**: Kill components. Simulate network partitions. Understand how the system degrades.

## Evolution Path

```
┌─────────────────┐
│    Phase 1      │
│  Single Node    │  ← Start here
│  ~$200/month    │
└────────┬────────┘
         │
         │  Hit 50K events/sec or need HA?
         ▼
┌─────────────────┐
│    Phase 2      │
│  + Kafka        │
│  ~$1,500/month  │
└────────┬────────┘
         │
         │  Need auto-scaling or multi-region?
         ▼
┌─────────────────┐
│    Phase 3      │
│  Kubernetes     │
│  + HPA          │
│  Variable       │
└────────┬────────┘
         │
         │  Need managed infrastructure?
         ▼
┌─────────────────┐
│    Phase 4      │
│  Terraform      │
│  + AWS/GCP      │
│  Cloud pricing  │
└─────────────────┘
```

## Key Metrics to Monitor (Your Own Stack)

| Metric | Warning | Critical |
|--------|---------|----------|
| Collector queue depth | >5,000 | >8,000 |
| Kafka consumer lag | >10,000 | >50,000 |
| Processor memory | >70% | >85% |
| Object storage latency | >100ms | >500ms |
| Query latency P99 | >5s | >30s |

## Final Thoughts

Building self-hosted observability is a significant undertaking. But for organizations where:

- Observability costs are a meaningful percentage of infrastructure spend
- You have the infrastructure expertise
- Data ownership matters

...the ROI is compelling. We achieved **90%+ cost savings** while maintaining the visibility needed to run reliable production systems.

Start with Phase 1. Scale when you hit real limitations. The architecture grows with you.

---

## Resources

- **GitHub Repository**: [opensource-otel-setup](https://github.com/shivam-g-mishra/opensource-otel-setup)
- **Architecture Deep Dive**: [Architecture Documentation](https://github.com/shivam-g-mishra/opensource-otel-setup/blob/main/docs/scalable/architecture.md)
- **Implementation Guide**: [Step-by-Step Guide](https://github.com/shivam-g-mishra/opensource-otel-setup/blob/main/docs/scalable/implementation-guide.md)
- **Configuration Files**: [All Configs](https://github.com/shivam-g-mishra/opensource-otel-setup/tree/main/docs/scalable/configs)

---

*Building observability at scale? I'd love to hear about your experience. Connect on [LinkedIn](https://www.linkedin.com/in/shivam-g-mishra).*
