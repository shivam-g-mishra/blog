---
sidebar_position: 2
title: Go Integration
description: Complete guide to instrumenting Go applications with OpenTelemetry - traces, metrics, logs, and distributed tracing.
keywords: [go, golang, opentelemetry, otel, instrumentation, tracing, metrics]
---

# Go OpenTelemetry Integration

A comprehensive guide to instrumenting Go applications with OpenTelemetry. Go's explicit nature means you have full control over instrumentation, resulting in efficient, production-ready telemetry.

## Prerequisites

- Go 1.21+ (for structured logging with `slog`)
- OpenTelemetry Collector running (see [Single-Node Setup](/blog/single-node-observability-setup))
- Basic familiarity with Go modules

## Installation

```bash
go get go.opentelemetry.io/otel \
       go.opentelemetry.io/otel/sdk \
       go.opentelemetry.io/otel/sdk/metric \
       go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc \
       go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc \
       go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp \
       go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc
```

## Project Structure

```
myservice/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── telemetry/
│   │   └── telemetry.go      # OTel initialization
│   ├── handlers/
│   │   └── handlers.go       # HTTP handlers
│   └── middleware/
│       └── middleware.go     # Custom middleware
├── go.mod
└── go.sum
```

## Step 1: Create the Telemetry Package

This package encapsulates all OpenTelemetry initialization logic:

```go title="internal/telemetry/telemetry.go"
package telemetry

import (
    "context"
    "fmt"
    "os"
    "time"

    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/propagation"
    "go.opentelemetry.io/otel/sdk/metric"
    "go.opentelemetry.io/otel/sdk/resource"
    "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.24.0"
)

// Config holds telemetry configuration
type Config struct {
    ServiceName    string
    ServiceVersion string
    Environment    string
    OTLPEndpoint   string
}

// LoadFromEnv creates Config from environment variables
func LoadFromEnv() Config {
    return Config{
        ServiceName:    getEnv("OTEL_SERVICE_NAME", "my-go-service"),
        ServiceVersion: getEnv("OTEL_SERVICE_VERSION", "1.0.0"),
        Environment:    getEnv("OTEL_ENVIRONMENT", "development"),
        OTLPEndpoint:   getEnv("OTEL_EXPORTER_OTLP_ENDPOINT", "localhost:4317"),
    }
}

func getEnv(key, fallback string) string {
    if v := os.Getenv(key); v != "" {
        return v
    }
    return fallback
}

// Telemetry holds initialized providers and shutdown function
type Telemetry struct {
    TracerProvider *trace.TracerProvider
    MeterProvider  *metric.MeterProvider
}

// Initialize sets up OpenTelemetry and returns a shutdown function
func Initialize(ctx context.Context, cfg Config) (*Telemetry, func(context.Context) error, error) {
    // Create resource describing this service
    res, err := resource.Merge(
        resource.Default(),
        resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceName(cfg.ServiceName),
            semconv.ServiceVersion(cfg.ServiceVersion),
            semconv.DeploymentEnvironment(cfg.Environment),
            attribute.String("service.namespace", "production"),
        ),
    )
    if err != nil {
        return nil, nil, fmt.Errorf("creating resource: %w", err)
    }

    // Initialize trace exporter
    traceExporter, err := otlptracegrpc.New(ctx,
        otlptracegrpc.WithEndpoint(cfg.OTLPEndpoint),
        otlptracegrpc.WithInsecure(), // Use WithTLSCredentials in production
    )
    if err != nil {
        return nil, nil, fmt.Errorf("creating trace exporter: %w", err)
    }

    // Initialize tracer provider with batching
    // Batching reduces network overhead by sending spans in groups rather than individually
    tracerProvider := trace.NewTracerProvider(
        trace.WithResource(res),
        trace.WithBatcher(traceExporter,
            trace.WithBatchTimeout(5*time.Second),    // Max time to wait before sending a batch
            trace.WithMaxExportBatchSize(512),        // Max spans per batch (tune based on payload size)
            trace.WithMaxQueueSize(2048),             // Buffer size - prevents memory issues under load
        ),
        // Sampling strategy:
        // - ParentBased: If parent span was sampled, sample this one too (maintains trace continuity)
        // - TraceIDRatioBased(1.0): Sample 100% of root spans (change to 0.1 for 10% in high-traffic prod)
        // For production with high traffic, use 0.1 or lower to reduce costs while keeping errors
        trace.WithSampler(trace.ParentBased(trace.TraceIDRatioBased(1.0))),
    )

    // Initialize metric exporter
    metricExporter, err := otlpmetricgrpc.New(ctx,
        otlpmetricgrpc.WithEndpoint(cfg.OTLPEndpoint),
        otlpmetricgrpc.WithInsecure(),
    )
    if err != nil {
        return nil, nil, fmt.Errorf("creating metric exporter: %w", err)
    }

    // Initialize meter provider
    meterProvider := metric.NewMeterProvider(
        metric.WithResource(res),
        metric.WithReader(metric.NewPeriodicReader(metricExporter,
            metric.WithInterval(15*time.Second),
        )),
    )

    // Set global providers
    otel.SetTracerProvider(tracerProvider)
    otel.SetMeterProvider(meterProvider)
    
    // Configure context propagation (W3C Trace Context + Baggage)
    otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(
        propagation.TraceContext{},
        propagation.Baggage{},
    ))

    // Create shutdown function
    shutdown := func(ctx context.Context) error {
        var errs []error
        if err := tracerProvider.Shutdown(ctx); err != nil {
            errs = append(errs, err)
        }
        if err := meterProvider.Shutdown(ctx); err != nil {
            errs = append(errs, err)
        }
        if len(errs) > 0 {
            return fmt.Errorf("shutdown errors: %v", errs)
        }
        return nil
    }

    return &Telemetry{
        TracerProvider: tracerProvider,
        MeterProvider:  meterProvider,
    }, shutdown, nil
}
```

## Step 2: HTTP Server with Auto-Instrumentation

Use `otelhttp` for automatic HTTP instrumentation:

```go title="cmd/server/main.go"
package main

import (
    "context"
    "encoding/json"
    "log/slog"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"

    "go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/codes"
    "go.opentelemetry.io/otel/metric"
    "go.opentelemetry.io/otel/trace"

    "myservice/internal/telemetry"
)

var (
    tracer         trace.Tracer
    meter          metric.Meter
    requestCounter metric.Int64Counter
    requestLatency metric.Float64Histogram
)

func main() {
    // Setup structured logging
    logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
        Level: slog.LevelInfo,
    }))
    slog.SetDefault(logger)

    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    // Initialize telemetry
    cfg := telemetry.LoadFromEnv()
    tel, shutdown, err := telemetry.Initialize(ctx, cfg)
    if err != nil {
        slog.Error("Failed to initialize telemetry", "error", err)
        os.Exit(1)
    }

    // Get tracer and meter instances
    tracer = otel.Tracer(cfg.ServiceName)
    meter = otel.Meter(cfg.ServiceName)

    // Initialize metrics
    if err := initMetrics(); err != nil {
        slog.Error("Failed to initialize metrics", "error", err)
        os.Exit(1)
    }

    // Setup HTTP routes
    mux := http.NewServeMux()
    mux.HandleFunc("/health", healthHandler)
    mux.HandleFunc("/api/users/", getUserHandler)
    mux.HandleFunc("/api/orders", createOrderHandler)

    // Wrap with OpenTelemetry instrumentation
    handler := otelhttp.NewHandler(mux, "http-server",
        otelhttp.WithMessageEvents(otelhttp.ReadEvents, otelhttp.WriteEvents),
        otelhttp.WithSpanNameFormatter(func(operation string, r *http.Request) string {
            return fmt.Sprintf("%s %s", r.Method, r.URL.Path)
        }),
    )

    server := &http.Server{
        Addr:         ":8080",
        Handler:      handler,
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  60 * time.Second,
    }

    // Graceful shutdown
    go func() {
        sigChan := make(chan os.Signal, 1)
        signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
        <-sigChan

        slog.Info("Shutting down server...")
        
        shutdownCtx, shutdownCancel := context.WithTimeout(ctx, 30*time.Second)
        defer shutdownCancel()

        // Shutdown HTTP server first
        if err := server.Shutdown(shutdownCtx); err != nil {
            slog.Error("Server shutdown error", "error", err)
        }

        // Then shutdown telemetry (flushes remaining data)
        if err := shutdown(shutdownCtx); err != nil {
            slog.Error("Telemetry shutdown error", "error", err)
        }

        cancel()
    }()

    slog.Info("Server starting", "addr", server.Addr, "service", cfg.ServiceName)
    if err := server.ListenAndServe(); err != http.ErrServerClosed {
        slog.Error("Server error", "error", err)
        os.Exit(1)
    }
}

func initMetrics() error {
    var err error
    
    requestCounter, err = meter.Int64Counter("http_server_requests_total",
        metric.WithDescription("Total HTTP requests received"),
        metric.WithUnit("{request}"),
    )
    if err != nil {
        return err
    }

    requestLatency, err = meter.Float64Histogram("http_server_request_duration_seconds",
        metric.WithDescription("HTTP request duration in seconds"),
        metric.WithUnit("s"),
        metric.WithExplicitBucketBoundaries(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
    )
    return err
}
```

## Step 3: Implement Handlers with Manual Spans

```go title="internal/handlers/handlers.go"
package main

func healthHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{"status": "healthy"})
}

func getUserHandler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    start := time.Now()

    // Extract user ID from path
    userID := strings.TrimPrefix(r.URL.Path, "/api/users/")
    
    // Get the current span (created by otelhttp) and enrich it
    span := trace.SpanFromContext(ctx)
    span.SetAttributes(
        attribute.String("user.id", userID),
        attribute.String("handler", "getUserHandler"),
    )

    // Create child span for database operation
    ctx, dbSpan := tracer.Start(ctx, "db.SelectUser",
        trace.WithSpanKind(trace.SpanKindClient),
        trace.WithAttributes(
            attribute.String("db.system", "postgresql"),
            attribute.String("db.operation", "SELECT"),
            attribute.String("db.sql.table", "users"),
        ),
    )

    // Simulate database query
    user, err := fetchUserFromDB(ctx, userID)
    dbSpan.End()

    if err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, "failed to fetch user")
        recordRequest(ctx, r.Method, "/api/users", "500", time.Since(start))
        http.Error(w, "Internal server error", http.StatusInternalServerError)
        return
    }

    // Record successful request
    recordRequest(ctx, r.Method, "/api/users", "200", time.Since(start))

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(user)
}

func createOrderHandler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    start := time.Now()

    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    span := trace.SpanFromContext(ctx)

    // Decode request body
    var orderReq struct {
        UserID string   `json:"user_id"`
        Items  []string `json:"items"`
        Total  float64  `json:"total"`
    }
    if err := json.NewDecoder(r.Body).Decode(&orderReq); err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, "invalid request body")
        http.Error(w, "Invalid request", http.StatusBadRequest)
        return
    }

    // Add business context to span
    span.SetAttributes(
        attribute.String("order.user_id", orderReq.UserID),
        attribute.Int("order.items_count", len(orderReq.Items)),
        attribute.Float64("order.total", orderReq.Total),
    )

    // Process order with nested spans
    orderID, err := processOrder(ctx, orderReq)
    if err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, "order processing failed")
        recordRequest(ctx, r.Method, "/api/orders", "500", time.Since(start))
        http.Error(w, "Failed to process order", http.StatusInternalServerError)
        return
    }

    span.SetAttributes(attribute.String("order.id", orderID))
    recordRequest(ctx, r.Method, "/api/orders", "201", time.Since(start))

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(map[string]string{
        "order_id": orderID,
        "status":   "created",
    })
}

func processOrder(ctx context.Context, order struct {
    UserID string
    Items  []string
    Total  float64
}) (string, error) {
    ctx, span := tracer.Start(ctx, "processOrder")
    defer span.End()

    // Step 1: Validate order
    ctx, validateSpan := tracer.Start(ctx, "validateOrder")
    if err := validateOrder(order); err != nil {
        validateSpan.RecordError(err)
        validateSpan.SetStatus(codes.Error, "validation failed")
        validateSpan.End()
        return "", err
    }
    validateSpan.SetAttributes(attribute.Bool("validation.passed", true))
    validateSpan.End()

    // Step 2: Reserve inventory
    ctx, inventorySpan := tracer.Start(ctx, "reserveInventory",
        trace.WithSpanKind(trace.SpanKindClient),
    )
    time.Sleep(50 * time.Millisecond) // Simulate API call
    inventorySpan.End()

    // Step 3: Process payment
    ctx, paymentSpan := tracer.Start(ctx, "processPayment",
        trace.WithSpanKind(trace.SpanKindClient),
        trace.WithAttributes(
            attribute.Float64("payment.amount", order.Total),
            attribute.String("payment.currency", "USD"),
        ),
    )
    time.Sleep(100 * time.Millisecond) // Simulate payment gateway
    paymentSpan.SetAttributes(attribute.String("payment.status", "approved"))
    paymentSpan.End()

    // Step 4: Save order to database
    ctx, saveSpan := tracer.Start(ctx, "saveOrder",
        trace.WithSpanKind(trace.SpanKindClient),
        trace.WithAttributes(
            attribute.String("db.system", "postgresql"),
            attribute.String("db.operation", "INSERT"),
        ),
    )
    time.Sleep(30 * time.Millisecond)
    orderID := generateOrderID()
    saveSpan.SetAttributes(attribute.String("db.order_id", orderID))
    saveSpan.End()

    return orderID, nil
}

func recordRequest(ctx context.Context, method, endpoint, status string, duration time.Duration) {
    attrs := []attribute.KeyValue{
        attribute.String("http.method", method),
        attribute.String("http.route", endpoint),
        attribute.String("http.status_code", status),
    }

    requestCounter.Add(ctx, 1, metric.WithAttributes(attrs...))
    requestLatency.Record(ctx, duration.Seconds(), metric.WithAttributes(attrs...))
}
```

## Step 4: Custom Metrics

```go title="internal/metrics/metrics.go"
package metrics

import (
    "context"
    "runtime"

    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/metric"
)

type Metrics struct {
    // Counters
    RequestsTotal metric.Int64Counter
    ErrorsTotal   metric.Int64Counter

    // Histograms
    RequestDuration metric.Float64Histogram
    DBQueryDuration metric.Float64Histogram

    // UpDownCounters
    ActiveConnections metric.Int64UpDownCounter
    QueueDepth        metric.Int64UpDownCounter
}

func New(serviceName string) (*Metrics, error) {
    meter := otel.Meter(serviceName)
    m := &Metrics{}
    var err error

    // Request counter
    m.RequestsTotal, err = meter.Int64Counter("http_requests_total",
        metric.WithDescription("Total HTTP requests"),
        metric.WithUnit("{request}"),
    )
    if err != nil {
        return nil, err
    }

    // Error counter
    m.ErrorsTotal, err = meter.Int64Counter("http_errors_total",
        metric.WithDescription("Total HTTP errors"),
        metric.WithUnit("{error}"),
    )
    if err != nil {
        return nil, err
    }

    // Request duration histogram
    m.RequestDuration, err = meter.Float64Histogram("http_request_duration_seconds",
        metric.WithDescription("HTTP request duration"),
        metric.WithUnit("s"),
        metric.WithExplicitBucketBoundaries(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
    )
    if err != nil {
        return nil, err
    }

    // Database query duration
    m.DBQueryDuration, err = meter.Float64Histogram("db_query_duration_seconds",
        metric.WithDescription("Database query duration"),
        metric.WithUnit("s"),
        metric.WithExplicitBucketBoundaries(0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5),
    )
    if err != nil {
        return nil, err
    }

    // Active connections gauge
    m.ActiveConnections, err = meter.Int64UpDownCounter("active_connections",
        metric.WithDescription("Number of active connections"),
        metric.WithUnit("{connection}"),
    )
    if err != nil {
        return nil, err
    }

    // Queue depth
    m.QueueDepth, err = meter.Int64UpDownCounter("queue_depth",
        metric.WithDescription("Current queue depth"),
        metric.WithUnit("{item}"),
    )
    if err != nil {
        return nil, err
    }

    // Register runtime metrics (goroutines, memory)
    if err := registerRuntimeMetrics(meter); err != nil {
        return nil, err
    }

    return m, nil
}

func registerRuntimeMetrics(meter metric.Meter) error {
    // Goroutine count
    _, err := meter.Int64ObservableGauge("runtime_goroutines",
        metric.WithDescription("Number of goroutines"),
        metric.WithUnit("{goroutine}"),
        metric.WithInt64Callback(func(ctx context.Context, o metric.Int64Observer) error {
            o.Observe(int64(runtime.NumGoroutine()))
            return nil
        }),
    )
    if err != nil {
        return err
    }

    // Heap memory
    _, err = meter.Int64ObservableGauge("runtime_heap_alloc_bytes",
        metric.WithDescription("Heap memory allocated"),
        metric.WithUnit("By"),
        metric.WithInt64Callback(func(ctx context.Context, o metric.Int64Observer) error {
            var m runtime.MemStats
            runtime.ReadMemStats(&m)
            o.Observe(int64(m.HeapAlloc))
            return nil
        }),
    )
    if err != nil {
        return err
    }

    // GC pause time
    _, err = meter.Float64ObservableGauge("runtime_gc_pause_seconds",
        metric.WithDescription("Last GC pause duration"),
        metric.WithUnit("s"),
        metric.WithFloat64Callback(func(ctx context.Context, o metric.Float64Observer) error {
            var m runtime.MemStats
            runtime.ReadMemStats(&m)
            if m.NumGC > 0 {
                o.Observe(float64(m.PauseNs[(m.NumGC+255)%256]) / 1e9)
            }
            return nil
        }),
    )

    return err
}

// RecordRequest records HTTP request metrics
func (m *Metrics) RecordRequest(ctx context.Context, method, route, status string, duration float64) {
    attrs := []attribute.KeyValue{
        attribute.String("method", method),
        attribute.String("route", route),
        attribute.String("status", status),
    }

    m.RequestsTotal.Add(ctx, 1, metric.WithAttributes(attrs...))
    m.RequestDuration.Record(ctx, duration, metric.WithAttributes(attrs...))

    if status[0] == '5' {
        m.ErrorsTotal.Add(ctx, 1, metric.WithAttributes(attrs...))
    }
}
```

## Step 5: Structured Logging with Trace Context

```go title="internal/logging/logger.go"
package logging

import (
    "context"
    "log/slog"
    "os"

    "go.opentelemetry.io/otel/trace"
)

// TraceHandler wraps slog.Handler to include trace context
type TraceHandler struct {
    slog.Handler
}

func (h *TraceHandler) Handle(ctx context.Context, r slog.Record) error {
    // Extract trace context and add to log record
    span := trace.SpanFromContext(ctx)
    if span.SpanContext().IsValid() {
        r.AddAttrs(
            slog.String("trace_id", span.SpanContext().TraceID().String()),
            slog.String("span_id", span.SpanContext().SpanID().String()),
        )
    }
    return h.Handler.Handle(ctx, r)
}

func (h *TraceHandler) WithAttrs(attrs []slog.Attr) slog.Handler {
    return &TraceHandler{Handler: h.Handler.WithAttrs(attrs)}
}

func (h *TraceHandler) WithGroup(name string) slog.Handler {
    return &TraceHandler{Handler: h.Handler.WithGroup(name)}
}

// NewLogger creates a structured logger with trace context support
func NewLogger(serviceName string) *slog.Logger {
    opts := &slog.HandlerOptions{
        Level: slog.LevelInfo,
        AddSource: true,
    }

    jsonHandler := slog.NewJSONHandler(os.Stdout, opts)
    traceHandler := &TraceHandler{Handler: jsonHandler}

    return slog.New(traceHandler).With(
        slog.String("service", serviceName),
    )
}

// Example usage in handlers
func ExampleHandler(ctx context.Context, logger *slog.Logger) {
    // trace_id and span_id are automatically added
    logger.InfoContext(ctx, "Processing request",
        slog.String("user_id", "123"),
        slog.String("action", "create_order"),
    )

    // Error logging includes trace context for correlation
    logger.ErrorContext(ctx, "Failed to process payment",
        slog.String("order_id", "456"),
        slog.Any("error", err),
    )
}
```

## Step 6: HTTP Client with Propagation

```go title="internal/httpclient/client.go"
package httpclient

import (
    "context"
    "net/http"
    "time"

    "go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/trace"
)

// Client wraps http.Client with OpenTelemetry instrumentation
type Client struct {
    *http.Client
    tracer trace.Tracer
}

// New creates an instrumented HTTP client
func New() *Client {
    return &Client{
        Client: &http.Client{
            Transport: otelhttp.NewTransport(http.DefaultTransport),
            Timeout:   30 * time.Second,
        },
        tracer: otel.Tracer("http-client"),
    }
}

// Get performs an instrumented GET request
func (c *Client) Get(ctx context.Context, url string) (*http.Response, error) {
    req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
    if err != nil {
        return nil, err
    }
    return c.Do(req)
}

// CallService calls a downstream service with full trace propagation
func (c *Client) CallService(ctx context.Context, serviceName, endpoint string, body io.Reader) (*http.Response, error) {
    ctx, span := c.tracer.Start(ctx, "call."+serviceName,
        trace.WithSpanKind(trace.SpanKindClient),
        trace.WithAttributes(
            attribute.String("peer.service", serviceName),
            attribute.String("http.url", endpoint),
        ),
    )
    defer span.End()

    req, err := http.NewRequestWithContext(ctx, http.MethodPost, endpoint, body)
    if err != nil {
        span.RecordError(err)
        return nil, err
    }
    req.Header.Set("Content-Type", "application/json")

    resp, err := c.Do(req)
    if err != nil {
        span.RecordError(err)
        return nil, err
    }

    span.SetAttributes(attribute.Int("http.status_code", resp.StatusCode))
    return resp, nil
}
```

## Step 7: gRPC Integration

```go title="internal/grpc/server.go"
package grpc

import (
    "context"
    "net"

    "go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc"
    "google.golang.org/grpc"
)

// NewServer creates a gRPC server with OpenTelemetry instrumentation
func NewServer() *grpc.Server {
    return grpc.NewServer(
        grpc.StatsHandler(otelgrpc.NewServerHandler()),
    )
}

// NewClient creates a gRPC client with OpenTelemetry instrumentation
func NewClient(addr string) (*grpc.ClientConn, error) {
    return grpc.Dial(addr,
        grpc.WithInsecure(),
        grpc.WithStatsHandler(otelgrpc.NewClientHandler()),
    )
}
```

## Docker Integration

```dockerfile title="Dockerfile"
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /server ./cmd/server

FROM alpine:latest
RUN apk --no-cache add ca-certificates
COPY --from=builder /server /server
EXPOSE 8080
CMD ["/server"]
```

```yaml title="docker-compose.yml"
services:
  my-go-service:
    build: .
    ports:
      - "8080:8080"
    environment:
      - OTEL_SERVICE_NAME=my-go-service
      - OTEL_SERVICE_VERSION=1.0.0
      - OTEL_ENVIRONMENT=production
      - OTEL_EXPORTER_OTLP_ENDPOINT=otel-collector:4317
    networks:
      - observability

networks:
  observability:
    external: true
```

## Best Practices

### 1. Always Use Context

```go
// Good: Context flows through all functions
func ProcessRequest(ctx context.Context, data Data) error {
    ctx, span := tracer.Start(ctx, "ProcessRequest")
    defer span.End()
    
    return processData(ctx, data) // Pass context
}

// Bad: Context is lost
func ProcessRequest(data Data) error {
    _, span := tracer.Start(context.Background(), "ProcessRequest")
    defer span.End()
    
    return processData(data) // No context propagation
}
```

### 2. Use Span Kinds Correctly

| Kind | Use Case |
|------|----------|
| `SpanKindServer` | Incoming requests (automatic with otelhttp) |
| `SpanKindClient` | Outgoing HTTP/gRPC/DB calls |
| `SpanKindProducer` | Publishing to message queues |
| `SpanKindConsumer` | Consuming from message queues |
| `SpanKindInternal` | Internal operations (default) |

### 3. Set Meaningful Attributes

```go
span.SetAttributes(
    // Semantic conventions
    attribute.String("http.method", "POST"),
    attribute.Int("http.status_code", 200),
    attribute.String("db.system", "postgresql"),
    
    // Business context
    attribute.String("order.id", orderID),
    attribute.Float64("order.total", 99.99),
    attribute.String("customer.tier", "premium"),
)
```

### 4. Handle Errors Properly

```go
if err != nil {
    span.RecordError(err)
    span.SetStatus(codes.Error, err.Error())
    return err
}
span.SetStatus(codes.Ok, "")
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No traces appearing | Collector not running | Verify `docker ps` shows otel-collector |
| Missing spans | `span.End()` not called | Use `defer span.End()` immediately after Start |
| Context not propagating | Missing `ctx` parameter | Pass context through all function calls |
| High memory usage | Too many spans | Enable sampling with `TraceIDRatioBased(0.1)` |
| gRPC connection refused | Wrong endpoint format | Use `host:port` not `http://host:port` |

---

**Next**: [.NET Integration →](./dotnet)
