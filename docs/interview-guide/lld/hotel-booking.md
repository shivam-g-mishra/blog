---
sidebar_position: 8
title: "Design Hotel Booking System"
description: >-
  Complete LLD for hotel booking system. Room management, reservations,
  pricing, and availability tracking.
keywords:
  - hotel booking design
  - LLD hotel
  - reservation system
  - room management
difficulty: Intermediate
estimated_time: 35 minutes
prerequisites:
  - SOLID Principles
companies: [Booking.com, Airbnb, Expedia]
---

# Design a Hotel Booking System

Hotel booking tests inventory management, reservation handling, and pricing logic.

---

## Requirements

- Search hotels by location, dates, guests
- View room availability and pricing
- Make reservations
- Cancel/modify bookings
- Handle multiple room types
- Apply dynamic pricing

---

## Class Diagram

```
┌─────────────────┐       ┌─────────────────┐
│  BookingSystem  │       │     Hotel       │
├─────────────────┤       ├─────────────────┤
│ - hotels        │──────▶│ - name          │
│ - reservations  │       │ - location      │
├─────────────────┤       │ - rooms[]       │
│ + searchHotels()│       │ - amenities     │
│ + book()        │       ├─────────────────┤
│ + cancel()      │       │ + getAvailable()│
└─────────────────┘       └────────┬────────┘
                                   │
                          ┌────────▼────────┐
                          │      Room       │
                          ├─────────────────┤
                          │ - roomNumber    │
                          │ - roomType      │
                          │ - basePrice     │
                          │ - amenities     │
                          └─────────────────┘

┌─────────────────┐       ┌─────────────────┐
│   Reservation   │       │     Guest       │
├─────────────────┤       ├─────────────────┤
│ - id            │──────▶│ - name          │
│ - guest         │       │ - email         │
│ - room          │       │ - phone         │
│ - checkIn       │       └─────────────────┘
│ - checkOut      │
│ - status        │
│ - totalPrice    │
└─────────────────┘
```

---

## Implementation

### Enums

```python
from enum import Enum
from datetime import date, datetime
from typing import List, Optional
import uuid

class RoomType(Enum):
    SINGLE = "single"
    DOUBLE = "double"
    DELUXE = "deluxe"
    SUITE = "suite"

class ReservationStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"
```

### Room and Hotel

```python
class Room:
    def __init__(self, room_number: str, room_type: RoomType, 
                 base_price: float, capacity: int):
        self.room_number = room_number
        self.room_type = room_type
        self.base_price = base_price
        self.capacity = capacity
        self.amenities = []
    
    def get_price(self, check_in: date, check_out: date, 
                  pricing_strategy) -> float:
        nights = (check_out - check_in).days
        return pricing_strategy.calculate(self, check_in, check_out) * nights

class Hotel:
    def __init__(self, hotel_id: str, name: str, location: str):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms: List[Room] = []
        self.reservations: List['Reservation'] = []
    
    def add_room(self, room: Room):
        self.rooms.append(room)
    
    def get_available_rooms(self, check_in: date, check_out: date, 
                           room_type: RoomType = None) -> List[Room]:
        available = []
        for room in self.rooms:
            if room_type and room.room_type != room_type:
                continue
            if self._is_room_available(room, check_in, check_out):
                available.append(room)
        return available
    
    def _is_room_available(self, room: Room, check_in: date, 
                          check_out: date) -> bool:
        for reservation in self.reservations:
            if reservation.room != room:
                continue
            if reservation.status == ReservationStatus.CANCELLED:
                continue
            # Check for overlap
            if not (check_out <= reservation.check_in or 
                    check_in >= reservation.check_out):
                return False
        return True
```

### Guest and Reservation

```python
class Guest:
    def __init__(self, name: str, email: str, phone: str):
        self.guest_id = str(uuid.uuid4())[:8]
        self.name = name
        self.email = email
        self.phone = phone

class Reservation:
    def __init__(self, guest: Guest, hotel: Hotel, room: Room,
                 check_in: date, check_out: date, total_price: float):
        self.reservation_id = str(uuid.uuid4())[:8]
        self.guest = guest
        self.hotel = hotel
        self.room = room
        self.check_in = check_in
        self.check_out = check_out
        self.total_price = total_price
        self.status = ReservationStatus.PENDING
        self.created_at = datetime.now()
    
    def confirm(self):
        if self.status == ReservationStatus.PENDING:
            self.status = ReservationStatus.CONFIRMED
            return True
        return False
    
    def cancel(self) -> float:
        if self.status in [ReservationStatus.PENDING, 
                          ReservationStatus.CONFIRMED]:
            self.status = ReservationStatus.CANCELLED
            return self._calculate_refund()
        return 0
    
    def _calculate_refund(self) -> float:
        days_until_checkin = (self.check_in - date.today()).days
        if days_until_checkin > 7:
            return self.total_price  # Full refund
        elif days_until_checkin > 3:
            return self.total_price * 0.5  # 50% refund
        return 0  # No refund
    
    def check_in_guest(self):
        if (self.status == ReservationStatus.CONFIRMED and 
            self.check_in <= date.today()):
            self.status = ReservationStatus.CHECKED_IN
            return True
        return False
    
    def check_out_guest(self):
        if self.status == ReservationStatus.CHECKED_IN:
            self.status = ReservationStatus.CHECKED_OUT
            return True
        return False
```

### Pricing Strategy

```python
from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, room: Room, check_in: date, 
                 check_out: date) -> float:
        pass

class StandardPricing(PricingStrategy):
    def calculate(self, room, check_in, check_out):
        return room.base_price

class SeasonalPricing(PricingStrategy):
    def __init__(self, peak_months: List[int], peak_multiplier: float = 1.5):
        self.peak_months = peak_months
        self.peak_multiplier = peak_multiplier
    
    def calculate(self, room, check_in, check_out):
        if check_in.month in self.peak_months:
            return room.base_price * self.peak_multiplier
        return room.base_price

class DynamicPricing(PricingStrategy):
    def __init__(self, hotel: Hotel):
        self.hotel = hotel
    
    def calculate(self, room, check_in, check_out):
        # Price based on occupancy
        available = len(self.hotel.get_available_rooms(check_in, check_out))
        total = len(self.hotel.rooms)
        occupancy_rate = 1 - (available / total)
        
        # Higher price when more occupied
        multiplier = 1 + (occupancy_rate * 0.5)
        return room.base_price * multiplier
```

### Booking System

```python
class BookingSystem:
    def __init__(self):
        self.hotels: dict[str, Hotel] = {}
        self.guests: dict[str, Guest] = {}
        self.pricing_strategy = StandardPricing()
    
    def add_hotel(self, hotel: Hotel):
        self.hotels[hotel.hotel_id] = hotel
    
    def search_hotels(self, location: str, check_in: date, 
                     check_out: date, guests: int,
                     room_type: RoomType = None) -> List[dict]:
        results = []
        for hotel in self.hotels.values():
            if location.lower() not in hotel.location.lower():
                continue
            
            available_rooms = hotel.get_available_rooms(
                check_in, check_out, room_type
            )
            suitable_rooms = [r for r in available_rooms 
                            if r.capacity >= guests]
            
            if suitable_rooms:
                results.append({
                    'hotel': hotel,
                    'available_rooms': suitable_rooms,
                    'min_price': min(r.get_price(check_in, check_out, 
                                    self.pricing_strategy) 
                                   for r in suitable_rooms)
                })
        
        return sorted(results, key=lambda x: x['min_price'])
    
    def create_reservation(self, guest: Guest, hotel_id: str,
                          room_number: str, check_in: date,
                          check_out: date) -> Reservation:
        hotel = self.hotels.get(hotel_id)
        if not hotel:
            raise ValueError("Hotel not found")
        
        room = next((r for r in hotel.rooms 
                    if r.room_number == room_number), None)
        if not room:
            raise ValueError("Room not found")
        
        if not hotel._is_room_available(room, check_in, check_out):
            raise ValueError("Room not available for these dates")
        
        total_price = room.get_price(check_in, check_out, 
                                     self.pricing_strategy)
        
        reservation = Reservation(guest, hotel, room, 
                                 check_in, check_out, total_price)
        hotel.reservations.append(reservation)
        
        return reservation
```

---

## Usage Example

```python
# Create system
system = BookingSystem()

# Add hotel
hotel = Hotel("H001", "Grand Hotel", "New York")
hotel.add_room(Room("101", RoomType.SINGLE, 100, 1))
hotel.add_room(Room("102", RoomType.DOUBLE, 150, 2))
hotel.add_room(Room("201", RoomType.DELUXE, 250, 2))
system.add_hotel(hotel)

# Search
results = system.search_hotels("New York", date(2024, 6, 1), 
                               date(2024, 6, 5), 2)

# Book
guest = Guest("John Doe", "john@email.com", "555-0100")
reservation = system.create_reservation(
    guest, "H001", "102", 
    date(2024, 6, 1), date(2024, 6, 5)
)
reservation.confirm()
```

---

## Key Takeaways

1. **Strategy pattern** for flexible pricing.
2. **Availability check** prevents double booking.
3. **Cancellation policy** based on days until check-in.
4. **Search filtering** by location, dates, capacity.
