---
sidebar_position: 4
title: "Networking Basics for Interviews"
description: >-
  Essential networking concepts for coding interviews. TCP/UDP, HTTP,
  DNS, and common interview questions.
keywords:
  - networking interview
  - TCP UDP
  - HTTP HTTPS
  - DNS
  - OSI model
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites: []
companies: [Google, Amazon, Meta, Cloudflare]
---

# Networking Basics: What Developers Need to Know

Networking questions are common in system design and general interviews.

---

## OSI Model (Simplified)

```
Layer 7: Application   (HTTP, DNS, FTP)
Layer 4: Transport     (TCP, UDP)
Layer 3: Network       (IP, routing)
Layer 2: Data Link     (Ethernet, MAC)
Layer 1: Physical      (Cables, signals)
```

---

## TCP vs UDP

| Aspect | TCP | UDP |
|--------|-----|-----|
| Connection | Connection-oriented | Connectionless |
| Reliability | Guaranteed delivery | Best effort |
| Ordering | Ordered | Unordered |
| Speed | Slower (overhead) | Faster |
| Use cases | HTTP, email, file transfer | Video streaming, gaming, DNS |

### TCP Three-Way Handshake

```
Client                    Server
   |                         |
   |-------- SYN ----------->|
   |                         |
   |<------ SYN-ACK ---------|
   |                         |
   |-------- ACK ----------->|
   |                         |
   |     Connection          |
   |     Established         |
```

---

## HTTP/HTTPS

### HTTP Methods

| Method | Purpose | Idempotent |
|--------|---------|------------|
| GET | Retrieve resource | Yes |
| POST | Create resource | No |
| PUT | Replace resource | Yes |
| PATCH | Partial update | No |
| DELETE | Delete resource | Yes |

### HTTP Status Codes

```
1xx: Informational
2xx: Success (200 OK, 201 Created, 204 No Content)
3xx: Redirect (301 Permanent, 302 Temporary, 304 Not Modified)
4xx: Client Error (400 Bad Request, 401 Unauthorized, 404 Not Found)
5xx: Server Error (500 Internal, 502 Bad Gateway, 503 Unavailable)
```

### HTTPS

```
HTTP + TLS = HTTPS

TLS provides:
1. Encryption (confidentiality)
2. Authentication (server identity)
3. Integrity (data not tampered)
```

---

## DNS (Domain Name System)

```
www.example.com → 93.184.216.34

Resolution process:
1. Browser cache
2. OS cache
3. Router cache
4. ISP DNS resolver
5. Root DNS server
6. TLD DNS server (.com)
7. Authoritative DNS server (example.com)
```

### DNS Record Types

| Type | Purpose |
|------|---------|
| A | Domain → IPv4 |
| AAAA | Domain → IPv6 |
| CNAME | Alias to another domain |
| MX | Mail server |
| TXT | Text (verification, SPF) |
| NS | Nameserver |

---

## Common Interview Questions

### What happens when you type google.com?

```
1. Parse URL
2. DNS lookup (google.com → IP)
3. TCP connection (3-way handshake)
4. TLS handshake (for HTTPS)
5. Send HTTP GET request
6. Server processes, returns response
7. Browser parses HTML
8. Browser fetches additional resources (CSS, JS, images)
9. Browser renders page
10. JavaScript executes
```

### How does a load balancer work?

```
Client requests → Load Balancer → Backend servers

Algorithms:
- Round Robin: Rotate through servers
- Least Connections: Send to least busy
- IP Hash: Same client → same server
- Weighted: Based on server capacity
```

### What is REST?

```
REpresentational State Transfer

Principles:
1. Stateless: No session state on server
2. Uniform interface: Standard HTTP methods
3. Resource-based: URLs represent resources
4. Self-descriptive: Response includes type info

Example:
GET /users/123        → Get user 123
POST /users           → Create user
PUT /users/123        → Replace user 123
DELETE /users/123     → Delete user 123
```

---

## WebSockets vs HTTP

| Aspect | HTTP | WebSocket |
|--------|------|-----------|
| Connection | Request-response | Persistent |
| Direction | Client-initiated | Bidirectional |
| Overhead | Headers per request | Low after handshake |
| Use case | Web pages, APIs | Chat, real-time updates |

---

## Key Takeaways

1. **TCP** for reliability, **UDP** for speed.
2. **HTTP is stateless**—use cookies/tokens for sessions.
3. **DNS is hierarchical** with caching at multiple levels.
4. **HTTPS = HTTP + TLS** for security.
5. **Know the URL resolution flow** thoroughly.
