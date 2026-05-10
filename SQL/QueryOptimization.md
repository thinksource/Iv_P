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


# Aggregation Optimization
在 SQL Server 中，GROUP BY, ORDER BY, DISTINCT三个操作被称为阻断性算子（Blocking Operators）
## 1. 为什么触发 Sort (排序)？
- ORDER BY：逻辑最直接。数据库必须对结果集进行全量排序，除非数据已经通过索引预先排好了序。
- GROUP BY：为了把相同的项聚在一起（例如统计每个城市的订单），SQL Server 通常有两种做法：
- 1. Stream Aggregate：要求输入数据必须是有序的。如果没索引，它会先执行一个 Sort 动作。
- 2. Hash Aggregate：如果数据量大且无序，它会构建哈希表。虽然不直接显示为“Sort”，但逻辑上同样需要处理全量数据。
- DISTINCT：去重的本质就是排序或哈希。数据库必须对比每一行，确定它是否出现过。最简单的办法就是先把数据排好序，然后跳过重复的相邻项。

## 2. 为什么触发 Memory Pressure (内存压力)？
- 工作内存 (Workspace Memory)：执行排序或构建哈希表需要申请 Memory Grant（内存授权）。
- 资源争抢：如果你的结果集很大（例如 100 万行），SQL Server 会尝试在内存中开辟一块空间来存放这些中间数据。
- 并发瓶颈：当多个查询同时请求大额内存时，会导致 RESOURCE_SEMAPHORE 等待，系统整体性能下降。

## 3. 为什么触发 TempDB (溢出)？

这是开发者最不希望看到的阶段，称为 Spill to TempDB

- 估算失误：如果 SQL Server 认为只有 100 行，但实际有 100 万行，它申请的内存就会不够用。
- 物理落盘：当内存空间不足以支撑当前的排序或哈希操作时，SQL Server 必须将中间结果写入 TempDB（磁盘）。
- 性能暴降：磁盘 I/O 的速度比内存慢数千倍。一旦发生 Spill，原本几毫秒的查询可能变成几秒甚至几分钟。

| 特性| OPTION (RECOMPILE) | OPTIMIZE FOR UNKNOWN |
|:---| :---|:---|
|精准度| 最高（针对当前值优化）|中等（针对平均值优化）|
| CPU 开销高 |（每次都要重新编译）| 极低（编译一次，长期缓存）| |缓存|不缓存计划 | 缓存平均计划 |
|稳定性|极佳|极佳（消除极端的“慢查询”）|
|适用场景| 复杂、运行频率低的报表 | 运行频率高、数据分布极度不均的 API |