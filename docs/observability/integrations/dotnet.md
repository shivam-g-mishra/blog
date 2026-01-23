---
sidebar_position: 3
title: .NET Integration
description: Complete guide to instrumenting .NET applications with OpenTelemetry - ASP.NET Core, Entity Framework, and more.
keywords: [dotnet, csharp, aspnetcore, opentelemetry, otel, instrumentation, tracing]
---

# .NET OpenTelemetry Integration

A comprehensive guide to instrumenting .NET applications with OpenTelemetry. .NET has excellent first-class support through the `System.Diagnostics` API and official OpenTelemetry packages.

## Prerequisites

- .NET 6.0 or later (examples use .NET 8)
- OpenTelemetry Collector running (see [Single-Node Setup](/single-node-observability-setup))
- Visual Studio, VS Code, or Rider

## Installation

```bash
# Core packages
dotnet add package OpenTelemetry
dotnet add package OpenTelemetry.Extensions.Hosting

# Exporters
dotnet add package OpenTelemetry.Exporter.OpenTelemetryProtocol

# Auto-instrumentation
dotnet add package OpenTelemetry.Instrumentation.AspNetCore
dotnet add package OpenTelemetry.Instrumentation.Http
dotnet add package OpenTelemetry.Instrumentation.SqlClient
dotnet add package OpenTelemetry.Instrumentation.EntityFrameworkCore
dotnet add package OpenTelemetry.Instrumentation.StackExchangeRedis

# Runtime metrics
dotnet add package OpenTelemetry.Instrumentation.Runtime
dotnet add package OpenTelemetry.Instrumentation.Process
```

## Basic Setup (Minimal API)

The simplest way to add OpenTelemetry to a .NET application:

```csharp title="Program.cs"
using OpenTelemetry.Logs;
using OpenTelemetry.Metrics;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

var builder = WebApplication.CreateBuilder(args);

// Define service identity
var serviceName = builder.Configuration["ServiceName"] ?? "my-dotnet-service";
var serviceVersion = typeof(Program).Assembly.GetName().Version?.ToString() ?? "1.0.0";

// Configure OpenTelemetry
builder.Services.AddOpenTelemetry()
    .ConfigureResource(resource => resource
        .AddService(
            serviceName: serviceName,
            serviceVersion: serviceVersion,
            serviceInstanceId: Environment.MachineName)
        .AddAttributes(new[]
        {
            new KeyValuePair<string, object>("deployment.environment", 
                builder.Environment.EnvironmentName),
        }))
    .WithTracing(tracing => tracing
        .AddAspNetCoreInstrumentation(opts =>
        {
            opts.RecordException = true;
            opts.Filter = ctx => !ctx.Request.Path.StartsWithSegments("/health");
        })
        .AddHttpClientInstrumentation(opts =>
        {
            opts.RecordException = true;
        })
        .AddSqlClientInstrumentation(opts =>
        {
            opts.SetDbStatementForText = true;
            opts.RecordException = true;
        })
        .AddEntityFrameworkCoreInstrumentation(opts =>
        {
            opts.SetDbStatementForText = true;
        })
        .AddSource(serviceName) // For custom ActivitySource
        .AddOtlpExporter(opts =>
        {
            opts.Endpoint = new Uri(
                builder.Configuration["Otel:Endpoint"] ?? "http://localhost:4317");
        }))
    .WithMetrics(metrics => metrics
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddRuntimeInstrumentation()
        .AddProcessInstrumentation()
        .AddMeter(serviceName) // For custom meters
        .AddOtlpExporter(opts =>
        {
            opts.Endpoint = new Uri(
                builder.Configuration["Otel:Endpoint"] ?? "http://localhost:4317");
        }));

// Configure logging to export via OTLP
builder.Logging.AddOpenTelemetry(logging =>
{
    logging.IncludeFormattedMessage = true;
    logging.IncludeScopes = true;
    logging.AddOtlpExporter(opts =>
    {
        opts.Endpoint = new Uri(
            builder.Configuration["Otel:Endpoint"] ?? "http://localhost:4317");
    });
});

var app = builder.Build();

app.MapGet("/health", () => Results.Ok(new { status = "healthy" }));

app.MapGet("/api/users/{id}", async (string id, ILogger<Program> logger) =>
{
    logger.LogInformation("Fetching user {UserId}", id);
    
    // Simulate database call
    await Task.Delay(50);
    
    return Results.Ok(new { id, name = "John Doe", email = "john@example.com" });
});

app.Run();
```

## Full Setup with Custom Instrumentation

For larger applications, organize telemetry setup into extension methods:

```csharp title="Extensions/TelemetryExtensions.cs"
using System.Diagnostics;
using System.Diagnostics.Metrics;
using OpenTelemetry.Logs;
using OpenTelemetry.Metrics;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

namespace MyService.Extensions;

public static class TelemetryExtensions
{
    public static IServiceCollection AddTelemetry(
        this IServiceCollection services,
        IConfiguration configuration,
        IWebHostEnvironment environment)
    {
        var serviceName = configuration["ServiceName"] ?? "my-dotnet-service";
        var serviceVersion = typeof(TelemetryExtensions).Assembly
            .GetName().Version?.ToString() ?? "1.0.0";
        var otlpEndpoint = configuration["Otel:Endpoint"] ?? "http://localhost:4317";

        // Register ActivitySource and Meter for DI
        services.AddSingleton(new ActivitySource(serviceName));
        services.AddSingleton(new Meter(serviceName));

        services.AddOpenTelemetry()
            .ConfigureResource(resource => resource
                .AddService(
                    serviceName: serviceName,
                    serviceVersion: serviceVersion,
                    serviceInstanceId: Environment.MachineName)
                .AddAttributes(new Dictionary<string, object>
                {
                    ["deployment.environment"] = environment.EnvironmentName,
                    ["host.name"] = Environment.MachineName,
                }))
            .WithTracing(tracing =>
            {
                tracing
                    .AddAspNetCoreInstrumentation(ConfigureAspNetCore)
                    .AddHttpClientInstrumentation(ConfigureHttpClient)
                    .AddSqlClientInstrumentation(ConfigureSqlClient)
                    .AddEntityFrameworkCoreInstrumentation(opts =>
                    {
                        opts.SetDbStatementForText = true;
                    })
                    .AddSource(serviceName);

                // Add OTLP exporter
                tracing.AddOtlpExporter(opts =>
                {
                    opts.Endpoint = new Uri(otlpEndpoint);
                });

                // Add console exporter for development
                if (environment.IsDevelopment())
                {
                    tracing.AddConsoleExporter();
                }
            })
            .WithMetrics(metrics =>
            {
                metrics
                    .AddAspNetCoreInstrumentation()
                    .AddHttpClientInstrumentation()
                    .AddRuntimeInstrumentation()
                    .AddProcessInstrumentation()
                    .AddMeter(serviceName)
                    .AddOtlpExporter(opts =>
                    {
                        opts.Endpoint = new Uri(otlpEndpoint);
                    });
            });

        return services;
    }

    private static void ConfigureAspNetCore(
        AspNetCoreTraceInstrumentationOptions opts)
    {
        opts.RecordException = true;
        opts.EnrichWithHttpRequest = (activity, request) =>
        {
            activity.SetTag("http.client_ip", 
                request.HttpContext.Connection.RemoteIpAddress?.ToString());
        };
        opts.EnrichWithHttpResponse = (activity, response) =>
        {
            activity.SetTag("http.response_content_length", 
                response.ContentLength);
        };
        opts.Filter = ctx =>
        {
            // Filter out health checks and metrics endpoints
            var path = ctx.Request.Path.Value ?? "";
            return !path.StartsWith("/health") && 
                   !path.StartsWith("/metrics") &&
                   !path.StartsWith("/ready");
        };
    }

    private static void ConfigureHttpClient(
        HttpClientTraceInstrumentationOptions opts)
    {
        opts.RecordException = true;
        opts.EnrichWithHttpRequestMessage = (activity, request) =>
        {
            activity.SetTag("http.request_content_length", 
                request.Content?.Headers.ContentLength);
        };
        opts.FilterHttpRequestMessage = request =>
        {
            // Filter out calls to certain hosts
            return request.RequestUri?.Host != "internal-service.local";
        };
    }

    private static void ConfigureSqlClient(
        SqlClientTraceInstrumentationOptions opts)
    {
        opts.SetDbStatementForText = true;
        opts.RecordException = true;
        opts.EnableConnectionLevelAttributes = true;
        opts.Enrich = (activity, eventName, rawObject) =>
        {
            if (eventName == "OnCustom" && rawObject is SqlCommand command)
            {
                activity.SetTag("db.rows_affected", command.StatementCompleted);
            }
        };
    }
}
```

## Custom Spans with ActivitySource

```csharp title="Services/OrderService.cs"
using System.Diagnostics;

namespace MyService.Services;

public class OrderService
{
    private readonly ActivitySource _activitySource;
    private readonly ILogger<OrderService> _logger;
    private readonly PaymentService _paymentService;
    private readonly InventoryService _inventoryService;

    public OrderService(
        ActivitySource activitySource,
        ILogger<OrderService> logger,
        PaymentService paymentService,
        InventoryService inventoryService)
    {
        _activitySource = activitySource;
        _logger = logger;
        _paymentService = paymentService;
        _inventoryService = inventoryService;
    }

    public async Task<OrderResult> CreateOrderAsync(CreateOrderRequest request)
    {
        // Create a span for the entire operation
        using var activity = _activitySource.StartActivity(
            "CreateOrder",
            ActivityKind.Internal);
        
        // Add business context as tags
        activity?.SetTag("order.user_id", request.UserId);
        activity?.SetTag("order.items_count", request.Items.Count);
        activity?.SetTag("order.total", request.Total);

        try
        {
            _logger.LogInformation(
                "Creating order for user {UserId} with {ItemCount} items",
                request.UserId, request.Items.Count);

            // Step 1: Validate order
            await ValidateOrderAsync(request);

            // Step 2: Reserve inventory
            await ReserveInventoryAsync(request.Items);

            // Step 3: Process payment
            var paymentResult = await ProcessPaymentAsync(request);

            // Step 4: Save order
            var order = await SaveOrderAsync(request, paymentResult);

            activity?.SetTag("order.id", order.Id);
            activity?.SetStatus(ActivityStatusCode.Ok);

            _logger.LogInformation(
                "Order {OrderId} created successfully for user {UserId}",
                order.Id, request.UserId);

            return new OrderResult { OrderId = order.Id, Status = "Created" };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, 
                "Failed to create order for user {UserId}", request.UserId);
            
            activity?.SetStatus(ActivityStatusCode.Error, ex.Message);
            activity?.RecordException(ex);
            throw;
        }
    }

    private async Task ValidateOrderAsync(CreateOrderRequest request)
    {
        using var activity = _activitySource.StartActivity("ValidateOrder");
        
        // Validation logic
        await Task.Delay(10); // Simulate validation
        
        activity?.SetTag("validation.passed", true);
        activity?.AddEvent(new ActivityEvent("ValidationComplete"));
    }

    private async Task ReserveInventoryAsync(List<OrderItem> items)
    {
        using var activity = _activitySource.StartActivity(
            "ReserveInventory",
            ActivityKind.Client);
        
        activity?.SetTag("inventory.items_count", items.Count);
        
        foreach (var item in items)
        {
            using var itemActivity = _activitySource.StartActivity("ReserveItem");
            itemActivity?.SetTag("item.sku", item.Sku);
            itemActivity?.SetTag("item.quantity", item.Quantity);
            
            await _inventoryService.ReserveAsync(item.Sku, item.Quantity);
        }
    }

    private async Task<PaymentResult> ProcessPaymentAsync(CreateOrderRequest request)
    {
        using var activity = _activitySource.StartActivity(
            "ProcessPayment",
            ActivityKind.Client);
        
        activity?.SetTag("payment.amount", request.Total);
        activity?.SetTag("payment.currency", "USD");
        activity?.SetTag("payment.method", request.PaymentMethod);

        var result = await _paymentService.ChargeAsync(
            request.UserId, 
            request.Total);

        activity?.SetTag("payment.transaction_id", result.TransactionId);
        activity?.SetTag("payment.status", result.Status);

        return result;
    }

    private async Task<Order> SaveOrderAsync(
        CreateOrderRequest request, 
        PaymentResult payment)
    {
        using var activity = _activitySource.StartActivity(
            "SaveOrder",
            ActivityKind.Client);
        
        activity?.SetTag("db.system", "postgresql");
        activity?.SetTag("db.operation", "INSERT");

        // Save to database
        await Task.Delay(30); // Simulate DB operation
        
        var order = new Order
        {
            Id = Guid.NewGuid().ToString(),
            UserId = request.UserId,
            Total = request.Total,
            TransactionId = payment.TransactionId,
            CreatedAt = DateTime.UtcNow
        };

        activity?.SetTag("db.order_id", order.Id);
        
        return order;
    }
}
```

## Custom Metrics

```csharp title="Metrics/ApplicationMetrics.cs"
using System.Diagnostics.Metrics;

namespace MyService.Metrics;

public class ApplicationMetrics
{
    private readonly Counter<long> _ordersCreated;
    private readonly Counter<long> _ordersFailed;
    private readonly Histogram<double> _orderProcessingDuration;
    private readonly Histogram<double> _orderValue;
    private readonly UpDownCounter<long> _activeOrders;
    private readonly ObservableGauge<long> _queueDepth;

    private long _currentQueueDepth;

    public ApplicationMetrics(Meter meter)
    {
        // Counter for successful orders
        _ordersCreated = meter.CreateCounter<long>(
            "orders_created_total",
            unit: "{order}",
            description: "Total number of orders created");

        // Counter for failed orders
        _ordersFailed = meter.CreateCounter<long>(
            "orders_failed_total",
            unit: "{order}",
            description: "Total number of failed orders");

        // Histogram for order processing time
        _orderProcessingDuration = meter.CreateHistogram<double>(
            "order_processing_duration_seconds",
            unit: "s",
            description: "Time to process an order");

        // Histogram for order values
        _orderValue = meter.CreateHistogram<double>(
            "order_value_dollars",
            unit: "USD",
            description: "Value of orders");

        // UpDownCounter for orders being processed
        _activeOrders = meter.CreateUpDownCounter<long>(
            "active_orders",
            unit: "{order}",
            description: "Number of orders currently being processed");

        // Observable gauge for queue depth
        _queueDepth = meter.CreateObservableGauge(
            "order_queue_depth",
            () => _currentQueueDepth,
            unit: "{order}",
            description: "Current depth of the order queue");
    }

    public void RecordOrderCreated(string customerId, string region, decimal value)
    {
        var tags = new TagList
        {
            { "customer_type", GetCustomerType(customerId) },
            { "region", region }
        };

        _ordersCreated.Add(1, tags);
        _orderValue.Record((double)value, tags);
    }

    public void RecordOrderFailed(string reason, string region)
    {
        _ordersFailed.Add(1, new TagList
        {
            { "reason", reason },
            { "region", region }
        });
    }

    public void RecordProcessingDuration(double seconds, string orderType)
    {
        _orderProcessingDuration.Record(seconds, new TagList
        {
            { "order_type", orderType }
        });
    }

    public void OrderProcessingStarted() => _activeOrders.Add(1);
    public void OrderProcessingCompleted() => _activeOrders.Add(-1);

    public void SetQueueDepth(long depth) => _currentQueueDepth = depth;

    private static string GetCustomerType(string customerId) =>
        customerId.StartsWith("ENT") ? "enterprise" : "standard";
}
```

Usage in a service:

```csharp
public class OrderProcessor
{
    private readonly ApplicationMetrics _metrics;
    private readonly Stopwatch _stopwatch = new();

    public OrderProcessor(ApplicationMetrics metrics)
    {
        _metrics = metrics;
    }

    public async Task ProcessOrderAsync(Order order)
    {
        _metrics.OrderProcessingStarted();
        _stopwatch.Restart();

        try
        {
            // Process order...
            await Task.Delay(100);

            _stopwatch.Stop();
            _metrics.RecordOrderCreated(
                order.CustomerId, 
                order.Region, 
                order.Total);
            _metrics.RecordProcessingDuration(
                _stopwatch.Elapsed.TotalSeconds, 
                order.Type);
        }
        catch (Exception ex)
        {
            _metrics.RecordOrderFailed(ex.GetType().Name, order.Region);
            throw;
        }
        finally
        {
            _metrics.OrderProcessingCompleted();
        }
    }
}
```

## Structured Logging with Scopes

```csharp title="Services/UserService.cs"
public class UserService
{
    private readonly ILogger<UserService> _logger;

    public UserService(ILogger<UserService> logger)
    {
        _logger = logger;
    }

    public async Task<User> GetUserAsync(string userId)
    {
        // Create a logging scope that adds context to all logs
        using (_logger.BeginScope(new Dictionary<string, object>
        {
            ["UserId"] = userId,
            ["Operation"] = "GetUser"
        }))
        {
            _logger.LogInformation("Starting user retrieval");

            try
            {
                var user = await FetchUserFromDatabaseAsync(userId);
                
                _logger.LogInformation(
                    "User retrieved successfully. Email: {Email}", 
                    user.Email);
                
                return user;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, 
                    "Failed to retrieve user");
                throw;
            }
        }
    }
}
```

## HTTP Client Factory Integration

```csharp title="Program.cs (HTTP Client)"
builder.Services.AddHttpClient<IPaymentClient, PaymentClient>(client =>
{
    client.BaseAddress = new Uri(builder.Configuration["PaymentService:Url"]!);
    client.DefaultRequestHeaders.Add("Accept", "application/json");
})
.AddStandardResilienceHandler(); // Polly resilience

// The OTel HttpClient instrumentation automatically traces these calls
```

```csharp title="Clients/PaymentClient.cs"
public interface IPaymentClient
{
    Task<PaymentResult> ChargeAsync(ChargeRequest request);
}

public class PaymentClient : IPaymentClient
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<PaymentClient> _logger;

    public PaymentClient(HttpClient httpClient, ILogger<PaymentClient> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
    }

    public async Task<PaymentResult> ChargeAsync(ChargeRequest request)
    {
        _logger.LogInformation(
            "Charging {Amount} for user {UserId}", 
            request.Amount, request.UserId);

        var response = await _httpClient.PostAsJsonAsync("/api/charge", request);
        response.EnsureSuccessStatusCode();

        return await response.Content.ReadFromJsonAsync<PaymentResult>()
            ?? throw new InvalidOperationException("Empty payment response");
    }
}
```

## Background Service Instrumentation

```csharp title="Services/OrderProcessorBackgroundService.cs"
public class OrderProcessorBackgroundService : BackgroundService
{
    private readonly ActivitySource _activitySource;
    private readonly ILogger<OrderProcessorBackgroundService> _logger;
    private readonly IServiceProvider _serviceProvider;
    private readonly Channel<Order> _orderChannel;

    public OrderProcessorBackgroundService(
        ActivitySource activitySource,
        ILogger<OrderProcessorBackgroundService> logger,
        IServiceProvider serviceProvider,
        Channel<Order> orderChannel)
    {
        _activitySource = activitySource;
        _logger = logger;
        _serviceProvider = serviceProvider;
        _orderChannel = orderChannel;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Order processor starting");

        await foreach (var order in _orderChannel.Reader.ReadAllAsync(stoppingToken))
        {
            // Create a new trace for each order processed
            using var activity = _activitySource.StartActivity(
                "ProcessOrder",
                ActivityKind.Consumer);

            activity?.SetTag("order.id", order.Id);
            activity?.SetTag("order.user_id", order.UserId);

            try
            {
                using var scope = _serviceProvider.CreateScope();
                var processor = scope.ServiceProvider
                    .GetRequiredService<IOrderProcessor>();

                await processor.ProcessAsync(order);

                activity?.SetStatus(ActivityStatusCode.Ok);
                _logger.LogInformation("Order {OrderId} processed", order.Id);
            }
            catch (Exception ex)
            {
                activity?.SetStatus(ActivityStatusCode.Error, ex.Message);
                activity?.RecordException(ex);
                _logger.LogError(ex, "Failed to process order {OrderId}", order.Id);
            }
        }
    }
}
```

## Configuration

```json title="appsettings.json"
{
  "ServiceName": "my-dotnet-service",
  "Otel": {
    "Endpoint": "http://localhost:4317"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "System.Net.Http.HttpClient": "Warning"
    }
  }
}
```

```json title="appsettings.Production.json"
{
  "Otel": {
    "Endpoint": "http://otel-collector:4317"
  }
}
```

## Docker Integration

```dockerfile title="Dockerfile"
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 8080

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["MyService.csproj", "./"]
RUN dotnet restore
COPY . .
RUN dotnet build -c Release -o /app/build

FROM build AS publish
RUN dotnet publish -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "MyService.dll"]
```

```yaml title="docker-compose.yml"
services:
  my-dotnet-service:
    build: .
    ports:
      - "8080:8080"
    environment:
      - ASPNETCORE_ENVIRONMENT=Production
      - ServiceName=my-dotnet-service
      - Otel__Endpoint=http://otel-collector:4317
    networks:
      - observability

networks:
  observability:
    external: true
```

## Best Practices

### 1. Use Dependency Injection for ActivitySource

```csharp
// Register once
services.AddSingleton(new ActivitySource("MyService"));

// Inject where needed
public class MyService(ActivitySource activitySource)
{
    public void DoWork()
    {
        using var activity = activitySource.StartActivity("DoWork");
        // ...
    }
}
```

### 2. Enrich Spans with Business Context

```csharp
activity?.SetTag("order.id", order.Id);
activity?.SetTag("customer.tier", customer.Tier);
activity?.SetTag("region", order.ShippingRegion);
```

### 3. Use Events for Important Milestones

```csharp
activity?.AddEvent(new ActivityEvent("PaymentAuthorized", 
    tags: new ActivityTagsCollection
    {
        { "transaction_id", transactionId },
        { "amount", amount }
    }));
```

### 4. Record Exceptions Properly

```csharp
try
{
    await ProcessAsync();
    activity?.SetStatus(ActivityStatusCode.Ok);
}
catch (Exception ex)
{
    activity?.RecordException(ex);
    activity?.SetStatus(ActivityStatusCode.Error, ex.Message);
    throw;
}
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No traces appearing | Collector not running | Verify `docker ps` shows otel-collector |
| Missing HTTP spans | Filter excluding paths | Check `opts.Filter` in `AddAspNetCoreInstrumentation` |
| Missing DB spans | Package not installed | Add `OpenTelemetry.Instrumentation.SqlClient` |
| Duplicate traces | Multiple exporters | Remove console exporter in production |
| High memory | Too many spans | Filter health checks, enable sampling |

---

**Next**: [Java Integration →](./java)
