---
slug: instrumenting-code-for-observability
title: "Instrumenting Your Code for Observability: A Practical Guide for Senior Engineers"
authors: [shivam]
tags: [observability, opentelemetry, distributed-systems, architecture, best-practices]
description: A hands-on guide to adding metrics, traces, and structured logging to your applications using OpenTelemetry. Written for senior engineers who want to understand the why and how of instrumentation.
image: ./social-card.png
---

When your service starts throwing errors at 2 AM, the difference between a 15-minute fix and a 3-hour investigation often comes down to one thing: how well you instrumented your code. I've been on both sides of this—debugging blind through log files hoping for a clue, and watching a distributed trace light up the exact line of code causing the problem. The latter is significantly more pleasant.

This guide walks through instrumenting applications with OpenTelemetry, covering the three pillars of observability: traces, metrics, and logs. I've written this for senior engineers who understand why observability matters and want practical guidance on implementing it. We'll look at real code across Go, Python, Java, C#, and Node.js—pick your language and follow along.

<!-- truncate -->

## Why OpenTelemetry?

Before we dive into code, let's address the elephant in the room: why OpenTelemetry specifically?

You could instrument your code with vendor-specific SDKs—Datadog's libraries, New Relic's agents, Splunk's tools. They work fine. But here's the problem: you're coupling your application code to your observability vendor. When (not if) you need to switch vendors, or add a new backend, or support multiple environments with different tooling, you're rewriting instrumentation code across every service.

OpenTelemetry solves this by separating what you capture from where you send it. Your application speaks OTLP (OpenTelemetry Protocol), and the OpenTelemetry Collector routes that data wherever you need—Jaeger, Prometheus, Datadog, your own backend, all of the above. Your code doesn't change when your infrastructure does.

The other reason is ecosystem. OpenTelemetry has auto-instrumentation libraries for virtually every popular framework. Flask, Express, Spring Boot, ASP.NET Core—they all have packages that automatically capture HTTP requests, database queries, and more without you writing a line of instrumentation code. You get 80% of the value immediately, then add custom instrumentation for the remaining 20% that's specific to your business logic.

## The Mental Model

Here's how I think about instrumentation. Every request that enters your system creates a story. Traces are the narrative—they tell you what happened, in what order, and how long each step took. Metrics are the statistics—how many requests, how fast, how often things fail. Logs are the dialogue—the specific details and context at each point in the story.

When something goes wrong, you typically start with metrics (is the error rate elevated?), drill into traces (which requests are failing?), and then check logs for the specific error messages. Good instrumentation makes this workflow seamless. Bad instrumentation—or worse, no instrumentation—leaves you guessing.

The goal isn't to instrument everything. It's to instrument thoughtfully. Capture enough to debug problems quickly, but not so much that you're drowning in data or adding significant overhead to your services.

## Getting Started: The Common Foundation

Regardless of which language you're using, the setup follows the same pattern:

1. **Initialize the SDK early**—before your application logic runs
2. **Configure exporters** to send data to your collector
3. **Enable auto-instrumentation** for common frameworks
4. **Add custom spans and metrics** for business logic

The OpenTelemetry Collector should already be running in your environment. If it isn't, you'll want to set that up first—check out the [single-node observability setup](/blog/single-node-observability-setup) guide for a complete walkthrough. For now, assume you have a collector accepting OTLP on port 4317 (gRPC) or 4318 (HTTP).

Let's look at how this works in practice. Choose your language below and follow along.

---

## Go

Go's explicit nature means you have full control over instrumentation. There's no magic—you'll see exactly what's happening. Some developers find this verbose; I find it clarifying.

### Setting Up the SDK

First, install the packages:

```bash
go get go.opentelemetry.io/otel \
       go.opentelemetry.io/otel/sdk \
       go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc \
       go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc \
       go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp
```

Create a telemetry initialization function. I typically put this in an `internal/telemetry` package:

```go
package telemetry

import (
    "context"
    "os"
    "time"

    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/propagation"
    "go.opentelemetry.io/otel/sdk/metric"
    "go.opentelemetry.io/otel/sdk/resource"
    "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.24.0"
)

func Initialize(ctx context.Context, serviceName string) (func(context.Context) error, error) {
    res, err := resource.Merge(
        resource.Default(),
        resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceName(serviceName),
            semconv.ServiceVersion(os.Getenv("SERVICE_VERSION")),
        ),
    )
    if err != nil {
        return nil, err
    }

    endpoint := os.Getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if endpoint == "" {
        endpoint = "localhost:4317"
    }

    traceExporter, err := otlptracegrpc.New(ctx,
        otlptracegrpc.WithEndpoint(endpoint),
        otlptracegrpc.WithInsecure(),
    )
    if err != nil {
        return nil, err
    }

    tracerProvider := trace.NewTracerProvider(
        trace.WithResource(res),
        trace.WithBatcher(traceExporter, trace.WithBatchTimeout(5*time.Second)),
    )

    metricExporter, err := otlpmetricgrpc.New(ctx,
        otlpmetricgrpc.WithEndpoint(endpoint),
        otlpmetricgrpc.WithInsecure(),
    )
    if err != nil {
        return nil, err
    }

    meterProvider := metric.NewMeterProvider(
        metric.WithResource(res),
        metric.WithReader(metric.NewPeriodicReader(metricExporter, metric.WithInterval(15*time.Second))),
    )

    otel.SetTracerProvider(tracerProvider)
    otel.SetMeterProvider(meterProvider)
    otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(
        propagation.TraceContext{},
        propagation.Baggage{},
    ))

    return func(ctx context.Context) error {
        if err := tracerProvider.Shutdown(ctx); err != nil {
            return err
        }
        return meterProvider.Shutdown(ctx)
    }, nil
}
```

### HTTP Server Instrumentation

Wrap your HTTP handlers with `otelhttp` for automatic request tracing:

```go
package main

import (
    "context"
    "log"
    "net/http"
    "os"
    "os/signal"

    "go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
    "myservice/internal/telemetry"
)

func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    shutdown, err := telemetry.Initialize(ctx, "my-go-service")
    if err != nil {
        log.Fatalf("failed to initialize telemetry: %v", err)
    }

    mux := http.NewServeMux()
    mux.HandleFunc("/api/orders", handleOrders)
    
    // Wrap with OpenTelemetry instrumentation
    handler := otelhttp.NewHandler(mux, "http-server")

    server := &http.Server{Addr: ":8080", Handler: handler}

    go func() {
        sigChan := make(chan os.Signal, 1)
        signal.Notify(sigChan, os.Interrupt)
        <-sigChan
        shutdown(ctx)
        server.Shutdown(ctx)
    }()

    log.Println("Server starting on :8080")
    server.ListenAndServe()
}
```

### Adding Custom Spans

For business logic that doesn't get auto-instrumented, create spans manually:

```go
func handleOrders(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    tracer := otel.Tracer("my-go-service")
    
    // Create a span for the order processing
    ctx, span := tracer.Start(ctx, "processOrder")
    defer span.End()
    
    // Add business context
    span.SetAttributes(
        attribute.String("order.user_id", r.URL.Query().Get("user_id")),
    )
    
    // Child span for database operation
    ctx, dbSpan := tracer.Start(ctx, "db.insertOrder",
        trace.WithSpanKind(trace.SpanKindClient),
    )
    dbSpan.SetAttributes(
        attribute.String("db.system", "postgresql"),
        attribute.String("db.operation", "INSERT"),
    )
    
    // Your database logic here
    
    dbSpan.End()
    
    w.WriteHeader(http.StatusCreated)
}
```

For a complete Go implementation with metrics, structured logging, and HTTP client propagation, see the [Go Integration Guide](/docs/observability/integrations/go).

---

## Python

Python's OpenTelemetry story is particularly strong. You can get started with zero-code auto-instrumentation, then add custom spans as needed.

### Zero-Code Instrumentation

The fastest path to observability:

```bash
pip install opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install
```

Now run your app with the auto-instrumentor:

```bash
opentelemetry-instrument \
    --service_name my-python-service \
    --exporter_otlp_endpoint http://localhost:4317 \
    python app.py
```

That's it. If you're running Flask, FastAPI, or Django, your HTTP endpoints are now traced. Database calls through SQLAlchemy? Traced. HTTP requests with `requests`? Traced. You haven't written a line of instrumentation code.

### SDK Integration for More Control

When you need custom spans or metrics, integrate the SDK directly:

```python
import os
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

def setup_telemetry():
    resource = Resource.create({
        SERVICE_NAME: os.getenv("OTEL_SERVICE_NAME", "my-python-service"),
    })
    
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "localhost:4317")
    
    # Tracing
    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True))
    )
    trace.set_tracer_provider(trace_provider)
    
    # Metrics
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=endpoint, insecure=True),
        export_interval_millis=15000,
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)
    
    return trace.get_tracer("my-python-service")
```

### Flask Example with Custom Instrumentation

```python
from flask import Flask, request, jsonify
from opentelemetry import trace
from opentelemetry.trace import SpanKind
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from telemetry import setup_telemetry

tracer = setup_telemetry()

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    
    # The HTTP span is created automatically by FlaskInstrumentor
    # Add custom child spans for business logic
    
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.user_id", data.get("user_id"))
        span.set_attribute("order.total", data.get("total"))
        
        # Database operation
        with tracer.start_as_current_span(
            "db.insert_order",
            kind=SpanKind.CLIENT
        ) as db_span:
            db_span.set_attribute("db.system", "postgresql")
            # Your database logic here
            order_id = save_order(data)
        
        span.set_attribute("order.id", order_id)
        return jsonify({"order_id": order_id}), 201
```

For the complete Python guide covering FastAPI, async patterns, Celery integration, and custom metrics, see the [Python Integration Guide](/docs/observability/integrations/python).

---

## Java

Java offers two paths: the zero-code Java Agent and SDK integration. I recommend the agent for existing applications and SDK integration for new projects where you want more control.

### Java Agent (Zero-Code)

Download the agent and attach it to your JVM:

```bash
curl -L -o opentelemetry-javaagent.jar \
  https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/latest/download/opentelemetry-javaagent.jar

java -javaagent:opentelemetry-javaagent.jar \
     -Dotel.service.name=my-java-service \
     -Dotel.exporter.otlp.endpoint=http://localhost:4317 \
     -jar my-application.jar
```

The agent instruments 100+ libraries automatically—Spring MVC, JDBC, Hibernate, Apache HttpClient, you name it.

### Spring Boot SDK Integration

For more control, add the SDK to your Spring Boot application:

```xml
<dependency>
    <groupId>io.opentelemetry.instrumentation</groupId>
    <artifactId>opentelemetry-spring-boot-starter</artifactId>
</dependency>
```

Configure in `application.yml`:

```yaml
otel:
  service:
    name: my-java-service
  exporter:
    otlp:
      endpoint: http://localhost:4317
```

### Custom Spans in Services

```java
@Service
public class OrderService {
    
    private final Tracer tracer;
    
    public OrderService(Tracer tracer) {
        this.tracer = tracer;
    }
    
    public OrderResult createOrder(CreateOrderRequest request) {
        Span span = tracer.spanBuilder("createOrder")
            .setAttribute("order.user_id", request.getUserId())
            .setAttribute("order.items_count", request.getItems().size())
            .startSpan();
        
        try (Scope scope = span.makeCurrent()) {
            // Validation
            validateOrder(request);
            
            // Payment processing with its own span
            Span paymentSpan = tracer.spanBuilder("processPayment")
                .setSpanKind(SpanKind.CLIENT)
                .setAttribute("payment.amount", request.getTotal())
                .startSpan();
            
            try (Scope paymentScope = paymentSpan.makeCurrent()) {
                PaymentResult payment = paymentService.charge(request);
                paymentSpan.setAttribute("payment.transaction_id", payment.getId());
            } finally {
                paymentSpan.end();
            }
            
            String orderId = saveOrder(request);
            span.setAttribute("order.id", orderId);
            
            return new OrderResult(orderId, "created");
        } catch (Exception e) {
            span.recordException(e);
            span.setStatus(StatusCode.ERROR, e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }
}
```

The complete Java guide with Spring Boot configuration, metrics, structured logging with MDC, and the `@WithSpan` annotation is available in the [Java Integration Guide](/docs/observability/integrations/java).

---

## C# / .NET

.NET has first-class OpenTelemetry support through the native `System.Diagnostics` API. The integration is clean and idiomatic.

### ASP.NET Core Setup

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddOpenTelemetry()
    .ConfigureResource(resource => resource
        .AddService(serviceName: "my-dotnet-service"))
    .WithTracing(tracing => tracing
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddSqlClientInstrumentation()
        .AddSource("my-dotnet-service")
        .AddOtlpExporter(opts => 
            opts.Endpoint = new Uri("http://localhost:4317")))
    .WithMetrics(metrics => metrics
        .AddAspNetCoreInstrumentation()
        .AddRuntimeInstrumentation()
        .AddMeter("my-dotnet-service")
        .AddOtlpExporter(opts => 
            opts.Endpoint = new Uri("http://localhost:4317")));
```

### Custom Spans with ActivitySource

In .NET, you use `ActivitySource` (the native .NET API) rather than OpenTelemetry's Tracer directly:

```csharp
public class OrderService
{
    private static readonly ActivitySource ActivitySource = new("my-dotnet-service");
    
    public async Task<OrderResult> CreateOrderAsync(CreateOrderRequest request)
    {
        using var activity = ActivitySource.StartActivity("CreateOrder");
        
        activity?.SetTag("order.user_id", request.UserId);
        activity?.SetTag("order.items_count", request.Items.Count);
        
        try
        {
            // Database span
            using var dbActivity = ActivitySource.StartActivity(
                "db.InsertOrder", 
                ActivityKind.Client);
            dbActivity?.SetTag("db.system", "postgresql");
            
            var order = await SaveOrderAsync(request);
            
            activity?.SetTag("order.id", order.Id);
            activity?.SetStatus(ActivityStatusCode.Ok);
            
            return new OrderResult { OrderId = order.Id };
        }
        catch (Exception ex)
        {
            activity?.RecordException(ex);
            activity?.SetStatus(ActivityStatusCode.Error, ex.Message);
            throw;
        }
    }
}
```

The complete .NET guide covering Entity Framework, background services, structured logging, and custom metrics is in the [.NET Integration Guide](/docs/observability/integrations/dotnet).

---

## Node.js

Node.js auto-instrumentation is excellent—it captures Express, Fastify, database drivers, and HTTP clients automatically.

### SDK Setup

The key with Node.js is loading instrumentation before any other modules:

```typescript
// instrumentation.ts - MUST be loaded first
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';
import { Resource } from '@opentelemetry/resources';
import { SEMRESATTRS_SERVICE_NAME } from '@opentelemetry/semantic-conventions';

const sdk = new NodeSDK({
    resource: new Resource({
        [SEMRESATTRS_SERVICE_NAME]: process.env.OTEL_SERVICE_NAME || 'my-nodejs-service',
    }),
    traceExporter: new OTLPTraceExporter({
        url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4317',
    }),
    instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

Load it first using the `--require` flag:

```bash
node --require ./dist/instrumentation.js ./dist/app.js
```

### Custom Spans in Express

```typescript
import express from 'express';
import { trace, SpanKind, SpanStatusCode } from '@opentelemetry/api';

const app = express();
const tracer = trace.getTracer('my-nodejs-service');

app.post('/api/orders', async (req, res) => {
    const { userId, items, total } = req.body;
    
    // HTTP span is created automatically
    const span = trace.getActiveSpan();
    span?.setAttribute('order.user_id', userId);
    
    try {
        const result = await tracer.startActiveSpan(
            'processOrder',
            async (orderSpan) => {
                // Database operation
                await tracer.startActiveSpan(
                    'db.insertOrder',
                    { kind: SpanKind.CLIENT },
                    async (dbSpan) => {
                        dbSpan.setAttribute('db.system', 'postgresql');
                        const orderId = await saveOrder({ userId, items, total });
                        dbSpan.setAttribute('order.id', orderId);
                        dbSpan.end();
                        return orderId;
                    }
                );
                
                orderSpan.end();
                return { orderId, status: 'created' };
            }
        );
        
        res.status(201).json(result);
    } catch (error) {
        span?.recordException(error);
        span?.setStatus({ code: SpanStatusCode.ERROR });
        res.status(500).json({ error: 'Order creation failed' });
    }
});
```

The full Node.js guide with Express, Fastify, NestJS patterns, TypeScript configuration, and custom metrics is available in the [Node.js Integration Guide](/docs/observability/integrations/nodejs).

---

## Best Practices Across All Languages

After instrumenting dozens of services, here are the patterns that consistently pay off:

**Name spans after what they do, not what calls them.** `processPayment` is more useful than `handlePaymentRequest`. When you're looking at a trace, you want to understand the operation, not the call graph.

**Add business context to spans.** Order IDs, user IDs, product SKUs—these attributes are what turn a trace from "a database query took 500ms" into "the order for customer ABC took 500ms because the inventory check for SKU-123 was slow."

**Use span kinds correctly.** Mark database calls as `CLIENT`, message queue consumers as `CONSUMER`, HTTP handlers as `SERVER`. This helps visualization tools render traces correctly and enables proper service maps.

**Propagate context through async boundaries.** If you're using goroutines, async/await, or thread pools, make sure trace context flows with the work. This is where most "missing span" bugs come from.

**Don't over-instrument.** Health checks, metrics endpoints, and internal Kubernetes probes don't need tracing. Filter them out to reduce noise and cost.

**Shut down gracefully.** OpenTelemetry batches data before sending. If your service exits without flushing, you lose that final batch. Always call `shutdown()` in your signal handlers.

## What's Next

This guide gets you started with instrumentation. The language-specific documentation goes deeper into each ecosystem:

- [Go Integration Guide](/docs/observability/integrations/go) — HTTP servers, gRPC, custom metrics, structured logging
- [Python Integration Guide](/docs/observability/integrations/python) — Flask, FastAPI, Django, Celery, async patterns
- [Java Integration Guide](/docs/observability/integrations/java) — Spring Boot, Java Agent, Micrometer bridge, @WithSpan
- [.NET Integration Guide](/docs/observability/integrations/dotnet) — ASP.NET Core, Entity Framework, ActivitySource, background services
- [Node.js Integration Guide](/docs/observability/integrations/nodejs) — Express, Fastify, NestJS, TypeScript patterns

Once your services are instrumented, you'll want to set up the observability backend. The [single-node setup guide](/blog/single-node-observability-setup) walks through deploying the OpenTelemetry Collector, Jaeger, Prometheus, Loki, and Grafana.

Good instrumentation is an investment. It takes time upfront, but it pays dividends every time something breaks—and something always breaks.

---

*Questions or war stories about instrumenting your services? I'd love to hear them. Find me on [LinkedIn](https://www.linkedin.com/in/shivam-g-mishra) or [GitHub](https://github.com/shivam-g-mishra).*
