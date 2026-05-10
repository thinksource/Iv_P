1. NumPy：高性能计算基石

面试考察重点：向量化运算 (Vectorization) 和 广播机制 (Broadcasting)。

🧠 知识点结构

    核心对象 (ndarray)

        属性：.shape, .dtype, .ndim。

        创建：np.array, np.zeros, np.arange, np.linspace。

    索引与切片 (Indexing & Slicing)

        基础切片：arr[0:5]。

        布尔索引 (Boolean Indexing): arr[arr > 0] (非常常用)。

        花式索引 (Fancy Indexing): 使用整数数组进行索引。

    数学运算

        广播机制 (Broadcasting): 这里的核心是不同形状数组如何自动对齐进行运算。

        聚合函数：sum, mean, std, min, max (注意 axis 参数)。

    线性代数 (np.linalg)

        矩阵乘法：np.dot 或 @。

        特征值/特征向量，SVD 分解。

💻 常用案例与代码

案例 A: 广播机制 (Broadcasting) - 必考 面试官常问：如何将一个向量加到矩阵的每一行上？
Python

import numpy as np

# 3x3 矩阵
matrix = np.array([[1, 2, 3], 
                   [4, 5, 6], 
                   [7, 8, 9]])
# 1x3 向量
vector = np.array([1, 0, 1])

# 广播机制：vector 自动扩展应用到 matrix 的每一行
result = matrix + vector 
# [1+1, 2+0, 3+1] -> [2, 2, 4]
# ...

print(result)

案例 B: 快速筛选 (Boolean Masking) 数据清洗常用，比 Python 循环快几百倍。
Python

data = np.array([10, -5, 30, -2, 50])
# 将所有负数替换为 0 (Relu 激活函数原理)
data[data < 0] = 0
print(data) # [10, 0, 30, 0, 50]

2. SciPy：科学计算工具箱

面试考察重点：统计 (stats), 优化 (optimize) 和 稀疏矩阵 (sparse)。

🧠 知识点结构 (按 DS 面试重要性排序)

    scipy.stats (统计模块 - 最重要)

        概率分布：norm (正态), binom (二项), poisson (泊松)。

        假设检验：ttest_ind (T检验), chisquare (卡方检验), ks_2samp。

    scipy.optimize (优化模块)

        最小化函数：minimize (用于寻找损失函数最小值)。

        曲线拟合：curve_fit (将数据拟合到特定函数模型)。

    scipy.sparse (稀疏矩阵)

        处理大部分元素为 0 的巨型矩阵（NLP、推荐系统必备）。

        格式：CSR (Compressed Sparse Row), CSC。

    scipy.linalg

        比 numpy.linalg 更全面、更快的线性代数操作。