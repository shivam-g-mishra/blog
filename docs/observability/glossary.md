---
sidebar_position: 4
title: Observability Glossary
description: Common terms and concepts in observability, distributed tracing, and the OpenTelemetry ecosystem.
keywords: [observability glossary, MTTD, MTTR, SLO, SLI, cardinality, span, trace]
---

# Observability Glossary

A reference guide to common terms you'll encounter when building and operating observability systems.

## Core Concepts

### Observability
The ability to understand the internal state of a system by examining its external outputs (traces, metrics, logs). Unlike monitoring, which answers predetermined questions, observability enables asking arbitrary questions about system behavior.

### Telemetry
Data collected from systems to understand their behavior. In observability, telemetry refers to the three signals: traces, metrics, and logs.

### Instrumentation
The process of adding code to collect telemetry data from an application. Can be manual (explicit code) or automatic (framework-level hooks).

---

## Distributed Tracing

### Trace
A complete record of a request's journey through a distributed system. Contains multiple spans representing individual operations.

### Span
A single operation within a trace. Spans have:
- A name (e.g., "HTTP GET /api/orders")
- Start and end timestamps (duration)
- Attributes (key-value metadata)
- Status (OK, Error)
- Parent span reference

### Trace ID
A globally unique identifier that correlates all spans belonging to a single trace. Format: 32-character hex string (128 bits).

### Span ID
A unique identifier for a single span within a trace. Format: 16-character hex string (64 bits).

### Parent Span
The span that initiated the current span. The root span has no parent.

### Context Propagation
The mechanism for passing trace context (trace ID, span ID) between services. Typically done via HTTP headers or message metadata.

### Sampling
The practice of keeping only a subset of traces to reduce storage and processing costs. Types include:
- **Head sampling**: Decision made at trace start
- **Tail sampling**: Decision made after trace completes (can keep all errors)
- **Probabilistic sampling**: Random selection based on percentage

### Baggage
Key-value pairs that propagate across service boundaries along with trace context. Useful for passing request-scoped data.

---

## Metrics

### Metric
A numerical measurement collected at regular intervals. Types include counters, gauges, and histograms.

### Counter
A metric that only increases (or resets to zero). Examples: total requests, total errors.

### Gauge
A metric that can increase or decrease. Examples: current queue depth, temperature, active connections.

### Histogram
A metric that captures the distribution of values. Enables calculating percentiles (p50, p95, p99).

### Cardinality
The number of unique combinations of label values for a metric. High cardinality (e.g., user_id as a label) can overwhelm metrics systems.

### Label / Tag / Attribute
Key-value pairs attached to metrics to enable filtering and aggregation. Example: `http_requests_total{method="GET", status="200"}`.

### Time Series
A sequence of metric values over time, identified by a unique combination of metric name and labels.

### Scraping
Pull-based metric collection where a collector periodically fetches metrics from targets. Prometheus uses this model.

### Push
Push-based metric collection where applications send metrics to a collector. OTLP uses this model.

---

## Logging

### Structured Logging
Logs formatted as key-value pairs (typically JSON) rather than free-form text. Enables efficient querying and analysis.

### Log Level
Severity classification for log entries:
- **ERROR**: Something failed
- **WARN**: Potential issue
- **INFO**: Significant event
- **DEBUG**: Detailed troubleshooting info

### Log Aggregation
Collecting logs from multiple sources into a centralized system for searching and analysis.

### Log Correlation
Linking logs to related traces using trace_id, enabling navigation from log entries to distributed traces.

---

## Reliability Metrics

### SLI (Service Level Indicator)
A quantitative measure of service behavior. Examples:
- Request latency (p99 < 200ms)
- Availability (successful requests / total requests)
- Error rate (errors / total requests)

### SLO (Service Level Objective)
A target value for an SLI. Example: "99.9% of requests should complete in under 200ms."

### SLA (Service Level Agreement)
A contract with customers specifying consequences if SLOs aren't met.

### Error Budget
The amount of acceptable unreliability. If SLO is 99.9%, error budget is 0.1% (about 43 minutes per month).

### MTTD (Mean Time to Detect)
Average time to discover an issue after it begins. Better observability reduces MTTD.

### MTTR (Mean Time to Recover)
Average time to resolve an issue after detection. Better observability reduces MTTR by accelerating root cause analysis.

---

## OpenTelemetry Specific

### OTLP (OpenTelemetry Protocol)
The native protocol for transmitting telemetry data. Supports gRPC (port 4317) and HTTP (port 4318).

### OTel Collector
A vendor-agnostic service for receiving, processing, and exporting telemetry. Components include receivers, processors, and exporters.

### Receiver
Collector component that accepts telemetry data from various sources (OTLP, Jaeger, Prometheus, etc.).

### Processor
Collector component that transforms telemetry (batching, filtering, sampling, attribute manipulation).

### Exporter
Collector component that sends telemetry to backends (Jaeger, Prometheus, Loki, commercial services).

### Pipeline
A configured flow connecting receivers → processors → exporters for a specific signal (traces, metrics, or logs).

### Resource
Attributes describing the entity producing telemetry (service name, version, host, container ID).

### Auto-Instrumentation
Libraries that automatically instrument common frameworks without requiring manual code changes.

---

## Infrastructure & Architecture

### Gateway Pattern
Centralized collectors that receive telemetry from all applications, enabling shared processing and routing.

### Sidecar Pattern
A collector running alongside each application instance, providing local buffering and processing.

### Agent Pattern
A collector running on each host/node, aggregating telemetry from all applications on that host.

### Head-Based Sampling
Sampling decision made at the start of a trace before knowing if it's interesting (fast, but may drop errors).

### Tail-Based Sampling
Sampling decision made after trace completes, allowing decisions based on duration, errors, or attributes (requires more memory).

### Object Storage
Scalable, cost-effective storage (S3, MinIO, GCS) used by modern observability backends for long-term retention.

### Hot Storage
Fast, expensive storage for recent data requiring quick queries.

### Cold Storage
Slower, cheaper storage for historical data with less frequent access.

---

## Query Languages

### PromQL
Prometheus Query Language for querying metrics. Example:
```promql
rate(http_requests_total{status="500"}[5m]) / rate(http_requests_total[5m])
```

### LogQL
Loki Query Language for querying logs. Example:
```logql
{service="api"} |= "error" | json | rate() by (level)
```

### TraceQL
Tempo Query Language for querying traces. Example:
```traceql
{span.http.status_code >= 500} | select(span.http.url)
```

---

## Common Acronyms

| Acronym | Meaning |
|---------|---------|
| APM | Application Performance Monitoring |
| CNCF | Cloud Native Computing Foundation |
| DDoS | Distributed Denial of Service |
| ELK | Elasticsearch, Logstash, Kibana |
| gRPC | Google Remote Procedure Call |
| HA | High Availability |
| K8s | Kubernetes |
| OOM | Out of Memory |
| OTel | OpenTelemetry |
| P99 | 99th percentile |
| RED | Rate, Errors, Duration |
| RPS | Requests Per Second |
| SDK | Software Development Kit |
| SRE | Site Reliability Engineering |
| TSB | Time Series Database |
| USE | Utilization, Saturation, Errors |

---

This glossary covers the essential terminology for understanding and discussing observability systems. As you work with these technologies, these concepts will become second nature.
