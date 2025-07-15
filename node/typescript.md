一、基础类型

    原始类型

        string、number、boolean、null、undefined、symbol、bigint。
    typescript
    Copy

    let name: string = "Alice";
    let age: number = 30;

    数组与元组

        数组：number[] 或 Array<number>。

        元组：固定类型和长度的数组。
    typescript
    Copy

    let list: [string, number] = ["Alice", 30];

    枚举（Enum）

        用于定义具名常量集合。
    typescript
    Copy

    enum Direction { Up, Down, Left, Right }

    特殊类型

        any：禁用类型检查。

        unknown：安全的 any，需类型断言后使用。

        void：表示函数无返回值。

        never：表示永不返回的函数（如抛出异常）。

二、高级类型

    联合类型与交叉类型

        联合类型：string | number。

        交叉类型：A & B（合并多个类型的属性）。

    类型别名与接口

        类型别名：type Point = { x: number; y: number }。

        接口：interface Point { x: number; y: number }。

        区别：接口可合并声明，类型别名支持联合/交叉类型。

    泛型

        用于创建可复用的组件。
    typescript
    Copy

    function identity<T>(arg: T): T { return arg; }

    实用类型

        Partial<T>：所有属性变为可选。

        Readonly<T>：所有属性变为只读。

        Pick<T, K>：选择部分属性。

        Record<K, T>：定义键值类型。

    条件类型与映射类型

        条件类型：T extends U ? X : Y。

        映射类型：{ [P in K]: T }。
    typescript
    Copy

    type Optional<T> = { [P in keyof T]?: T[P] };

三、面向对象编程

    类与继承

        类成员访问修饰符：public、private、protected。
    typescript
    Copy

    class Animal {
      constructor(public name: string) {}
      move() { console.log("Moving"); }
    }

    抽象类

        定义抽象方法，需子类实现。
    typescript
    Copy

    abstract class Shape {
      abstract getArea(): number;
    }

    接口实现

        类可实现多个接口。
    typescript
    Copy

    interface Flyable { fly(): void; }
    class Bird implements Flyable { fly() { /* ... */ } }

    装饰器

        用于附加元数据或修改类/方法行为（需启用 experimentalDecorators）。
    typescript
    Copy

    function log(target: any, key: string) {
      console.log(`Method ${key} called`);
    }
    class MyClass { @log myMethod() {} }

四、模块与命名空间

    ES 模块

        导入/导出语法：
    typescript
    Copy

    import { Component } from 'react';
    export const name = "Alice";

    命名空间

        旧有模块化方案，现推荐使用 ES 模块。
    typescript
    Copy

    namespace MathUtils {
      export function add(a: number, b: number) { return a + b; }
    }

    声明文件（.d.ts）

        为第三方库或全局变量提供类型定义。
    typescript
    Copy

    declare module "jquery" { /* ... */ }

五、工具与配置

    tsconfig.json 配置

        关键配置项：
        json
        Copy

        {
          "compilerOptions": {
            "target": "ES6",
            "module": "CommonJS",
            "strict": true,
            "outDir": "./dist"
          }
        }

    类型推断与断言

        类型推断：自动推导变量类型（如 let x = 10 推断为 number）。

        类型断言：value as string 或 <string>value。

    类型守卫

        使用 typeof、instanceof 或自定义类型谓词。
    typescript
    Copy

    function isString(value: any): value is string {
      return typeof value === "string";
    }

六、最佳实践

    避免 any

        优先使用 unknown 或明确类型。

    精确类型定义

        使用联合类型替代 any，如 string | number。

    合理使用类型断言

        仅在明确类型时使用，避免滥用。

    第三方库类型支持

        通过 @types/包名 安装类型定义（如 npm install @types/react）。

七、常见问题与解决方案

    类型不匹配错误

        检查变量赋值和函数参数类型是否一致。

    声明文件缺失

        使用 declare 临时定义或安装 @types 包。

    装饰器不生效

        确保 tsconfig.json 中启用 experimentalDecorators。