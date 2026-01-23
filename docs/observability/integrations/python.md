---
sidebar_position: 5
title: Python Integration
description: Complete guide to instrumenting Python applications with OpenTelemetry - Flask, FastAPI, Django, and more.
keywords: [python, flask, fastapi, django, opentelemetry, otel, instrumentation]
---

# Python OpenTelemetry Integration

A comprehensive guide to instrumenting Python applications with OpenTelemetry. Python offers both zero-code auto-instrumentation and flexible SDK integration.

## Prerequisites

- Python 3.8+ (3.11+ recommended)
- OpenTelemetry Collector running (see [Single-Node Setup](/single-node-observability-setup))
- pip or poetry package manager

## Installation

```bash
# Core packages
pip install opentelemetry-api \
            opentelemetry-sdk \
            opentelemetry-exporter-otlp-proto-grpc

# Auto-instrumentation
pip install opentelemetry-distro
opentelemetry-bootstrap -a install

# Or install specific instrumentations
pip install opentelemetry-instrumentation-flask \
            opentelemetry-instrumentation-fastapi \
            opentelemetry-instrumentation-django \
            opentelemetry-instrumentation-requests \
            opentelemetry-instrumentation-httpx \
            opentelemetry-instrumentation-sqlalchemy \
            opentelemetry-instrumentation-redis \
            opentelemetry-instrumentation-celery
```

## Quick Start: Zero-Code Instrumentation

The fastest way to add observability without code changes:

```bash
# Install distro and bootstrap instrumentations
pip install opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install

# Run your app with auto-instrumentation
opentelemetry-instrument \
    --service_name my-python-service \
    --exporter_otlp_endpoint http://localhost:4317 \
    --exporter_otlp_insecure true \
    python app.py
```

This automatically instruments Flask, FastAPI, Django, requests, httpx, SQLAlchemy, and many more.

## SDK Integration (Recommended)

For more control, integrate the SDK directly:

```python title="telemetry.py"
import os
import logging
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry._logs import set_logger_provider
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.composite import CompositePropagator
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.baggage.propagation import W3CBaggagePropagator

# Configuration
OTEL_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "localhost:4317")
SERVICE_NAME_VALUE = os.getenv("OTEL_SERVICE_NAME", "my-python-service")
SERVICE_VERSION_VALUE = os.getenv("OTEL_SERVICE_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("OTEL_ENVIRONMENT", "development")


def setup_telemetry() -> trace.Tracer:
    """Initialize OpenTelemetry with traces, metrics, and logs."""
    
    # Create resource describing this service
    resource = Resource.create({
        SERVICE_NAME: SERVICE_NAME_VALUE,
        SERVICE_VERSION: SERVICE_VERSION_VALUE,
        "deployment.environment": ENVIRONMENT,
        "host.name": os.uname().nodename,
    })
    
    # ============ TRACING ============
    trace_exporter = OTLPSpanExporter(
        endpoint=OTEL_ENDPOINT,
        insecure=True,  # Use secure=True in production with TLS
    )
    
    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(
        BatchSpanProcessor(
            trace_exporter,
            max_queue_size=2048,
            max_export_batch_size=512,
            schedule_delay_millis=5000,
        )
    )
    trace.set_tracer_provider(trace_provider)
    
    # ============ METRICS ============
    metric_exporter = OTLPMetricExporter(
        endpoint=OTEL_ENDPOINT,
        insecure=True,
    )
    
    metric_reader = PeriodicExportingMetricReader(
        metric_exporter,
        export_interval_millis=15000,  # Export every 15 seconds
    )
    
    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[metric_reader],
    )
    metrics.set_meter_provider(meter_provider)
    
    # ============ LOGGING ============
    log_exporter = OTLPLogExporter(
        endpoint=OTEL_ENDPOINT,
        insecure=True,
    )
    
    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(log_exporter)
    )
    set_logger_provider(logger_provider)
    
    # Add OTel handler to root logger
    handler = LoggingHandler(
        level=logging.INFO,
        logger_provider=logger_provider,
    )
    logging.getLogger().addHandler(handler)
    
    # ============ PROPAGATION ============
    set_global_textmap(CompositePropagator([
        TraceContextTextMapPropagator(),
        W3CBaggagePropagator(),
    ]))
    
    logging.info(f"OpenTelemetry initialized for {SERVICE_NAME_VALUE}")
    
    return trace.get_tracer(SERVICE_NAME_VALUE)


def get_tracer(name: str = None) -> trace.Tracer:
    """Get a tracer instance."""
    return trace.get_tracer(name or SERVICE_NAME_VALUE)


def get_meter(name: str = None) -> metrics.Meter:
    """Get a meter instance."""
    return metrics.get_meter(name or SERVICE_NAME_VALUE)
```

## Flask Application

```python title="app.py"
import logging
import time
from flask import Flask, request, jsonify, g
from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

from telemetry import setup_telemetry, get_tracer, get_meter

# Initialize telemetry FIRST
tracer = setup_telemetry()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Auto-instrument Flask and libraries
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
# SQLAlchemyInstrumentor().instrument(engine=your_engine)

# Create custom metrics
meter = get_meter()
request_counter = meter.create_counter(
    "http_requests_total",
    description="Total HTTP requests",
    unit="1",
)
request_duration = meter.create_histogram(
    "http_request_duration_seconds",
    description="HTTP request duration",
    unit="s",
)
active_requests = meter.create_up_down_counter(
    "http_active_requests",
    description="Number of active requests",
    unit="1",
)


@app.before_request
def before_request():
    """Track request start time and increment active requests."""
    g.start_time = time.time()
    active_requests.add(1)


@app.after_request
def after_request(response):
    """Record metrics after each request."""
    duration = time.time() - g.start_time
    
    labels = {
        "method": request.method,
        "endpoint": request.endpoint or "unknown",
        "status": str(response.status_code),
    }
    
    request_counter.add(1, labels)
    request_duration.record(duration, labels)
    active_requests.add(-1)
    
    return response


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/api/users/<user_id>")
def get_user(user_id: str):
    span = trace.get_current_span()
    span.set_attribute("user.id", user_id)
    
    logger.info(f"Fetching user {user_id}")
    
    try:
        # Create child span for database operation
        with tracer.start_as_current_span(
            "db.get_user",
            kind=SpanKind.CLIENT,
        ) as db_span:
            db_span.set_attributes({
                "db.system": "postgresql",
                "db.operation": "SELECT",
                "db.sql.table": "users",
            })
            
            # Simulate database call
            time.sleep(0.05)
            
            user = {
                "id": user_id,
                "name": "John Doe",
                "email": "john@example.com",
            }
        
        return jsonify(user)
        
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
        span.record_exception(e)
        span.set_status(Status(StatusCode.ERROR, str(e)))
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/orders", methods=["POST"])
def create_order():
    span = trace.get_current_span()
    data = request.get_json()
    
    user_id = data.get("user_id")
    items = data.get("items", [])
    total = data.get("total", 0)
    
    span.set_attributes({
        "order.user_id": user_id,
        "order.items_count": len(items),
        "order.total": total,
    })
    
    logger.info(f"Creating order for user {user_id}")
    
    try:
        result = process_order(user_id, items, total)
        return jsonify(result), 201
    except Exception as e:
        logger.error(f"Order creation failed: {e}")
        span.record_exception(e)
        span.set_status(Status(StatusCode.ERROR))
        return jsonify({"error": str(e)}), 500


def process_order(user_id: str, items: list, total: float) -> dict:
    """Process an order with multiple steps."""
    with tracer.start_as_current_span("process_order") as span:
        span.set_attributes({
            "order.user_id": user_id,
            "order.items_count": len(items),
        })
        
        # Step 1: Validate
        with tracer.start_as_current_span("validate_order"):
            time.sleep(0.01)
            logger.info("Order validated")
        
        # Step 2: Reserve inventory
        with tracer.start_as_current_span(
            "reserve_inventory",
            kind=SpanKind.CLIENT,
        ) as inv_span:
            inv_span.set_attribute("inventory.items_count", len(items))
            time.sleep(0.05)
            logger.info("Inventory reserved")
        
        # Step 3: Process payment
        with tracer.start_as_current_span(
            "process_payment",
            kind=SpanKind.CLIENT,
        ) as pay_span:
            pay_span.set_attributes({
                "payment.amount": total,
                "payment.currency": "USD",
            })
            time.sleep(0.1)
            pay_span.set_attribute("payment.status", "approved")
            logger.info("Payment processed")
        
        # Step 4: Save order
        order_id = f"order_{int(time.time() * 1000)}"
        with tracer.start_as_current_span(
            "save_order",
            kind=SpanKind.CLIENT,
        ) as save_span:
            save_span.set_attributes({
                "db.system": "postgresql",
                "db.operation": "INSERT",
            })
            time.sleep(0.03)
            save_span.set_attribute("order.id", order_id)
            logger.info(f"Order {order_id} saved")
        
        span.set_attribute("order.id", order_id)
        return {"order_id": order_id, "status": "created"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
```

## FastAPI Application

```python title="main.py"
import logging
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

from telemetry import setup_telemetry, get_tracer, get_meter

# Initialize telemetry
tracer = setup_telemetry()
meter = get_meter()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Metrics
request_counter = meter.create_counter("http_requests_total")
request_duration = meter.create_histogram("http_request_duration_seconds")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("Application starting")
    yield
    logger.info("Application shutting down")


app = FastAPI(
    title="My FastAPI Service",
    version="1.0.0",
    lifespan=lifespan,
)

# Auto-instrument FastAPI
FastAPIInstrumentor.instrument_app(app)
HTTPXClientInstrumentor().instrument()


# Request middleware for metrics
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    labels = {
        "method": request.method,
        "path": request.url.path,
        "status": str(response.status_code),
    }
    
    request_counter.add(1, labels)
    request_duration.record(duration, labels)
    
    return response


class OrderRequest(BaseModel):
    user_id: str
    items: list[dict]
    total: float


class OrderResponse(BaseModel):
    order_id: str
    status: str


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    span = trace.get_current_span()
    span.set_attribute("user.id", user_id)
    
    logger.info(f"Fetching user {user_id}")
    
    with tracer.start_as_current_span(
        "db.get_user",
        kind=SpanKind.CLIENT,
    ) as db_span:
        db_span.set_attributes({
            "db.system": "postgresql",
            "db.operation": "SELECT",
        })
        
        # Simulate async database call
        import asyncio
        await asyncio.sleep(0.05)
        
        return {
            "id": user_id,
            "name": "John Doe",
            "email": "john@example.com",
        }


@app.post("/api/orders", response_model=OrderResponse)
async def create_order(order: OrderRequest):
    span = trace.get_current_span()
    span.set_attributes({
        "order.user_id": order.user_id,
        "order.items_count": len(order.items),
        "order.total": order.total,
    })
    
    logger.info(f"Creating order for user {order.user_id}")
    
    try:
        result = await process_order_async(order)
        return result
    except Exception as e:
        span.record_exception(e)
        span.set_status(Status(StatusCode.ERROR))
        raise HTTPException(status_code=500, detail=str(e))


async def process_order_async(order: OrderRequest) -> OrderResponse:
    """Async order processing with spans."""
    import asyncio
    
    with tracer.start_as_current_span("process_order") as span:
        # Validate
        with tracer.start_as_current_span("validate_order"):
            await asyncio.sleep(0.01)
        
        # Reserve inventory
        with tracer.start_as_current_span("reserve_inventory", kind=SpanKind.CLIENT):
            await asyncio.sleep(0.05)
        
        # Process payment
        with tracer.start_as_current_span("process_payment", kind=SpanKind.CLIENT) as pay_span:
            pay_span.set_attribute("payment.amount", order.total)
            await asyncio.sleep(0.1)
        
        # Save order
        order_id = f"order_{int(time.time() * 1000)}"
        with tracer.start_as_current_span("save_order", kind=SpanKind.CLIENT):
            await asyncio.sleep(0.03)
        
        span.set_attribute("order.id", order_id)
        return OrderResponse(order_id=order_id, status="created")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Custom Metrics

```python title="metrics.py"
from opentelemetry import metrics
from typing import Dict, Any
import psutil

meter = metrics.get_meter("my-python-service")

# Counters
orders_created = meter.create_counter(
    "orders_created_total",
    description="Total orders created",
    unit="1",
)

orders_failed = meter.create_counter(
    "orders_failed_total",
    description="Total failed orders",
    unit="1",
)

# Histograms
order_value = meter.create_histogram(
    "order_value_dollars",
    description="Order value distribution",
    unit="USD",
)

order_processing_time = meter.create_histogram(
    "order_processing_seconds",
    description="Time to process orders",
    unit="s",
)

# UpDownCounters
active_orders = meter.create_up_down_counter(
    "active_orders",
    description="Orders being processed",
    unit="1",
)

# Observable Gauges
def get_cpu_usage(options):
    """Callback for CPU usage gauge."""
    yield metrics.Observation(
        psutil.cpu_percent(),
        {"cpu": "total"},
    )

cpu_usage = meter.create_observable_gauge(
    "system_cpu_percent",
    callbacks=[get_cpu_usage],
    description="CPU usage percentage",
    unit="%",
)

def get_memory_usage(options):
    """Callback for memory usage gauge."""
    mem = psutil.virtual_memory()
    yield metrics.Observation(mem.used, {"type": "used"})
    yield metrics.Observation(mem.available, {"type": "available"})

memory_usage = meter.create_observable_gauge(
    "system_memory_bytes",
    callbacks=[get_memory_usage],
    description="Memory usage in bytes",
    unit="By",
)


# Helper functions
def record_order_created(customer_id: str, region: str, value: float):
    """Record successful order metrics."""
    labels = {
        "customer_type": "enterprise" if customer_id.startswith("ENT") else "standard",
        "region": region,
    }
    orders_created.add(1, labels)
    order_value.record(value, labels)


def record_order_failed(reason: str, region: str):
    """Record failed order metrics."""
    orders_failed.add(1, {"reason": reason, "region": region})


class OrderProcessingContext:
    """Context manager for tracking order processing."""
    
    def __init__(self, order_type: str):
        self.order_type = order_type
        self.start_time = None
    
    def __enter__(self):
        import time
        self.start_time = time.time()
        active_orders.add(1)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        duration = time.time() - self.start_time
        status = "error" if exc_type else "success"
        
        order_processing_time.record(duration, {
            "order_type": self.order_type,
            "status": status,
        })
        active_orders.add(-1)


# Usage
async def process_order(order):
    with OrderProcessingContext(order.type):
        # Processing logic
        pass
```

## Context Propagation

```python title="propagation.py"
from opentelemetry import trace
from opentelemetry.propagate import inject, extract
import requests
import httpx

tracer = trace.get_tracer("my-service")


def call_downstream_sync(url: str, data: dict) -> dict:
    """Call downstream service with trace propagation (sync)."""
    headers = {}
    inject(headers)  # Inject trace context
    
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()


async def call_downstream_async(url: str, data: dict) -> dict:
    """Call downstream service with trace propagation (async)."""
    headers = {}
    inject(headers)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()


# Extract context from incoming request (usually handled by instrumentation)
from flask import request

@app.before_request
def extract_context():
    """Extract trace context from incoming request headers."""
    ctx = extract(request.headers)
    # Context is now available for child spans
```

## Celery Integration

```python title="celery_app.py"
from celery import Celery
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from telemetry import setup_telemetry, get_tracer

# Initialize telemetry
tracer = setup_telemetry()

# Create Celery app
app = Celery("tasks", broker="redis://localhost:6379/0")

# Instrument Celery
CeleryInstrumentor().instrument()


@app.task
def process_order_task(order_id: str, user_id: str, total: float):
    """Celery task with automatic tracing."""
    # Span is automatically created by instrumentation
    span = trace.get_current_span()
    span.set_attributes({
        "order.id": order_id,
        "order.user_id": user_id,
        "order.total": total,
    })
    
    with tracer.start_as_current_span("process_payment"):
        # Payment logic
        pass
    
    with tracer.start_as_current_span("send_notification"):
        # Notification logic
        pass
    
    return {"status": "completed"}
```

## Docker Integration

```dockerfile title="Dockerfile"
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Option 1: Auto-instrumentation
CMD ["opentelemetry-instrument", "--service_name", "my-python-service", "python", "app.py"]

# Option 2: SDK integration
# CMD ["python", "app.py"]
```

```yaml title="docker-compose.yml"
services:
  my-python-service:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OTEL_SERVICE_NAME=my-python-service
      - OTEL_EXPORTER_OTLP_ENDPOINT=otel-collector:4317
      - OTEL_ENVIRONMENT=production
    networks:
      - observability

networks:
  observability:
    external: true
```

## Best Practices

### 1. Initialize Telemetry First

```python
# CORRECT
from telemetry import setup_telemetry
tracer = setup_telemetry()

from flask import Flask
app = Flask(__name__)

# WRONG - Flask loaded before telemetry
from flask import Flask
app = Flask(__name__)

from telemetry import setup_telemetry  # Too late!
```

### 2. Use Context Managers for Spans

```python
# Good: Span automatically ends
with tracer.start_as_current_span("my_operation") as span:
    span.set_attribute("key", "value")
    do_work()

# Manual: Must remember to end span
span = tracer.start_span("my_operation")
try:
    do_work()
finally:
    span.end()
```

### 3. Add Business Context

```python
span.set_attributes({
    "order.id": order_id,
    "customer.tier": customer.tier,
    "payment.method": payment_method,
})
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No traces | Telemetry not initialized | Call `setup_telemetry()` before imports |
| Missing spans | Context not propagating | Use `start_as_current_span` |
| gRPC errors | Wrong endpoint format | Use `host:port`, not `http://host:port` |
| Memory issues | Spans not ending | Use context managers |
| High latency | Sync exporter | Use `BatchSpanProcessor` |

---

**Next**: [Java Integration →](./java)
