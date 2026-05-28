# 🔮 CodeGraph Insight

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg" alt="Node.js">
</p>

<p align="center">
  <b>🌐 语言选择</b>：
  <a href="./README.md">English</a> |
  <a href="./README.zh-CN.md">简体中文</a> |
  <a href="./README.zh-TW.md">繁體中文</a>
</p>

---

## 🎉 Project Introduction

**CodeGraph Insight** is an intelligent code knowledge graph analysis tool that transforms any codebase into an interactive knowledge graph. Stop reading code blindly—start visualizing how every piece fits together!

### 💡 Why CodeGraph Insight?

- **🚀 Instant Understanding**: Visualize your entire codebase structure in seconds
- **🔍 Smart Search**: Find functions, classes, and dependencies with fuzzy search
- **🌐 Interactive Dashboard**: Explore code relationships through an intuitive web interface
- **📊 Deep Analysis**: Understand import/export relationships, function calls, and class hierarchies
- **⚡ Lightning Fast**: Built with performance in mind for large codebases

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📁 **Multi-Language Support** | TypeScript, JavaScript, and extensible for more languages |
| 🕸️ **Knowledge Graph** | Transform code into nodes and edges for easy exploration |
| 🎯 **AST Parsing** | Deep analysis using Abstract Syntax Tree |
| 🖥️ **Web Dashboard** | Beautiful, interactive visualization with real-time updates |
| 🔎 **Smart Search** | Find any code element instantly |
| 📈 **Statistics** | Comprehensive metrics about your codebase |
| 🛠️ **CLI Tools** | Command-line interface for automation |
| 🔌 **Extensible** | Plugin architecture for custom analyzers |

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** >= 18.0.0
- **npm** or **yarn**

### Installation

```bash
# Install globally
npm install -g codegraph-insight

# Or use npx (no installation needed)
npx codegraph-insight <command>
```

### One-Command Analysis

```bash
# Analyze a project and launch dashboard
codegraph quick /path/to/your/project
```

This will:
1. 🔍 Scan and analyze your codebase
2. 🕸️ Generate a knowledge graph
3. 🌐 Start the interactive dashboard
4. 🖥️ Open your browser automatically

---

## 📖 Detailed Usage Guide

### CLI Commands

#### 1. Analyze Project

```bash
# Basic analysis
codegraph analyze /path/to/project

# With custom output
codegraph analyze /path/to/project -o ./output/graph.json

# Include/exclude patterns
codegraph analyze /path/to/project -i "src,lib" -e "test,node_modules"
```

#### 2. Launch Dashboard

```bash
# Start dashboard with existing graph
codegraph dashboard ./graph.json -p 3000
```

#### 3. Quick Mode (Analyze + Dashboard)

```bash
# One command to analyze and view
codegraph quick /path/to/project -p 8080
```

### Dashboard Features

- **🖱️ Interactive Graph**: Click and drag nodes, zoom in/out
- **🔍 Search**: Real-time search across all code elements
- **📊 Statistics Panel**: View metrics about your codebase
- **📋 Node Details**: Click any node to see detailed information
- **🎨 Color Coding**: Different colors for different node types

---

## 💡 Design Philosophy

### Why Knowledge Graph?

Traditional code analysis tools show flat lists or tree structures. CodeGraph Insight uses **knowledge graphs** because:

1. **Relationships Matter**: Code is not just files—it's a network of dependencies
2. **Visual Intuition**: Humans understand visual patterns better than text
3. **Scalable**: Graphs scale better for large codebases
4. **Queryable**: Graph structures enable complex queries

### Technical Choices

- **TypeScript**: Type safety and excellent developer experience
- **Babel Parser**: Industry-standard AST parsing
- **Vis.js**: Powerful, performant graph visualization
- **WebSocket**: Real-time communication for interactive features

---

## 📦 Build & Deployment

### Development Setup

```bash
# Clone the repository
git clone https://github.com/gitstq/codegraph-insight.git
cd codegraph-insight

# Install dependencies
npm install

# Build the project
npm run build

# Run in development mode
npm run dev
```

### Project Structure

```
codegraph-insight/
├── src/
│   ├── analyzer/       # Code analysis engines
│   │   ├── ast-parser.ts
│   │   └── index.ts
│   ├── graph/          # Graph building utilities
│   │   └── builder.ts
│   ├── server/         # Dashboard server
│   │   └── dashboard.ts
│   ├── utils/          # Helper functions
│   │   └── file-utils.ts
│   ├── types.ts        # TypeScript definitions
│   ├── cli.ts          # CLI entry point
│   └── index.ts        # Library exports
├── dist/               # Compiled output
├── package.json
├── tsconfig.json
└── README.md
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'feat: add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by the need for better code understanding tools
- Built with modern open-source technologies
- Community-driven development

---

<p align="center">
  <b>⭐ Star this repo if you find it helpful!</b>
</p>

<p align="center">
  Made with ❤️ by the CodeGraph Team
</p>