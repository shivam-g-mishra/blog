---
sidebar_position: 12
title: "Design E-commerce Platform"
description: >-
  Complete system design for an e-commerce platform like Amazon. Product catalog,
  inventory, cart, checkout, and order management.
keywords:
  - design amazon
  - e-commerce design
  - shopping cart
  - inventory system
  - checkout flow
difficulty: Advanced
estimated_time: 50 minutes
prerequisites:
  - Building Blocks
  - Databases
companies: [Amazon, Walmart, Shopify, eBay]
---

# Design an E-Commerce Platform

E-commerce combines many complex systems: catalog, inventory, cart, payments, orders, recommendations, and more.

---

## Requirements

### Functional
- Product catalog with search
- Shopping cart
- Checkout and payment
- Order management
- Inventory tracking
- User accounts and history

### Non-Functional
- **Availability:** 99.99% (revenue loss on downtime)
- **Latency:** < 200ms for browsing
- **Consistency:** Strong for inventory/payments
- **Scale:** Millions of products, peak during sales

---

## High-Level Architecture

```
┌───────────────────────────────────────────────────────────────────────────┐
│                              API Gateway                                   │
└───────────────────────────────────────────────────────────────────────────┘
         │          │          │          │          │          │
         ▼          ▼          ▼          ▼          ▼          ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
    │ Product │ │  Cart   │ │ Order   │ │ Payment │ │  User   │ │ Search  │
    │ Catalog │ │ Service │ │ Service │ │ Service │ │ Service │ │ Service │
    └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
         │          │          │          │          │          │
    ┌────▼────┐ ┌────▼────┐ ┌────▼────┐ ┌────▼────┐ ┌────▼────┐ ┌────▼────┐
    │ Product │ │ Cart DB │ │ Order   │ │ Payment │ │ User DB │ │Elastic- │
    │   DB    │ │ (Redis) │ │   DB    │ │ Gateway │ │         │ │ search  │
    └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
                                │
                                ▼
                         ┌──────────────┐
                         │  Inventory   │
                         │   Service    │
                         └──────────────┘
```

---

## Product Catalog

### Data Model

```sql
CREATE TABLE products (
    product_id UUID PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    category_id UUID,
    brand VARCHAR(100),
    base_price DECIMAL(10,2),
    created_at TIMESTAMP
);

CREATE TABLE product_variants (
    variant_id UUID PRIMARY KEY,
    product_id UUID REFERENCES products,
    sku VARCHAR(50) UNIQUE,
    size VARCHAR(20),
    color VARCHAR(20),
    price DECIMAL(10,2),
    image_urls TEXT[]
);

CREATE TABLE inventory (
    sku VARCHAR(50) PRIMARY KEY,
    warehouse_id UUID,
    quantity INT,
    reserved INT DEFAULT 0,
    updated_at TIMESTAMP
);
```

---

## Shopping Cart

### Design Choices

```
Option 1: Session-based (Redis)
- Fast, ephemeral
- Lost on logout
- Good for anonymous users

Option 2: Persistent (Database)
- Survives logout
- Cross-device sync
- Good for logged-in users

Recommendation: Hybrid
- Redis for active session
- Persist to DB on key events
```

### Cart Operations

```python
class CartService:
    def add_item(self, user_id, sku, quantity):
        # Check inventory
        available = inventory_service.check(sku)
        if available < quantity:
            raise InsufficientStock()
        
        # Add to cart
        cart_key = f"cart:{user_id}"
        redis.hincrby(cart_key, sku, quantity)
        redis.expire(cart_key, 86400 * 7)  # 7 days
    
    def get_cart(self, user_id):
        cart_key = f"cart:{user_id}"
        items = redis.hgetall(cart_key)
        
        # Enrich with product details
        return self._enrich_cart_items(items)
```

---

## Checkout Flow

```
1. User clicks "Checkout"
   │
   ▼
2. Validate cart items (still in stock?)
   │
   ▼
3. Reserve inventory (soft lock)
   │
   ▼
4. Calculate totals (items + tax + shipping)
   │
   ▼
5. Collect payment info
   │
   ▼
6. Process payment (with retry)
   │
   ▼
7. Create order (status: CONFIRMED)
   │
   ▼
8. Deduct inventory (hard commit)
   │
   ▼
9. Clear cart
   │
   ▼
10. Send confirmation
```

---

## Inventory Management

### The Challenge

```
Problem: Race condition during flash sales

User A checks: 1 item left → adds to cart
User B checks: 1 item left → adds to cart
Both try to buy → oversell!

Solution: Reserve on add to cart

inventory.quantity = 10
inventory.reserved = 3
available = quantity - reserved = 7
```

### Reservation Pattern

```python
def reserve_inventory(sku, quantity, reservation_id, ttl=600):
    with redis.pipeline() as pipe:
        while True:
            try:
                pipe.watch(f"inventory:{sku}")
                
                current = int(pipe.get(f"inventory:{sku}") or 0)
                reserved = int(pipe.get(f"reserved:{sku}") or 0)
                available = current - reserved
                
                if available < quantity:
                    raise InsufficientStock()
                
                pipe.multi()
                pipe.incrby(f"reserved:{sku}", quantity)
                pipe.setex(f"reservation:{reservation_id}", ttl, quantity)
                pipe.execute()
                return True
            except WatchError:
                continue  # Retry on conflict
```

---

## Order Service

```sql
CREATE TABLE orders (
    order_id UUID PRIMARY KEY,
    user_id UUID,
    status VARCHAR(20),  -- PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
    subtotal DECIMAL(10,2),
    tax DECIMAL(10,2),
    shipping DECIMAL(10,2),
    total DECIMAL(10,2),
    shipping_address JSONB,
    created_at TIMESTAMP
);

CREATE TABLE order_items (
    order_item_id UUID PRIMARY KEY,
    order_id UUID REFERENCES orders,
    sku VARCHAR(50),
    product_name VARCHAR(255),
    quantity INT,
    unit_price DECIMAL(10,2),
    total_price DECIMAL(10,2)
);
```

---

## Handling Flash Sales

```
Challenge: 100K users want 1K items at 12:00

Solutions:
1. Virtual queue
   - Users get queue position
   - Processed in order
   - Show wait time

2. Rate limiting
   - Limit requests per user
   - Prevent bots

3. Pre-validation
   - Validate cart before sale starts
   - One-click checkout

4. Inventory pre-allocation
   - Reserve for active sessions
   - Release after timeout
```

---

## Key Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Cart storage | Redis + DB | Speed + persistence |
| Inventory | Reserved + committed | Prevent overselling |
| Search | Elasticsearch | Full-text, facets |
| Payments | External gateway | PCI compliance |
| Orders | PostgreSQL | ACID transactions |

---

## Key Takeaways

1. **Inventory reservation** prevents overselling.
2. **Cart in Redis** with periodic DB persistence.
3. **Checkout is transactional**—all or nothing.
4. **Flash sales need queuing** and rate limiting.
5. **Payment processing** should be idempotent.
