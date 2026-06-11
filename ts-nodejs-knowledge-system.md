# TypeScript / Node.js / JavaScript 知识体系

## 📋 目录

1. [核心概念与关系](#核心概念与关系)
2. [JavaScript 基础](#javascript-基础)
3. [Node.js 运行时](#nodejs-运行时)
4. [TypeScript 类型系统](#typescript-类型系统)
5. [三者对比](#三者对比)
6. [使用场景](#使用场景)
7. [学习路径](#学习路径)

---

## 核心概念与关系

```
┌─────────────────────────────────────────┐
│           JavaScript (语言)              │
│    - ECMAScript 标准实现                  │
│    - 动态类型、解释执行                     │
└─────────────────────────────────────────┘
              ↓ 扩展
┌─────────────────────────────────────────┐
│         TypeScript (超集)                │
│    - JS + 静态类型系统                    │
│    - 编译为 JavaScript 执行               │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│          Node.js (运行时)                │
│    - 基于 V8 引擎                        │
│    - 可运行 JS/TS (需编译)               │
│    - 提供系统级 API                      │
└─────────────────────────────────────────┘
```

**关系说明**：
- **JavaScript** 是编程语言规范
- **TypeScript** 是 JavaScript 的超集，添加了类型系统
- **Node.js** 是运行环境，让 JS/TS 可以在服务器端运行

---

## JavaScript 基础

### 核心特性

| 特性 | 说明 | 示例 |
|------|------|------|
| 动态类型 | 变量类型在运行时确定 | `let x = 1; x = "hello";` |
| 函数式编程 | 函数是一等公民 | `const add = (a, b) => a + b;` |
| 原型继承 | 基于原型的对象系统 | `Object.create(proto)` |
| 事件循环 | 单线程异步模型 | `setTimeout`, `Promise` |
| 闭包 | 函数可以访问外部作用域 | `function outer() { let x = 1; return () => x; }` |

### ES6+ 现代语法

```javascript
// 解构赋值
const { name, age } = user;
const [first, ...rest] = array;

// 可选链
const city = user?.address?.city;

// 空值合并
const value = input ?? "default";

// 模块化
import { readFile } from 'fs/promises';
export const calculate = (x, y) => x + y;

// 异步/等待
async function fetchData() {
  const response = await fetch(url);
  return response.json();
}
```

### 核心概念详解

#### 1. 事件循环 (Event Loop)

```javascript
console.log('1'); // 同步

setTimeout(() => {
  console.log('2'); // 宏任务
}, 0);

Promise.resolve().then(() => {
  console.log('3'); // 微任务
});

console.log('4'); // 同步

// 输出顺序: 1, 4, 3, 2
```

#### 2. 原型链与继承

```javascript
// ES5 原型
function Person(name) {
  this.name = name;
}
Person.prototype.sayHi = function() {
  console.log(`Hi, I'm ${this.name}`);
};

// ES6 class (语法糖)
class Animal {
  constructor(name) {
    this.name = name;
  }
  speak() {
    console.log(`${this.name} makes a sound`);
  }
}

class Dog extends Animal {
  speak() {
    console.log(`${this.name} barks`);
  }
}
```

#### 3. 闭包与作用域

```javascript
function counter() {
  let count = 0; // 私有变量
  return {
    increment: () => ++count,
    getCount: () => count
  };
}

const c = counter();
c.increment(); // 1
c.increment(); // 2
c.getCount();  // 2
```

#### 4. Promise 与异步

```javascript
// Promise 链
fetchData()
  .then(data => processData(data))
  .then(result => saveResult(result))
  .catch(error => handleError(error));

// async/await
try {
  const data = await fetchData();
  const result = await processData(data);
  await saveResult(result);
} catch (error) {
  handleError(error);
}

// 并发控制
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts()
]);
```

---

## Node.js 运行时

### 核心模块

#### 1. 文件系统 (fs)

```javascript
import { readFile, writeFile, readdir } from 'fs/promises';
import { createReadStream } from 'fs';

// 读取文件
const content = await readFile('file.txt', 'utf-8');

// 写入文件
await writeFile('output.txt', 'data');

// 流式处理（大文件）
const stream = createReadStream('large.csv');
stream.on('data', chunk => processChunk(chunk));
```

#### 2. HTTP 服务器

```javascript
import http from 'http';

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello World\n');
});

server.listen(3000);
```

#### 3. 进程与子进程

```javascript
import { exec, spawn } from 'child_process';

// 执行命令
exec('ls -la', (error, stdout) => {
  console.log(stdout);
});

// 流式子进程
const child = spawn('ping', ['google.com']);
child.stdout.on('data', data => console.log(data.toString()));
```

#### 4. 事件发射器

```javascript
import { EventEmitter } from 'events';

class MyEmitter extends EventEmitter {}

const emitter = new MyEmitter();
emitter.on('event', (data) => console.log(data));
emitter.emit('event', 'Hello');
```

### Node.js 特有概念

| 概念 | 说明 | 示例 |
|------|------|------|
| CommonJS | 模块规范 | `require()`, `module.exports` |
| 全局对象 | `process`, `Buffer`, `__dirname` | `process.env.NODE_ENV` |
| 流 (Stream) | 处理大数据流 | `Readable`, `Writable`, `Transform` |
| Buffer | 二进制数据处理 | `Buffer.from('hello')` |
| REPL | 交互式解释器 | `node` 命令进入 |

### Node.js vs 浏览器

| 特性 | Node.js | 浏览器 |
|------|---------|--------|
| 全局对象 | `global` | `window` |
| DOM | ❌ 无 | ✅ 有 |
| 文件系统 | ✅ 有 | ❌ 无 (需 API) |
| 模块系统 | CommonJS/ESM | ESM (现代) |
| 入口文件 | `process.argv` | HTML 脚本标签 |

---

## TypeScript 类型系统

### 基础类型

```typescript
// 原始类型
let name: string = "Alice";
let age: number = 25;
let active: boolean = true;
let data: null = null;
let nothing: undefined = undefined;

// 数组
let numbers: number[] = [1, 2, 3];
let items: Array<string> = ["a", "b"];

// 元组
let pair: [string, number] = ["age", 25];

// 枚举
enum Color { Red, Green, Blue }
let c: Color = Color.Green;

// any (避免使用)
let value: any = "hello";
value = 123; // 不报错，但不安全

// unknown (安全的 any)
let data: unknown = "hello";
if (typeof data === "string") {
  console.log(data.length); // 类型守卫
}

// void
function log(): void {
  console.log("no return");
}

// never (永远不会返回)
function error(): never {
  throw new Error("error");
}
```

### 对象与接口

```typescript
// 接口
interface User {
  id: number;
  name: string;
  email?: string; // 可选
  readonly createdAt: Date; // 只读
}

// 类型别名
type Point = {
  x: number;
  y: number;
};

// 函数类型
type MathFunc = (a: number, b: number) => number;
const add: MathFunc = (a, b) => a + b;

// 索引签名
interface Dictionary {
  [key: string]: string;
}
```

### 高级类型

#### 1. 联合与交叉类型

```typescript
// 联合类型 (OR)
type StringOrNumber = string | number;
let value: StringOrNumber = "hello";
value = 123; // OK

// 交叉类型 (AND)
type HasName = { name: string };
type HasAge = { age: number };
type Person = HasName & HasAge;
let person: Person = { name: "Alice", age: 25 };
```

#### 2. 字面量类型

```typescript
type Direction = "up" | "down" | "left" | "right";
let dir: Direction = "up";

type ErrorCode = 404 | 500 | 503;
let code: ErrorCode = 404;
```

#### 3. 类型守卫

```typescript
// typeof
function process(value: string | number) {
  if (typeof value === "string") {
    return value.toUpperCase();
  }
  return value.toFixed(2);
}

// instanceof
if (error instanceof TypeError) {
  console.log("Type error occurred");
}

// in
interface Fish { swim: () => void }
interface Bird { fly: () => void }

function move(animal: Fish | Bird) {
  if ("swim" in animal) {
    animal.swim();
  } else {
    animal.fly();
  }
}
```

#### 4. 泛型

```typescript
// 泛型函数
function identity<T>(arg: T): T {
  return arg;
}
let output = identity<string>("hello");

// 泛型接口
interface Container<T> {
  value: T;
  getValue(): T;
}

// 泛型约束
function getLength<T extends { length: number }>(arg: T): number {
  return arg.length;
}
getLength("hello"); // OK
getLength([1, 2, 3]); // OK
// getLength(123); // Error

// 泛型类
class Stack<T> {
  private items: T[] = [];
  
  push(item: T): void {
    this.items.push(item);
  }
  
  pop(): T | undefined {
    return this.items.pop();
  }
}
```

#### 5. 类型工具

```typescript
// Partial - 所有属性可选
type PartialUser = Partial<User>;

// Required - 所有属性必填
type RequiredUser = Required<Partial<User>>;

// Pick - 选取部分属性
type UserPreview = Pick<User, "id" | "name">;

// Omit - 排除部分属性
type UserWithoutId = Omit<User, "id">;

// Record - 键值对映射
type UserRoles = Record<string, "admin" | "user" | "guest">;

// ReturnType - 获取函数返回类型
type Result = ReturnType<typeof fetchData>;

// Parameters - 获取函数参数类型
type FuncParams = Parameters<typeof process>;
```

### 类与装饰器

```typescript
// 抽象类
abstract class Shape {
  abstract area(): number;
  
  describe(): void {
    console.log(`Area: ${this.area()}`);
  }
}

class Circle extends Shape {
  constructor(private radius: number) {
    super();
  }
  
  area(): number {
    return Math.PI * this.radius ** 2;
  }
}

// 访问修饰符
class BankAccount {
  private balance: number = 0;
  
  constructor(public readonly owner: string) {}
  
  deposit(amount: number): void {
    this.balance += amount;
  }
  
  getBalance(): number {
    return this.balance;
  }
}
```

---

## 三者对比

### 语言特性对比

| 特性 | JavaScript | TypeScript | Node.js |
|------|------------|------------|---------|
| **类型系统** | 动态类型 | 静态类型 | 运行时环境 |
| **编译** | 解释执行 | 编译为 JS | 执行 JS |
| **类型检查** | 运行时 | 编译时 | 运行时 |
| **IDE 支持** | 基础 | 强大自动补全 | 基础 |
| **学习曲线** | 低 | 中 | 中 |
| **代码体积** | 小 | 大 (有类型注解) | N/A |
| **运行性能** | 快 | 编译后与 JS 相同 | 快 |

### 生态系统对比

| 生态 | JavaScript | TypeScript | Node.js |
|------|------------|------------|---------|
| **包管理** | npm/yarn/pnpm | npm/yarn/pnpm | npm (默认) |
| **框架** | React, Vue, Angular | NestJS, Express, Fastify | Express, Fastify, Koa |
| **工具链** | ESLint, Prettier | tsc, TSLint (deprecated) | nodemon, pm2 |
| **测试** | Jest, Mocha | Jest (原生支持), Vitest | Jest, Supertest |
| **构建工具** | Webpack, Vite | Webpack, esbuild, tsup | 无需构建 (直接运行) |

### 开发体验对比

| 场景 | JavaScript | TypeScript | Node.js |
|------|------------|------------|---------|
| **重构** | 困难，需手动查找 | 安全，编译器检查 | 困难 |
| **调试** | 运行时发现错误 | 编译时发现错误 | 运行时调试 |
| **文档** | 需要额外文档 | 类型即文档 | 需要额外文档 |
| **团队协作** | 容易产生 bug | 约束性强，减少错误 | 依赖团队规范 |
| **原型开发** | 快速 | 稍慢 (需定义类型) | 快速 |
| **大型项目** | 难以维护 | 易于维护 | 中等难度 |

### 性能对比

```javascript
// JavaScript - 直接运行
function add(a, b) { return a + b; }

// TypeScript - 编译后
function add(a, b) { return a + b; }
// 编译后与 JS 完全相同，无性能损耗

// Node.js 特有优化
// - V8 JIT 编译
// - 流式处理大文件
// - Worker Threads 多线程
```

---

## 使用场景

### JavaScript 最佳场景

#### ✅ 适合

1. **快速原型开发**
   ```javascript
   // 无需类型定义，快速验证想法
   const app = express();
   app.get('/', (req, res) => res.send('Hello'));
   ```

2. **小型脚本和工具**
   ```javascript
   #!/usr/bin/env node
   // 简单的文件处理脚本
   const fs = require('fs');
   fs.readdirSync('.').forEach(f => console.log(f));
   ```

3. **前端交互逻辑**
   ```javascript
   // DOM 操作、事件处理
   document.querySelector('.btn').addEventListener('click', () => {
     // ...
   });
   ```

4. **学习和教学**
   - 无需理解类型系统
   - 专注编程概念

#### ❌ 不适合

- 大型团队项目
- 复杂的数据结构
- 需要强类型保证的场景

---

### TypeScript 最佳场景

#### ✅ 适合

1. **大型企业应用**
   ```typescript
   // 清晰的接口定义
   interface UserService {
     getUser(id: number): Promise<User>;
     createUser(data: CreateUserDto): Promise<User>;
     updateUser(id: number, data: UpdateUserDto): Promise<User>;
   }
   ```

2. **API 开发**
   ```typescript
   // 请求/响应类型安全
   interface CreateUserRequest {
     name: string;
     email: string;
     age?: number;
   }
   
   app.post('/users', (req: Request<{}, {}, CreateUserRequest>, res) => {
     const { name, email } = req.body; // 类型安全
   });
   ```

3. **复杂数据处理**
   ```typescript
   // 类型转换和验证
   function parseCSV(data: string): Record<string, string>[] {
     // 编译器确保返回类型正确
   }
   ```

4. **库和框架开发**
   ```typescript
   // 提供类型定义，改善用户体验
   export function createServer(options: ServerOptions): Server;
   ```

5. **团队协作项目**
   - 类型即文档
   - 减少沟通成本
   - 编译时捕获错误

#### 典型项目

- NestJS 后端框架
- Angular 前端框架
- VS Code 编辑器
- Discord.js 库

---

### Node.js 最佳场景

#### ✅ 适合

1. **后端 API 服务**
   ```javascript
   const express = require('express');
   const app = express();
   
   app.get('/api/users', async (req, res) => {
     const users = await db.query('SELECT * FROM users');
     res.json(users);
   });
   ```

2. **CLI 工具**
   ```javascript
   #!/usr/bin/env node
   const { program } = require('commander');
   
   program
     .option('-n, --name <name>', 'your name')
     .action(options => console.log(`Hello ${options.name}`));
   
   program.parse();
   ```

3. **实时应用**
   ```javascript
   // WebSocket 服务器
   const WebSocket = require('ws');
   const wss = new WebSocket.Server({ port: 8080 });
   
   wss.on('connection', ws => {
     ws.on('message', message => {
       wss.clients.forEach(client => client.send(message));
     });
   });
   ```

4. **微服务**
   ```javascript
   // 轻量级服务
   const fastify = require('fastify');
   const app = fastify();
   
   app.get('/health', async () => ({ status: 'ok' }));
   ```

5. **文件处理和构建工具**
   ```javascript
   // Gulp, Webpack 插件
   const through = require('through2');
   
   module.exports = function() {
     return through.obj(function(file, enc, cb) {
       // 处理文件
       cb(null, file);
     });
   };
   ```

6. **Serverless 函数**
   ```javascript
   // AWS Lambda
   exports.handler = async (event) => {
     return { statusCode: 200, body: 'Hello' };
   };
   ```

#### 不适合

- CPU 密集型计算 (考虑 Python/C++)
- 图形界面应用 (考虑 Electron)
- 嵌入式系统 (考虑 C/Rust)

---

## 组合使用场景

### JavaScript + Node.js

```javascript
// 快速开发的 Web 服务
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello World');
});

app.listen(3000);
```

**适用**: 原型、小工具、快速验证

---

### TypeScript + Node.js

```typescript
// 类型安全的后端服务
import express, { Request, Response } from 'express';

interface User {
  id: number;
  name: string;
}

const app = express();

app.get('/users', async (req: Request, res: Response<User[]>) => {
  const users: User[] = await getUsers();
  res.json(users);
});

app.listen(3000);
```

**适用**: 生产级后端、企业应用

---

### 前端 + Node.js (全栈)

```javascript
// 前端 (React)
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(setUser);
  }, [userId]);
  
  return <div>{user?.name}</div>;
}

// 后端 (Node.js)
app.get('/api/users/:id', async (req, res) => {
  const user = await db.findUser(req.params.id);
  res.json(user);
});
```

**适用**: 全栈 Web 应用

---

## 学习路径

### 路径一：前端开发者

```
1. JavaScript 基础 (1-2 周)
   ├── 语法基础
   ├── DOM 操作
   ├── 事件处理
   └── ES6+ 特性

2. 前端框架 (2-4 周)
   ├── React / Vue / Angular
   ├── 状态管理
   └── 路由

3. TypeScript (2-3 周)
   ├── 基础类型
   ├── 接口与类型
   ├── 泛型
   └── 在框架中使用

4. Node.js 基础 (1-2 周)
   ├── 模块系统
   ├── 文件系统
   └── HTTP 服务器
```

---

### 路径二：后端开发者

```
1. Node.js 基础 (1-2 周)
   ├── 事件循环
   ├── 异步编程
   ├── 核心模块
   └── npm 生态

2. JavaScript 深入 (2-3 周)
   ├── 原型链
   ├── 闭包
   ├── 异步模式
   └── 函数式编程

3. TypeScript (2-3 周)
   ├── 类型系统
   ├── 接口与类
   ├── 泛型
   └── 装饰器

4. 后端框架 (3-4 周)
   ├── Express / Fastify
   ├── NestJS (TypeScript)
   ├── 数据库 ORM
   └── 测试
```

---

### 路径三：全栈开发者

```
1. JavaScript 核心 (2-3 周)
   ├── 语言基础
   ├── 异步编程
   └── 模块化

2. Node.js 后端 (3-4 周)
   ├── Express/Fastify
   ├── REST API 设计
   ├── 数据库
   └── 认证授权

3. 前端基础 (2-3 周)
   ├── HTML/CSS
   ├── JavaScript DOM
   └── 响应式设计

4. TypeScript (2-3 周)
   ├── 类型系统
   └── 前后端应用

5. 现代框架 (4-6 周)
   ├── React/Vue
   ├── Next.js / Nuxt
   └── 全栈部署
```

---

## 推荐资源

### 文档

- [MDN Web Docs](https://developer.mozilla.org/) - JavaScript 权威文档
- [TypeScript 官方文档](https://www.typescriptlang.org/docs/)
- [Node.js 官方文档](https://nodejs.org/docs/)

### 书籍

- **JavaScript**: 《JavaScript 高级程序设计》《你不知道的 JavaScript》
- **TypeScript**: 《TypeScript 编程》《Programming TypeScript》
- **Node.js**: 《Node.js 设计模式》《Node.js 开发指南》

### 在线课程

- freeCodeCamp (免费)
- Frontend Masters
- Udemy (JavaScript/Node.js 课程)

### 练习平台

- [LeetCode](https://leetcode.com/) - 算法练习
- [Exercism](https://exercism.org/) - 语言练习
- [Codewars](https://www.codewars.com/) - 编程挑战

---

## 总结

| 选择 | 场景 | 优势 |
|------|------|------|
| **JavaScript** | 快速原型、小项目、学习 | 简单、灵活、生态丰富 |
| **TypeScript** | 大型项目、团队协作、生产环境 | 类型安全、可维护、IDE 友好 |
| **Node.js** | 后端服务、CLI、实时应用 | 高性能、非阻塞、全栈统一语言 |

**最佳实践**：
- 新项目推荐 **TypeScript + Node.js**
- 学习阶段可以从 **JavaScript + Node.js** 开始
- 前端项目优先使用 **TypeScript**
- 小脚本和快速原型可以用 **JavaScript**

记住：工具是为了解决问题，选择最适合你当前需求的，而不是最"先进"的。
