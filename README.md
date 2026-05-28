# 🔍 CodeGraph-Insight

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)]()

**Transform your codebase into an interactive knowledge graph**

</div>

---

## 🌍 Language Selection

- [🇺🇸 English](#english)
- [🇨🇳 简体中文](#simplified-chinese)

---

<a name="english"></a>
## 🇺🇸 English

### 🎉 Introduction

**CodeGraph-Insight** is a lightweight, powerful code knowledge graph visualization tool that transforms any codebase into an interactive knowledge graph. Unlike complex enterprise solutions, CodeGraph-Insight focuses on simplicity, speed, and ease of use.

**Key Differentiators:**
- 🚀 **Lightweight**: No heavy dependencies, pure Python implementation
- 🌐 **Multi-language**: Supports 12+ programming languages
- 🎯 **Local-first**: All processing happens locally, no code leaves your machine
- ⚡ **Fast**: Parses large codebases in seconds
- 🎨 **Beautiful**: Interactive D3.js visualizations

### ✨ Core Features

| Feature | Description | Emoji |
|---------|-------------|-------|
| **Multi-Language Parser** | Python, JavaScript, TypeScript, Java, Go, Rust, C/C++, Ruby, PHP, Swift, Kotlin, Scala | 🌐 |
| **Interactive Visualization** | Force-directed graph with zoom, pan, and search | 🎨 |
| **Graph Analysis** | NetworkX-powered metrics and centrality analysis | 📊 |
| **Web Server Mode** | Live exploration with local HTTP server | 🌐 |
| **Multiple Export Formats** | JSON, D3.js, GraphViz DOT | 📦 |
| **CLI Interface** | Analyze, visualize, serve, export, search commands | 💻 |
| **Zero Dependencies** | Core functionality works without external libs | 🎯 |

### 🚀 Quick Start

#### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/codegraph-insight.git
cd codegraph-insight

# Install dependencies (optional - for enhanced features)
pip install -r requirements.txt

# Or install as package
pip install -e .
```

#### Basic Usage

```bash
# Analyze a codebase
python -m codegraph_insight analyze ./my-project

# Generate interactive visualization
python -m codegraph_insight visualize ./my-project -o graph.html --open

# Start web server
python -m codegraph_insight serve ./my-project -p 8080

# Export to JSON
python -m codegraph_insight export ./my-project -f json -o data.json

# Search for specific entities
python -m codegraph_insight search ./my-project "User" --type class
```

#### Python API

```python
from codegraph_insight import CodeParser, GraphBuilder, Visualizer

# Parse codebase
parser = CodeParser("./my-project")
nodes, edges = parser.parse_project()

# Build graph
builder = GraphBuilder(nodes, edges)
print(builder.get_summary())

# Generate visualization
visualizer = Visualizer(builder)
visualizer.generate_html("graph.html")
```

### 📖 Detailed Usage Guide

#### Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `analyze` | Print code analysis summary | `codegraph-insight analyze ./src` |
| `visualize` | Generate HTML visualization | `codegraph-insight visualize ./src -o out.html` |
| `serve` | Start web server | `codegraph-insight serve ./src -p 8080` |
| `export` | Export graph data | `codegraph-insight export ./src -f json` |
| `search` | Search code entities | `codegraph-insight search ./src "auth"` |

#### Visualization Features

The generated HTML visualization includes:
- 🔍 **Search**: Real-time node filtering
- 🖱️ **Interactive**: Drag nodes, zoom, pan
- 📊 **Statistics**: Live node/edge counts
- 🎨 **Color-coded**: Different colors for different node types
- 💾 **Export**: Download graph data as JSON

### 💡 Design Philosophy

CodeGraph-Insight was designed with these principles:

1. **Simplicity First**: Easy to install, easy to use
2. **Privacy Focused**: Local processing only
3. **Language Agnostic**: Support as many languages as possible
4. **Extensible**: Modular architecture for easy extension
5. **Beautiful**: Visualizations should be aesthetically pleasing

### 📦 Packaging & Deployment

#### As Python Package

```bash
# Build package
python setup.py sdist bdist_wheel

# Install locally
pip install dist/codegraph_insight-1.0.0-py3-none-any.whl
```

#### Requirements

- Python 3.8+
- Optional: NetworkX 3.0+ (for advanced graph analysis)
- Optional: Modern web browser (for visualization)

### 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="simplified-chinese"></a>
## 🇨🇳 简体中文

### 🎉 项目介绍

**CodeGraph-Insight** 是一款轻量级、强大的代码知识图谱可视化工具，可以将任何代码库转换为交互式知识图谱。与复杂的企业级解决方案不同，CodeGraph-Insight 专注于简洁、快速和易用性。

**核心差异化优势：**
- 🚀 **轻量级**：无重量级依赖，纯 Python 实现
- 🌐 **多语言支持**：支持 12+ 种编程语言
- 🎯 **本地优先**：所有处理均在本地完成，代码不会离开您的机器
- ⚡ **极速**：几秒钟内解析大型代码库
- 🎨 **美观**：交互式 D3.js 可视化

### ✨ 核心特性

| 特性 | 描述 | 图标 |
|---------|-------------|-------|
| **多语言解析器** | Python、JavaScript、TypeScript、Java、Go、Rust、C/C++、Ruby、PHP、Swift、Kotlin、Scala | 🌐 |
| **交互式可视化** | 力导向图，支持缩放、平移和搜索 | 🎨 |
| **图谱分析** | 基于 NetworkX 的指标和中心性分析 | 📊 |
| **Web 服务器模式** | 本地 HTTP 服务器实时探索 | 🌐 |
| **多种导出格式** | JSON、D3.js、GraphViz DOT | 📦 |
| **CLI 界面** | 分析、可视化、服务、导出、搜索命令 | 💻 |
| **零依赖** | 核心功能无需外部库 | 🎯 |

### 🚀 快速开始

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/codegraph-insight.git
cd codegraph-insight

# 安装依赖（可选 - 用于增强功能）
pip install -r requirements.txt

# 或作为包安装
pip install -e .
```

#### 基本用法

```bash
# 分析代码库
python -m codegraph_insight analyze ./my-project

# 生成交互式可视化
python -m codegraph_insight visualize ./my-project -o graph.html --open

# 启动 Web 服务器
python -m codegraph_insight serve ./my-project -p 8080

# 导出为 JSON
python -m codegraph_insight export ./my-project -f json -o data.json

# 搜索特定实体
python -m codegraph_insight search ./my-project "User" --type class
```

#### Python API

```python
from codegraph_insight import CodeParser, GraphBuilder, Visualizer

# 解析代码库
parser = CodeParser("./my-project")
nodes, edges = parser.parse_project()

# 构建图谱
builder = GraphBuilder(nodes, edges)
print(builder.get_summary())

# 生成可视化
visualizer = Visualizer(builder)
visualizer.generate_html("graph.html")
```

### 📖 详细使用指南

#### 命令参考

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `analyze` | 打印代码分析摘要 | `codegraph-insight analyze ./src` |
| `visualize` | 生成 HTML 可视化 | `codegraph-insight visualize ./src -o out.html` |
| `serve` | 启动 Web 服务器 | `codegraph-insight serve ./src -p 8080` |
| `export` | 导出图谱数据 | `codegraph-insight export ./src -f json` |
| `search` | 搜索代码实体 | `codegraph-insight search ./src "auth"` |

#### 可视化功能

生成的 HTML 可视化包含：
- 🔍 **搜索**：实时节点过滤
- 🖱️ **交互**：拖拽节点、缩放、平移
- 📊 **统计**：实时节点/边计数
- 🎨 **颜色编码**：不同类型节点不同颜色
- 💾 **导出**：下载图谱数据为 JSON

### 💡 设计理念

CodeGraph-Insight 遵循以下设计原则：

1. **简洁优先**：易于安装，易于使用
2. **隐私保护**：仅本地处理
3. **语言无关**：支持尽可能多的语言
4. **可扩展**：模块化架构，易于扩展
5. **美观**：可视化效果赏心悦目

### 📦 打包与部署

#### 作为 Python 包

```bash
# 构建包
python setup.py sdist bdist_wheel

# 本地安装
pip install dist/codegraph_insight-1.0.0-py3-none-any.whl
```

#### 环境要求

- Python 3.8+
- 可选：NetworkX 3.0+（用于高级图谱分析）
- 可选：现代 Web 浏览器（用于可视化）

### 🤝 贡献指南

我们欢迎贡献！请参阅我们的 [贡献指南](CONTRIBUTING.md) 了解详情。

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'feat: 添加惊人的功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

### 📄 开源协议

本项目采用 MIT 协议开源 - 详情请参阅 [LICENSE](LICENSE) 文件。

---

<div align="center">

**Made with ❤️ by the CodeGraph Team**

[⬆ Back to Top](#-codegraph-insight)

</div>
