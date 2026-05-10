import numpy

# 1. Read N (rows) and M (columns)
n, m, p= map(int, input().split())
matrix1 = numpy.array([input().split() for _ in range(n)], int)
matrix2 = numpy.array([input().split() for _ in range(m)], int)
print(numpy.concatenate((matrix1, matrix2)))