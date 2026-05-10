# SARGable Queries


避免：
```SQL
WHERE YEAR(order_date) = 2025
```
改成：
```SQL
WHERE order_date >= '2025-01-01'
AND order_date < '2026-01-01'
```