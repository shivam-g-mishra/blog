---
sidebar_position: 6
title: Java Integration
description: Complete guide to instrumenting Java applications with OpenTelemetry - Spring Boot, Micronaut, Quarkus, and the Java Agent.
keywords: [java, spring boot, opentelemetry, otel, instrumentation, tracing, micrometer]
---

# Java OpenTelemetry Integration

A comprehensive guide to instrumenting Java applications with OpenTelemetry. Java offers multiple integration paths: the zero-code Java Agent and the OpenTelemetry SDK.

## Prerequisites

- Java 11+ (17+ recommended)
- OpenTelemetry Collector running (see [Single-Node Setup](/blog/single-node-observability-setup))
- Maven or Gradle

## Integration Options

| Option | Best For | Effort | Control |
|--------|----------|--------|---------|
| **Java Agent** | Existing apps, quick start | Zero code | Limited |
| **SDK + Auto** | New apps, some customization | Low | Medium |
| **SDK Manual** | Full control, performance-critical | High | Full |

## Option 1: Java Agent (Zero-Code)

The OpenTelemetry Java Agent provides automatic instrumentation for 100+ libraries.

### Download the Agent

```bash
# Download latest agent
curl -L -o opentelemetry-javaagent.jar \
  https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/latest/download/opentelemetry-javaagent.jar
```

### Run with Agent

```bash
java -javaagent:opentelemetry-javaagent.jar \
     -Dotel.service.name=my-java-service \
     -Dotel.exporter.otlp.endpoint=http://localhost:4317 \
     -Dotel.exporter.otlp.protocol=grpc \
     -Dotel.metrics.exporter=otlp \
     -Dotel.logs.exporter=otlp \
     -jar my-application.jar
```

### Agent Configuration

```properties title="otel.properties"
# Service identification
otel.service.name=my-java-service
otel.service.version=1.0.0
otel.resource.attributes=deployment.environment=production

# Exporter configuration
otel.exporter.otlp.endpoint=http://localhost:4317
otel.exporter.otlp.protocol=grpc
otel.metrics.exporter=otlp
otel.logs.exporter=otlp

# Sampling (for high-traffic services)
otel.traces.sampler=parentbased_traceidratio
otel.traces.sampler.arg=0.1

# Disable specific instrumentations
otel.instrumentation.jdbc.enabled=true
otel.instrumentation.spring-webmvc.enabled=true
```

```bash
# Run with properties file
java -javaagent:opentelemetry-javaagent.jar \
     -Dotel.javaagent.configuration-file=otel.properties \
     -jar my-application.jar
```

## Option 2: Spring Boot with SDK

### Dependencies (Maven)

```xml title="pom.xml"
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>io.opentelemetry</groupId>
            <artifactId>opentelemetry-bom</artifactId>
            <version>1.34.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
        <dependency>
            <groupId>io.opentelemetry.instrumentation</groupId>
            <artifactId>opentelemetry-instrumentation-bom-alpha</artifactId>
            <version>2.0.0-alpha</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependencies>
    <!-- OpenTelemetry API and SDK -->
    <dependency>
        <groupId>io.opentelemetry</groupId>
        <artifactId>opentelemetry-api</artifactId>
    </dependency>
    <dependency>
        <groupId>io.opentelemetry</groupId>
        <artifactId>opentelemetry-sdk</artifactId>
    </dependency>
    <dependency>
        <groupId>io.opentelemetry</groupId>
        <artifactId>opentelemetry-sdk-extension-autoconfigure</artifactId>
    </dependency>
    
    <!-- OTLP Exporters -->
    <dependency>
        <groupId>io.opentelemetry</groupId>
        <artifactId>opentelemetry-exporter-otlp</artifactId>
    </dependency>
    
    <!-- Spring Boot Starter -->
    <dependency>
        <groupId>io.opentelemetry.instrumentation</groupId>
        <artifactId>opentelemetry-spring-boot-starter</artifactId>
    </dependency>
    
    <!-- Micrometer Bridge (for Spring metrics) -->
    <dependency>
        <groupId>io.opentelemetry.instrumentation</groupId>
        <artifactId>opentelemetry-micrometer-1.5</artifactId>
    </dependency>
</dependencies>
```

### Dependencies (Gradle)

```kotlin title="build.gradle.kts"
plugins {
    java
    id("org.springframework.boot") version "3.2.0"
    id("io.spring.dependency-management") version "1.1.4"
}

dependencyManagement {
    imports {
        mavenBom("io.opentelemetry:opentelemetry-bom:1.34.0")
        mavenBom("io.opentelemetry.instrumentation:opentelemetry-instrumentation-bom-alpha:2.0.0-alpha")
    }
}

dependencies {
    implementation("io.opentelemetry:opentelemetry-api")
    implementation("io.opentelemetry:opentelemetry-sdk")
    implementation("io.opentelemetry:opentelemetry-sdk-extension-autoconfigure")
    implementation("io.opentelemetry:opentelemetry-exporter-otlp")
    implementation("io.opentelemetry.instrumentation:opentelemetry-spring-boot-starter")
}
```

### Configuration

```yaml title="application.yml"
spring:
  application:
    name: my-java-service

otel:
  service:
    name: ${spring.application.name}
  exporter:
    otlp:
      endpoint: http://localhost:4317
      protocol: grpc
  metrics:
    exporter: otlp
  logs:
    exporter: otlp
  resource:
    attributes:
      deployment.environment: ${ENVIRONMENT:development}
      service.version: ${VERSION:1.0.0}

management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  metrics:
    tags:
      application: ${spring.application.name}
```

### Telemetry Configuration Class

```java title="src/main/java/com/example/config/TelemetryConfig.java"
package com.example.config;

import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.api.metrics.Meter;
import io.opentelemetry.api.common.Attributes;
import io.opentelemetry.context.propagation.ContextPropagators;
import io.opentelemetry.exporter.otlp.trace.OtlpGrpcSpanExporter;
import io.opentelemetry.exporter.otlp.metrics.OtlpGrpcMetricExporter;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import io.opentelemetry.sdk.trace.SdkTracerProvider;
import io.opentelemetry.sdk.trace.export.BatchSpanProcessor;
import io.opentelemetry.sdk.metrics.SdkMeterProvider;
import io.opentelemetry.sdk.metrics.export.PeriodicMetricReader;
import io.opentelemetry.sdk.resources.Resource;
import io.opentelemetry.semconv.ResourceAttributes;
import io.opentelemetry.api.trace.propagation.W3CTraceContextPropagator;
import io.opentelemetry.context.propagation.TextMapPropagator;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.Duration;

@Configuration
public class TelemetryConfig {

    @Value("${otel.service.name:my-java-service}")
    private String serviceName;

    @Value("${otel.exporter.otlp.endpoint:http://localhost:4317}")
    private String otlpEndpoint;

    @Value("${otel.resource.attributes.deployment.environment:development}")
    private String environment;

    @Bean
    public OpenTelemetry openTelemetry() {
        // Create resource
        Resource resource = Resource.getDefault()
            .merge(Resource.create(Attributes.builder()
                .put(ResourceAttributes.SERVICE_NAME, serviceName)
                .put(ResourceAttributes.SERVICE_VERSION, "1.0.0")
                .put(ResourceAttributes.DEPLOYMENT_ENVIRONMENT, environment)
                .build()));

        // Create trace exporter
        OtlpGrpcSpanExporter spanExporter = OtlpGrpcSpanExporter.builder()
            .setEndpoint(otlpEndpoint)
            .setTimeout(Duration.ofSeconds(10))
            .build();

        // Create tracer provider with batch processing
        // BatchSpanProcessor groups spans before export to reduce network overhead
        SdkTracerProvider tracerProvider = SdkTracerProvider.builder()
            .setResource(resource)
            .addSpanProcessor(BatchSpanProcessor.builder(spanExporter)
                .setScheduleDelay(Duration.ofSeconds(5))  // Max wait before sending a batch
                .setMaxExportBatchSize(512)               // Spans per batch (tune for your payload size)
                .setMaxQueueSize(2048)                    // Buffer size - prevents OOM under high load
                .build())
            .build();

        // Create metric exporter
        OtlpGrpcMetricExporter metricExporter = OtlpGrpcMetricExporter.builder()
            .setEndpoint(otlpEndpoint)
            .build();

        // Create meter provider
        SdkMeterProvider meterProvider = SdkMeterProvider.builder()
            .setResource(resource)
            .registerMetricReader(PeriodicMetricReader.builder(metricExporter)
                .setInterval(Duration.ofSeconds(15))
                .build())
            .build();

        // Build OpenTelemetry instance
        return OpenTelemetrySdk.builder()
            .setTracerProvider(tracerProvider)
            .setMeterProvider(meterProvider)
            .setPropagators(ContextPropagators.create(
                W3CTraceContextPropagator.getInstance()))
            .buildAndRegisterGlobal();
    }

    @Bean
    public Tracer tracer(OpenTelemetry openTelemetry) {
        return openTelemetry.getTracer(serviceName);
    }

    @Bean
    public Meter meter(OpenTelemetry openTelemetry) {
        return openTelemetry.getMeter(serviceName);
    }
}
```

### Service with Custom Spans

```java title="src/main/java/com/example/service/OrderService.java"
package com.example.service;

import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.SpanKind;
import io.opentelemetry.api.trace.StatusCode;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.api.common.AttributeKey;
import io.opentelemetry.api.common.Attributes;
import io.opentelemetry.context.Context;
import io.opentelemetry.context.Scope;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

@Service
public class OrderService {

    private static final Logger log = LoggerFactory.getLogger(OrderService.class);
    
    private final Tracer tracer;
    private final PaymentService paymentService;
    private final InventoryService inventoryService;

    public OrderService(Tracer tracer, PaymentService paymentService, 
                       InventoryService inventoryService) {
        this.tracer = tracer;
        this.paymentService = paymentService;
        this.inventoryService = inventoryService;
    }

    public OrderResult createOrder(CreateOrderRequest request) {
        // Create span for entire operation
        Span span = tracer.spanBuilder("createOrder")
            .setSpanKind(SpanKind.INTERNAL)
            .setAttribute("order.user_id", request.getUserId())
            .setAttribute("order.items_count", request.getItems().size())
            .setAttribute("order.total", request.getTotal().doubleValue())
            .startSpan();

        try (Scope scope = span.makeCurrent()) {
            log.info("Creating order for user {}", request.getUserId());

            // Step 1: Validate order
            validateOrder(request);

            // Step 2: Reserve inventory
            reserveInventory(request.getItems());

            // Step 3: Process payment
            PaymentResult payment = processPayment(request);

            // Step 4: Save order
            String orderId = saveOrder(request, payment);

            span.setAttribute("order.id", orderId);
            span.setStatus(StatusCode.OK);

            log.info("Order {} created successfully", orderId);
            return new OrderResult(orderId, "created");

        } catch (Exception e) {
            log.error("Failed to create order: {}", e.getMessage(), e);
            span.recordException(e);
            span.setStatus(StatusCode.ERROR, e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }

    private void validateOrder(CreateOrderRequest request) {
        Span span = tracer.spanBuilder("validateOrder")
            .setSpanKind(SpanKind.INTERNAL)
            .startSpan();

        try (Scope scope = span.makeCurrent()) {
            // Validation logic
            Thread.sleep(10);
            
            span.setAttribute("validation.passed", true);
            span.addEvent("Validation completed", Attributes.of(
                AttributeKey.stringKey("validation.type"), "full"
            ));
            
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            span.recordException(e);
        } finally {
            span.end();
        }
    }

    private void reserveInventory(List<OrderItem> items) {
        Span span = tracer.spanBuilder("reserveInventory")
            .setSpanKind(SpanKind.CLIENT)
            .setAttribute("inventory.items_count", items.size())
            .startSpan();

        try (Scope scope = span.makeCurrent()) {
            for (OrderItem item : items) {
                Span itemSpan = tracer.spanBuilder("reserveItem")
                    .setSpanKind(SpanKind.CLIENT)
                    .setAttribute("item.sku", item.getSku())
                    .setAttribute("item.quantity", item.getQuantity())
                    .startSpan();

                try (Scope itemScope = itemSpan.makeCurrent()) {
                    inventoryService.reserve(item.getSku(), item.getQuantity());
                } finally {
                    itemSpan.end();
                }
            }
        } finally {
            span.end();
        }
    }

    private PaymentResult processPayment(CreateOrderRequest request) {
        Span span = tracer.spanBuilder("processPayment")
            .setSpanKind(SpanKind.CLIENT)
            .setAttribute("payment.amount", request.getTotal().doubleValue())
            .setAttribute("payment.currency", "USD")
            .setAttribute("peer.service", "payment-service")
            .startSpan();

        try (Scope scope = span.makeCurrent()) {
            PaymentResult result = paymentService.charge(
                request.getUserId(),
                request.getTotal()
            );

            span.setAttribute("payment.transaction_id", result.getTransactionId());
            span.setAttribute("payment.status", result.getStatus());

            return result;
        } finally {
            span.end();
        }
    }

    private String saveOrder(CreateOrderRequest request, PaymentResult payment) {
        Span span = tracer.spanBuilder("saveOrder")
            .setSpanKind(SpanKind.CLIENT)
            .setAttribute(AttributeKey.stringKey("db.system"), "postgresql")
            .setAttribute(AttributeKey.stringKey("db.operation"), "INSERT")
            .startSpan();

        try (Scope scope = span.makeCurrent()) {
            Thread.sleep(30);
            
            String orderId = UUID.randomUUID().toString();
            span.setAttribute("db.order_id", orderId);
            
            return orderId;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            span.recordException(e);
            throw new RuntimeException(e);
        } finally {
            span.end();
        }
    }
}
```

### Custom Metrics

```java title="src/main/java/com/example/metrics/ApplicationMetrics.java"
package com.example.metrics;

import io.opentelemetry.api.metrics.Meter;
import io.opentelemetry.api.metrics.LongCounter;
import io.opentelemetry.api.metrics.DoubleHistogram;
import io.opentelemetry.api.metrics.LongUpDownCounter;
import io.opentelemetry.api.metrics.ObservableLongGauge;
import io.opentelemetry.api.common.Attributes;
import org.springframework.stereotype.Component;

import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
import java.util.concurrent.atomic.AtomicLong;

@Component
public class ApplicationMetrics {

    private final LongCounter ordersCreated;
    private final LongCounter ordersFailed;
    private final DoubleHistogram orderProcessingTime;
    private final DoubleHistogram orderValue;
    private final LongUpDownCounter activeOrders;
    private final AtomicLong queueDepth = new AtomicLong(0);

    public ApplicationMetrics(Meter meter) {
        // Counter for successful orders
        this.ordersCreated = meter.counterBuilder("orders_created_total")
            .setDescription("Total orders created")
            .setUnit("{order}")
            .build();

        // Counter for failed orders
        this.ordersFailed = meter.counterBuilder("orders_failed_total")
            .setDescription("Total failed orders")
            .setUnit("{order}")
            .build();

        // Histogram for processing time
        this.orderProcessingTime = meter.histogramBuilder("order_processing_seconds")
            .setDescription("Time to process orders")
            .setUnit("s")
            .setExplicitBucketBoundariesAdvice(
                java.util.List.of(0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0))
            .build();

        // Histogram for order values
        this.orderValue = meter.histogramBuilder("order_value_dollars")
            .setDescription("Order value distribution")
            .setUnit("USD")
            .build();

        // UpDownCounter for active orders
        this.activeOrders = meter.upDownCounterBuilder("active_orders")
            .setDescription("Orders being processed")
            .setUnit("{order}")
            .build();

        // Observable gauge for queue depth
        meter.gaugeBuilder("order_queue_depth")
            .setDescription("Current order queue depth")
            .setUnit("{order}")
            .buildWithCallback(measurement -> 
                measurement.record(queueDepth.get()));

        // Observable gauge for heap memory
        MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
        meter.gaugeBuilder("jvm_heap_used_bytes")
            .setDescription("JVM heap memory used")
            .setUnit("By")
            .buildWithCallback(measurement ->
                measurement.record(memoryBean.getHeapMemoryUsage().getUsed()));
    }

    public void recordOrderCreated(String customerId, String region, double value) {
        Attributes attrs = Attributes.builder()
            .put("customer_type", customerId.startsWith("ENT") ? "enterprise" : "standard")
            .put("region", region)
            .build();

        ordersCreated.add(1, attrs);
        orderValue.record(value, attrs);
    }

    public void recordOrderFailed(String reason, String region) {
        ordersFailed.add(1, Attributes.builder()
            .put("reason", reason)
            .put("region", region)
            .build());
    }

    public void recordProcessingTime(double seconds, String orderType, boolean success) {
        orderProcessingTime.record(seconds, Attributes.builder()
            .put("order_type", orderType)
            .put("status", success ? "success" : "error")
            .build());
    }

    public void orderProcessingStarted() {
        activeOrders.add(1);
    }

    public void orderProcessingCompleted() {
        activeOrders.add(-1);
    }

    public void setQueueDepth(long depth) {
        queueDepth.set(depth);
    }
}
```

### REST Controller

```java title="src/main/java/com/example/controller/OrderController.java"
package com.example.controller;

import com.example.service.OrderService;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.instrumentation.annotations.WithSpan;
import io.opentelemetry.instrumentation.annotations.SpanAttribute;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class OrderController {

    private static final Logger log = LoggerFactory.getLogger(OrderController.class);
    
    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @GetMapping("/users/{userId}")
    @WithSpan("getUserById")  // Automatic span creation
    public ResponseEntity<UserResponse> getUser(
            @SpanAttribute("user.id") @PathVariable String userId) {
        
        log.info("Fetching user {}", userId);
        
        // Current span is automatically created by @WithSpan
        Span.current().setAttribute("handler", "getUserById");
        
        // Simulate database lookup
        UserResponse user = new UserResponse(userId, "John Doe", "john@example.com");
        
        return ResponseEntity.ok(user);
    }

    @PostMapping("/orders")
    public ResponseEntity<OrderResult> createOrder(@RequestBody CreateOrderRequest request) {
        // Span is created by Spring instrumentation
        Span.current().setAttributes(
            io.opentelemetry.api.common.Attributes.builder()
                .put("order.user_id", request.getUserId())
                .put("order.items_count", request.getItems().size())
                .build()
        );

        try {
            OrderResult result = orderService.createOrder(request);
            return ResponseEntity.status(HttpStatus.CREATED).body(result);
        } catch (Exception e) {
            log.error("Order creation failed", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(new OrderResult(null, "failed"));
        }
    }

    @GetMapping("/health")
    public ResponseEntity<HealthResponse> health() {
        return ResponseEntity.ok(new HealthResponse("healthy"));
    }
}
```

### Logging with MDC (Trace Context)

```java title="src/main/java/com/example/config/LoggingConfig.java"
package com.example.config;

import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.SpanContext;
import org.slf4j.MDC;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

@Component
public class LoggingConfig extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain) 
            throws ServletException, IOException {
        
        try {
            SpanContext spanContext = Span.current().getSpanContext();
            if (spanContext.isValid()) {
                MDC.put("traceId", spanContext.getTraceId());
                MDC.put("spanId", spanContext.getSpanId());
            }
            filterChain.doFilter(request, response);
        } finally {
            MDC.remove("traceId");
            MDC.remove("spanId");
        }
    }
}
```

```xml title="src/main/resources/logback-spring.xml"
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} [traceId=%X{traceId}, spanId=%X{spanId}] - %msg%n</pattern>
        </encoder>
    </appender>

    <appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
        <encoder class="net.logstash.logback.encoder.LogstashEncoder">
            <includeMdcKeyName>traceId</includeMdcKeyName>
            <includeMdcKeyName>spanId</includeMdcKeyName>
        </encoder>
    </appender>

    <root level="INFO">
        <appender-ref ref="JSON"/>
    </root>
</configuration>
```

## Docker Integration

```dockerfile title="Dockerfile"
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Download OpenTelemetry Java Agent
ADD https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/latest/download/opentelemetry-javaagent.jar /app/opentelemetry-javaagent.jar

COPY target/*.jar app.jar

EXPOSE 8080

# Run with Java Agent
ENTRYPOINT ["java", \
    "-javaagent:/app/opentelemetry-javaagent.jar", \
    "-Dotel.service.name=${OTEL_SERVICE_NAME:-my-java-service}", \
    "-Dotel.exporter.otlp.endpoint=${OTEL_EXPORTER_OTLP_ENDPOINT:-http://localhost:4317}", \
    "-jar", "app.jar"]
```

```yaml title="docker-compose.yml"
services:
  my-java-service:
    build: .
    ports:
      - "8080:8080"
    environment:
      - OTEL_SERVICE_NAME=my-java-service
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
      - OTEL_METRICS_EXPORTER=otlp
      - OTEL_LOGS_EXPORTER=otlp
    networks:
      - observability

networks:
  observability:
    external: true
```

## Best Practices

### 1. Use @WithSpan for Simple Cases

```java
@WithSpan("processPayment")
public PaymentResult process(@SpanAttribute("payment.amount") BigDecimal amount) {
    // Automatically traced
}
```

### 2. Manual Spans for Complex Logic

```java
Span span = tracer.spanBuilder("complexOperation")
    .setSpanKind(SpanKind.CLIENT)
    .setAttribute("db.system", "postgresql")
    .startSpan();

try (Scope scope = span.makeCurrent()) {
    // Your code
} finally {
    span.end();
}
```

### 3. Always Close Spans

```java
// Good: try-with-resources ensures span ends
try (Scope scope = span.makeCurrent()) {
    doWork();
} finally {
    span.end();
}

// Good: explicit finally block
Span span = tracer.spanBuilder("operation").startSpan();
try {
    doWork();
} finally {
    span.end();
}
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No traces | Agent not loaded | Check `-javaagent` flag |
| Missing spans | Scope not current | Use `span.makeCurrent()` |
| High memory | Too many spans | Enable sampling |
| Duplicate traces | Agent + SDK | Use only one approach |
| gRPC errors | Wrong protocol | Set `otel.exporter.otlp.protocol=grpc` |

---

These integration guides provide comprehensive coverage for the most popular languages and frameworks. Each guide follows a consistent pattern—from quick start to production-ready configurations.
