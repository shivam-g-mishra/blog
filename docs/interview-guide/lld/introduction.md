---
sidebar_position: 1
title: "Low Level Design Introduction"
description: >-
  Introduction to Low Level Design interviews. OOP principles, design patterns,
  and how LLD differs from system design.
keywords:
  - low level design
  - object oriented design
  - OOP interview
  - design patterns
  - SOLID principles
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - Basic OOP concepts
companies: [Google, Amazon, Microsoft, Uber, Flipkart]
---

# Low Level Design: Code Architecture

System Design asks "how do distributed components interact?" LLD asks "how do classes and objects interact?"

**LLD is about designing clean, maintainable, extensible code.**

---

## LLD vs System Design

| Aspect | System Design (HLD) | Low Level Design |
|--------|---------------------|------------------|
| **Focus** | Distributed architecture | Class structure |
| **Scale** | Millions of users | Single application |
| **Deliverable** | Architecture diagram | Class diagram + code |
| **Concerns** | Scalability, availability | Maintainability, extensibility |
| **Level** | Senior+ | All levels |

---

## What Interviewers Evaluate

| Skill | What They Look For |
|-------|-------------------|
| **OOP fundamentals** | Proper use of classes, inheritance, composition |
| **SOLID principles** | Clean, maintainable design |
| **Design patterns** | Appropriate pattern selection |
| **Code organization** | Separation of concerns |
| **Extensibility** | Easy to add features |
| **Edge cases** | Handling unusual scenarios |

---

## Common LLD Interview Problems

### Games & Entertainment
- Chess
- Tic-Tac-Toe
- Snake and Ladder
- Card games (Blackjack, Poker)

### Real-World Systems
- Parking lot
- Elevator system
- Library management
- Hotel booking
- Movie ticket booking

### Software Systems
- Logging framework
- Cache (LRU)
- Rate limiter
- Task scheduler

---

## The LLD Framework

```
1. CLARIFY REQUIREMENTS (5 min)
   - What entities exist?
   - What are the main use cases?
   - Any constraints or assumptions?

2. IDENTIFY CLASSES (5 min)
   - Nouns → Classes
   - Verbs → Methods
   - Relationships between classes

3. DEFINE INTERFACES (5 min)
   - What methods does each class expose?
   - What data does each class hold?

4. IMPLEMENT CORE LOGIC (20 min)
   - Start with skeleton
   - Implement key methods
   - Handle edge cases

5. DISCUSS TRADE-OFFS (5 min)
   - Design decisions made
   - Alternative approaches
   - Extensibility considerations
```

---

## SOLID Principles (Quick Review)

| Principle | Meaning |
|-----------|---------|
| **S**ingle Responsibility | One class, one reason to change |
| **O**pen/Closed | Open for extension, closed for modification |
| **L**iskov Substitution | Subtypes must be substitutable |
| **I**nterface Segregation | Many specific interfaces > one general |
| **D**ependency Inversion | Depend on abstractions, not concretions |

---

## Design Patterns to Know

### Creational
- **Singleton:** Single instance (config, logger)
- **Factory:** Create objects without specifying class
- **Builder:** Construct complex objects step by step

### Structural
- **Adapter:** Make incompatible interfaces work together
- **Decorator:** Add behavior dynamically
- **Facade:** Simplified interface to complex system

### Behavioral
- **Strategy:** Swap algorithms at runtime
- **Observer:** Notify dependents of state changes
- **State:** Object behavior changes with state

---

## Example: Parking Lot (Quick Sketch)

```python
# Classes identified from requirements
class ParkingLot:
    def __init__(self, floors, spots_per_floor):
        self.floors = [ParkingFloor(i, spots_per_floor) for i in range(floors)]
    
    def park_vehicle(self, vehicle):
        for floor in self.floors:
            spot = floor.find_spot(vehicle.type)
            if spot:
                spot.park(vehicle)
                return Ticket(vehicle, spot)
        return None

class ParkingFloor:
    def __init__(self, floor_num, spots):
        self.floor_num = floor_num
        self.spots = self._create_spots(spots)
    
    def find_spot(self, vehicle_type):
        for spot in self.spots:
            if spot.can_fit(vehicle_type) and spot.is_available():
                return spot
        return None

class ParkingSpot:
    def __init__(self, spot_type):
        self.type = spot_type
        self.vehicle = None
    
    def is_available(self):
        return self.vehicle is None
    
    def park(self, vehicle):
        self.vehicle = vehicle
    
    def unpark(self):
        self.vehicle = None

class Vehicle:
    def __init__(self, license_plate, vehicle_type):
        self.license_plate = license_plate
        self.type = vehicle_type

class Ticket:
    def __init__(self, vehicle, spot):
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = datetime.now()
```

---

## Key Takeaways

1. **Start with requirements.** Clarify before designing.
2. **Nouns → Classes, Verbs → Methods.**
3. **Apply SOLID principles** for clean design.
4. **Use design patterns** where appropriate.
5. **Think about extensibility** from the start.

---

## What's Next?

Deep dive into SOLID principles:

👉 [SOLID Principles →](./solid-principles)
