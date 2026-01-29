---
sidebar_position: 6
title: "SQL Advanced Queries"
description: >-
  Advanced SQL for coding interviews. Window functions, CTEs, complex joins,
  and query optimization.
keywords:
  - advanced SQL
  - window functions
  - CTE
  - SQL interview
difficulty: Advanced
estimated_time: 25 minutes
prerequisites:
  - SQL Essentials
companies: [All Companies]
---

# Advanced SQL: Beyond the Basics

Senior roles often include SQL questions. Master these advanced concepts.

---

## Window Functions

Window functions perform calculations across rows related to the current row.

### ROW_NUMBER, RANK, DENSE_RANK

```sql
-- ROW_NUMBER: Unique sequential number
-- RANK: Same rank for ties, gaps after
-- DENSE_RANK: Same rank for ties, no gaps

SELECT 
    name,
    department,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num,
    RANK() OVER (ORDER BY salary DESC) as rank,
    DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank
FROM employees;

-- Result for salaries: 100, 100, 90, 80
-- row_num: 1, 2, 3, 4
-- rank:    1, 1, 3, 4
-- dense:   1, 1, 2, 3
```

### PARTITION BY

```sql
-- Top 3 salaries per department
WITH ranked AS (
    SELECT 
        name,
        department,
        salary,
        DENSE_RANK() OVER (
            PARTITION BY department 
            ORDER BY salary DESC
        ) as rank
    FROM employees
)
SELECT * FROM ranked WHERE rank <= 3;
```

### LAG and LEAD

```sql
-- Compare with previous/next row
SELECT 
    date,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY date) as prev_day,
    revenue - LAG(revenue, 1) OVER (ORDER BY date) as daily_change,
    LEAD(revenue, 1) OVER (ORDER BY date) as next_day
FROM daily_sales;
```

### Running Totals and Moving Averages

```sql
-- Running total
SELECT 
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as running_total
FROM transactions;

-- Moving average (last 7 days)
SELECT 
    date,
    revenue,
    AVG(revenue) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7d
FROM daily_sales;
```

---

## Common Table Expressions (CTEs)

```sql
-- Basic CTE
WITH high_earners AS (
    SELECT * FROM employees WHERE salary > 100000
)
SELECT department, COUNT(*) as count
FROM high_earners
GROUP BY department;

-- Recursive CTE (hierarchical data)
WITH RECURSIVE org_chart AS (
    -- Base case: top-level managers
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case
    SELECT e.id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT * FROM org_chart ORDER BY level;
```

---

## Complex Joins

### Self Join

```sql
-- Find employees who earn more than their manager
SELECT 
    e.name as employee,
    e.salary as emp_salary,
    m.name as manager,
    m.salary as mgr_salary
FROM employees e
JOIN employees m ON e.manager_id = m.id
WHERE e.salary > m.salary;
```

### Multiple Joins

```sql
-- Orders with customer and product info
SELECT 
    o.order_id,
    c.name as customer,
    p.name as product,
    oi.quantity,
    oi.quantity * p.price as total
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.id;
```

### Anti-Join (NOT EXISTS)

```sql
-- Customers who never ordered
SELECT c.*
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);

-- Alternative with LEFT JOIN
SELECT c.*
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;
```

---

## Common Interview Patterns

### Second Highest Salary

```sql
-- Method 1: Subquery
SELECT MAX(salary) 
FROM employees 
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Method 2: Window function
SELECT salary FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rank
    FROM employees
) ranked
WHERE rank = 2;
```

### Consecutive Days/Streaks

```sql
-- Find users with 3+ consecutive login days
WITH numbered AS (
    SELECT 
        user_id,
        login_date,
        login_date - INTERVAL ROW_NUMBER() OVER (
            PARTITION BY user_id ORDER BY login_date
        ) DAY as grp
    FROM logins
)
SELECT user_id, MIN(login_date) as streak_start, 
       COUNT(*) as streak_length
FROM numbered
GROUP BY user_id, grp
HAVING COUNT(*) >= 3;
```

### Year-over-Year Comparison

```sql
SELECT 
    YEAR(date) as year,
    SUM(revenue) as total_revenue,
    LAG(SUM(revenue)) OVER (ORDER BY YEAR(date)) as prev_year,
    (SUM(revenue) - LAG(SUM(revenue)) OVER (ORDER BY YEAR(date))) 
        / LAG(SUM(revenue)) OVER (ORDER BY YEAR(date)) * 100 as yoy_growth
FROM sales
GROUP BY YEAR(date);
```

### Median Calculation

```sql
-- Median salary
WITH ordered AS (
    SELECT 
        salary,
        ROW_NUMBER() OVER (ORDER BY salary) as row_num,
        COUNT(*) OVER () as total_count
    FROM employees
)
SELECT AVG(salary) as median
FROM ordered
WHERE row_num IN (
    (total_count + 1) / 2,
    (total_count + 2) / 2
);
```

---

## Query Optimization

### Use Indexes

```sql
-- Create index on frequently queried columns
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);

-- Composite index for common query patterns
CREATE INDEX idx_orders_cust_date ON orders(customer_id, order_date);
```

### Avoid SELECT *

```sql
-- Bad: Fetches all columns
SELECT * FROM orders WHERE customer_id = 123;

-- Good: Only needed columns
SELECT order_id, order_date, total FROM orders WHERE customer_id = 123;
```

### Use EXISTS Instead of IN

```sql
-- Slower with large subquery
SELECT * FROM orders WHERE customer_id IN (
    SELECT id FROM customers WHERE city = 'NYC'
);

-- Faster with EXISTS
SELECT * FROM orders o WHERE EXISTS (
    SELECT 1 FROM customers c 
    WHERE c.id = o.customer_id AND c.city = 'NYC'
);
```

---

## Practice Problems

| Problem | Key Concept |
|---------|-------------|
| Nth Highest Salary | DENSE_RANK, LIMIT |
| Consecutive Numbers | LAG/LEAD or self-join |
| Department Top 3 | PARTITION BY + ranking |
| Cumulative Sum | Window SUM |
| Tree Node Type | CASE + self-join |
| Trips and Users | Complex joins + filtering |

---

## Key Takeaways

1. **Window functions** for ranking and running calculations.
2. **CTEs** for readable, modular queries.
3. **Self-joins** for comparing rows in same table.
4. **EXISTS** often faster than IN for subqueries.
5. **Indexes** critical for query performance.
