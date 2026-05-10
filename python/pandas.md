# Pandas 数据导入：read_csv（重点）

| 功能     | 方法                                             |
| ------ | ---------------------------------------------- |
| 读 CSV  | `pd.read_csv("file.csv")`                      |
| 编码     | `encoding="utf-8"` / `"gbk"` / `"utf-8-sig"`   |
| 选列     | `usecols=[...]`                                |
| 指定类型   | `dtype={...}`                                  |
| 解析日期   | `parse_dates=[...]`                            |
| 导出 CSV | `to_csv(..., encoding="utf-8-sig")`            |
| 写数据库   | `df.to_sql(table, engine, if_exists="append")` |
| 避免乱码   | CSV 用 `"utf-8-sig"`                            |

## pandas 数据重塑全流程思维导图

Pandas 数据重塑 (Reshaping)
│
├── ① 形状改变（长 ↔ 宽）
│     │
│     ├── 宽 → 长
│     │     ├── melt()
│     │     ├── stack()
│     │     ├── wide_to_long()
│     │     └── json_normalize()（嵌套 JSON）
│     │
│     ├── 长 → 宽
│     │     ├── pivot()
│     │     ├── pivot_table()
│     │     ├── unstack()
│     │     └── groupby().unstack()
│     │
│     └── 行列互换
│           └── transpose() / T
│
├── ② 多级索引（MultiIndex）重塑
│     │
│     ├── 创建多级索引
│     │     ├── set_index()
│     │     ├── groupby()
│     │     └── pivot / pivot_table 产生的列层级
│     │
│     ├── 修改层级结构
│     │     ├── swaplevel()
│     │     └── reorder_levels()
│     │
│     ├── 重排索引
│     │     ├── sort_index()
│     │     └── reindex()
│     │
│     └── 展开索引
│           └── reset_index()
│
├── ③ 表格拆分与合并
│     │
│     ├── 合并 Merge
│     │     ├── merge()（SQL 风格 join）
│     │     └── join()
│     │
│     ├── 堆叠/拼接 Concatenate
│     │     ├── concat(axis=0) 行拼
│     │     └── concat(axis=1) 列拼
│     │
│     └── 拆列/新增列
│           ├── str.split(expand=True)
│           ├── assign()
│           └── DataFrame.apply()
│
├── ④ 时间序列重塑
│     │
│     ├── 重采样（频率改变）
│     │     └── resample('M').sum()
│     │
│     ├── 时间窗口
│     │     └── rolling().mean()
│     │
│     └── 移位
│           └── shift()
│
├── ⑤ 分组后的重塑
│     │
│     ├── 聚合
│     │     └── groupby().agg()
│     │
│     ├── 转回等长（对齐原数据）
│     │     └── groupby().transform()
│     │
│     └── pivot-like 操作
│           └── groupby(['A','B'])['value'].sum().unstack()
│
└── ⑥ 变量重塑（数值 → 分箱分类）
      │
      ├── cut()    （等宽区间）
      ├── qcut()   （等人数区间）
      └── astype('category')
