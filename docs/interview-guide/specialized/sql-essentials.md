---
sidebar_position: 2
title: "SQL Interview Essentials"
description: >-
  SQL fundamentals for coding interviews. JOINs, GROUP BY, window functions,
  and common interview queries.
keywords:
  - SQL interview
  - SQL queries
  - SQL joins
  - window functions
  - SQL practice
difficulty: Intermediate
estimated_time: 30 minutes
prerequisites: []
companies: [All Companies]
---

# SQL Essentials: Query with Confidence

Many companies include SQL rounds. Master these patterns.

---

## JOIN Types

```sql
-- INNER JOIN: Only matching rows
SELECT *
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id;

-- LEFT JOIN: All from left, matching from right
SELECT *
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id;
-- Includes customers with no orders (NULL in order columns)

-- RIGHT JOIN: All from right, matching from left
SELECT *
FROM orders o
RIGHT JOIN customers c ON o.customer_id = c.id;

-- FULL OUTER JOIN: All from both
SELECT *
FROM customers c
FULL OUTER JOIN orders o ON c.id = o.customer_id;
```

---

## GROUP BY & Aggregates

```sql
-- Count orders per customer
SELECT 
    customer_id,
    COUNT(*) as order_count,
    SUM(amount) as total_spent,
    AVG(amount) as avg_order
FROM orders
GROUP BY customer_id;

-- With HAVING (filter after grouping)
SELECT 
    customer_id,
    COUNT(*) as order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 5;  -- Only customers with 5+ orders
```

---

## Window Functions

```sql
-- Row number within partition
SELECT 
    name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees;

-- Running total
SELECT 
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as running_total
FROM transactions;

-- Rank (with ties)
SELECT 
    name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank
FROM employees;

-- Lead/Lag (access adjacent rows)
SELECT 
    date,
    price,
    LAG(price) OVER (ORDER BY date) as prev_price,
    LEAD(price) OVER (ORDER BY date) as next_price
FROM stock_prices;
```

---

## Common Interview Queries

### Second Highest Salary

```sql
-- Method 1: Subquery
SELECT MAX(salary) as second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Method 2: DENSE_RANK
SELECT salary as second_highest
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rank
    FROM employees
) ranked
WHERE rank = 2;

-- Method 3: LIMIT/OFFSET
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 1;
```

### Nth Highest Salary

```sql
SELECT salary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rank
    FROM employees
) ranked
WHERE rank = N;
```

### Duplicate Emails

```sql
SELECT email
FROM users
GROUP BY email
HAVING COUNT(*) > 1;
```

### Employees Earning More Than Manager

```sql
SELECT e.name as employee
FROM employees e
JOIN employees m ON e.manager_id = m.id
WHERE e.salary > m.salary;
```

### Consecutive Numbers

```sql
SELECT DISTINCT l1.num as consecutive_num
FROM logs l1
JOIN logs l2 ON l1.id = l2.id - 1
JOIN logs l3 ON l2.id = l3.id - 1
WHERE l1.num = l2.num AND l2.num = l3.num;

-- Or with window functions
SELECT DISTINCT num
FROM (
    SELECT num,
           LAG(num) OVER (ORDER BY id) as prev,
           LEAD(num) OVER (ORDER BY id) as next
    FROM logs
) t
WHERE num = prev AND num = next;
```

### Department Top 3 Salaries

```sql
SELECT department, name, salary
FROM (
    SELECT 
        d.name as department,
        e.name,
        e.salary,
        DENSE_RANK() OVER (PARTITION BY d.id ORDER BY e.salary DESC) as rank
    FROM employees e
    JOIN departments d ON e.department_id = d.id
) ranked
WHERE rank <= 3;
```

---

## CTEs (Common Table Expressions)

```sql
-- More readable than subqueries
WITH high_earners AS (
    SELECT *
    FROM employees
    WHERE salary > 100000
),
dept_counts AS (
    SELECT department_id, COUNT(*) as count
    FROM high_earners
    GROUP BY department_id
)
SELECT d.name, dc.count
FROM dept_counts dc
JOIN departments d ON dc.department_id = d.id;
```

---

## Optimization Tips

```sql
-- Use indexes on JOIN and WHERE columns
-- Avoid SELECT * in production
-- Use EXPLAIN to understand query plan

-- Bad: Function on indexed column
WHERE YEAR(created_at) = 2024

-- Good: Range condition
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'
```

---

## Practice Problems

| Problem | Concept | Difficulty |
|---------|---------|------------|
| Second Highest Salary | Subquery/Window | Easy |
| Nth Highest Salary | Window function | Medium |
| Rank Scores | DENSE_RANK | Medium |
| Consecutive Numbers | Self-join/Window | Medium |
| Department Top Salaries | Partition + rank | Hard |
| Trips and Users | Complex joins | Hard |

---

## Key Takeaways

1. **Master JOINs.** Know the difference between INNER, LEFT, RIGHT.
2. **Window functions** solve ranking and running total problems.
3. **GROUP BY + HAVING** for aggregate filtering.
4. **CTEs** make complex queries readable.
5. **Practice LeetCode SQL** problems.
