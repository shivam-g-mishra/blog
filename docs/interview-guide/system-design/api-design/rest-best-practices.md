---
sidebar_position: 1
title: "REST API Design Best Practices"
description: >-
  Design RESTful APIs for system design interviews. Naming, versioning,
  pagination, error handling, and security.
keywords:
  - REST API
  - API design
  - RESTful
  - API best practices
  - API versioning
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - Networking Basics
companies: [All Companies]
---

# REST API Design: Build APIs That Last

Good API design is crucial. APIs are contracts—hard to change once published.

---

## REST Principles

```
1. Stateless: No session state on server
2. Resource-based: URLs represent resources
3. Standard methods: HTTP verbs for operations
4. Self-descriptive: Response includes type info
```

---

## URL Design

### Use Nouns, Not Verbs

```
✓ GET /users/123
✗ GET /getUser?id=123

✓ POST /orders
✗ POST /createOrder

✓ DELETE /users/123
✗ POST /deleteUser
```

### Hierarchical Resources

```
/users/123/orders          # User's orders
/users/123/orders/456      # Specific order
/users/123/orders/456/items # Order items

Keep nesting shallow (max 2-3 levels)
```

### Plural Nouns

```
✓ /users
✓ /orders
✓ /products

✗ /user
✗ /order
✗ /product
```

---

## HTTP Methods

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Retrieve resource | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Partial update | No | No |
| DELETE | Delete resource | Yes | No |

---

## Status Codes

### Success (2xx)

```
200 OK           - General success
201 Created      - Resource created (POST)
204 No Content   - Success, no body (DELETE)
```

### Client Errors (4xx)

```
400 Bad Request     - Invalid input
401 Unauthorized    - Authentication required
403 Forbidden       - Authenticated but not allowed
404 Not Found       - Resource doesn't exist
409 Conflict        - State conflict (duplicate)
422 Unprocessable   - Validation error
429 Too Many Requests - Rate limited
```

### Server Errors (5xx)

```
500 Internal Server Error - Generic error
502 Bad Gateway           - Upstream error
503 Service Unavailable   - Temporarily down
504 Gateway Timeout       - Upstream timeout
```

---

## API Versioning

### URL Path (Recommended)

```
/v1/users
/v2/users

Pros: Clear, easy to route
Cons: URL changes
```

### Header

```
Accept: application/vnd.myapi.v1+json

Pros: Clean URLs
Cons: Hidden, harder to test
```

### Query Parameter

```
/users?version=1

Pros: Simple
Cons: Can be forgotten
```

---

## Pagination

### Offset-Based

```
GET /users?offset=20&limit=10

Response:
{
  "data": [...],
  "total": 100,
  "offset": 20,
  "limit": 10
}

Cons: Inconsistent with inserts/deletes
```

### Cursor-Based (Recommended)

```
GET /users?cursor=abc123&limit=10

Response:
{
  "data": [...],
  "next_cursor": "def456",
  "has_more": true
}

Pros: Consistent, performant
Cons: Can't jump to page N
```

---

## Error Handling

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input provided",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ],
    "request_id": "req_abc123"
  }
}
```

---

## Filtering, Sorting, Fields

```
Filtering:
GET /users?status=active&role=admin

Sorting:
GET /users?sort=created_at&order=desc
GET /users?sort=-created_at  # Alternative

Field selection:
GET /users?fields=id,name,email
```

---

## Authentication

```
Bearer Token (JWT):
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

API Key:
X-API-Key: your-api-key

OAuth 2.0:
Authorization: Bearer {access_token}
```

---

## Rate Limiting Headers

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
Retry-After: 60  (when 429)
```

---

## Example: Users API

```
# List users
GET /v1/users?status=active&limit=20

# Get single user
GET /v1/users/123

# Create user
POST /v1/users
{
  "name": "Alice",
  "email": "alice@example.com"
}

# Update user
PATCH /v1/users/123
{
  "name": "Alice Smith"
}

# Delete user
DELETE /v1/users/123

# User's orders
GET /v1/users/123/orders
```

---

## Key Takeaways

1. **Nouns for URLs**, verbs are HTTP methods.
2. **Version your API** from day one.
3. **Cursor pagination** for large datasets.
4. **Consistent error format** with details.
5. **Include rate limit headers** in responses.
