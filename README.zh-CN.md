# 🔮 CodeGraph Insight

<p align="center">
  <img src="https://img.shields.io/badge/版本-1.0.0-blue.svg" alt="版本">
  <img src="https://img.shields.io/badge/许可证-MIT-green.svg" alt="许可证">
  <img src="https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg" alt="Node.js">
</p>

<p align="center">
  <b>🌐 语言选择</b>：
  <a href="./README.md">English</a> |
  <a href="./README.zh-CN.md">简体中文</a> |
  <a href="./README.zh-TW.md">繁體中文</a>
</p>

---

## 🎉 项目介绍

**CodeGraph Insight** 是一款智能代码知识图谱分析工具，能够将任何代码库转换为交互式知识图谱。告别盲目阅读代码，开始可视化地理解每一部分如何协同工作！

### 💡 为什么选择 CodeGraph Insight？

- **🚀 即时理解**：几秒钟内可视化整个代码库结构
- **🔍 智能搜索**：通过模糊搜索查找函数、类和依赖关系
- **🌐 交互式仪表盘**：通过直观的 Web 界面探索代码关系
- **📊 深度分析**：理解导入/导出关系、函数调用和类层次结构
- **⚡ 极速性能**：为大型代码库的性能而构建

### ✨ 核心特性

| 特性 | 描述 |
|---------|-------------|
| 📁 **多语言支持** | TypeScript、JavaScript，可扩展支持更多语言 |
| 🕸️ **知识图谱** | 将代码转换为节点和边，便于探索 |
| 🎯 **AST 解析** | 使用抽象语法树进行深度分析 |
| 🖥️ **Web 仪表盘** | 美观、交互式的可视化，支持实时更新 |
| 🔎 **智能搜索** | 即时查找任何代码元素 |
| 📈 **统计分析** | 关于代码库的综合指标 |
| 🛠️ **CLI 工具** | 用于自动化的命令行界面 |
| 🔌 **可扩展** | 插件架构支持自定义分析器 |

---

## 🚀 快速开始

### 环境要求

- **Node.js** >= 18.0.0
- **npm** 或 **yarn**

### 安装

```bash
# 全局安装
npm install -g codegraph-insight

# 或使用 npx（无需安装）
npx codegraph-insight <命令>
```

### 一键分析

```bash
# 分析项目并启动仪表盘
codegraph quick /path/to/your/project
```

这将：
1. 🔍 扫描并分析您的代码库
2. 🕸️ 生成知识图谱
3. 🌐 启动交互式仪表盘
4. 🖥️ 自动打开浏览器

---

## 📖 详细使用指南

### CLI 命令

#### 1. 分析项目

```bash
# 基础分析
codegraph analyze /path/to/project

# 自定义输出路径
codegraph analyze /path/to/project -o ./output/graph.json

# 包含/排除模式
codegraph analyze /path/to/project -i "src,lib" -e "test,node_modules"
```

#### 2. 启动仪表盘

```bash
# 使用现有图谱启动仪表盘
codegraph dashboard ./graph.json -p 3000
```

#### 3. 快速模式（分析 + 仪表盘）

```bash
# 一个命令完成分析和查看
codegraph quick /path/to/project -p 8080
```

### 仪表盘功能

- **🖱️ 交互式图谱**：点击和拖动节点，缩放
- **🔍 搜索**：跨所有代码元素实时搜索
- **📊 统计面板**：查看代码库指标
- **📋 节点详情**：点击任意节点查看详细信息
- **🎨 颜色编码**：不同类型节点用不同颜色区分

---

## 💡 设计理念

### 为什么选择知识图谱？

传统的代码分析工具显示平面列表或树形结构。CodeGraph Insight 使用**知识图谱**，因为：

1. **关系很重要**：代码不仅仅是文件——它是一个依赖网络
2. **视觉直观**：人类理解视觉模式比文本更好
3. **可扩展**：图谱更适合大型代码库
4. **可查询**：图谱结构支持复杂查询

### 技术选型

- **TypeScript**：类型安全和出色的开发体验
- **Babel Parser**：行业标准的 AST 解析
- **Vis.js**：强大、高性能的图谱可视化
- **WebSocket**：实时通信，支持交互功能

---

## 📦 构建与部署

### 开发环境搭建

```bash
# 克隆仓库
git clone https://github.com/gitstq/codegraph-insight.git
cd codegraph-insight

# 安装依赖
npm install

# 构建项目
npm run build

# 开发模式运行
npm run dev
```

### 项目结构

```
codegraph-insight/
├── src/
│   ├── analyzer/       # 代码分析引擎
│   │   ├── ast-parser.ts
│   │   └── index.ts
│   ├── graph/          # 图谱构建工具
│   │   └── builder.ts
│   ├── server/         # 仪表盘服务器
│   │   └── dashboard.ts
│   ├── utils/          # 辅助函数
│   │   └── file-utils.ts
│   ├── types.ts        # TypeScript 定义
│   ├── cli.ts          # CLI 入口
│   └── index.ts        # 库导出
├── dist/               # 编译输出
├── package.json
├── tsconfig.json
└── README.md
```

---

## 🤝 贡献指南

我们欢迎贡献！请按以下步骤操作：

1. **Fork** 本仓库
2. **创建** 功能分支 (`git checkout -b feature/amazing-feature`)
3. **提交** 您的更改 (`git commit -m 'feat: add amazing feature'`)
4. **推送** 到分支 (`git push origin feature/amazing-feature`)
5. **打开** Pull Request

### 提交规范

我们遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)：

- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档变更
- `refactor:` 代码重构
- `test:` 添加测试
- `chore:` 维护任务

---

## 📄 开源协议

本项目采用 **MIT 许可证** - 详情请参阅 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- 灵感来源于对更好的代码理解工具的需求
- 使用现代开源技术构建
- 社区驱动开发

---

<p align="center">
  <b>⭐ 如果这个项目对您有帮助，请给它一个星标！</b>
</p>

<p align="center">
  用 ❤️ 由 CodeGraph 团队制作
</p>