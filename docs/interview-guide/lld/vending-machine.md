---
sidebar_position: 9
title: "Design Vending Machine"
description: >-
  Complete LLD for vending machine. State pattern, inventory management,
  payment handling, and error recovery.
keywords:
  - vending machine design
  - LLD vending machine
  - state pattern
  - object oriented design
difficulty: Intermediate
estimated_time: 30 minutes
prerequisites:
  - SOLID Principles
  - State Pattern
companies: [Amazon, Google, Microsoft]
---

# Design a Vending Machine

Vending machine is a classic LLD problem that tests state management and payment handling.

---

## Requirements

- Select product from available items
- Accept multiple payment methods (cash, card)
- Dispense product and change
- Handle out-of-stock items
- Admin can refill products and collect cash

---

## Class Diagram

```
┌─────────────────┐       ┌─────────────────┐
│ VendingMachine  │       │   Inventory     │
├─────────────────┤       ├─────────────────┤
│ - inventory     │──────▶│ - items{}       │
│ - state         │       ├─────────────────┤
│ - currentBalance│       │ + addItem()     │
│ - selectedItem  │       │ + getItem()     │
├─────────────────┤       │ + updateQty()   │
│ + selectItem()  │       └─────────────────┘
│ + insertMoney() │
│ + dispense()    │       ┌─────────────────┐
│ + cancel()      │       │     Product     │
└────────┬────────┘       ├─────────────────┤
         │                │ - code          │
         │                │ - name          │
         │                │ - price         │
         ▼                │ - quantity      │
┌─────────────────┐       └─────────────────┘
│     State       │
├─────────────────┤
│ <<interface>>   │
│ + selectItem()  │
│ + insertMoney() │
│ + dispense()    │
│ + cancel()      │
└─────────────────┘
         △
         │
    ┌────┴────┬──────────┬──────────┐
    │         │          │          │
┌───┴───┐ ┌───┴───┐ ┌────┴────┐ ┌───┴────┐
│ Idle  │ │HasItem│ │HasMoney │ │Dispense│
│ State │ │ State │ │  State  │ │ State  │
└───────┘ └───────┘ └─────────┘ └────────┘
```

---

## Implementation

### Product and Inventory

```python
from enum import Enum
from typing import Dict, Optional

class Product:
    def __init__(self, code: str, name: str, price: float, quantity: int):
        self.code = code
        self.name = name
        self.price = price
        self.quantity = quantity

class Inventory:
    def __init__(self):
        self.items: Dict[str, Product] = {}
    
    def add_product(self, product: Product):
        self.items[product.code] = product
    
    def get_product(self, code: str) -> Optional[Product]:
        return self.items.get(code)
    
    def is_available(self, code: str) -> bool:
        product = self.items.get(code)
        return product is not None and product.quantity > 0
    
    def reduce_quantity(self, code: str):
        if self.is_available(code):
            self.items[code].quantity -= 1
    
    def restock(self, code: str, quantity: int):
        if code in self.items:
            self.items[code].quantity += quantity
```

### State Interface and Implementations

```python
from abc import ABC, abstractmethod

class State(ABC):
    def __init__(self, machine: 'VendingMachine'):
        self.machine = machine
    
    @abstractmethod
    def select_item(self, code: str) -> str:
        pass
    
    @abstractmethod
    def insert_money(self, amount: float) -> str:
        pass
    
    @abstractmethod
    def dispense(self) -> str:
        pass
    
    @abstractmethod
    def cancel(self) -> float:
        pass

class IdleState(State):
    def select_item(self, code: str) -> str:
        if self.machine.inventory.is_available(code):
            product = self.machine.inventory.get_product(code)
            self.machine.selected_item = product
            self.machine.state = HasItemState(self.machine)
            return f"Selected: {product.name} - ${product.price}"
        return "Item not available"
    
    def insert_money(self, amount: float) -> str:
        return "Please select an item first"
    
    def dispense(self) -> str:
        return "Please select an item first"
    
    def cancel(self) -> float:
        return 0

class HasItemState(State):
    def select_item(self, code: str) -> str:
        return "Item already selected. Insert money or cancel."
    
    def insert_money(self, amount: float) -> str:
        self.machine.current_balance += amount
        
        if self.machine.current_balance >= self.machine.selected_item.price:
            self.machine.state = HasMoneyState(self.machine)
            return f"Balance: ${self.machine.current_balance}. Press dispense."
        
        remaining = self.machine.selected_item.price - self.machine.current_balance
        return f"Balance: ${self.machine.current_balance}. Insert ${remaining} more."
    
    def dispense(self) -> str:
        return "Please insert money first"
    
    def cancel(self) -> float:
        refund = self.machine.current_balance
        self.machine.reset()
        return refund

class HasMoneyState(State):
    def select_item(self, code: str) -> str:
        return "Item selected. Press dispense or cancel."
    
    def insert_money(self, amount: float) -> str:
        self.machine.current_balance += amount
        return f"Balance: ${self.machine.current_balance}"
    
    def dispense(self) -> str:
        self.machine.state = DispensingState(self.machine)
        return self.machine.state.dispense()
    
    def cancel(self) -> float:
        refund = self.machine.current_balance
        self.machine.reset()
        return refund

class DispensingState(State):
    def select_item(self, code: str) -> str:
        return "Please wait, dispensing..."
    
    def insert_money(self, amount: float) -> str:
        return "Please wait, dispensing..."
    
    def dispense(self) -> str:
        product = self.machine.selected_item
        change = self.machine.current_balance - product.price
        
        self.machine.inventory.reduce_quantity(product.code)
        self.machine.collected_cash += product.price
        
        result = f"Dispensed: {product.name}"
        if change > 0:
            result += f". Change: ${change:.2f}"
        
        self.machine.reset()
        return result
    
    def cancel(self) -> float:
        return 0  # Can't cancel during dispense
```

### Vending Machine

```python
class VendingMachine:
    def __init__(self):
        self.inventory = Inventory()
        self.state: State = IdleState(self)
        self.current_balance = 0.0
        self.selected_item: Optional[Product] = None
        self.collected_cash = 0.0
    
    def select_item(self, code: str) -> str:
        return self.state.select_item(code)
    
    def insert_money(self, amount: float) -> str:
        return self.state.insert_money(amount)
    
    def dispense(self) -> str:
        return self.state.dispense()
    
    def cancel(self) -> float:
        return self.state.cancel()
    
    def reset(self):
        self.current_balance = 0.0
        self.selected_item = None
        self.state = IdleState(self)
    
    # Admin methods
    def add_product(self, product: Product):
        self.inventory.add_product(product)
    
    def restock(self, code: str, quantity: int):
        self.inventory.restock(code, quantity)
    
    def collect_cash(self) -> float:
        amount = self.collected_cash
        self.collected_cash = 0
        return amount
    
    def get_inventory_status(self) -> Dict[str, int]:
        return {code: p.quantity for code, p in self.inventory.items.items()}
```

---

## Usage Example

```python
# Create machine
machine = VendingMachine()

# Stock products
machine.add_product(Product("A1", "Chips", 1.50, 10))
machine.add_product(Product("A2", "Soda", 2.00, 5))
machine.add_product(Product("B1", "Candy", 1.00, 15))

# Customer flow
print(machine.select_item("A1"))      # Selected: Chips - $1.50
print(machine.insert_money(1.00))     # Balance: $1.00. Insert $0.50 more.
print(machine.insert_money(1.00))     # Balance: $2.00. Press dispense.
print(machine.dispense())             # Dispensed: Chips. Change: $0.50

# Admin operations
print(machine.get_inventory_status()) # {'A1': 9, 'A2': 5, 'B1': 15}
print(machine.collect_cash())         # 1.50
```

---

## State Transitions

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│     ┌───────┐  select_item   ┌─────────┐  insert_money      │
│     │       │ ─────────────▶ │         │ (enough)           │
│     │ IDLE  │                │HAS_ITEM │ ──────────┐        │
│     │       │ ◀───────────── │         │           │        │
│     └───────┘    cancel      └─────────┘           │        │
│         ▲                                          ▼        │
│         │                                   ┌───────────┐   │
│         │                                   │           │   │
│         │      dispense_complete            │ HAS_MONEY │   │
│         └─────────────────────────────────  │           │   │
│                                             └─────┬─────┘   │
│                                                   │         │
│                                          dispense │         │
│                                                   ▼         │
│                                            ┌───────────┐    │
│                                            │DISPENSING │    │
│                                            └───────────┘    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Key Takeaways

1. **State pattern** cleanly handles different machine states.
2. **Single responsibility** - Inventory manages products, State handles behavior.
3. **Clear transitions** between states prevent invalid operations.
4. **Admin operations** separate from customer flow.
