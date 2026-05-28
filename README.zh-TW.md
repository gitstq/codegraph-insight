# 🔮 CodeGraph Insight

<p align="center">
  <img src="https://img.shields.io/badge/版本-1.0.0-blue.svg" alt="版本">
  <img src="https://img.shields.io/badge/授權-MIT-green.svg" alt="授權">
  <img src="https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg" alt="Node.js">
</p>

<p align="center">
  <b>🌐 語言選擇</b>：
  <a href="./README.md">English</a> |
  <a href="./README.zh-CN.md">简体中文</a> |
  <a href="./README.zh-TW.md">繁體中文</a>
</p>

---

## 🎉 專案介紹

**CodeGraph Insight** 是一款智慧型程式碼知識圖譜分析工具，能夠將任何程式碼庫轉換為互動式知識圖譜。告別盲目閱讀程式碼，開始視覺化地理解每一部分如何協同運作！

### 💡 為什麼選擇 CodeGraph Insight？

- **🚀 即時理解**：幾秒鐘內視覺化整個程式碼庫結構
- **🔍 智慧搜尋**：透過模糊搜尋查找函數、類別和依賴關係
- **🌐 互動式儀表板**：透過直覺的 Web 介面探索程式碼關係
- **📊 深度分析**：理解匯入/匯出關係、函數呼叫和類別階層結構
- **⚡ 極速效能**：為大型程式碼庫的效能而構建

### ✨ 核心特性

| 特性 | 描述 |
|---------|-------------|
| 📁 **多語言支援** | TypeScript、JavaScript，可擴展支援更多語言 |
| 🕸️ **知識圖譜** | 將程式碼轉換為節點和邊，便於探索 |
| 🎯 **AST 解析** | 使用抽象語法樹進行深度分析 |
| 🖥️ **Web 儀表板** | 美觀、互動式的視覺化，支援即時更新 |
| 🔎 **智慧搜尋** | 即時查找任何程式碼元素 |
| 📈 **統計分析** | 關於程式碼庫的綜合指標 |
| 🛠️ **CLI 工具** | 用於自動化的命令列介面 |
| 🔌 **可擴展** | 插件架構支援自訂分析器 |

---

## 🚀 快速開始

### 環境要求

- **Node.js** >= 18.0.0
- **npm** 或 **yarn**

### 安裝

```bash
# 全域安裝
npm install -g codegraph-insight

# 或使用 npx（無需安裝）
npx codegraph-insight <命令>
```

### 一鍵分析

```bash
# 分析專案並啟動儀表板
codegraph quick /path/to/your/project
```

這將：
1. 🔍 掃描並分析您的程式碼庫
2. 🕸️ 生成知識圖譜
3. 🌐 啟動互動式儀表板
4. 🖥️ 自動開啟瀏覽器

---

## 📖 詳細使用指南

### CLI 命令

#### 1. 分析專案

```bash
# 基礎分析
codegraph analyze /path/to/project

# 自訂輸出路徑
codegraph analyze /path/to/project -o ./output/graph.json

# 包含/排除模式
codegraph analyze /path/to/project -i "src,lib" -e "test,node_modules"
```

#### 2. 啟動儀表板

```bash
# 使用現有圖譜啟動儀表板
codegraph dashboard ./graph.json -p 3000
```

#### 3. 快速模式（分析 + 儀表板）

```bash
# 一個命令完成分析和查看
codegraph quick /path/to/project -p 8080
```

### 儀表板功能

- **🖱️ 互動式圖譜**：點擊和拖動節點，縮放
- **🔍 搜尋**：跨所有程式碼元素即時搜尋
- **📊 統計面板**：查看程式碼庫指標
- **📋 節點詳情**：點擊任意節點查看詳細資訊
- **🎨 顏色編碼**：不同類型節點用不同顏色區分

---

## 💡 設計理念

### 為什麼選擇知識圖譜？

傳統的程式碼分析工具顯示平面列表或樹形結構。CodeGraph Insight 使用**知識圖譜**，因為：

1. **關係很重要**：程式碼不僅僅是檔案——它是一個依賴網路
2. **視覺直觀**：人類理解視覺模式比文字更好
3. **可擴展**：圖譜更適合大型程式碼庫
4. **可查詢**：圖譜結構支援複雜查詢

### 技術選型

- **TypeScript**：型別安全和出色的開發體驗
- **Babel Parser**：業界標準的 AST 解析
- **Vis.js**：強大、高效能的圖譜視覺化
- **WebSocket**：即時通訊，支援互動功能

---

## 📦 構建與部署

### 開發環境搭建

```bash
# 克隆倉庫
git clone https://github.com/gitstq/codegraph-insight.git
cd codegraph-insight

# 安裝依賴
npm install

# 構建專案
npm run build

# 開發模式執行
npm run dev
```

### 專案結構

```
codegraph-insight/
├── src/
│   ├── analyzer/       # 程式碼分析引擎
│   │   ├── ast-parser.ts
│   │   └── index.ts
│   ├── graph/          # 圖譜構建工具
│   │   └── builder.ts
│   ├── server/         # 儀表板伺服器
│   │   └── dashboard.ts
│   ├── utils/          # 輔助函數
│   │   └── file-utils.ts
│   ├── types.ts        # TypeScript 定義
│   ├── cli.ts          # CLI 入口
│   └── index.ts        # 庫匯出
├── dist/               # 編譯輸出
├── package.json
├── tsconfig.json
└── README.md
```

---

## 🤝 貢獻指南

我們歡迎貢獻！請按以下步驟操作：

1. **Fork** 本倉庫
2. **建立** 功能分支 (`git checkout -b feature/amazing-feature`)
3. **提交** 您的更改 (`git commit -m 'feat: add amazing feature'`)
4. **推送** 到分支 (`git push origin feature/amazing-feature`)
5. **開啟** Pull Request

### 提交規範

我們遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hant/)：

- `feat:` 新功能
- `fix:` 修復問題
- `docs:` 文件變更
- `refactor:` 程式碼重構
- `test:` 新增測試
- `chore:` 維護任務

---

## 📄 開源授權

本專案採用 **MIT 授權條款** - 詳情請參閱 [LICENSE](LICENSE) 檔案。

---

## 🙏 致謝

- 靈感來源於對更好的程式碼理解工具的需求
- 使用現代開源技術構建
- 社群驅動開發

---

<p align="center">
  <b>⭐ 如果這個專案對您有幫助，請給它一個星標！</b>
</p>

<p align="center">
  用 ❤️ 由 CodeGraph 團隊製作
</p>