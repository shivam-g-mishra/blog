---
sidebar_position: 4
title: Node.js Integration
description: Complete guide to instrumenting Node.js and TypeScript applications with OpenTelemetry - Express, Fastify, NestJS, and more.
keywords: [nodejs, javascript, typescript, express, opentelemetry, otel, instrumentation]
---

# Node.js OpenTelemetry Integration

A comprehensive guide to instrumenting Node.js applications with OpenTelemetry. Node.js has excellent auto-instrumentation support that captures most common operations automatically.

## Prerequisites

- Node.js 18+ (LTS recommended)
- OpenTelemetry Collector running (see [Single-Node Setup](https://shivamm.info/blog/blog/single-node-observability-setup))
- npm or yarn package manager

## Installation

```bash
# Core SDK
npm install @opentelemetry/sdk-node \
            @opentelemetry/api

# Auto-instrumentation (recommended)
npm install @opentelemetry/auto-instrumentations-node

# Exporters
npm install @opentelemetry/exporter-trace-otlp-grpc \
            @opentelemetry/exporter-metrics-otlp-grpc \
            @opentelemetry/exporter-logs-otlp-grpc

# Logging integration
npm install @opentelemetry/sdk-logs \
            @opentelemetry/api-logs
```

## Project Structure

```
my-service/
├── src/
│   ├── instrumentation.ts   # OTel setup (loaded FIRST)
│   ├── app.ts               # Express/Fastify app
│   ├── routes/
│   ├── services/
│   └── metrics/
├── package.json
└── tsconfig.json
```

## Step 1: Create Instrumentation File

**This file must be loaded before any other application code.**

```typescript title="src/instrumentation.ts"
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-grpc';
import { OTLPLogExporter } from '@opentelemetry/exporter-logs-otlp-grpc';
import { PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { BatchLogRecordProcessor } from '@opentelemetry/sdk-logs';
import { Resource } from '@opentelemetry/resources';
import { 
  SEMRESATTRS_SERVICE_NAME,
  SEMRESATTRS_SERVICE_VERSION,
  SEMRESATTRS_DEPLOYMENT_ENVIRONMENT,
} from '@opentelemetry/semantic-conventions';
import { diag, DiagConsoleLogger, DiagLogLevel } from '@opentelemetry/api';

// Enable debug logging in development
if (process.env.NODE_ENV === 'development') {
  diag.setLogger(new DiagConsoleLogger(), DiagLogLevel.INFO);
}

const OTLP_ENDPOINT = process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4317';

// Define service resource
const resource = new Resource({
  [SEMRESATTRS_SERVICE_NAME]: process.env.OTEL_SERVICE_NAME || 'my-nodejs-service',
  [SEMRESATTRS_SERVICE_VERSION]: process.env.npm_package_version || '1.0.0',
  [SEMRESATTRS_DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV || 'development',
});

// Create exporters
const traceExporter = new OTLPTraceExporter({
  url: OTLP_ENDPOINT,
});

const metricExporter = new OTLPMetricExporter({
  url: OTLP_ENDPOINT,
});

const logExporter = new OTLPLogExporter({
  url: OTLP_ENDPOINT,
});

// Configure SDK
const sdk = new NodeSDK({
  resource,
  traceExporter,
  metricReader: new PeriodicExportingMetricReader({
    exporter: metricExporter,
    exportIntervalMillis: 15000, // Export metrics every 15 seconds
  }),
  logRecordProcessor: new BatchLogRecordProcessor(logExporter),
  instrumentations: [
    getNodeAutoInstrumentations({
      // Disable noisy instrumentations
      '@opentelemetry/instrumentation-fs': {
        enabled: false,
      },
      '@opentelemetry/instrumentation-dns': {
        enabled: false,
      },
      // Configure HTTP instrumentation
      '@opentelemetry/instrumentation-http': {
        ignoreIncomingPaths: ['/health', '/ready', '/metrics'],
        ignoreOutgoingUrls: [/localhost:4317/], // Don't trace OTel calls
      },
      // Configure Express instrumentation
      '@opentelemetry/instrumentation-express': {
        ignoreLayersType: ['middleware'],
      },
    }),
  ],
});

// Graceful shutdown
const shutdown = async () => {
  console.log('Shutting down OpenTelemetry...');
  try {
    await sdk.shutdown();
    console.log('OpenTelemetry shut down successfully');
  } catch (error) {
    console.error('Error shutting down OpenTelemetry', error);
  }
};

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);

// Start SDK
sdk.start();
console.log(`OpenTelemetry initialized for ${process.env.OTEL_SERVICE_NAME || 'my-nodejs-service'}`);

export { sdk };
```

## Step 2: Load Instrumentation First

### Option A: Using --require flag (Recommended)

```json title="package.json"
{
  "scripts": {
    "start": "node --require ./dist/instrumentation.js ./dist/app.js",
    "dev": "ts-node-dev --require ./src/instrumentation.ts ./src/app.ts"
  }
}
```

### Option B: Import at Top of Entry File

```typescript title="src/app.ts"
// MUST be first import
import './instrumentation';

import express from 'express';
// ... rest of imports
```

## Step 3: Express Application with Custom Spans

```typescript title="src/app.ts"
import './instrumentation';

import express, { Request, Response, NextFunction } from 'express';
import { trace, SpanStatusCode, context, SpanKind } from '@opentelemetry/api';
import { metrics } from '@opentelemetry/api';

const app = express();
app.use(express.json());

// Get tracer and meter
const tracer = trace.getTracer('my-nodejs-service');
const meter = metrics.getMeter('my-nodejs-service');

// Create custom metrics
const requestCounter = meter.createCounter('http_requests_total', {
  description: 'Total HTTP requests',
  unit: '{request}',
});

const requestDuration = meter.createHistogram('http_request_duration_seconds', {
  description: 'HTTP request duration',
  unit: 's',
});

const activeRequests = meter.createUpDownCounter('http_active_requests', {
  description: 'Number of active HTTP requests',
  unit: '{request}',
});

// Metrics middleware
app.use((req: Request, res: Response, next: NextFunction) => {
  const startTime = Date.now();
  activeRequests.add(1);

  res.on('finish', () => {
    const duration = (Date.now() - startTime) / 1000;
    const labels = {
      method: req.method,
      route: req.route?.path || req.path,
      status_code: res.statusCode.toString(),
    };

    requestCounter.add(1, labels);
    requestDuration.record(duration, labels);
    activeRequests.add(-1);
  });

  next();
});

// Health check (not traced due to filter)
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// Example endpoint with custom spans
app.get('/api/users/:id', async (req: Request, res: Response) => {
  const userId = req.params.id;
  
  // Get current span and add attributes
  const span = trace.getActiveSpan();
  span?.setAttribute('user.id', userId);

  console.log(`Fetching user ${userId}`);

  try {
    // Create child span for database operation
    const user = await tracer.startActiveSpan(
      'db.getUser',
      { kind: SpanKind.CLIENT },
      async (dbSpan) => {
        dbSpan.setAttribute('db.system', 'postgresql');
        dbSpan.setAttribute('db.operation', 'SELECT');
        dbSpan.setAttribute('db.sql.table', 'users');

        // Simulate database query
        await new Promise(resolve => setTimeout(resolve, 50));

        dbSpan.end();
        return { id: userId, name: 'John Doe', email: 'john@example.com' };
      }
    );

    res.json(user);
  } catch (error) {
    span?.recordException(error as Error);
    span?.setStatus({ code: SpanStatusCode.ERROR, message: (error as Error).message });
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Order creation with nested spans
app.post('/api/orders', async (req: Request, res: Response) => {
  const span = trace.getActiveSpan();
  const { userId, items, total } = req.body;

  span?.setAttributes({
    'order.user_id': userId,
    'order.items_count': items?.length || 0,
    'order.total': total,
  });

  try {
    const result = await processOrder(userId, items, total);
    res.status(201).json(result);
  } catch (error) {
    span?.recordException(error as Error);
    span?.setStatus({ code: SpanStatusCode.ERROR });
    res.status(500).json({ error: 'Order processing failed' });
  }
});

async function processOrder(userId: string, items: any[], total: number) {
  return tracer.startActiveSpan('processOrder', async (span) => {
    try {
      // Validate order
      await tracer.startActiveSpan('validateOrder', async (validateSpan) => {
        await new Promise(resolve => setTimeout(resolve, 10));
        validateSpan.setAttribute('validation.passed', true);
        validateSpan.end();
      });

      // Reserve inventory
      await tracer.startActiveSpan(
        'reserveInventory',
        { kind: SpanKind.CLIENT },
        async (inventorySpan) => {
          inventorySpan.setAttribute('inventory.items_count', items.length);
          await new Promise(resolve => setTimeout(resolve, 50));
          inventorySpan.end();
        }
      );

      // Process payment
      await tracer.startActiveSpan(
        'processPayment',
        { kind: SpanKind.CLIENT },
        async (paymentSpan) => {
          paymentSpan.setAttributes({
            'payment.amount': total,
            'payment.currency': 'USD',
          });
          await new Promise(resolve => setTimeout(resolve, 100));
          paymentSpan.setAttribute('payment.status', 'approved');
          paymentSpan.end();
        }
      );

      // Save order
      const orderId = `order_${Date.now()}`;
      await tracer.startActiveSpan(
        'saveOrder',
        { kind: SpanKind.CLIENT },
        async (saveSpan) => {
          saveSpan.setAttributes({
            'db.system': 'postgresql',
            'db.operation': 'INSERT',
          });
          await new Promise(resolve => setTimeout(resolve, 30));
          saveSpan.setAttribute('order.id', orderId);
          saveSpan.end();
        }
      );

      span.setAttribute('order.id', orderId);
      span.setStatus({ code: SpanStatusCode.OK });

      return { orderId, status: 'created' };
    } catch (error) {
      span.recordException(error as Error);
      span.setStatus({ code: SpanStatusCode.ERROR });
      throw error;
    } finally {
      span.end();
    }
  });
}

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

## Step 4: Custom Metrics Module

```typescript title="src/metrics/index.ts"
import { metrics, ValueType } from '@opentelemetry/api';

const meter = metrics.getMeter('my-nodejs-service');

// Business metrics
export const ordersCreated = meter.createCounter('orders_created_total', {
  description: 'Total orders created',
  unit: '{order}',
});

export const orderValue = meter.createHistogram('order_value_dollars', {
  description: 'Order value distribution',
  unit: 'USD',
});

export const orderProcessingTime = meter.createHistogram('order_processing_seconds', {
  description: 'Time to process orders',
  unit: 's',
});

export const activeOrders = meter.createUpDownCounter('active_orders', {
  description: 'Orders currently being processed',
  unit: '{order}',
});

// Observable gauge for queue depth
let queueDepth = 0;
meter.createObservableGauge('order_queue_depth', {
  description: 'Current order queue depth',
  unit: '{order}',
}, (observableResult) => {
  observableResult.observe(queueDepth);
});

export function setQueueDepth(depth: number) {
  queueDepth = depth;
}

// Helper functions
export function recordOrderCreated(
  customerId: string,
  region: string,
  value: number
) {
  ordersCreated.add(1, {
    customer_type: customerId.startsWith('ENT') ? 'enterprise' : 'standard',
    region,
  });
  orderValue.record(value, { region });
}

export function recordOrderFailed(reason: string, region: string) {
  meter.createCounter('orders_failed_total').add(1, { reason, region });
}

export function measureProcessingTime(
  fn: () => Promise<void>,
  orderType: string
): Promise<void> {
  const startTime = Date.now();
  activeOrders.add(1);

  return fn()
    .then(() => {
      orderProcessingTime.record((Date.now() - startTime) / 1000, {
        order_type: orderType,
        status: 'success',
      });
    })
    .catch((error) => {
      orderProcessingTime.record((Date.now() - startTime) / 1000, {
        order_type: orderType,
        status: 'error',
      });
      throw error;
    })
    .finally(() => {
      activeOrders.add(-1);
    });
}
```

## Step 5: Structured Logging with Trace Context

```typescript title="src/logger.ts"
import { context, trace } from '@opentelemetry/api';
import pino from 'pino';

// Create base logger
const baseLogger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
});

// Logger that automatically includes trace context
export function getLogger(name?: string) {
  return {
    info: (msg: string, data?: Record<string, any>) => log('info', msg, data, name),
    warn: (msg: string, data?: Record<string, any>) => log('warn', msg, data, name),
    error: (msg: string, data?: Record<string, any>) => log('error', msg, data, name),
    debug: (msg: string, data?: Record<string, any>) => log('debug', msg, data, name),
  };
}

function log(
  level: 'info' | 'warn' | 'error' | 'debug',
  msg: string,
  data?: Record<string, any>,
  name?: string
) {
  const span = trace.getActiveSpan();
  const spanContext = span?.spanContext();

  const logData = {
    ...data,
    ...(name && { logger: name }),
    ...(spanContext && {
      trace_id: spanContext.traceId,
      span_id: spanContext.spanId,
    }),
  };

  baseLogger[level](logData, msg);
}

// Usage example
const logger = getLogger('OrderService');

export async function processOrder(orderId: string) {
  // trace_id and span_id automatically included
  logger.info('Processing order', { orderId });

  try {
    // ... processing logic
    logger.info('Order processed successfully', { orderId });
  } catch (error) {
    logger.error('Order processing failed', { orderId, error: (error as Error).message });
    throw error;
  }
}
```

## Step 6: HTTP Client with Context Propagation

```typescript title="src/clients/payment-client.ts"
import { trace, SpanKind, SpanStatusCode, context, propagation } from '@opentelemetry/api';
import axios, { AxiosInstance } from 'axios';

const tracer = trace.getTracer('http-client');

export class PaymentClient {
  private client: AxiosInstance;

  constructor(baseURL: string) {
    this.client = axios.create({
      baseURL,
      timeout: 30000,
    });

    // Add request interceptor to inject trace context
    this.client.interceptors.request.use((config) => {
      const headers: Record<string, string> = {};
      propagation.inject(context.active(), headers);
      
      config.headers = {
        ...config.headers,
        ...headers,
      };
      
      return config;
    });
  }

  async charge(userId: string, amount: number): Promise<PaymentResult> {
    return tracer.startActiveSpan(
      'payment.charge',
      { kind: SpanKind.CLIENT },
      async (span) => {
        span.setAttributes({
          'payment.user_id': userId,
          'payment.amount': amount,
          'payment.currency': 'USD',
          'peer.service': 'payment-service',
        });

        try {
          const response = await this.client.post<PaymentResult>('/api/charge', {
            userId,
            amount,
          });

          span.setAttributes({
            'http.status_code': response.status,
            'payment.transaction_id': response.data.transactionId,
          });
          span.setStatus({ code: SpanStatusCode.OK });

          return response.data;
        } catch (error) {
          span.recordException(error as Error);
          span.setStatus({ code: SpanStatusCode.ERROR });
          throw error;
        } finally {
          span.end();
        }
      }
    );
  }
}

interface PaymentResult {
  transactionId: string;
  status: string;
}
```

## Step 7: NestJS Integration

```typescript title="src/tracing.module.ts"
import { Module, OnModuleDestroy, OnModuleInit } from '@nestjs/common';
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';
import { Resource } from '@opentelemetry/resources';
import { SEMRESATTRS_SERVICE_NAME } from '@opentelemetry/semantic-conventions';

@Module({})
export class TracingModule implements OnModuleInit, OnModuleDestroy {
  private sdk: NodeSDK;

  onModuleInit() {
    this.sdk = new NodeSDK({
      resource: new Resource({
        [SEMRESATTRS_SERVICE_NAME]: process.env.OTEL_SERVICE_NAME,
      }),
      traceExporter: new OTLPTraceExporter({
        url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT,
      }),
      instrumentations: [getNodeAutoInstrumentations()],
    });

    this.sdk.start();
  }

  async onModuleDestroy() {
    await this.sdk.shutdown();
  }
}
```

```typescript title="src/decorators/trace.decorator.ts"
import { trace, SpanKind, SpanStatusCode } from '@opentelemetry/api';

export function Trace(spanName?: string) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;
    const tracer = trace.getTracer('nestjs-service');

    descriptor.value = async function (...args: any[]) {
      const name = spanName || `${target.constructor.name}.${propertyKey}`;

      return tracer.startActiveSpan(name, async (span) => {
        try {
          const result = await originalMethod.apply(this, args);
          span.setStatus({ code: SpanStatusCode.OK });
          return result;
        } catch (error) {
          span.recordException(error as Error);
          span.setStatus({ code: SpanStatusCode.ERROR });
          throw error;
        } finally {
          span.end();
        }
      });
    };

    return descriptor;
  };
}

// Usage
@Injectable()
export class OrderService {
  @Trace('order.create')
  async createOrder(dto: CreateOrderDto) {
    // Method is automatically traced
  }
}
```

## TypeScript Configuration

```json title="tsconfig.json"
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "esModuleInterop": true,
    "strict": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## Docker Integration

```dockerfile title="Dockerfile"
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./

EXPOSE 3000
CMD ["node", "--require", "./dist/instrumentation.js", "./dist/app.js"]
```

```yaml title="docker-compose.yml"
services:
  my-nodejs-service:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - OTEL_SERVICE_NAME=my-nodejs-service
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
    networks:
      - observability

networks:
  observability:
    external: true
```

## Best Practices

### 1. Always Load Instrumentation First

```typescript
// CORRECT: Instrumentation loads before everything
import './instrumentation';
import express from 'express';

// WRONG: Express loads before instrumentation
import express from 'express';
import './instrumentation'; // Too late!
```

### 2. Use startActiveSpan for Automatic Context

```typescript
// Good: Context automatically propagated
await tracer.startActiveSpan('myOperation', async (span) => {
  await doWork(); // Child spans will be linked
  span.end();
});

// Manual: Requires explicit context handling
const span = tracer.startSpan('myOperation');
try {
  await context.with(trace.setSpan(context.active(), span), async () => {
    await doWork();
  });
} finally {
  span.end();
}
```

### 3. Add Business Context to Spans

```typescript
span.setAttributes({
  'order.id': orderId,
  'customer.tier': customerTier,
  'payment.method': paymentMethod,
});
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No traces | Instrumentation loaded too late | Use `--require` flag or import first |
| Missing HTTP spans | Path filtered | Check `ignoreIncomingPaths` config |
| Memory leaks | Spans not ended | Always call `span.end()` |
| Context not propagating | Using callbacks without context | Use `startActiveSpan` or explicit context |
| High overhead | All instrumentations enabled | Disable unused instrumentations |

---

**Next**: [Python Integration →](./python)
