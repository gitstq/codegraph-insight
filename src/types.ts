/**
 * CodeGraph Insight - 类型定义
 */

/** 节点类型 */
export enum NodeType {
  FILE = 'file',
  FUNCTION = 'function',
  CLASS = 'class',
  INTERFACE = 'interface',
  VARIABLE = 'variable',
  IMPORT = 'import',
  EXPORT = 'export',
  METHOD = 'method',
  PROPERTY = 'property'
}

/** 边类型 */
export enum EdgeType {
  IMPORTS = 'imports',
  EXPORTS = 'exports',
  CALLS = 'calls',
  EXTENDS = 'extends',
  IMPLEMENTS = 'implements',
  CONTAINS = 'contains',
  REFERENCES = 'references',
  DEPENDS_ON = 'depends_on'
}

/** 代码节点 */
export interface CodeNode {
  id: string;
  type: NodeType;
  name: string;
  filePath: string;
  lineStart: number;
  lineEnd: number;
  code?: string;
  language: string;
  metadata?: Record<string, any>;
}

/** 代码边 */
export interface CodeEdge {
  id: string;
  source: string;
  target: string;
  type: EdgeType;
  metadata?: Record<string, any>;
}

/** 知识图谱 */
export interface KnowledgeGraph {
  nodes: CodeNode[];
  edges: CodeEdge[];
  metadata: {
    projectName: string;
    analyzedAt: string;
    totalFiles: number;
    totalLines: number;
    languages: string[];
  };
}

/** 分析配置 */
export interface AnalyzerConfig {
  entryPoint?: string;
  include?: string[];
  exclude?: string[];
  maxDepth?: number;
  parseImports?: boolean;
  parseExports?: boolean;
}

/** 分析结果 */
export interface AnalysisResult {
  graph: KnowledgeGraph;
  stats: {
    totalNodes: number;
    totalEdges: number;
    filesAnalyzed: number;
    duration: number;
  };
}

/** 文件信息 */
export interface FileInfo {
  path: string;
  content: string;
  language: string;
  size: number;
  lines: number;
}