一、.NET基础核心概念

    CLR与CTS/CLS
        CLR(公共语言运行时):负责代码执行、内存管理(GC)、异常处理。
        CTS(通用类型系统):定义所有.NET语言共享的类型规范。
        CLS(公共语言规范):确保多语言互操作性。

        提到此基础问题的高频性。

    内存管理与垃圾回收(GC)
        托管堆与栈的区别。
        IDisposable接口与using语句(释放非托管资源):关键考察点,需结合Dispose()方法的实现说明。

    C#语言特性
        async/await异步编程模型。
        LINQ、Lambda表达式。
        值类型与引用类型(装箱/拆箱效率问题)。

    .NET Core与Framework区别
        跨平台能力、性能优化、依赖注入原生支持。
        例如:.NET Core中间件管道与.NET Framework的HTTP模块/处理器区别。

二、单元测试与NUnit

    NUnit框架要点
        断言方法:Assert.AreEqual(), Assert.IsTrue(), Assert.Throws()等。
        测试生命周期属性:
            [TestFixture]:标记测试类。
            [Test], [SetUp], [TearDown], [OneTimeSetUp].
        参数化测试:用[TestCase]传递多组输入参数。

    单元测试最佳实践
        AAA模式(Arrange-Act-Assert)。
        Mocking框架(如Moq)用于隔离依赖。
        测试覆盖率标准与意义(如

        工具)。

三、进阶与架构设计

    设计模式
        依赖注入(DI)、工厂模式、单例模式。
        ASP.NET Core内置DI容器使用方法(Startup.ConfigureServices)。

    ASP.NET Core核心机制
        中间件(Middleware)管道与请求处理。
        路由配置(约定路由vs特性路由)。
        EF Core的延迟加载与跟踪机制差异。

    性能优化
        缓存策略(内存缓存、分布式缓存)。
        Span<T>与Memory<T>的高效内存操作。

四、高频面试题示例

    差异性比较类
        string与String的区别?

            github.com示例作答

        :string是C#关键字(System.String别名),推荐用于声明变量,String用于静态方法调用(如String.IsNullOrEmpty())。

场景分析类

    如何诊断内存泄漏?

        工具推荐:dotnet-counters, dotnet-dump, Visual Studio内存分析器。

NUnit实战代码

    [TestFixture]
    public class CalculatorTests {
        private Calculator _calculator;

        [SetUp]
        public void Setup() => _calculator = new Calculator();

        [TestCase(3, 5, 8)]
        public void Add_ShouldReturnCorrectSum(int a, int b, int expected) {
            var result = _calculator.Add(a, b);
            Assert.That(result, Is.EqualTo(expected));
        }
    }

五、资源推荐

    GitHub实战题库:aershov24/net-core-interview-questions

包含完整代码示例。
模拟面试路径:dotnettricks.com

    提供结构化学习路径。

建议结合自身项目经验,通过具体案例(如性能优化、BUG修复)体现技术深度。