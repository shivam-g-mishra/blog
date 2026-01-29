---
sidebar_position: 2
title: "SOLID Principles"
description: >-
  Master SOLID principles for LLD interviews. Single responsibility, open/closed,
  Liskov substitution, interface segregation, and dependency inversion.
keywords:
  - SOLID principles
  - single responsibility
  - open closed principle
  - liskov substitution
  - dependency inversion
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - LLD Introduction
companies: [All Companies]
---

# SOLID Principles: Foundation of Good Design

SOLID isn't academic theory—it's practical guidance that makes code maintainable.

---

## S: Single Responsibility Principle

**A class should have only one reason to change.**

### Bad Example

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def save_to_database(self):
        # Database logic
        pass
    
    def send_email(self, message):
        # Email logic
        pass
    
    def generate_report(self):
        # Report logic
        pass
```

### Good Example

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    def save(self, user):
        # Database logic
        pass

class EmailService:
    def send(self, user, message):
        # Email logic
        pass

class ReportGenerator:
    def generate(self, user):
        # Report logic
        pass
```

---

## O: Open/Closed Principle

**Open for extension, closed for modification.**

### Bad Example

```python
class PaymentProcessor:
    def process(self, payment_type, amount):
        if payment_type == "credit_card":
            # Credit card logic
            pass
        elif payment_type == "paypal":
            # PayPal logic
            pass
        elif payment_type == "bitcoin":
            # Bitcoin logic - had to modify class!
            pass
```

### Good Example

```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount):
        pass

class CreditCardPayment(PaymentMethod):
    def process(self, amount):
        # Credit card logic
        pass

class PayPalPayment(PaymentMethod):
    def process(self, amount):
        # PayPal logic
        pass

class BitcoinPayment(PaymentMethod):
    def process(self, amount):
        # Bitcoin logic - new class, no modification
        pass

class PaymentProcessor:
    def process(self, payment_method: PaymentMethod, amount):
        payment_method.process(amount)
```

---

## L: Liskov Substitution Principle

**Subtypes must be substitutable for their base types.**

### Bad Example

```python
class Bird:
    def fly(self):
        print("Flying")

class Penguin(Bird):  # Violates LSP!
    def fly(self):
        raise Exception("Penguins can't fly")
```

### Good Example

```python
class Bird:
    def move(self):
        pass

class FlyingBird(Bird):
    def move(self):
        self.fly()
    
    def fly(self):
        print("Flying")

class Penguin(Bird):
    def move(self):
        self.swim()
    
    def swim(self):
        print("Swimming")
```

---

## I: Interface Segregation Principle

**Many specific interfaces are better than one general interface.**

### Bad Example

```python
class Worker(ABC):
    @abstractmethod
    def work(self):
        pass
    
    @abstractmethod
    def eat(self):
        pass
    
    @abstractmethod
    def sleep(self):
        pass

class Robot(Worker):  # Robots don't eat or sleep!
    def work(self):
        pass
    
    def eat(self):
        raise NotImplementedError()
    
    def sleep(self):
        raise NotImplementedError()
```

### Good Example

```python
class Workable(ABC):
    @abstractmethod
    def work(self):
        pass

class Eatable(ABC):
    @abstractmethod
    def eat(self):
        pass

class Sleepable(ABC):
    @abstractmethod
    def sleep(self):
        pass

class Human(Workable, Eatable, Sleepable):
    def work(self):
        pass
    def eat(self):
        pass
    def sleep(self):
        pass

class Robot(Workable):  # Only implements what it needs
    def work(self):
        pass
```

---

## D: Dependency Inversion Principle

**Depend on abstractions, not concretions.**

### Bad Example

```python
class MySQLDatabase:
    def query(self, sql):
        pass

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # Coupled to MySQL
    
    def get_user(self, id):
        return self.db.query(f"SELECT * FROM users WHERE id = {id}")
```

### Good Example

```python
class Database(ABC):
    @abstractmethod
    def query(self, sql):
        pass

class MySQLDatabase(Database):
    def query(self, sql):
        pass

class PostgreSQLDatabase(Database):
    def query(self, sql):
        pass

class UserService:
    def __init__(self, database: Database):  # Depends on abstraction
        self.db = database
    
    def get_user(self, id):
        return self.db.query(f"SELECT * FROM users WHERE id = {id}")

# Can swap databases easily
service = UserService(MySQLDatabase())
service = UserService(PostgreSQLDatabase())
```

---

## Quick Reference

| Principle | Remember |
|-----------|----------|
| **S**ingle Responsibility | One class, one job |
| **O**pen/Closed | Extend, don't modify |
| **L**iskov Substitution | Subtypes work anywhere parent works |
| **I**nterface Segregation | Small, focused interfaces |
| **D**ependency Inversion | Depend on abstractions |

---

## Key Takeaways

1. **SRP:** If your class does too much, split it.
2. **OCP:** Use polymorphism for extensibility.
3. **LSP:** If inheritance feels wrong, use composition.
4. **ISP:** Don't force classes to implement unused methods.
5. **DIP:** Inject dependencies, don't create them.
