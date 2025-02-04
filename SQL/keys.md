## SQL 通用知识
1. 基础语法

    DDL（数据定义语言）

        CREATE TABLE / ALTER TABLE / DROP TABLE

        数据类型（INT, VARCHAR, DATE, BOOLEAN 等）

        约束（PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL, CHECK）

    DML（数据操作语言）

        INSERT / UPDATE / DELETE

        事务控制（BEGIN, COMMIT, ROLLBACK, SAVEPOINT）

    DQL（数据查询语言）

        SELECT 基础（FROM, WHERE, GROUP BY, HAVING, ORDER BY）

        别名（AS）、去重（DISTINCT）、条件逻辑（CASE WHEN）

2. 查询进阶

    聚合函数

        SUM, AVG, COUNT, MIN, MAX

        GROUP BY 分组与 HAVING 过滤

    多表连接

        INNER JOIN / LEFT JOIN / RIGHT JOIN / FULL OUTER JOIN

        自连接（Self-Join）、交叉连接（CROSS JOIN）

    子查询与 CTE

        标量子查询、行子查询、EXISTS / NOT EXISTS

        公共表表达式（WITH ... AS ...）

3. 高级功能

    窗口函数

        ROW_NUMBER(), RANK(), DENSE_RANK(), NTILE()

        LAG(), LEAD(), FIRST_VALUE(), LAST_VALUE()

        OVER 子句（PARTITION BY, ORDER BY, ROWS/RANGE）

    递归查询

        WITH RECURSIVE 处理层次结构（如树形数据）

    JSON 处理

        JSON / JSONB 类型操作符（->, ->>, #>）

        函数：jsonb_set, jsonb_array_elements