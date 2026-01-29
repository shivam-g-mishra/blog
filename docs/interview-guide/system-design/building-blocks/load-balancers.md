---
sidebar_position: 1
title: "Load Balancers — Traffic Distribution"
description: >-
  Master load balancers for system design interviews. Algorithms, L4 vs L7,
  health checks, and implementation patterns.
keywords:
  - load balancer
  - traffic distribution
  - round robin
  - consistent hashing
  - system design
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - System Design Introduction
companies: [Google, Amazon, Meta, Netflix, Uber]
---

# Load Balancers: The Traffic Controllers

"Design a system that handles 100,000 requests per second."

One server can handle maybe 1,000 RPS. You need 100+ servers. But how do requests know which server to hit?

**Load balancers distribute traffic across servers.**

---

## Why Load Balancers?

```
Without Load Balancer:
┌────────┐
│ Client │───▶ Single Server (bottleneck, single point of failure)
└────────┘

With Load Balancer:
┌────────┐     ┌────────────────┐     ┌──────────┐
│ Client │────▶│ Load Balancer  │────▶│ Server 1 │
└────────┘     └────────────────┘     ├──────────┤
                                      │ Server 2 │
                                      ├──────────┤
                                      │ Server N │
                                      └──────────┘
```

### Benefits

| Benefit | Description |
|---------|-------------|
| **Scalability** | Add servers to handle more traffic |
| **Availability** | If one server fails, others continue |
| **Flexibility** | Deploy, upgrade servers without downtime |
| **Performance** | Route to fastest/closest server |

---

## Load Balancing Algorithms

### 1. Round Robin

Distribute requests in circular order.

```
Request 1 → Server 1
Request 2 → Server 2
Request 3 → Server 3
Request 4 → Server 1 (cycle repeats)
```

**Pros:** Simple, fair distribution
**Cons:** Ignores server capacity, request complexity

### 2. Weighted Round Robin

Servers with higher capacity get more traffic.

```python
# Server weights: A=5, B=3, C=2
# Distribution: A, A, A, A, A, B, B, B, C, C, repeat

servers = [('A', 5), ('B', 3), ('C', 2)]

def weighted_round_robin(servers):
    while True:
        for server, weight in servers:
            for _ in range(weight):
                yield server
```

**Use when:** Servers have different capacities.

### 3. Least Connections

Route to server with fewest active connections.

```python
def least_connections(servers):
    return min(servers, key=lambda s: s.active_connections)
```

**Use when:** Request processing times vary significantly.

### 4. IP Hash

Hash client IP to always route to same server.

```python
def ip_hash(client_ip, num_servers):
    return hash(client_ip) % num_servers
```

**Use when:** Need session persistence without cookies.

### 5. Consistent Hashing

Minimize redistribution when servers change.

```
Hash Ring:
        Server A
           │
    ┌──────┴──────┐
    │             │
Server D      Server B
    │             │
    └──────┬──────┘
           │
        Server C

Key "user123" → hash → nearest server clockwise
```

**Use when:** Adding/removing servers frequently (caches, distributed stores).

---

## L4 vs L7 Load Balancing

### Layer 4 (Transport)

Operates on TCP/UDP level. Sees: IP addresses, ports.

```
┌────────┐     ┌─────────────┐     ┌────────┐
│ Client │────▶│ L4 LB       │────▶│ Server │
└────────┘     │ (TCP/IP)    │     └────────┘
               └─────────────┘
               Routes based on:
               - Source/dest IP
               - Source/dest port
```

**Pros:** Fast, low overhead
**Cons:** No application awareness

### Layer 7 (Application)

Operates on HTTP level. Sees: URLs, headers, cookies, content.

```
┌────────┐     ┌─────────────┐     ┌────────────┐
│ Client │────▶│ L7 LB       │────▶│ API Server │
└────────┘     │ (HTTP)      │     └────────────┘
               └─────────────┘     ┌────────────┐
               Routes based on:───▶│ Web Server │
               - URL path          └────────────┘
               - Headers           ┌────────────┐
               - Cookies      ────▶│ File Server│
               - Content           └────────────┘
```

**Pros:** Smart routing, SSL termination, caching
**Cons:** Higher latency, more complex

### When to Use Which

| Use Case | Recommendation |
|----------|----------------|
| Simple TCP distribution | L4 |
| Content-based routing | L7 |
| SSL termination | L7 |
| WebSocket support | L7 |
| Ultra-low latency | L4 |
| A/B testing | L7 |

---

## Health Checks

Load balancers must detect unhealthy servers.

### Passive Health Checks

Monitor responses from normal traffic.

```
Server returns 500 errors → mark unhealthy
Server times out → mark unhealthy
```

### Active Health Checks

Periodically probe servers.

```
Every 10 seconds:
  GET /health → 200 OK? → healthy
                  else → unhealthy
```

### Health Check Configuration

```yaml
health_check:
  path: /health
  interval: 10s
  timeout: 5s
  healthy_threshold: 2    # 2 successes → healthy
  unhealthy_threshold: 3  # 3 failures → unhealthy
```

---

## High Availability

Load balancers themselves can fail. Use redundancy.

### Active-Passive

```
┌────────────────────────────────────┐
│         Virtual IP (VIP)           │
└────────────────────────────────────┘
           │ (active)    │ (standby)
    ┌──────▼─────┐  ┌────▼────────┐
    │ Primary LB │  │ Secondary LB │
    └────────────┘  └─────────────┘
           │
    ┌──────▼──────┐
    │   Servers   │
    └─────────────┘
```

If primary fails, secondary takes over VIP.

### Active-Active

```
┌─────────────────────────────────────┐
│             DNS                     │
│    Returns multiple LB IPs          │
└─────────────────────────────────────┘
         │              │
   ┌─────▼────┐   ┌─────▼────┐
   │   LB 1   │   │   LB 2   │
   └──────────┘   └──────────┘
         │              │
   ┌─────▼──────────────▼─────┐
   │        Servers           │
   └──────────────────────────┘
```

Both LBs active, DNS distributes across them.

---

## Common Load Balancers

| Tool | Type | Use Case |
|------|------|----------|
| **HAProxy** | Software L4/L7 | High performance, flexible |
| **NGINX** | Software L7 | Web servers, reverse proxy |
| **AWS ALB** | Cloud L7 | AWS applications |
| **AWS NLB** | Cloud L4 | AWS TCP/UDP |
| **Google Cloud LB** | Cloud L4/L7 | GCP applications |
| **F5** | Hardware | Enterprise, legacy |

---

## Interview Tips

### Common Questions

1. "How would you handle sticky sessions?"
   - Use cookies or IP hash
   - Store session in shared cache (Redis)

2. "What if load balancer fails?"
   - Active-passive or active-active setup
   - DNS failover

3. "How to handle SSL?"
   - SSL termination at L7 LB
   - Or pass-through for end-to-end encryption

### Design Pattern

```
Internet
    │
┌───▼───────────────┐
│   DNS (Route53)   │  Geographic routing
└───────────────────┘
    │
┌───▼───────────────┐
│   Global LB       │  Cross-region failover
└───────────────────┘
    │
┌───▼───────────────┐
│   Regional LB     │  L7 routing, SSL termination
└───────────────────┘
    │
┌───▼───────────────┐
│   App Servers     │
└───────────────────┘
```

---

## Key Takeaways

1. **Choose algorithm based on use case:** Round robin for uniform requests, least connections for variable workloads.

2. **L4 for speed, L7 for intelligence.**

3. **Health checks are essential.** Both active and passive.

4. **Load balancers need redundancy too.**

5. **Consistent hashing** for distributed caches.

---

## What's Next?

Caching strategies to reduce database load:

👉 [Caching →](./caching)
