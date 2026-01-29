---
sidebar_position: 3
title: "Design Parking Lot"
description: >-
  Complete LLD for parking lot system. Classes, relationships, and implementation
  with extensibility in mind.
keywords:
  - parking lot design
  - LLD parking lot
  - object oriented design
  - low level design example
difficulty: Intermediate
estimated_time: 35 minutes
prerequisites:
  - SOLID Principles
companies: [Amazon, Google, Uber, Microsoft]
---

# Design a Parking Lot

The parking lot is the "Hello World" of LLD interviews. Simple enough to complete in 45 minutes, complex enough to show design skills.

---

## Requirements

### Functional
- Multiple floors
- Different spot types (compact, regular, large)
- Different vehicle types (motorcycle, car, truck)
- Issue ticket on entry
- Calculate fee on exit
- Track available spots

### Non-Functional
- Support multiple entry/exit points
- Handle concurrent access
- Extensible for new vehicle/spot types

---

## Class Diagram

```
┌─────────────────┐       ┌─────────────────┐
│   ParkingLot    │       │  ParkingFloor   │
├─────────────────┤       ├─────────────────┤
│ - floors[]      │──────▶│ - floor_number  │
│ - entry_panels[]│       │ - spots[]       │
│ - exit_panels[] │       ├─────────────────┤
├─────────────────┤       │ + find_spot()   │
│ + park_vehicle()│       │ + free_spot()   │
│ + unpark()      │       └────────┬────────┘
└─────────────────┘                │
                                   │
                           ┌───────▼────────┐
                           │  ParkingSpot   │
                           ├────────────────┤
┌─────────────────┐        │ - spot_number  │
│    Vehicle      │◀───────│ - spot_type    │
├─────────────────┤        │ - vehicle      │
│ - license_plate │        ├────────────────┤
│ - vehicle_type  │        │ + is_available │
└────────┬────────┘        │ + park()       │
         │                 │ + unpark()     │
    ┌────┴────┬────┐       └────────────────┘
    ▼         ▼    ▼
┌──────┐ ┌─────┐ ┌──────┐
│Motor │ │ Car │ │Truck │
│cycle │ │     │ │      │
└──────┘ └─────┘ └──────┘
```

---

## Implementation

### Enums

```python
from enum import Enum

class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    TRUCK = 3

class SpotType(Enum):
    COMPACT = 1
    REGULAR = 2
    LARGE = 3

class TicketStatus(Enum):
    ACTIVE = 1
    PAID = 2
```

### Vehicle Classes

```python
from abc import ABC

class Vehicle(ABC):
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type

class Motorcycle(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.MOTORCYCLE)

class Car(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.CAR)

class Truck(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.TRUCK)
```

### Parking Spot

```python
class ParkingSpot:
    def __init__(self, spot_number: int, spot_type: SpotType):
        self.spot_number = spot_number
        self.spot_type = spot_type
        self.vehicle = None
    
    def is_available(self) -> bool:
        return self.vehicle is None
    
    def can_fit(self, vehicle: Vehicle) -> bool:
        if self.vehicle is not None:
            return False
        
        # Mapping: which spots can fit which vehicles
        compatibility = {
            VehicleType.MOTORCYCLE: [SpotType.COMPACT, SpotType.REGULAR, SpotType.LARGE],
            VehicleType.CAR: [SpotType.REGULAR, SpotType.LARGE],
            VehicleType.TRUCK: [SpotType.LARGE]
        }
        
        return self.spot_type in compatibility[vehicle.vehicle_type]
    
    def park(self, vehicle: Vehicle) -> bool:
        if self.can_fit(vehicle):
            self.vehicle = vehicle
            return True
        return False
    
    def unpark(self) -> Vehicle:
        vehicle = self.vehicle
        self.vehicle = None
        return vehicle
```

### Parking Floor

```python
class ParkingFloor:
    def __init__(self, floor_number: int, compact: int, regular: int, large: int):
        self.floor_number = floor_number
        self.spots = []
        
        spot_num = 1
        for _ in range(compact):
            self.spots.append(ParkingSpot(spot_num, SpotType.COMPACT))
            spot_num += 1
        for _ in range(regular):
            self.spots.append(ParkingSpot(spot_num, SpotType.REGULAR))
            spot_num += 1
        for _ in range(large):
            self.spots.append(ParkingSpot(spot_num, SpotType.LARGE))
            spot_num += 1
    
    def find_spot(self, vehicle: Vehicle) -> ParkingSpot:
        for spot in self.spots:
            if spot.can_fit(vehicle):
                return spot
        return None
    
    def get_available_count(self) -> dict:
        counts = {SpotType.COMPACT: 0, SpotType.REGULAR: 0, SpotType.LARGE: 0}
        for spot in self.spots:
            if spot.is_available():
                counts[spot.spot_type] += 1
        return counts
```

### Ticket

```python
from datetime import datetime
import uuid

class Ticket:
    def __init__(self, vehicle: Vehicle, spot: ParkingSpot, floor: int):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.spot = spot
        self.floor = floor
        self.entry_time = datetime.now()
        self.exit_time = None
        self.status = TicketStatus.ACTIVE
    
    def close(self):
        self.exit_time = datetime.now()
        self.status = TicketStatus.PAID
    
    def get_duration_hours(self) -> float:
        end_time = self.exit_time or datetime.now()
        duration = end_time - self.entry_time
        return duration.total_seconds() / 3600
```

### Fee Calculator (Strategy Pattern)

```python
from abc import ABC, abstractmethod

class FeeStrategy(ABC):
    @abstractmethod
    def calculate(self, ticket: Ticket) -> float:
        pass

class HourlyFeeStrategy(FeeStrategy):
    def __init__(self, rates: dict):
        # rates = {VehicleType.CAR: 10, VehicleType.MOTORCYCLE: 5, ...}
        self.rates = rates
    
    def calculate(self, ticket: Ticket) -> float:
        hours = ticket.get_duration_hours()
        rate = self.rates.get(ticket.vehicle.vehicle_type, 10)
        return max(1, int(hours)) * rate  # Minimum 1 hour

class FlatFeeStrategy(FeeStrategy):
    def __init__(self, flat_rate: float):
        self.flat_rate = flat_rate
    
    def calculate(self, ticket: Ticket) -> float:
        return self.flat_rate
```

### Parking Lot

```python
import threading

class ParkingLot:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, name: str, floors_config: list):
        if hasattr(self, '_initialized'):
            return
        
        self.name = name
        self.floors = []
        self.tickets = {}  # license_plate -> Ticket
        self.fee_strategy = HourlyFeeStrategy({
            VehicleType.MOTORCYCLE: 5,
            VehicleType.CAR: 10,
            VehicleType.TRUCK: 15
        })
        self._lock = threading.Lock()
        
        for i, config in enumerate(floors_config):
            floor = ParkingFloor(i + 1, **config)
            self.floors.append(floor)
        
        self._initialized = True
    
    def park_vehicle(self, vehicle: Vehicle) -> Ticket:
        with self._lock:
            for floor in self.floors:
                spot = floor.find_spot(vehicle)
                if spot:
                    spot.park(vehicle)
                    ticket = Ticket(vehicle, spot, floor.floor_number)
                    self.tickets[vehicle.license_plate] = ticket
                    return ticket
            return None  # No spot available
    
    def unpark_vehicle(self, license_plate: str) -> float:
        with self._lock:
            ticket = self.tickets.get(license_plate)
            if not ticket:
                raise ValueError("Vehicle not found")
            
            ticket.spot.unpark()
            ticket.close()
            fee = self.fee_strategy.calculate(ticket)
            del self.tickets[license_plate]
            
            return fee
    
    def get_available_spots(self) -> dict:
        total = {SpotType.COMPACT: 0, SpotType.REGULAR: 0, SpotType.LARGE: 0}
        for floor in self.floors:
            counts = floor.get_available_count()
            for spot_type, count in counts.items():
                total[spot_type] += count
        return total
```

---

## Usage Example

```python
# Initialize parking lot
parking_lot = ParkingLot("Downtown Parking", [
    {"compact": 10, "regular": 20, "large": 5},  # Floor 1
    {"compact": 10, "regular": 20, "large": 5},  # Floor 2
])

# Park a car
car = Car("ABC-123")
ticket = parking_lot.park_vehicle(car)
print(f"Parked at Floor {ticket.floor}, Spot {ticket.spot.spot_number}")

# Park a motorcycle
motorcycle = Motorcycle("XYZ-789")
ticket2 = parking_lot.park_vehicle(motorcycle)

# Check availability
available = parking_lot.get_available_spots()
print(f"Available: {available}")

# Unpark and pay
fee = parking_lot.unpark_vehicle("ABC-123")
print(f"Fee: ${fee}")
```

---

## Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Singleton | ParkingLot | Single source of truth |
| Strategy | Fee calculation | Flexible pricing |
| Composition | Floor contains Spots | Clear ownership |
| Thread safety | Locks on mutations | Concurrent access |

---

## Extensions

1. **Multiple entry/exit points:** Add EntryPanel and ExitPanel classes
2. **Reservations:** Add reservation system with time slots
3. **EV charging:** Add EVSpot subclass with charging logic
4. **Display boards:** Observer pattern for availability updates
