---
sidebar_position: 8
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

### Waterfall View
A visualization of a distributed trace showing spans as horizontal bars on a timeline. The hierarchical layout reveals parent-child relationships, parallel vs. sequential execution, and where time is spent. Also called a Gantt chart view or trace timeline.

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

### Exemplar
A sample trace ID attached to a metric observation, enabling direct navigation from a metric data point to an example trace. When you see high p99 latency, exemplars let you jump directly to a specific slow request trace.

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

### Canonical Log Line
A logging pattern where one comprehensive log entry is emitted per request containing all relevant information (timing, user context, business data, outcome). Reduces log volume while improving queryability compared to scattered partial log entries.

### Log Correlation
Linking logs to related traces using trace_id, enabling navigation from log entries to distributed traces.

---

## Alerting

### Alert
A notification triggered when a defined condition is met, intended to prompt human action. Good alerts are actionable, significant, and require immediate attention.

### Alert Fatigue
The phenomenon where responders become desensitized to alerts due to high volume or low signal-to-noise ratio. Leads to slow response times and missed incidents.

### Burn Rate
The rate at which error budget is being consumed relative to the sustainable rate. A burn rate of 2x means budget will be exhausted in half the expected time.

### Runbook
A documented procedure for responding to a specific alert or incident type. Contains diagnosis steps, common causes, and remediation actions.

### On-Call
The practice of having engineers available to respond to production incidents outside normal working hours. Typically involves rotating schedules and escalation paths.

### Escalation
The process of involving additional or more senior responders when an incident isn't resolved within expected timeframes or requires additional expertise.

### Paging
The act of sending an urgent notification (typically via phone/SMS/app) to an on-call responder requiring immediate attention.

### Severity
Classification of alert importance. Common levels: Critical (page immediately), Warning (address soon), Info (no action needed).

### Inhibition
Suppressing alerts when a related, more significant alert is already firing. Prevents alert storms during cascading failures.

### Deduplication
Grouping multiple instances of the same alert into a single notification. Reduces noise during widespread issues.

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
| TSDB | Time Series Database |
| USE | Utilization, Saturation, Errors |

---

This glossary covers the essential terminology for understanding and discussing observability systems. As you work with these technologies, these concepts will become second nature.
