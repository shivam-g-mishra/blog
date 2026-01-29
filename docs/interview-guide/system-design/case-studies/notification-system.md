---
sidebar_position: 10
title: "Design Notification System"
description: >-
  Complete system design for notification service. Push notifications,
  email, SMS, and preference management.
keywords:
  - notification system
  - push notification
  - notification design
  - alert system
difficulty: Intermediate
estimated_time: 40 minutes
prerequisites:
  - Message Queues
companies: [Google, Amazon, Meta, Uber, Airbnb]
---

# Design a Notification System

Notifications seem simple: send a message to a user. The complexity: multiple channels, user preferences, rate limiting, and reliability at scale.

---

## Requirements

### Functional
- Support multiple channels (push, email, SMS)
- User preference management
- Template management
- Priority levels
- Scheduling
- Analytics (delivery, open rates)

### Non-Functional
- **Latency:** High priority < 1 second
- **Reliability:** No duplicate notifications
- **Scale:** 10M notifications/day
- **Availability:** 99.9%

---

## High-Level Architecture

```
┌───────────────┐
│   Services    │
│ (trigger      │
│  notifications)│
└───────┬───────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────┐
│                    Notification Service                        │
├───────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │   API       │  │  Validator  │  │  Router     │           │
│  │   Gateway   │──▶│  & Enricher │──▶│  (by type)  │           │
│  └─────────────┘  └─────────────┘  └──────┬──────┘           │
│                                           │                   │
│         ┌─────────────────────────────────┼─────────────────┐│
│         │                                 │                 ││
│         ▼                                 ▼                 ▼│
│  ┌─────────────┐                  ┌─────────────┐   ┌─────────────┐
│  │ Push Queue  │                  │ Email Queue │   │  SMS Queue  │
│  └──────┬──────┘                  └──────┬──────┘   └──────┬──────┘
│         │                                │                 │ │
│         ▼                                ▼                 ▼ │
│  ┌─────────────┐                  ┌─────────────┐   ┌─────────────┐
│  │Push Workers │                  │Email Workers│   │ SMS Workers │
│  └──────┬──────┘                  └──────┬──────┘   └──────┬──────┘
└─────────┼─────────────────────────────────┼─────────────────┼─────┘
          │                                 │                 │
          ▼                                 ▼                 ▼
     ┌─────────┐                       ┌─────────┐       ┌─────────┐
     │  APNS/  │                       │ SendGrid│       │ Twilio  │
     │  FCM    │                       │ Mailgun │       │ Nexmo   │
     └─────────┘                       └─────────┘       └─────────┘
```

---

## API Design

```
POST /v1/notifications
{
  "user_id": "user_123",
  "type": "order_shipped",
  "channels": ["push", "email"],
  "priority": "high",
  "data": {
    "order_id": "order_456",
    "tracking_number": "1Z999AA10123456784"
  },
  "scheduled_at": null  // null = immediate
}

Response:
{
  "notification_id": "notif_789",
  "status": "queued"
}
```

---

## Notification Flow

```
1. Service triggers notification
   │
   ▼
2. API Gateway receives request
   │
   ▼
3. Validator & Enricher
   ├── Validate payload
   ├── Check user preferences (opted out?)
   ├── Rate limit check
   ├── Fetch user contact info
   └── Render template
   │
   ▼
4. Router
   ├── Determine channels based on:
   │   - Request
   │   - User preferences
   │   - Notification type
   └── Queue to appropriate channel queues
   │
   ▼
5. Channel Workers
   ├── Dequeue message
   ├── Call external provider
   ├── Handle retries
   └── Log delivery status
   │
   ▼
6. Analytics
   └── Track delivery, opens, clicks
```

---

## User Preferences

```sql
CREATE TABLE user_preferences (
    user_id UUID PRIMARY KEY,
    push_enabled BOOLEAN DEFAULT true,
    email_enabled BOOLEAN DEFAULT true,
    sms_enabled BOOLEAN DEFAULT true,
    quiet_hours_start TIME,
    quiet_hours_end TIME,
    timezone VARCHAR(50),
    notification_settings JSONB  -- Per-type settings
);

-- Example notification_settings:
{
  "order_updates": ["push", "email"],
  "promotions": ["email"],
  "security_alerts": ["push", "email", "sms"]
}
```

---

## Template System

```python
# Template definition
{
  "template_id": "order_shipped",
  "push": {
    "title": "Your order has shipped!",
    "body": "Order #{{order_id}} is on its way. Track: {{tracking_number}}"
  },
  "email": {
    "subject": "Your order #{{order_id}} has shipped",
    "template_file": "order_shipped.html"
  },
  "sms": {
    "body": "Order #{{order_id}} shipped. Track at: {{tracking_url}}"
  }
}

# Rendering
def render_notification(template_id, data, channel):
    template = get_template(template_id, channel)
    return template.render(**data)
```

---

## Priority & Rate Limiting

```python
# Priority queues
QUEUES = {
    'critical': 'notifications:critical',  # Security alerts
    'high': 'notifications:high',          # Order updates
    'normal': 'notifications:normal',      # General
    'low': 'notifications:low'             # Promotions
}

# Rate limiting per user
def check_rate_limit(user_id, channel):
    key = f"rate_limit:{user_id}:{channel}"
    current = redis.incr(key)
    
    if current == 1:
        redis.expire(key, 3600)  # 1 hour window
    
    limits = {'push': 50, 'email': 20, 'sms': 5}
    return current <= limits[channel]
```

---

## Reliability

### Idempotency

```python
def process_notification(notification):
    # Check if already processed
    if redis.sismember('processed_notifications', notification.id):
        return  # Skip duplicate
    
    try:
        send_notification(notification)
        redis.sadd('processed_notifications', notification.id)
    except Exception as e:
        # Don't mark as processed, allow retry
        raise
```

### Retry Strategy

```python
def send_with_retry(notification, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = send_to_provider(notification)
            return result
        except TransientError:
            wait_time = 2 ** attempt  # Exponential backoff
            time.sleep(wait_time)
        except PermanentError:
            log_failure(notification)
            return None
    
    # Max retries exceeded
    move_to_dlq(notification)
```

---

## Database Schema

```sql
-- Notifications
CREATE TABLE notifications (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    type VARCHAR(100) NOT NULL,
    priority VARCHAR(20) DEFAULT 'normal',
    data JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    scheduled_at TIMESTAMP
);

-- Delivery attempts
CREATE TABLE delivery_logs (
    id UUID PRIMARY KEY,
    notification_id UUID REFERENCES notifications(id),
    channel VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,  -- queued, sent, delivered, failed
    provider_response JSONB,
    attempted_at TIMESTAMP DEFAULT NOW()
);
```

---

## Key Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Queue per channel | Separate queues | Independent scaling |
| Priority queues | Multiple priorities | Critical alerts first |
| External providers | Multiple | Redundancy |
| Idempotency | Deduplication key | No duplicate sends |
| Templates | Centralized | Consistency |

---

## Key Takeaways

1. **Separate queues** per channel for independent scaling.
2. **Priority levels** ensure critical notifications go first.
3. **User preferences** must be respected.
4. **Rate limiting** prevents notification spam.
5. **Idempotency** prevents duplicate sends.
