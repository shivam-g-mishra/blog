---
sidebar_position: 1
title: "Fault Tolerance & High Availability"
description: >-
  Design fault-tolerant systems for interviews. Redundancy, failover,
  health checks, and graceful degradation.
keywords:
  - fault tolerance
  - high availability
  - redundancy
  - failover
  - disaster recovery
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - System Design Introduction
companies: [All Companies]
---

# Fault Tolerance: Expect Failures

Everything fails eventually. Design for it.

---

## Availability Math

```
Availability = Uptime / (Uptime + Downtime)

99% = 3.65 days downtime/year
99.9% = 8.76 hours downtime/year
99.99% = 52.6 minutes downtime/year
99.999% = 5.26 minutes downtime/year (five nines)
```

---

## Redundancy Patterns

### Active-Passive (Failover)

```
┌─────────────────┐     ┌─────────────────┐
│     Active      │     │    Passive      │
│    (Primary)    │────▶│   (Standby)     │
│   Handles all   │     │   Ready to      │
│    traffic      │     │   take over     │
└─────────────────┘     └─────────────────┘

- Standby monitors primary
- Takes over on failure
- May have brief downtime during switchover
```

### Active-Active

```
┌─────────────────┐     ┌─────────────────┐
│     Active      │     │     Active      │
│   Server A      │     │   Server B      │
│  Handles 50%    │     │  Handles 50%    │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
              Load Balancer

- Both handle traffic
- No wasted resources
- Instant failover
- More complex (data sync)
```

---

## Failover Strategies

### Health Checks

```python
# Types of health checks:

# 1. Shallow (liveness)
GET /health → 200 OK

# 2. Deep (readiness)  
GET /health/ready
- Check database connection
- Check dependent services
- Check disk space
```

### Automatic Failover

```
Load Balancer monitors health:

Server A: ✓ ✓ ✓ ✗ ✗ ✗ → Remove from pool
Server B: ✓ ✓ ✓ ✓ ✓ ✓ → Handle all traffic

After recovery:
Server A: ✓ ✓ ✓ ✓ → Add back to pool
```

---

## Graceful Degradation

When something fails, degrade gracefully instead of total failure.

```
Example: E-commerce site

Full functionality:
- Product catalog ✓
- Recommendations ✓
- Reviews ✓
- Search ✓

Recommendation service down:
- Product catalog ✓
- Recommendations: "Popular items" (fallback)
- Reviews ✓
- Search ✓

Better than: "500 Internal Server Error"
```

---

## Circuit Breaker Pattern

```
         ┌─────────────────────────────────────────┐
         │                                         │
    ┌────▼────┐      ┌───────────┐      ┌─────────┴───┐
    │ Closed  │─────▶│   Open    │─────▶│ Half-Open   │
    │(Normal) │      │ (Failing) │      │  (Testing)  │
    └─────────┘      └───────────┘      └─────────────┘
         ▲                                     │
         └─────────────────────────────────────┘

Closed: Normal operation, track failures
Open: Fail fast, don't call service
Half-Open: Test if service recovered
```

```python
class CircuitBreaker:
    def __init__(self, threshold=5, timeout=30):
        self.failures = 0
        self.threshold = threshold
        self.timeout = timeout
        self.state = "CLOSED"
        self.last_failure_time = None
    
    def call(self, func):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise CircuitOpenError()
        
        try:
            result = func()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
    
    def on_success(self):
        self.failures = 0
        self.state = "CLOSED"
    
    def on_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.threshold:
            self.state = "OPEN"
```

---

## Disaster Recovery

```
RPO: Recovery Point Objective
- How much data loss is acceptable?
- Determines backup frequency

RTO: Recovery Time Objective
- How long can system be down?
- Determines recovery strategy

Example:
RPO = 1 hour → Backup every hour
RTO = 4 hours → Hot standby may not be needed
```

---

## Multi-Region Deployment

```
              Global Load Balancer
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │ US-East │   │ EU-West │   │ AP-South│
   │ Region  │   │ Region  │   │ Region  │
   └─────────┘   └─────────┘   └─────────┘

Benefits:
- Geographic redundancy
- Lower latency for users
- Disaster recovery

Challenges:
- Data synchronization
- Consistency across regions
- Higher complexity and cost
```

---

## Key Takeaways

1. **Redundancy everywhere**—no single points of failure.
2. **Health checks** enable automatic failover.
3. **Graceful degradation** beats total failure.
4. **Circuit breakers** prevent cascade failures.
5. **Know your RTO/RPO**—they drive design decisions.
