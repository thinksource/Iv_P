# Vue 3 复习大纲（2025 版）

&gt; 按“面试必问 → 项目必用 → 源码进阶”三级递进，每点给出「是什么-为什么-怎么用-易错点」四步解析，可打印成 check-list。

---

## 1. 创建与启动

| 重点            | 解析（4W1H）                                                                                                                                      |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **createApp** | 什么是：新的工厂函数，返回应用实例；&lt;br&gt;为什么：解决 Vue2 全局构造函数污染；&lt;br&gt;怎么用：`createApp(App).use(router).mount('#app')`；&lt;br&gt;易错：仍然写 `new Vue()` 会直接报错。 |
| **Teleport**  | 模板里写 `&lt;teleport to="body"&gt;` 可把 DOM 搬到任意位置，常用于 Modal、Toast，避免 z-index 嵌套地狱。                                                              |
| **Fragments** | 组件不再要求单一根节点，可返回同级多标签，减少无意义 wrapper。                                                                                                           |

---

## 2. 响应式核心

| 重点                          | 解析                                                                                                                                         |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **Proxy 替代 defineProperty** | 可监听新增/删除属性、数组下标、Map/Set；初始化递归→运行时懒追踪，性能↑；&lt;br&gt;Reflect 保证 this 指向正确。                                                                   |
| **ref vs reactive**         | `ref` 包装基本类型，访问需 `.value`；`reactive` 只接受对象；嵌套引用时自动解包；&lt;br&gt;泛型场景用 `Ref&lt;T&gt;` 保证类型。                                                  |
| **toRef / toRefs**          | 解构不丢响应式：`const { name } = toRefs(obj)`；`toRef` 可做「可选属性」安全代理。                                                                               |
| **computed & watch**        | `computed` 懒计算且缓存；`watch` 可监 ref、getter、数组，支持 `flush: 'post'` 在 DOM 更新后触发；&lt;br&gt;异步用 `watchEffect`（立即执行一次）。 |
| **shallowRef / triggerRef** | 对“大对象/第三方类”做性能优化，手动 `triggerRef` 触发视图更新。                                                                                                   |

---

## 3. 组合式 API（重点）

| 重点                                     | 解析                                                                                                    |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **setup 语法糖 `&lt;script setup&gt;`**   | 编译期隐式返回顶层绑定，无需 `return {}`；可写 await，自动生成 async setup；与普通 `&lt;script&gt;` 共存解决部分选项式需求。                |
| **生命周期**                               | `onBeforeMount / onMounted / onUnmounted` 等；&lt;br&gt;Vue2 的 `beforeCreate/created` 被 `setup()` 本身替代。 |
| **provide / inject**                   | 跨多级组件传值；可传 ref 保持响应式；配合 `InjectionKey&lt;T&gt;` 做类型安全。                                                |
| **customRef**                          | 手动控制追踪与触发，做防抖输入框：`useDebouncedRef(value, delay)`。                                                     |
| **useCssModule / useSlots / useAttrs** | 在 `&lt;script setup&gt;` 获取 `slots`、`attrs`、`css module`，避免未声明报错。                                     |

---

## 4. 组件通信速查表

| 场景   | 方案                                                    |
| ---- | ----------------------------------------------------- |
| 父子   | `props + emit（defineEmits）`                           |
| 双向绑定 | `v-model:foo` 对应 `modelValue + update:modelValue`；可多个 |
| 深层   | `provide/inject`                                      |
| 事件总线 | 移除 `$on/$off`；推荐 `mitt` 或 `useEventBus` 自建            |
| 全局常量 | `app.config.globalProperties` + TS 模块扩充声明             |

---

## 5. 性能优化

| 重点                               | 解析                                                                                                                    |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **v-memo**                       | 模板级缓存：`&lt;div v-memo="[value]"&gt;` 数组不变跳过 Diff；列表渲染利器。                                                              |
| **shallowReactive / shallowRef** | 大对象、第三方库实例（ECharts、Mapbox）只监顶层，避免深递归。                                                                                 |
| **defineAsyncComponent**         | 异步组件：`const Foo = defineAsyncComponent(() =&gt; import('./Foo.vue'))`；可配 `loadingComponent`、`delay`、`errorComponent`。 |
| **v-once / v-pre**               | 静态内容直接跳过编译/更新；博客、Markdown 渲染常用。                                                                                       |
| **keep-alive**                   | 缓存组件实例，可配 `include / exclude / max`；切换标签页不丢表单。                                                                        |

---

## 6. 路由（Vue Router 4）

| 重点                       | 解析                                                                                                                            |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| **createRouter**         | 历史模式：`createWebHistory()`；hash 模式：`createWebHashHistory()`；&lt;br&gt;路由表扁平，不再嵌套 `*` 通配符。                                      |
| **路由守卫**                 | 全局 `beforeEach`；组件内 `onBeforeRouteLeave / onBeforeRouteUpdate`（组合式）；&lt;br&gt;路由独享 `beforeEnter`；可返回 `false` 或 `'/login'` 拦截。 |
| **useRouter / useRoute** | 在 `&lt;script setup&gt;` 直接获取实例与当前路由；`route.params / query` 均为响应式 ref。                                                        |
| **动态路由**                 | `addRoute(parentName, route)` 做权限菜单；`removeRoute` 热卸载。                                                                        |

---

## 7. 状态管理

| 重点              | 解析                                                                                               |
| --------------- | ------------------------------------------------------------------------------------------------ |
| **Pinia**       | 官方替代 Vuex；`defineStore('id', () =&gt; {})` 返回组合式函数；&lt;br&gt;无需 modules 嵌套，天然 TS 推断；热更新 HMR 免配置。 |
| **storeToRefs** | 解构不丢响应式：`const { count } = storeToRefs(useMainStore())`；方法直接解构即可。                                |
| **全局与局部**       | 小范围 `provide/inject`；跨模块/页面再抬到 Pinia；避免“一上手就全局”。                                                 |

---

## 8. 语法糖 & 新特性

| 重点                 | 解析                                                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------------------------------ |
| **defineOptions**  | 在 `&lt;script setup&gt;` 里写 `name / inheritAttrs / expose` 等选项；无需再开普通 `&lt;script&gt;`。                            |
| **defineExpose**   | 暴露子组件内部 ref 给父组件调用；配合 `useTemplateRef` 类型安全。                                                                       |
| **useTemplateRef** | Vue3.5+ 新 API：`const canvas = useTemplateRef&lt;'canvas'&gt;()` 自动推导元素类型。                                          |
| **defineModel**    | Vue3.4+ 简化双向绑定：`const model = defineModel&lt;string&gt;()` 直接读写；等价 `props.modelValue + emit('update:modelValue')`。 |

---

## 9. TypeScript

| 重点                  | 解析                                                                                                             |
| ------------------- | -------------------------------------------------------------------------------------------------------------- |
| **defineComponent** | 给选项式组件提供类型推断；`&lt;script setup&gt;` 已自动推导，可省。                                                                  |
| **props 泛型**        | `defineProps&lt;{ title: string }&gt;()` 直接接口；带默认值用 `withDefaults(defineProps&lt;...&gt;(), { title: 'hi' })`。 |
| **emits 类型**        | `defineEmits&lt;{ change: [id: number] }&gt;()` 元组语法限定参数。                                                      |
| **全局增强**            | `declare module '@vue/runtime-core' { interface ComponentCustomProperties { $http: AxiosInstance } }`          |

---

## 10. 测试

| 重点                   | 解析                                                                                 |
| -------------------- | ---------------------------------------------------------------------------------- |
| **Vue Test Utils 2** | `mount` 返回 `VueWrapper`；`findComponent / getByTestId`；支持 `global.plugins / stubs`。 |
| **Pinia 测试**         | `createTestingPinia({ stubActions: false })` 自动 mock store；可 `store.$patch` 直接改状态。 |
| **组件快照**             | `expect(wrapper.html()).toMatchSnapshot()`；配合 `jsdom` 环境。                          |

---

## 11. 常见踩坑速查

| 踩坑                                | 正确姿势                                                          |
| --------------------------------- | ------------------------------------------------------------- |
| 解构 reactive 丢失响应                  | 用 `toRefs` 或 `storeToRefs`                                    |
| v-model 自定义多个却写 `modelValue`      | 用 `v-model:foo` + `defineModel('foo')`                        |
| 在 `&lt;script setup&gt;` 写 `this` | 不存在，直接引入函数/库                                                  |
| 把 ref 传给 reactive                 | `const state = reactive({ count: ref(0) })` 会丢失解包，直接 `ref` 即可 |
| 路由守卫 next()                       | Vue3 已移除 `next` 参数，直接 `return true / false / '/path'`         |

---

## 12. 7 天冲刺路线

| 天    | 任务                     | 产出                       |
| ---- | ---------------------- | ------------------------ |
| Day1 | Vite 起手 + 组合式计数器       | 熟悉 ref/reactive/computed |
| Day2 | 待办列表（新增/删除/过滤）         | 练习 v-for/key、watchEffect |
| Day3 | 多级组件通信：provide/inject  | 颜色主题切换                   |
| Day4 | 加路由 + 路由守卫 + 异步组件      | 权限拦截                     |
| Day5 | Pinia 购物车 + 本地持久化      | 模块化、热更新                  |
| Day6 | 单元测试 + 组件快照            | 覆盖率报告                    |
| Day7 | 读源码：Proxy 依赖收集、组件实例初始化 | 输出 3 篇笔记                 |

&gt; 打印本大纲，每掌握一条打钩，全部完成 = Vue3 面试/开发双通关。
