---
sidebar_position: 1
title: "Frontend Engineer Interview Guide"
description: >-
  Comprehensive guide for frontend engineering interviews. JavaScript,
  React, CSS, web performance, and frontend system design.
keywords:
  - frontend interview
  - javascript interview
  - react interview
  - web development
difficulty: Mixed
estimated_time: 20 minutes
prerequisites: []
companies: [Meta, Google, Amazon, Airbnb]
---

# Frontend Engineer Interview Guide

Frontend interviews blend coding, domain knowledge, and system design. Here's what to expect.

---

## Interview Structure

```
Typical frontend interview loop:

1. Phone Screen (45-60 min)
   - JavaScript fundamentals
   - DOM manipulation OR React question

2. Onsite (4-6 rounds)
   - Coding × 2 (algorithms + frontend-specific)
   - Frontend System Design × 1
   - UI Coding × 1 (build a component)
   - Behavioral × 1
```

---

## JavaScript Fundamentals

### Must-Know Topics

| Topic | Key Concepts |
|-------|--------------|
| **Closures** | Lexical scope, data privacy |
| **this** | Binding rules, arrow functions |
| **Promises** | async/await, error handling |
| **Event Loop** | Call stack, callback queue, microtasks |
| **Prototypes** | Inheritance, prototype chain |
| **ES6+** | Destructuring, spread, modules |

### Common Questions

```javascript
// Implement debounce
function debounce(fn, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
}

// Implement throttle
function throttle(fn, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// Implement Promise.all
function promiseAll(promises) {
  return new Promise((resolve, reject) => {
    const results = [];
    let completed = 0;
    
    promises.forEach((promise, index) => {
      Promise.resolve(promise)
        .then(value => {
          results[index] = value;
          completed++;
          if (completed === promises.length) {
            resolve(results);
          }
        })
        .catch(reject);
    });
  });
}
```

---

## React Concepts

### Must-Know

```
- Component lifecycle
- Hooks (useState, useEffect, useContext, useMemo, useCallback)
- Virtual DOM and reconciliation
- State management patterns
- Performance optimization
```

### Common Questions

```jsx
// Implement useDebounce hook
function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);
  
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    
    return () => clearTimeout(handler);
  }, [value, delay]);
  
  return debouncedValue;
}

// Implement usePrevious hook
function usePrevious(value) {
  const ref = useRef();
  
  useEffect(() => {
    ref.current = value;
  });
  
  return ref.current;
}
```

---

## Frontend System Design

### Common Questions

- Design a news feed
- Design an autocomplete component
- Design an image carousel
- Design a spreadsheet
- Design a chat application

### Framework

```
1. Requirements
   - Functional (features)
   - Non-functional (performance, accessibility)

2. Component Architecture
   - Component hierarchy
   - State management
   - Data flow

3. API Design
   - Endpoints needed
   - Data shapes
   - Caching strategy

4. Performance
   - Lazy loading
   - Virtualization
   - Caching

5. Accessibility
   - Keyboard navigation
   - Screen readers
   - ARIA attributes
```

---

## CSS & Layout

```css
/* Flexbox centering */
.center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Grid layout */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

/* CSS specificity */
/* ID > Class > Element */
/* 1-0-0 > 0-1-0 > 0-0-1 */
```

---

## Web Performance

```
Key metrics:
- LCP (Largest Contentful Paint) < 2.5s
- FID (First Input Delay) < 100ms
- CLS (Cumulative Layout Shift) < 0.1

Optimization techniques:
- Code splitting
- Lazy loading images
- Caching strategies
- Bundle optimization
- Critical CSS
```

---

## Key Takeaways

1. **JavaScript fundamentals** are heavily tested.
2. **Build components live**—practice implementing from scratch.
3. **Performance matters**—know optimization techniques.
4. **Accessibility** is increasingly important.
5. **Frontend system design** is different from backend.
