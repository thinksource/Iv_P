# 面试高频考点


1. 动态类型与静态类型的本质区别是什么？

    类型绑定时机（运行时 vs 编译时）

2. 动态类型的优缺点如何权衡？

    适合快速迭代 vs 大型项目维护成本

3. Python的类型提示（Type Hints）是否改变了动态类型特性？

```python

def greeting(name: str) -> str:  # 仅是提示，不强制检查
    return "Hello " + name
```