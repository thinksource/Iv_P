## 异步编程与同步编程的区别 主要体现在 任务执行方式、资源利用率 和 适用场景 上
一、核心区别
维度	同步编程	异步编程
执行顺序	代码按顺序执行，前一个任务完成后再执行下一个	任务可并行或非阻塞执行，无需等待前一个任务完成
阻塞性	阻塞主线程（如等待 I/O 操作完成）	非阻塞，主线程可继续处理其他任务
资源占用	线程可能因等待资源而闲置	高效利用 CPU 和线程资源（如单线程处理多任务）
代码复杂度	逻辑简单直观	回调嵌套或协程管理可能增加复杂度
适用场景	CPU 密集型任务、简单流程控制	I/O 密集型任务（如网络请求、文件读写）、高并发

## 递归公共表表达式（Recursive CTE） 是一种在 SQL 中处理 层次结构数据（如树形结构、图遍历、无限级联关系）的高级技术。PostgreSQL 完全支持递归 CTE，语法遵循 SQL 标准，使用 WITH RECURSIVE 关键字定义。
一、递归 CTE 基本语法
sql
Copy

WITH RECURSIVE cte_name (列列表) AS (
  -- 初始查询（非递归部分）
  SELECT ... FROM 表 WHERE 基础条件
  UNION ALL
  -- 递归部分：引用 CTE 自身
  SELECT ... FROM 表 JOIN cte_name ON 递归条件
)
-- 最终查询
SELECT * FROM cte_name;

关键点：

    初始查询：生成递归的起点数据。

    递归查询：基于前一次迭代的结果继续生成数据。

    终止条件：当递归部分不再产生新数据时自动停止。

二、PostgreSQL 中的实际应用示例
1. 组织结构遍历：查询所有下属

表结构：
sql
Copy

CREATE TABLE employees (
  id INT PRIMARY KEY,
  name VARCHAR(50),
  manager_id INT REFERENCES employees(id)
);

需求：查询某个管理者（如 ID=1）的所有下属（包括间接下属）。

递归 CTE：
sql
Copy

WITH RECURSIVE subordinates AS (
  -- 初始查询：直接下属
  SELECT id, name, manager_id
  FROM employees
  WHERE manager_id = 1
  UNION ALL
  -- 递归查询：逐级向下查找
  SELECT e.id, e.name, e.manager_id
  FROM employees e
  JOIN subordinates s ON e.manager_id = s.id
)
SELECT * FROM subordinates;

结果示例：
id	name	manager_id
2	Alice	1
3	Bob	2
4	Carol	3
2. 树形结构路径展开：论坛评论层级

表结构：
sql
Copy

CREATE TABLE comments (
  comment_id INT PRIMARY KEY,
  parent_id INT REFERENCES comments(comment_id),
  content TEXT
);

需求：展开评论 ID=101 的所有回复（包括嵌套回复）。

递归 CTE：
sql
Copy

WITH RECURSIVE comment_tree AS (
  -- 初始查询：根评论
  SELECT comment_id, parent_id, content, ARRAY[comment_id] AS path
  FROM comments
  WHERE comment_id = 101
  UNION ALL
  -- 递归查询：逐级展开子评论
  SELECT c.comment_id, c.parent_id, c.content, ct.path || c.comment_id
  FROM comments c
  JOIN comment_tree ct ON c.parent_id = ct.comment_id
)
SELECT comment_id, parent_id, content, path
FROM comment_tree
ORDER BY path;

结果示例：
comment_id	parent_id	content	path
101	NULL	主贴	{101}
201	101	回复主贴	{101,201}
301	201	回复回复	{101,201,301}
3. 数字序列生成：生成 1 到 10 的数字

递归 CTE：
sql
Copy

WITH RECURSIVE numbers AS (
  SELECT 1 AS n
  UNION ALL
  SELECT n + 1 FROM numbers WHERE n < 10
)
SELECT * FROM numbers;

结果：
n
1
2
...
10
4. 路径查找：查找所有可能的路径

表结构（有向图）：
sql
Copy

CREATE TABLE graph (
  from_node INT,
  to_node INT
);

需求：查找从节点 A（ID=1）到所有可达节点的路径。

递归 CTE：
sql
Copy

WITH RECURSIVE paths AS (
  SELECT from_node, to_node, ARRAY[from_node, to_node] AS path
  FROM graph
  WHERE from_node = 1
  UNION ALL
  SELECT p.from_node, g.to_node, p.path || g.to_node
  FROM graph g
  JOIN paths p ON g.from_node = p.to_node
  WHERE NOT g.to_node = ANY(p.path) -- 避免循环
)
SELECT * FROM paths;

结果示例：
from_node	to_node	path
1	2	{1,2}
1	3	{1,2,3}
三、注意事项

    终止条件：确保递归部分最终无法生成新行（否则无限循环）。PostgreSQL 默认限制递归深度为 1000，可通过 SET max_recursive_iterations = N 调整。

    性能优化：递归 CTE 可能效率较低，复杂场景可结合索引或物化路径（如 ltree 扩展）优化。

    避免重复计算：使用 UNION（去重）或 UNION ALL（保留重复）根据需求选择。

四、适用场景总结

    树形/层次结构：组织架构、分类目录、评论回复。

    图遍历：社交网络关系、路由路径。

    序列生成：日期范围、数字序列。

    依赖解析：任务执行顺序、课程先修关系。

通过递归 CTE，可以高效处理需要逐级展开或循环依赖的数据逻辑，是 PostgreSQL 中处理复杂查询的利器。


## 乐观锁与悲观锁是两种并发控制策略，用于解决多个事务/线程同时操作同一数据时的冲突问题。它们的核心区别在于对冲突的预期和处理方式。
一、悲观锁（Pessimistic Locking）
1. 核心思想

    假设冲突频繁：默认认为并发操作中数据会被其他事务修改，因此在操作前先加锁，确保独占访问。

    实现方式：通过数据库或编程语言提供的锁机制（如行锁、表锁）直接锁定数据。

2. 典型应用

    数据库操作：
    sql
    Copy

    BEGIN;
    SELECT * FROM accounts WHERE id = 1 FOR UPDATE; -- 加行级锁
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    COMMIT;

    编程语言：Java 中的 synchronized 关键字或 ReentrantLock。

3. 特点

    优点：强一致性，保证操作期间数据不被修改。

    缺点：

        锁开销大，降低并发性能。

        可能引发死锁（需超时或死锁检测机制）。

4. 适用场景

    高冲突环境：如银行账户扣款、库存超卖预防。

    长事务：需要长时间持有数据的场景。

二、乐观锁（Optimistic Locking）
1. 核心思想

    假设冲突很少：默认认为并发操作中数据冲突概率低，因此不提前加锁，只在提交时检查数据是否被修改。

    实现方式：通过版本号（Version）、时间戳或哈希值标记数据状态。

2. 典型应用

    数据库操作：
    sql
    Copy

    -- 读取时获取版本号
    SELECT id, balance, version FROM accounts WHERE id = 1;

    -- 更新时校验版本号
    UPDATE accounts 
    SET balance = balance - 100, version = version + 1 
    WHERE id = 1 AND version = 123; -- 若返回影响行数为0，说明版本冲突

    编程框架：JPA（Hibernate）的 @Version 注解、Redis 的 WATCH 命令。

3. 特点

    优点：无锁开销，高并发性能。

    缺点：

        需处理提交失败（如重试或业务补偿）。

        不适用于高冲突场景（频繁重试可能抵消性能优势）。

4. 适用场景

    低冲突环境：如评论点赞、配置更新。

    短事务：操作快速完成，减少冲突窗口。

三、对比总结
维度	悲观锁	乐观锁
冲突预期	假设高冲突	假设低冲突
加锁时机	操作前加锁	提交时检查
实现复杂度	简单（依赖数据库锁）	较高（需版本管理或重试逻辑）
性能开销	高（锁竞争、死锁风险）	低（无锁，但需处理冲突）
适用场景	金融交易、库存扣减	社交应用、配置管理
四、实战选择建议

    优先乐观锁：在低冲突场景（如读多写少）提升性能。

    谨慎用悲观锁：仅在必须保证强一致性时使用（如账户余额修改）。

    混合策略：

        对核心业务数据使用悲观锁（如支付）。

        对非核心数据使用乐观锁（如用户资料更新）。

五、示例：电商库存扣减
1. 悲观锁实现
sql
Copy

BEGIN;
SELECT stock FROM products WHERE id = 1001 FOR UPDATE; -- 锁定库存
IF stock >= 1 THEN
  UPDATE products SET stock = stock - 1 WHERE id = 1001;
END IF;
COMMIT;

2. 乐观锁实现
sql
Copy

-- 读取当前库存和版本号
SELECT stock, version FROM products WHERE id = 1001;

-- 假设当前 stock=1, version=5
UPDATE products 
SET stock = stock - 1, version = version + 1 
WHERE id = 1001 AND version = 5; -- 若失败则重试或提示库存不足

六、常见问题

    乐观锁如何避免 ABA 问题？

        使用递增版本号（而非时间戳）或追加操作日志。

    数据库事务隔离级别的影响？

        如使用 READ COMMITTED，需结合乐观锁版本检查防止不可重复读。

总结：乐观锁与悲观锁无绝对优劣，需根据业务场景的冲突频率、性能要求及数据一致性需求权衡选择。


MVCC（多版本并发控制）通过以下机制避免锁竞争：
1. 核心原理：数据多版本

    写操作不覆盖旧数据：每次修改数据时，MVCC 会生成该数据的新版本（新行），旧版本仍保留。

    读操作访问快照：事务读取数据时，基于事务开始的时刻，选择可见的版本（由事务ID决定），而非直接读取最新数据。

2. 关键实现机制
a. 事务 ID（XID）

    每个事务分配唯一 ID（如 xmin 和 xmax）。

    数据行记录版本信息：

        xmin：创建该行的事务 ID。

        xmax：删除/更新该行的事务 ID（初始为 NULL）。

b. 可见性规则

    事务只能看到满足以下条件的行：

        该行 xmin < 当前事务 ID，且 xmax 未提交或大于当前事务 ID。

    示例：
    plaintext
    Copy

    事务 A（XID=100）插入一行 → xmin=100, xmax=NULL  
    事务 B（XID=101）更新该行 → 原行 xmax=101，新行 xmin=101  
    事务 C（XID=102）读取时：
      - 原行对 C 不可见（xmax=101 < 102 且已提交）
      - 新行可见（xmin=101 < 102）

c. 快照隔离（Snapshot Isolation）

    事务启动时获取数据快照，后续操作基于此快照执行，不受其他事务的写入影响。

3. 如何避免锁竞争？
a. 读操作不阻塞写操作

    读操作访问旧版本数据，无需加锁。

    写操作生成新版本，不阻塞正在进行的读操作。

b. 写操作间的最小化锁竞争

    行级锁：仅对当前修改的行加锁（如 FOR UPDATE），而非整个表。

    无读锁：其他事务仍可读取旧版本数据，无需等待锁释放。

c. 乐观并发控制

    事务提交时检查冲突（如更新同一行），而非在修改时立即加锁。

4. MVCC 的优势

    高并发：读多写少场景下性能显著提升。

    避免死锁：减少锁的持有时间和范围。

    一致性视图：事务始终看到一致的快照，无需关心其他事务的中间状态。

5. 副作用与解决方案

    版本膨胀：旧版本数据堆积 → 通过 VACUUM 清理过期版本。

    事务 ID 回卷：XID 耗尽 → PostgreSQL 使用冻结（Freeze）机制处理。

示例场景

    事务 A 更新行：生成新版本，原行标记为失效。

    事务 B 同时读取该行：读取未失效的旧版本，无需等待事务 A 提交。

    事务 A 提交后：新版本对其他事务可见，旧版本由 VACUUM 清理。

总结

MVCC 通过维护数据多版本和快照隔离，使读操作无需锁、写操作最小化锁范围，从而避免传统锁机制中的竞争问题。它是 PostgreSQL、MySQL InnoDB 等数据库实现高并发的核心机制。