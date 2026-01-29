---
sidebar_position: 10
title: "Design ATM System"
description: >-
  Complete LLD for ATM system. Authentication, transactions, cash dispensing,
  and chain of responsibility pattern.
keywords:
  - ATM design
  - LLD ATM
  - banking system
  - chain of responsibility
difficulty: Intermediate
estimated_time: 35 minutes
prerequisites:
  - SOLID Principles
  - State Pattern
  - Chain of Responsibility
companies: [Goldman Sachs, JP Morgan, Amazon]
---

# Design an ATM System

ATM design tests authentication flows, transaction handling, and cash dispensing logic.

---

## Requirements

- Card authentication with PIN
- Check balance
- Withdraw cash (dispense optimal denomination)
- Deposit money
- Transfer between accounts
- Handle insufficient funds, daily limits

---

## Class Diagram

```
┌─────────────────┐       ┌─────────────────┐
│       ATM       │       │   BankService   │
├─────────────────┤       ├─────────────────┤
│ - cashDispenser │       │ + authenticate()│
│ - state         │──────▶│ + getBalance()  │
│ - currentCard   │       │ + withdraw()    │
│ - currentAccount│       │ + deposit()     │
├─────────────────┤       └─────────────────┘
│ + insertCard()  │
│ + enterPin()    │       ┌─────────────────┐
│ + selectTxn()   │       │  CashDispenser  │
│ + ejectCard()   │       ├─────────────────┤
└─────────────────┘       │ - cashInventory │
                          ├─────────────────┤
                          │ + dispense()    │
                          │ + hasSufficient()│
                          └─────────────────┘

┌─────────────────┐       ┌─────────────────┐
│      Card       │       │    Account      │
├─────────────────┤       ├─────────────────┤
│ - cardNumber    │       │ - accountNumber │
│ - expiryDate    │       │ - balance       │
│ - cardHolder    │       │ - dailyLimit    │
└─────────────────┘       │ - withdrawnToday│
                          └─────────────────┘
```

---

## Implementation

### Account and Card

```python
from enum import Enum
from datetime import date
from typing import Optional

class Account:
    def __init__(self, account_number: str, balance: float, 
                 daily_limit: float = 1000):
        self.account_number = account_number
        self.balance = balance
        self.daily_limit = daily_limit
        self.withdrawn_today = 0.0
        self.last_withdrawal_date = None
    
    def can_withdraw(self, amount: float) -> tuple[bool, str]:
        # Reset daily limit if new day
        if self.last_withdrawal_date != date.today():
            self.withdrawn_today = 0.0
        
        if amount > self.balance:
            return False, "Insufficient funds"
        
        if self.withdrawn_today + amount > self.daily_limit:
            remaining = self.daily_limit - self.withdrawn_today
            return False, f"Daily limit exceeded. Remaining: ${remaining}"
        
        return True, "OK"
    
    def withdraw(self, amount: float) -> bool:
        can, _ = self.can_withdraw(amount)
        if can:
            self.balance -= amount
            self.withdrawn_today += amount
            self.last_withdrawal_date = date.today()
            return True
        return False
    
    def deposit(self, amount: float):
        self.balance += amount

class Card:
    def __init__(self, card_number: str, pin: str, account: Account):
        self.card_number = card_number
        self.pin = pin
        self.account = account
        self.attempts = 0
        self.blocked = False
    
    def validate_pin(self, pin: str) -> bool:
        if self.blocked:
            return False
        
        if self.pin == pin:
            self.attempts = 0
            return True
        
        self.attempts += 1
        if self.attempts >= 3:
            self.blocked = True
        return False
```

### Cash Dispenser (Chain of Responsibility)

```python
from abc import ABC, abstractmethod

class CashHandler(ABC):
    def __init__(self, denomination: int, count: int):
        self.denomination = denomination
        self.count = count
        self.next_handler: Optional['CashHandler'] = None
    
    def set_next(self, handler: 'CashHandler') -> 'CashHandler':
        self.next_handler = handler
        return handler
    
    def dispense(self, amount: int) -> dict:
        notes_needed = min(amount // self.denomination, self.count)
        result = {}
        
        if notes_needed > 0:
            result[self.denomination] = notes_needed
            self.count -= notes_needed
            amount -= notes_needed * self.denomination
        
        if amount > 0 and self.next_handler:
            result.update(self.next_handler.dispense(amount))
        
        return result

class CashDispenser:
    def __init__(self):
        # Chain: $100 -> $50 -> $20 -> $10
        self.handler_100 = CashHandler(100, 100)
        self.handler_50 = CashHandler(50, 100)
        self.handler_20 = CashHandler(20, 100)
        self.handler_10 = CashHandler(10, 100)
        
        self.handler_100.set_next(self.handler_50)
        self.handler_50.set_next(self.handler_20)
        self.handler_20.set_next(self.handler_10)
    
    def dispense(self, amount: int) -> dict:
        if amount % 10 != 0:
            raise ValueError("Amount must be multiple of 10")
        
        return self.handler_100.dispense(amount)
    
    def has_sufficient_cash(self, amount: int) -> bool:
        total = (
            self.handler_100.count * 100 +
            self.handler_50.count * 50 +
            self.handler_20.count * 20 +
            self.handler_10.count * 10
        )
        return total >= amount
    
    def get_cash_inventory(self) -> dict:
        return {
            100: self.handler_100.count,
            50: self.handler_50.count,
            20: self.handler_20.count,
            10: self.handler_10.count
        }
    
    def refill(self, denomination: int, count: int):
        handlers = {
            100: self.handler_100,
            50: self.handler_50,
            20: self.handler_20,
            10: self.handler_10
        }
        if denomination in handlers:
            handlers[denomination].count += count
```

### ATM State Machine

```python
class ATMState(Enum):
    IDLE = "idle"
    CARD_INSERTED = "card_inserted"
    AUTHENTICATED = "authenticated"
    TRANSACTION = "transaction"

class TransactionType(Enum):
    BALANCE = "balance"
    WITHDRAW = "withdraw"
    DEPOSIT = "deposit"

class ATM:
    def __init__(self, bank_service: 'BankService'):
        self.bank_service = bank_service
        self.cash_dispenser = CashDispenser()
        self.state = ATMState.IDLE
        self.current_card: Optional[Card] = None
    
    def insert_card(self, card: Card) -> str:
        if self.state != ATMState.IDLE:
            return "Please complete current transaction first"
        
        if card.blocked:
            return "Card is blocked. Please contact your bank."
        
        self.current_card = card
        self.state = ATMState.CARD_INSERTED
        return "Card accepted. Please enter PIN."
    
    def enter_pin(self, pin: str) -> str:
        if self.state != ATMState.CARD_INSERTED:
            return "Please insert card first"
        
        if self.current_card.validate_pin(pin):
            self.state = ATMState.AUTHENTICATED
            return "PIN accepted. Select transaction."
        
        if self.current_card.blocked:
            self.eject_card()
            return "Card blocked due to too many attempts."
        
        return f"Incorrect PIN. {3 - self.current_card.attempts} attempts remaining."
    
    def check_balance(self) -> str:
        if self.state != ATMState.AUTHENTICATED:
            return "Please authenticate first"
        
        balance = self.current_card.account.balance
        return f"Current balance: ${balance:.2f}"
    
    def withdraw(self, amount: int) -> str:
        if self.state != ATMState.AUTHENTICATED:
            return "Please authenticate first"
        
        account = self.current_card.account
        
        # Check account limits
        can, message = account.can_withdraw(amount)
        if not can:
            return message
        
        # Check ATM cash
        if not self.cash_dispenser.has_sufficient_cash(amount):
            return "ATM has insufficient cash"
        
        # Process withdrawal
        if account.withdraw(amount):
            notes = self.cash_dispenser.dispense(amount)
            notes_str = ", ".join(f"{count}x${denom}" 
                                 for denom, count in sorted(notes.items(), 
                                                          reverse=True))
            return f"Dispensed ${amount}: {notes_str}"
        
        return "Transaction failed"
    
    def deposit(self, amount: float) -> str:
        if self.state != ATMState.AUTHENTICATED:
            return "Please authenticate first"
        
        self.current_card.account.deposit(amount)
        return f"Deposited ${amount:.2f}. New balance: ${self.current_card.account.balance:.2f}"
    
    def eject_card(self) -> str:
        self.current_card = None
        self.state = ATMState.IDLE
        return "Card ejected. Thank you."
    
    # Admin methods
    def refill_cash(self, denomination: int, count: int):
        self.cash_dispenser.refill(denomination, count)
    
    def get_cash_inventory(self) -> dict:
        return self.cash_dispenser.get_cash_inventory()
```

### Bank Service (Mock)

```python
class BankService:
    def __init__(self):
        self.accounts: dict[str, Account] = {}
        self.cards: dict[str, Card] = {}
    
    def add_account(self, account: Account):
        self.accounts[account.account_number] = account
    
    def add_card(self, card: Card):
        self.cards[card.card_number] = card
    
    def get_card(self, card_number: str) -> Optional[Card]:
        return self.cards.get(card_number)
```

---

## Usage Example

```python
# Setup
bank = BankService()
account = Account("ACC001", 5000.00, daily_limit=1000)
card = Card("1234-5678-9012-3456", "1234", account)
bank.add_account(account)
bank.add_card(card)

atm = ATM(bank)

# Customer flow
print(atm.insert_card(card))          # Card accepted. Please enter PIN.
print(atm.enter_pin("1234"))          # PIN accepted. Select transaction.
print(atm.check_balance())            # Current balance: $5000.00
print(atm.withdraw(270))              # Dispensed $270: 2x$100, 1x$50, 1x$20
print(atm.check_balance())            # Current balance: $4730.00
print(atm.eject_card())               # Card ejected. Thank you.
```

---

## Key Takeaways

1. **State machine** for clear transaction flow.
2. **Chain of Responsibility** for optimal cash dispensing.
3. **Daily limits** and **PIN attempts** for security.
4. **Separation** between ATM hardware and bank services.
