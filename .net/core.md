以下是一份结构化的 .NET Core 知识体系总结,涵盖核心概念、关键特性和高频面试考察点,结合最新.NET 8特性和实际开发场景:
一、.NET Core 基础架构

    跨平台机制
        支持Windows/Linux/macOS的运行时(CoreCLR)。
        独立部署 (Self-contained) vs 框架依赖部署 (Framework-dependent)。
        发布和修剪 (Publish Trimmed):减少部署包大小的原理与注意事项(反射可能被裁剪的问题)。

    运行环境与启动机制
        Program.cs中的 HostBuilder 和 WebApplication(推荐模板)。
        Startup类的演变(在.NET 6+中是否必须?)。
        配置源优先级:环境变量 > 命令行 > appsettings.{Environment}.json > appsettings.json。

    依赖注入 (DI)
        Service Lifetime:Singleton、Scoped、Transient的作用域差异。
        服务注册方法:AddSingleton<>()、AddScoped<>()、TryAdd()。
        解决循环依赖的常见方式(重构代码或使用IServiceProvider延迟解析)。
        选项模式 (Options Pattern):通过IOptions<T>绑定配置。

二、ASP.NET Core 核心组件

    中间件 (Middleware)
        请求管道 (Use, Run, Map) 的执行顺序非常重要,例如:

    app.UseMiddleware<CustomMiddleware>();
    app.UseAuthentication();
    app.UseAuthorization();

    终结点路由 (UseEndpoints) 与 最小API(.NET 6+特性,MapGet(), MapPost())。

模型绑定与验证

    [FromBody], [FromQuery] 等属性指定数据来源。
    FluentValidation 或 DataAnnotations 实现模型验证:

        public class User
        {
            [Required(ErrorMessage = "Name is required")]
            public string Name { get; set; }
        }

    Web API 进阶
        版本控制策略(URL路径、Header、QueryString)。
        Swagger/OpenAPI集成(Swashbuckle.AspNetCore包)。
        响应缓存 (ResponseCacheAttribute) 与输出缓存(.NET 7+的OutputCache)。

三、数据访问与 ORM

    Entity Framework Core
        Code First vs Database First 选择场景。
        导航属性的 延迟加载 (Lazy Loading) 与 显式加载 (Explicit Loading)。
        事务管理:

        using var transaction = context.Database.BeginTransaction();
        try 
        {
            // 操作1
            // 操作2
            transaction.Commit();
        }
        catch 
        {
            transaction.Rollback();
        }

        DbContext池化:通过AddDbContextPool优化性能。

    Dapper 高性能访问
        与EF Core对比的优势(轻量、原生SQL、高性能)。
        多结果集查询 (QueryMultiple)。
        参数化查询防止SQL注入。

    Repository 与 UnitOfWork 模式
        如何抽象数据访问层(实现领域驱动设计)。
        潜在的陷阱(过度抽象导致代码复杂化)。

四、性能优化与诊断

    高性能技巧
        Span<T> 和 Memory<T>:无需分配堆内存的切片操作。
        StringBuilder vs StringInterpolation:大量拼接时选择前者。
        ValueTask 取代 Task:避免不必要的堆分配。

    缓存策略
        内存缓存 (IMemoryCache)与分布式缓存 (IDistributedCache):Redis实现方案。
        缓存击穿/雪崩解决方案:锁机制、随机过期时间。

    诊断工具
        dotnet-counters:实时监控GC、CPU等指标。
        dotnet-dump 分析内存泄漏。
        MiniProfiler:性能热点定位。

五、测试驱动开发 (TDD) 与 NUnit 深入

    NUnit 进阶用法
        [TestCase] 参数化测试与动态数据源 ([TestCaseSource])。
        测试套件组织 ([Category], [Explicit])。
        并发测试控制 ([NonParallelizable])。

    Mocking 与依赖隔离
        使用 Moq:

        var mockService = new Mock<IService>();
        mockService.Setup(s => s.GetData()).Returns("mocked data");

        Stubs vs Mocks:理解二者差异(验证行为 vs 提供预设值)。

    集成测试
        使用 WebApplicationFactory 模拟ASP.NET Core环境。
        数据库测试的常用方法(使用内存数据库如SQLite)。

六、.NET Core 高级主题

    微服务架构
        服务间通信(gRPC、HTTP API、消息队列如RabbitMQ)。
        健康检查 (AddHealthChecks()) 与 服务发现。

    安全性
        身份认证(JWT Bearer、OpenID Connect)。
        角色与策略授权 ([Authorize(Roles = "Admin")])。
        防跨站请求伪造 (CSRF) 保护机制。

    并发与异步
        Task.WhenAll() 批量异步操作。
        避免 async void(仅用于事件处理器)。
        SemaphoreSlim 控制资源并发访问。

七、高频 .NET Core 面试题

    GC 如何工作?分代回收有哪几代?如何手动触发GC?

        答:分代回收(Gen 0,1,2),新对象在Gen0,幸存后晋升。手动调用GC.Collect()但不推荐。

    ConfigureServices和Configure方法分别在何时调用?

        答:ConfigureServices注册服务,Configure构建中间件管道。

    Hosting Model 中IHost、IWebHost的区别?

        答:.NET 6以后统一为WebApplication,旧版中IWebHost专用于Web应用。

    如何跨中间件传递数据?

        答:使用HttpContext.Items字典或自定义中间件封装扩展方法。

八、扩展学习资源

    官方文档
        Microsoft Learn

.NET Core 性能指南  

GitHub 项目

    .NET Core基本知识点示例 https://github.com/zdz72113/NETCore_BasicKnowledge.Examples

(包含代码案例)
aspnetcore-examples

        (实际场景演示)

建议结合实践搭建项目(如电商API服务),遇到问题时深入源码(如ASP.NET Core GitHub仓库
),并积极参与.NET社区讨论。