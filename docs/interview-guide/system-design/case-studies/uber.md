---
sidebar_position: 5
title: "Design Uber — Ride Sharing"
description: >-
  Complete system design for Uber/ride sharing. Location tracking, matching,
  ETA calculation, and real-time updates.
keywords:
  - design uber
  - ride sharing
  - location tracking
  - matching system
  - real-time location
difficulty: Advanced
estimated_time: 50 minutes
prerequisites:
  - Message Queues
  - Databases
  - Caching
companies: [Uber, Lyft, DoorDash, Instacart]
---

# Design Uber: Real-Time Location at Scale

Uber matches riders with drivers in real-time, tracking millions of moving vehicles continuously.

---

## Requirements

### Functional
- Request ride
- Match with nearby driver
- Real-time driver location tracking
- ETA calculation
- Trip history
- Payments

### Non-Functional
- **Latency:** Match < 30 seconds
- **Location update:** Every 3-5 seconds
- **Availability:** 99.99%
- **Scale:** 1M concurrent rides

---

## High-Level Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌─────────────────┐
│Rider App    │────▶│   API Gateway   │────▶│  Trip Service   │
└─────────────┘     └─────────────────┘     └────────┬────────┘
                                                     │
┌─────────────┐            │                         │
│Driver App   │◄───────────┘                         │
└──────┬──────┘                                      │
       │                                             │
       ▼                                             ▼
┌─────────────────┐     ┌─────────────────┐    ┌─────────────────┐
│Location Service │     │ Matching Service│    │  Maps Service   │
│ (Real-time)     │────▶│ (Driver-Rider)  │    │  (ETA/Routes)   │
└────────┬────────┘     └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐
│ Geospatial DB   │
│ (Redis/QuadTree)│
└─────────────────┘
```

---

## Location Tracking

### Driver Location Updates

```python
# Driver sends location every 4 seconds
def update_location(driver_id, lat, lng):
    # Update in geospatial index
    geohash = compute_geohash(lat, lng)
    redis.geoadd("drivers", lng, lat, driver_id)
    
    # Publish for active trip tracking
    kafka.publish("driver_locations", {
        "driver_id": driver_id,
        "lat": lat,
        "lng": lng,
        "timestamp": time.now()
    })
```

### Geospatial Indexing

```
Option 1: Geohash + Redis
GEOADD drivers -122.4194 37.7749 "driver_123"
GEORADIUS drivers -122.42 37.78 5 km

Option 2: QuadTree
- Divide map into quadrants
- Store drivers in leaf nodes
- Query: Find leaf containing point, check neighbors
```

---

## Matching Algorithm

```python
def find_nearby_drivers(rider_lat, rider_lng, radius_km=5):
    # Query nearby drivers
    drivers = redis.georadius(
        "available_drivers",
        rider_lng, rider_lat,
        radius_km, unit="km",
        withdist=True,
        sort="ASC"
    )
    
    # Filter by driver state, rating, car type
    eligible = []
    for driver_id, distance in drivers:
        driver = get_driver(driver_id)
        if driver.status == "available" and driver.rating >= 4.0:
            eta = maps_service.get_eta(driver.location, (rider_lat, rider_lng))
            eligible.append((driver_id, distance, eta))
    
    # Sort by ETA
    eligible.sort(key=lambda x: x[2])
    return eligible[:10]

def match_rider_to_driver(rider_id, rider_location):
    drivers = find_nearby_drivers(*rider_location)
    
    for driver_id, distance, eta in drivers:
        # Send request to driver
        response = notify_driver(driver_id, rider_id, eta)
        
        if response == "accepted":
            create_trip(rider_id, driver_id)
            return driver_id
    
    return None  # No match found
```

---

## Trip State Machine

```
┌─────────────┐
│  Requested  │
└──────┬──────┘
       │ Driver accepts
       ▼
┌─────────────┐
│  Accepted   │
└──────┬──────┘
       │ Driver arrives
       ▼
┌─────────────┐
│  Arrived    │
└──────┬──────┘
       │ Trip starts
       ▼
┌─────────────┐
│ In Progress │
└──────┬──────┘
       │ Trip ends
       ▼
┌─────────────┐
│  Completed  │
└─────────────┘
```

---

## ETA Calculation

```python
def calculate_eta(origin, destination):
    # Simple: Graph-based shortest path
    # Real: Consider traffic, road closures, historical data
    
    route = maps_service.get_route(origin, destination)
    
    # Adjust for traffic
    traffic_factor = get_traffic_factor(route, time.now())
    
    base_eta = route.duration
    adjusted_eta = base_eta * traffic_factor
    
    return adjusted_eta
```

---

## Database Schema

```sql
-- Trips
CREATE TABLE trips (
    trip_id UUID PRIMARY KEY,
    rider_id UUID,
    driver_id UUID,
    status TEXT,
    pickup_location POINT,
    dropoff_location POINT,
    fare DECIMAL,
    created_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Driver locations (time-series)
CREATE TABLE driver_locations (
    driver_id UUID,
    location POINT,
    timestamp TIMESTAMP,
    PRIMARY KEY (driver_id, timestamp)
);
```

---

## Key Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Location index | Redis GEO | Fast radius queries |
| Updates | Kafka | Handle high throughput |
| Matching | Nearest + ETA | Balance speed and distance |
| Maps | Google Maps / OSRM | Accurate ETA |
| Trip DB | PostgreSQL | ACID for payments |

---

## Key Takeaways

1. **Geospatial indexing** (Redis GEO, QuadTree) for location queries.
2. **High-frequency updates** via Kafka streaming.
3. **ETA-based matching** not just distance.
4. **State machine** for trip lifecycle management.
5. **Separate read/write paths** for location data.
