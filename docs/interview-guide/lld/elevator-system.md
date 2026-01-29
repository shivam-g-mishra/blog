---
sidebar_position: 5
title: "Design Elevator System"
description: >-
  Complete LLD for elevator system. State machine, scheduling algorithms,
  and handling multiple elevators.
keywords:
  - elevator design
  - LLD elevator
  - elevator scheduling
  - state machine
difficulty: Intermediate
estimated_time: 35 minutes
prerequisites:
  - SOLID Principles
  - State Pattern
companies: [Amazon, Google, Uber, Microsoft]
---

# Design an Elevator System

Elevator system design tests state management, scheduling algorithms, and handling concurrent requests.

---

## Requirements

- Multiple elevators in a building
- Handle floor requests (inside elevator)
- Handle hall calls (outside, with direction)
- Optimize for wait time
- Display current floor and direction

---

## Class Diagram

```
┌─────────────────┐       ┌─────────────────┐
│ ElevatorSystem  │       │    Building     │
├─────────────────┤       ├─────────────────┤
│ - elevators[]   │──────▶│ - floors        │
│ - scheduler     │       │ - elevators[]   │
├─────────────────┤       └─────────────────┘
│ + request()     │
│ + status()      │
└─────────────────┘
         │
         ▼
┌─────────────────┐       ┌─────────────────┐
│    Elevator     │       │    Request      │
├─────────────────┤       ├─────────────────┤
│ - id            │       │ - floor         │
│ - currentFloor  │       │ - direction     │
│ - direction     │       │ - type          │
│ - state         │       └─────────────────┘
│ - requests[]    │
├─────────────────┤
│ + move()        │
│ + addRequest()  │
│ + openDoor()    │
└─────────────────┘
```

---

## Implementation

### Enums

```python
from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0

class ElevatorState(Enum):
    IDLE = "idle"
    MOVING = "moving"
    DOOR_OPEN = "door_open"

class RequestType(Enum):
    HALL_CALL = "hall_call"      # From outside
    FLOOR_REQUEST = "floor_request"  # From inside
```

### Request

```python
class Request:
    def __init__(self, floor: int, direction: Direction = None, 
                 request_type: RequestType = RequestType.FLOOR_REQUEST):
        self.floor = floor
        self.direction = direction
        self.request_type = request_type
        self.timestamp = time.time()
```

### Elevator

```python
class Elevator:
    def __init__(self, elevator_id: int, min_floor: int = 0, max_floor: int = 10):
        self.id = elevator_id
        self.current_floor = 0
        self.direction = Direction.IDLE
        self.state = ElevatorState.IDLE
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.up_requests = set()    # Floors to visit going up
        self.down_requests = set()  # Floors to visit going down
    
    def add_request(self, floor: int, direction: Direction = None):
        if floor == self.current_floor:
            self.open_door()
            return
        
        if floor > self.current_floor:
            self.up_requests.add(floor)
        else:
            self.down_requests.add(floor)
        
        if self.state == ElevatorState.IDLE:
            self._start_moving()
    
    def _start_moving(self):
        if self.up_requests and (self.direction == Direction.UP or 
                                  not self.down_requests):
            self.direction = Direction.UP
        elif self.down_requests:
            self.direction = Direction.DOWN
        else:
            self.direction = Direction.IDLE
            return
        
        self.state = ElevatorState.MOVING
    
    def move(self):
        if self.state != ElevatorState.MOVING:
            return
        
        # Move one floor
        self.current_floor += self.direction.value
        
        # Check if we should stop
        if self._should_stop():
            self.open_door()
        elif self._should_change_direction():
            self.direction = Direction.DOWN if self.direction == Direction.UP else Direction.UP
            if self._should_stop():
                self.open_door()
    
    def _should_stop(self):
        if self.direction == Direction.UP:
            return self.current_floor in self.up_requests
        else:
            return self.current_floor in self.down_requests
    
    def _should_change_direction(self):
        if self.direction == Direction.UP:
            return not self.up_requests or self.current_floor >= max(self.up_requests)
        else:
            return not self.down_requests or self.current_floor <= min(self.down_requests)
    
    def open_door(self):
        self.state = ElevatorState.DOOR_OPEN
        
        # Remove current floor from requests
        self.up_requests.discard(self.current_floor)
        self.down_requests.discard(self.current_floor)
    
    def close_door(self):
        if self.up_requests or self.down_requests:
            self._start_moving()
        else:
            self.state = ElevatorState.IDLE
            self.direction = Direction.IDLE
```

### Scheduler (Strategy Pattern)

```python
from abc import ABC, abstractmethod

class ElevatorScheduler(ABC):
    @abstractmethod
    def select_elevator(self, elevators: list, floor: int, 
                       direction: Direction) -> Elevator:
        pass

class NearestElevatorScheduler(ElevatorScheduler):
    def select_elevator(self, elevators, floor, direction):
        best = None
        min_distance = float('inf')
        
        for elevator in elevators:
            # Prefer elevators going in same direction
            if self._is_suitable(elevator, floor, direction):
                distance = abs(elevator.current_floor - floor)
                if distance < min_distance:
                    min_distance = distance
                    best = elevator
        
        return best or elevators[0]
    
    def _is_suitable(self, elevator, floor, direction):
        if elevator.state == ElevatorState.IDLE:
            return True
        
        if elevator.direction == Direction.UP and direction == Direction.UP:
            return elevator.current_floor <= floor
        
        if elevator.direction == Direction.DOWN and direction == Direction.DOWN:
            return elevator.current_floor >= floor
        
        return False

class LookScheduler(ElevatorScheduler):
    """SCAN/LOOK algorithm - like disk scheduling"""
    def select_elevator(self, elevators, floor, direction):
        # Find elevator that will reach this floor soonest
        # considering its current direction and pending requests
        pass
```

### Elevator System

```python
class ElevatorSystem:
    def __init__(self, num_elevators: int, num_floors: int):
        self.elevators = [
            Elevator(i, 0, num_floors) for i in range(num_elevators)
        ]
        self.scheduler = NearestElevatorScheduler()
        self.num_floors = num_floors
    
    def hall_call(self, floor: int, direction: Direction):
        """External button press"""
        elevator = self.scheduler.select_elevator(
            self.elevators, floor, direction
        )
        elevator.add_request(floor, direction)
        return elevator.id
    
    def floor_request(self, elevator_id: int, floor: int):
        """Internal button press"""
        self.elevators[elevator_id].add_request(floor)
    
    def step(self):
        """Simulate one time unit"""
        for elevator in self.elevators:
            if elevator.state == ElevatorState.MOVING:
                elevator.move()
            elif elevator.state == ElevatorState.DOOR_OPEN:
                elevator.close_door()
    
    def status(self):
        return [
            {
                "id": e.id,
                "floor": e.current_floor,
                "direction": e.direction.name,
                "state": e.state.name
            }
            for e in self.elevators
        ]
```

---

## Usage Example

```python
system = ElevatorSystem(num_elevators=3, num_floors=20)

# Hall call from floor 5, going up
assigned = system.hall_call(5, Direction.UP)
print(f"Elevator {assigned} dispatched")

# Once in elevator, request floor 12
system.floor_request(assigned, 12)

# Simulate
for _ in range(20):
    system.step()
    print(system.status())
```

---

## Scheduling Algorithms

| Algorithm | Description | Pros | Cons |
|-----------|-------------|------|------|
| **FCFS** | First come first served | Simple | Long wait times |
| **Nearest** | Closest elevator | Low wait | Uneven load |
| **SCAN/LOOK** | Complete one direction first | Efficient | Can be unfair |
| **Destination Dispatch** | Group by destination | Very efficient | Complex |

---

## Key Takeaways

1. **State machine** manages elevator states cleanly.
2. **Strategy pattern** for pluggable scheduling algorithms.
3. **Separate request sets** for up/down optimize LOOK algorithm.
4. **Consider edge cases:** Full elevator, stuck doors, maintenance.
