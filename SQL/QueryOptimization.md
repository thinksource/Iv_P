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

因为：

* 函数会导致 index 失效
* 变成 full scan

# SELECT *

避免：

SELECT *

原因：

* 更多 IO
* 更多 network traffic
* 覆盖索引失效

# JOIN Optimization

## INNER JOIN vs. LEFT JOIN

### INNER JOIN (等值连接)：
* 逻辑：只返回两表匹配的行。
* 优化器行为：非常灵活。SQL Server 优化器可以自由决定谁是“驱动表”（先读哪张表），以及使用哪种算法（Hash, Merge, 或 Loop）。

### LEFT JOIN (左外连接)：
* 逻辑：保留左表所有行，右表无匹配则补 NULL。
* 优化器行为：约束较多。优化器通常必须先处理左表，这限制了它调整执行顺序的空间。如果左表很大而你只需要过滤后的数据，用 LEFT JOIN 往往比 INNER JOIN 慢。

## EXISTS vs. IN

这两个通常用于“半连接”（Semi-Join），即只关心是否存在，不关心具体内容。

### IN：
* 适合子查询返回结果集较小的情况。
* 风险：如果子查询结果包含 NULL，NOT IN 会导致整个查询不返回任何结果。

### EXISTS：

* 性能通常更稳：一旦找到匹配行就会立即停止扫描（短路逻辑）。
* 它在处理 NULL 时更符合逻辑，且在复杂子查询中，优化器通常能更好地将其转化为高效的 JOIN 算法。

## JOIN 顺序 (Join Order)

* 原理：SQL Server 使用基于成本的优化器 (CBO)。它会尝试不同的排列组合，估算 CPU 和内存开销。
* 黄金法则：先过滤，后连接。
    - 理想情况下，优化器会选择结果集最小的操作作为起点（驱动表），去连接大表。
    - 如果发现执行计划里先扫描了大表，可能需要检查统计信息 (Statistics) 是否过期，导致优化器误判了行数。

1. Nested Loops (嵌套循环)
* 类比： 像是在两个嵌套的 for 循环中查找数据。
* 特点： 只要外层表够小，或者大表索引覆盖得好，这是效率最高的算法。

2. Hash Join (哈希连接)
* 类比： 把一个小杯子里的球根据颜色分类放进篮子（Hash Table），然后拿着大箱子里的球去对颜色。
* 执行逻辑：
    - 1. Build 阶段： 扫描较小的表 (Products)，对 ProductID 进行哈希运算，存入内存中的 Hash Table。
    - 2. Probe 阶段： 扫描大表 (Sales)，对每一行的 ProductID 做同样的哈希运算，去内存表里找匹配。
* 特点： 它是处理大量无序数据的“暴力”解法。风险是如果内存放不下那个 Hash Table，SQL Server 必须把数据写入 TempDB（磁盘），速度会瞬间掉下悬崖。

3. Merge Join (合并连接)
* 类比： 两叠已经按编号排好序的简历，你只需要从头开始同时移动两只手对比即可。
* 执行逻辑：
    - 1. 优化器同时从两张表的第一行开始读。
    - 2. 如果 c.ID == p.ID，匹配成功。
    - 3. 如果 c.ID < p.ID，指针向下移动 c 表；反之移动 p 表。

| 算法 | 驱动表 (左) | 被驱动表 (右) | 核心依赖 | 内存消耗 |
| :--- | :---       | ---:         |   ---:  |    ---:  |
|Nested Loops|极小结果集|巨大表| 索引(Index Seek)|极低  |  
|Hash Join|较小表 (Build)|较大表 (Probe)|内存 (CPU 密集)|极高 |
|Merge Join|大表|大表|排序 (聚集索引)|低|



# Pagination

| Paging Method | Core Syntax | Performance | Ideal Use Case |
|:---| :---|:---|:---|
|OFFSET / FETCH |OFFSET X ROWS| Degrades linearly (Slower as page depth increases)|Small datasets, simple internal admin panels|
|Keyset (Seek)| WHERE ID > X | Consistently Fast (O(log N) complexity)|Infinite scroll, mobile apps, high-concurrency public APIs|
|Indexed (Deferred Join)|Covering Index + Join | Lowest I/O overhead | Large tables where many columns (LOBs) must be returned |