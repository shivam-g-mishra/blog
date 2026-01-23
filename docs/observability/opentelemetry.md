---
sidebar_position: 3
title: Understanding OpenTelemetry
description: A comprehensive guide to OpenTelemetry - the vendor-neutral standard for instrumenting applications and collecting telemetry data.
keywords: [opentelemetry, otel, instrumentation, OTLP, collector, distributed tracing]
---

# Understanding OpenTelemetry

When building an observability platform, you face a fundamental choice: what instrumentation standard should you use?

You could use vendor-specific SDKs (Datadog's libraries, New Relic's agents), but that creates lock-in. You could use multiple specialized tools (Jaeger for traces, Prometheus client for metrics, Fluentd for logs), but that means maintaining multiple instrumentation systems.

**OpenTelemetry solves both problems.**

## What OpenTelemetry Actually Is

OpenTelemetry (OTel) is three things:

1. **A specification** that defines how telemetry data should be structured
2. **SDKs for every major language** that implement this specification
3. **The OpenTelemetry Collector**, a vendor-agnostic data pipeline

The key insight is **separation of concerns**. Your application code instruments itself using the OpenTelemetry SDK, speaking a standard protocol (OTLP). Where that data goes—Jaeger, Datadog, Honeycomb, your own backends—is a deployment-time decision, not a code-time decision.

```
┌───────────────────────────────────────────────────────────────┐
│                    YOUR APPLICATION CODE                       │
│    ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│    │  Go SDK  │  │ Java SDK │  │ .NET SDK │  │  Python  │     │
│    └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
│         │             │             │             │            │
│         └─────────────┴──────┬──────┴─────────────┘            │
│                              │                                 │
│                        OTLP Protocol                           │
│                       (Open Standard)                          │
└──────────────────────────────┬─────────────────────────────────┘
                               │
                               ▼
┌───────────────────────────────────────────────────────────────┐
│                   OPENTELEMETRY COLLECTOR                      │
│              Receive → Process → Export (your choice)          │
└──────────────────────────────┬─────────────────────────────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
        ┌─────────┐       ┌─────────┐       ┌─────────┐
        │ Jaeger  │       │  Your   │       │ Datadog │
        │ (Self-  │       │ Backend │       │ (If you │
        │ hosted) │       │  Here   │       │  want)  │
        └─────────┘       └─────────┘       └─────────┘
```

## Why OpenTelemetry Matters

### No Vendor Lock-In

If you start with self-hosted backends and later decide you want a managed service, you change your Collector configuration—not your application code. Your investment in instrumentation is protected.

### One SDK to Learn

Instead of teaching your team Jaeger's SDK for traces, Prometheus client for metrics, and some logging framework for logs, everyone learns OpenTelemetry. One set of concepts, one set of APIs.

### Industry Momentum

OpenTelemetry is a CNCF project with contributions from Google, Microsoft, Amazon, Splunk, Datadog, and most other major players. It's rapidly becoming **the** standard way to instrument applications.

### Rich Ecosystem

Auto-instrumentation libraries exist for most common frameworks. In many cases, you can add observability to an existing application with minimal code changes.

## Core Concepts

### Signals

OpenTelemetry supports three telemetry signals:

| Signal | Description | Status |
|--------|-------------|--------|
| **Traces** | Distributed traces with spans | Stable |
| **Metrics** | Counters, gauges, histograms | Stable |
| **Logs** | Structured log records | Stable |

### The OTLP Protocol

OTLP (OpenTelemetry Protocol) is the native protocol for transmitting telemetry. It supports both gRPC and HTTP transport:

| Transport | Port | Use Case |
|-----------|------|----------|
| gRPC | 4317 | High-throughput, production workloads |
| HTTP | 4318 | Environments where gRPC is problematic |

### Context Propagation

Context propagation is how trace context flows between services. When Service A calls Service B, the trace ID must be passed along so spans can be correlated.

OpenTelemetry supports multiple propagation formats:

| Format | Description |
|--------|-------------|
| **W3C Trace Context** | Standard format, recommended |
| **B3** | Zipkin format, legacy compatibility |
| **Jaeger** | Jaeger native format |

## The OpenTelemetry Collector

The Collector is the component that gives you flexibility. It's a standalone service that receives telemetry from anywhere, transforms it however you need, and sends it wherever you want.

### Collector Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    OTEL COLLECTOR                           │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  Receivers  │ → │  Processors  │ → │  Exporters  │     │
│  │             │    │             │    │             │     │
│  │ • otlp      │    │ • batch     │    │ • otlp      │     │
│  │ • jaeger    │    │ • memory    │    │ • jaeger    │     │
│  │ • prometheus│    │ • filter    │    │ • prometheus│     │
│  │ • zipkin    │    │ • sampling  │    │ • loki      │     │
│  │ • syslog    │    │ • transform │    │ • datadog   │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Receivers: Accepting Data

Receivers accept telemetry data from various sources:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
  
  prometheus:
    config:
      scrape_configs:
        - job_name: 'my-service'
          static_configs:
            - targets: ['localhost:8080']
```

### Processors: Transforming Data

Processors modify or filter telemetry before export:

```yaml
processors:
  # Batch data for efficient export
  batch:
    timeout: 1s
    send_batch_size: 1024
  
  # Prevent OOM crashes
  memory_limiter:
    check_interval: 1s
    limit_mib: 1500
    spike_limit_mib: 500
  
  # Add metadata
  resource:
    attributes:
      - key: environment
        value: production
        action: insert
  
  # Filter out noisy data
  filter:
    traces:
      span:
        - 'attributes["http.target"] == "/health"'
```

### Exporters: Sending Data

Exporters send processed telemetry to backends:

```yaml
exporters:
  # Traces to Jaeger
  otlp/jaeger:
    endpoint: jaeger:4317
    tls:
      insecure: true
  
  # Metrics to Prometheus
  prometheus:
    endpoint: "0.0.0.0:8889"
  
  # Logs to Loki
  loki:
    endpoint: http://loki:3100/loki/api/v1/push
```

### Pipelines: Connecting Components

Pipelines wire receivers, processors, and exporters together:

```yaml
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [otlp/jaeger]
    
    metrics:
      receivers: [otlp, prometheus]
      processors: [memory_limiter, batch]
      exporters: [prometheus]
    
    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [loki]
```

## Auto-Instrumentation

One of OpenTelemetry's most powerful features is auto-instrumentation—adding observability to applications with minimal code changes.

### How It Works

Auto-instrumentation libraries wrap common frameworks and libraries, automatically creating spans for:

- HTTP requests (incoming and outgoing)
- Database queries
- Message queue operations
- gRPC calls
- And many more

### Language Examples

**Go**: Explicit but clean

```go
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
)

func initTracer() func() {
    exporter, _ := otlptracegrpc.New(ctx,
        otlptracegrpc.WithEndpoint("localhost:4317"),
        otlptracegrpc.WithInsecure(),
    )
    // ... setup provider
}
```

**Python**: Zero-code option available

```bash
# Install
pip install opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install

# Run with auto-instrumentation
opentelemetry-instrument \
    --service_name my-service \
    --exporter_otlp_endpoint http://localhost:4317 \
    python app.py
```

**Node.js**: Minimal code required

```javascript
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-grpc');

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({ url: 'http://localhost:4317' }),
  instrumentations: [getNodeAutoInstrumentations()],
});
sdk.start();
```

**.NET**: Built into the runtime

```csharp
builder.Services.AddOpenTelemetry()
    .WithTracing(t => t
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddOtlpExporter(o => o.Endpoint = new Uri("http://localhost:4317")))
    .WithMetrics(m => m
        .AddAspNetCoreInstrumentation()
        .AddOtlpExporter(o => o.Endpoint = new Uri("http://localhost:4317")));
```

## Deployment Patterns

### Pattern 1: Sidecar

Each application has its own collector:

```
┌─────────────────────┐    ┌─────────────────────┐
│       Pod A         │    │       Pod B         │
│  ┌──────┐ ┌──────┐  │    │  ┌──────┐ ┌──────┐  │
│  │ App  │→│ OTel │  │    │  │ App  │→│ OTel │  │
│  └──────┘ └──────┘  │    │  └──────┘ └──────┘  │
└──────────┬──────────┘    └──────────┬──────────┘
           │                          │
           └──────────┬───────────────┘
                      ▼
               ┌─────────────┐
               │   Backend   │
               └─────────────┘
```

**Pros**: Isolation, per-app configuration  
**Cons**: Resource overhead, many collectors to manage

### Pattern 2: Gateway

Centralized collector(s) receive from all applications:

```
┌───────┐  ┌───────┐  ┌───────┐
│ App A │  │ App B │  │ App C │
└───┬───┘  └───┬───┘  └───┬───┘
    │          │          │
    └──────────┼──────────┘
               │
               ▼
       ┌───────────────┐
       │ OTel Gateway  │ ← Load balanced
       │   Collector   │
       └───────┬───────┘
               │
               ▼
          ┌─────────┐
          │ Backend │
          └─────────┘
```

**Pros**: Centralized management, efficient resource use  
**Cons**: Single point of failure (unless HA)

### Pattern 3: Agent + Gateway (Recommended for Production)

Best of both worlds:

```
┌─────────────────────┐    ┌─────────────────────┐
│   Node/Host A       │    │   Node/Host B       │
│  ┌───┐ ┌───┐ ┌───┐  │    │  ┌───┐ ┌───┐ ┌───┐  │
│  │App│ │App│ │App│  │    │  │App│ │App│ │App│  │
│  └─┬─┘ └─┬─┘ └─┬─┘  │    │  └─┬─┘ └─┬─┘ └─┬─┘  │
│    └──┬──┘    │     │    │    └──┬──┘    │     │
│       ▼       │     │    │       ▼       │     │
│   ┌───────┐   │     │    │   ┌───────┐   │     │
│   │ Agent │←──┘     │    │   │ Agent │←──┘     │
│   └───┬───┘         │    │   └───┬───┘         │
└───────┼─────────────┘    └───────┼─────────────┘
        │                          │
        └──────────┬───────────────┘
                   ▼
           ┌───────────────┐
           │ OTel Gateway  │
           │   Cluster     │
           └───────┬───────┘
                   ▼
              ┌─────────┐
              │ Backend │
              └─────────┘
```

**Pros**: Local buffering, centralized processing, scalable  
**Cons**: More complex setup

---

## Key Takeaways

1. **OpenTelemetry is the standard** — invest in learning it
2. **Separate instrumentation from destination** — your code shouldn't know where telemetry goes
3. **The Collector is your Swiss Army knife** — use it for receiving, processing, and routing
4. **Auto-instrumentation gets you 80% there** — add custom spans for business logic
5. **Start simple** — sidecar pattern first, evolve to gateway as you scale

---

**Next**: [Observability Glossary →](./glossary)
