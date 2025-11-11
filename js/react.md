# React 复习大纲（2025 版）

按「面试必问 → 项目必用 → 源码必懂」三层递进，每点都给出「是什么-为什么-怎么用-易错点」四步解析，可直接当作 check-list 使用。

---

## 1. 组件设计核心

| 重点                  | 解析（4W1H）                                                                                                                                                                                 |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **函数组件 + Hooks** 优先 | 什么是：纯函数 `({props}) =&gt; UI`；&lt;br&gt;为什么：Tree-Shaking 更好、逻辑复用更轻、未来 Concurrent 特性只支持函数组件；&lt;br&gt;怎么用：默认写 FC，除非强依赖生命周期才用 class；&lt;br&gt;易错：在 FC 里写 `let a = 0` 每次渲染重置，必须用 `useState`。 |
| **单一数据源 & 单向数据流**   | 父 → 子只通过 props；子 → 父只通过 callback；兄弟节点通过最近公共祖先上升状态。杜绝“双向绑定”带来的隐式更新。                                                                                                                       |
| **UI = f(state)**   | 拒绝直接 DOM 操作；所有视觉变化必须落账到 state，再驱动 React 渲染。                                                                                                                                              |

---

## 2. 状态管理

| 重点                          | 解析                                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------------------- |
| **useState**                | 异步批量更新：`setCount(c =&gt; c+1)` 用函数式避免闭包旧值；&lt;br&gt;惰性初始：`useState(() =&gt; expensive())` 只执行一次。        |
| **useReducer**              | 适合“下一状态依赖上一状态”或“多子值”场景，如表单、购物车；可配合 `useContext` 做轻量全局状态。                                                |
| **useRef**                  | `.current` 不触发渲染，常用于“保存任意可变值”或“引用 DOM”；区别于 `useState` 不会导致重渲染。                                          |
| **状态提升 & 组合**               | 两个兄弟组件共享数据 → 找到最近公共父节点提升；优于盲目上 Redux。                                                                   |
| **Redux / Zustand / Jotai** | 项目级再考虑：Redux（时间旅行、中间件）、Zustand（轻量）、Jotai（原子化）；小项目用 Context + useReducer 即可。 |

---

## 3. 副作用与生命周期

| 重点                  | 解析                                                                                                                                                 |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **useEffect**       | 模拟 `componentDidMount / Update / Unmount`；&lt;br&gt;依赖数组 `[]` 仅执行一次；无数组则每次渲染后都执行；&lt;br&gt;清理函数 `return () =&gt; {}` 在组件卸载或依赖变化前执行，防止内存泄漏（定时器、订阅）。 |
| **useLayoutEffect** | 同步执行，DOM 变更后、浏览器绘制前触发；用于测量 DOM 布局（如 tooltip 定位），避免闪烁。                                                                                              |
| **事件绑定与清理**         | `useEffect(() =&gt; { window.addEventListener(...); return () =&gt; removeListener(...); }, []);`                                                  |

---

## 4. 性能优化

| 重点                        | 解析                                                                                                          |
| ------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **React.memo**            | 默认浅比较 props；可自定义比较函数；&lt;br&gt;配合“稳定回调”使用：`useCallback` + `useMemo`。                                        |
| **useCallback / useMemo** | 缓存“函数”与“计算值”；依赖变化才重建；&lt;br&gt;不要过度包裹，缓存成本 &gt; 重渲染成本 就亏。                                                   |
| **key 的作用**               | 同级数组兄弟节点标识身份，用于 Diff；&lt;br&gt;禁止用数组下标，会导致输入框错位、动画异常；&lt;br&gt;列表唯一 ID 最好来自后端主键。                            |
| **虚拟化**                   | 长列表用 `react-window` / `react-virtualized`，只渲染可视区，减少 DOM 节点。                                                 |
| **Code-Splitting**        | `lazy(() =&gt; import('./Page'))` + `&lt;Suspense fallback={&lt;Loading /&gt;}&gt;`；按路由或组件维度拆包，首屏加载体积↓30%+。 |

---

## 5. Hooks 深入

| 重点           | 解析                                                                                                               |
| ------------ | ---------------------------------------------------------------------------------------------------------------- |
| **自定义 Hook** | 以 `use` 开头，内部可调用其他 Hook；本质是“状态逻辑复用”，非 UI 复用；&lt;br&gt;例：`useDebounce`、`useInterval`、`useLocalStorage`。           |
| **Hook 规则**  | 1. 只在顶层调用，禁止在循环/条件/嵌套函数中；&lt;br&gt;2. 只在 React 函数或自定义 Hook 中调用；&lt;br&gt;eslint-plugin-react-hooks 自动校验。         |
| **闭包陷阱**     | `setInterval(() =&gt; console.log(count), 1000)` 打印永远是初始值；&lt;br&gt;解决：用 `setCount(c =&gt; c+1)` 或把 count 放 ref。 |

---

## 6. 组件通信模式

| 场景   | 方案                                                                                                    |
| ---- | ----------------------------------------------------------------------------------------------------- |
| 父子   | props + callback                                                                                      |
| 跨层   | Context（小）、Redux/Zustand（大）                                                                           |
| 插槽   | `props.children` 或 Render Props：`&lt;Mouse&gt;{mouse =&gt; &lt;Cat mouse={mouse}/&gt;}&lt;/Mouse&gt;` |
| 事件总线 | 不推荐，难追踪；用订阅发布库（mitt）也要谨慎卸载。                                                                           |

---

## 7. 路由（React-Router v6）

| 重点                | 解析                                                                                       |
| ----------------- | ---------------------------------------------------------------------------------------- |
| **声明式**           | `&lt;Routes&gt;&lt;Route path="/user/:id" element={&lt;User /&gt;} /&gt;&lt;/Routes&gt;` |
| **嵌套路由**          | Outlet 占位，父路由布局复用；URL 与组件树同构。                                                            |
| **Loader + lazy** | 路由级数据预取：`loader={() =&gt; fetchUser()}`，配合 `lazy()` 实现“边载边取”。                            |
| **导航守卫**          | 用 `useNavigate` + 自定义 `AuthRoute` 高阶组件：未登录跳转 `/login?redirect=xxx`。                      |

---

## 8. 错误处理

| 重点                 | 解析                                                                                                                                                    |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Error Boundary** | class 组件实现 `componentDidCatch` / `static getDerivedStateFromError`；&lt;br&gt;函数组件暂未支持，可用第三方 `react-error-boundary`；&lt;br&gt;只捕获渲染阶段错误，不捕获事件处理器/异步代码。 |
| **全局监控**           | 结合 Sentry：`Sentry.captureException(error, {extra: state})`。                                                                                           |

---

## 9. 测试

| 重点                              | 解析                                                                           |
| ------------------------------- | ---------------------------------------------------------------------------- |
| **RTL (React Testing Library)** | 测试行为而非实现：`getByRole`, `getByLabelText`；&lt;br&gt;避免查询 DOM 结构细节，重构不 break 用例。 |
| **Mock 钩子**                     | `jest.mock('axios')` 或 `msw` 拦截网络；&lt;br&gt;用 `renderHook` 测自定义 Hook。        |
| **覆盖率阈值**                       | 业务核心 ≥80%，工具函数 ≥90%；警惕“为盖而盖”。                                                |

---

## 10. 并发与未来特性

| 重点                    | 解析                                                                                                     |
| --------------------- | ------------------------------------------------------------------------------------------------------ |
| **Concurrent Mode**   | 可中断渲染，保证高优更新（打字、动画）不掉帧；&lt;br&gt;开启：`createRoot(root).render(&lt;App /&gt;)`。                          |
| **useTransition**     | 标记“低优更新”：`startTransition(() =&gt; setFilter(text))`；输入框即时响应，列表异步过滤。                                   |
| **useDeferredValue**  | 延迟渲染版本：`const deferredQuery = useDeferredValue(query)`；&lt;br&gt;比 transition 更细粒度，适合第三方库不可控 setState。 |
| **Suspense for Data** | 组件级“等数据”声明：`const data = use(fetcher)`；&lt;br&gt;与 Error Boundary 组合，完成“加载中-错误-正常”三态。                  |

---

## 11. 常见踩坑速查表

| 踩坑                    | 正确姿势                                            |
| --------------------- | ----------------------------------------------- |
| `setState` 后立刻读 state | 用函数式更新或 `useEffect` 监听                          |
| 在 `useEffect` 里不写依赖   | eslint 警告必须处理，要么加依赖，要么加注释解释                     |
| 把对象直接作为依赖             | 每次渲染都是新对象 → 无限循环；用 `useDeepCompareEffect` 或拆原始值 |
| 事件监听未清理               | 内存泄漏，组件卸载前 `removeEventListener`                |
| 把 `ref.current` 当依赖   | ref 变化不会触发 useEffect，需用 callback ref 模式         |

---

## 12. 复习路线（7 天速成）

| 天数   | 任务                             | 产出                         |
| ---- | ------------------------------ | -------------------------- |
| Day1 | 写 10 个常用 Hook 的小 demo          | CodePen 合集                 |
| Day2 | 用 Vite 起项目，实现 TodoMVC          | 状态提升、localStorage 持久化      |
| Day3 | 加路由 + 分页 + 骨架屏                 | Code-Splitting、Suspense    |
| Day4 | 性能调优：memo、useCallback、虚拟列表     | React DevTools Profiler 截图 |
| Day5 | 接入 Redux-Toolkit，写异步 Thunk     | 时间旅行调试                     |
| Day6 | 写 Error Boundary + 测试用例        | RTL 覆盖率报告                  |
| Day7 | 读源码：Hooks 链表、Fiber 双缓冲、Diff 策略 | 输出 3 篇笔记                   |

&gt; 把以上大纲打印出来，每掌握一条就在纸上打钩，全部勾完 React 面试/开发稳过。
