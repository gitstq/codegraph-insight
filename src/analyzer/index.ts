/**
 * 代码分析器主入口
 */
import { scanProject, readFileInfo } from '../utils/file-utils';
import { parseJavaScript } from './ast-parser';
import { AnalyzerConfig, AnalysisResult, KnowledgeGraph, CodeNode, CodeEdge } from '../types';

/**
 * 分析项目
 */
export async function analyzeProject(projectPath: string, config: AnalyzerConfig = {}): Promise<AnalysisResult> {
  const startTime = Date.now();
  
  console.log(`🔍 开始分析项目: ${projectPath}`);
  
  // 扫描文件
  const files = await scanProject(projectPath, config.include, config.exclude);
  console.log(`📁 发现 ${files.length} 个文件`);

  const allNodes: CodeNode[] = [];
  const allEdges: CodeEdge[] = [];
  let totalLines = 0;
  const languages = new Set<string>();

  // 分析每个文件
  for (let i = 0; i < files.length; i++) {
    const filePath = files[i];
    const fileInfo = readFileInfo(filePath);
    
    if (!fileInfo) continue;

    // 进度显示
    if ((i + 1) % 10 === 0 || i === files.length - 1) {
      console.log(`  分析进度: ${i + 1}/${files.length} (${Math.round((i + 1) / files.length * 100)}%)`);
    }

    totalLines += fileInfo.lines;
    languages.add(fileInfo.language);

    // 根据语言选择解析器
    if (['typescript', 'javascript'].includes(fileInfo.language)) {
      const { nodes, edges } = parseJavaScript(fileInfo, projectPath);
      allNodes.push(...nodes);
      allEdges.push(...edges);
    }
    // 可以扩展支持其他语言
  }

  const duration = Date.now() - startTime;

  // 构建知识图谱
  const graph: KnowledgeGraph = {
    nodes: allNodes,
    edges: allEdges,
    metadata: {
      projectName: projectPath.split('/').pop() || 'unknown',
      analyzedAt: new Date().toISOString(),
      totalFiles: files.length,
      totalLines,
      languages: Array.from(languages)
    }
  };

  console.log(`✅ 分析完成! 耗时 ${duration}ms`);
  console.log(`   节点数: ${allNodes.length}`);
  console.log(`   边数: ${allEdges.length}`);
  console.log(`   语言: ${Array.from(languages).join(', ')}`);

  return {
    graph,
    stats: {
      totalNodes: allNodes.length,
      totalEdges: allEdges.length,
      filesAnalyzed: files.length,
      duration
    }
  };
}

export * from './ast-parser';