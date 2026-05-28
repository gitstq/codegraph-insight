/**
 * 图谱构建器
 */
import { KnowledgeGraph, CodeNode, CodeEdge, NodeType, EdgeType } from '../types';

/**
 * 图谱构建器类
 */
export class GraphBuilder {
  private nodes: Map<string, CodeNode> = new Map();
  private edges: Map<string, CodeEdge> = new Map();

  /**
   * 添加节点
   */
  addNode(node: CodeNode): void {
    this.nodes.set(node.id, node);
  }

  /**
   * 添加边
   */
  addEdge(edge: CodeEdge): void {
    this.edges.set(edge.id, edge);
  }

  /**
   * 获取节点
   */
  getNode(id: string): CodeNode | undefined {
    return this.nodes.get(id);
  }

  /**
   * 获取所有节点
   */
  getAllNodes(): CodeNode[] {
    return Array.from(this.nodes.values());
  }

  /**
   * 获取所有边
   */
  getAllEdges(): CodeEdge[] {
    return Array.from(this.edges.values());
  }

  /**
   * 按类型获取节点
   */
  getNodesByType(type: NodeType): CodeNode[] {
    return this.getAllNodes().filter(n => n.type === type);
  }

  /**
   * 获取节点的入边
   */
  getIncomingEdges(nodeId: string): CodeEdge[] {
    return this.getAllEdges().filter(e => e.target === nodeId);
  }

  /**
   * 获取节点的出边
   */
  getOutgoingEdges(nodeId: string): CodeEdge[] {
    return this.getAllEdges().filter(e => e.source === nodeId);
  }

  /**
   * 获取节点的邻居
   */
  getNeighbors(nodeId: string): CodeNode[] {
    const neighborIds = new Set<string>();
    
    this.getAllEdges().forEach(edge => {
      if (edge.source === nodeId) neighborIds.add(edge.target);
      if (edge.target === nodeId) neighborIds.add(edge.source);
    });

    return Array.from(neighborIds).map(id => this.nodes.get(id)).filter(Boolean) as CodeNode[];
  }

  /**
   * 搜索节点
   */
  searchNodes(query: string): CodeNode[] {
    const lowerQuery = query.toLowerCase();
    return this.getAllNodes().filter(node => 
      node.name.toLowerCase().includes(lowerQuery) ||
      node.filePath.toLowerCase().includes(lowerQuery)
    );
  }

  /**
   * 获取文件的所有节点
   */
  getFileNodes(filePath: string): CodeNode[] {
    return this.getAllNodes().filter(n => n.filePath === filePath);
  }

  /**
   * 计算图谱统计信息
   */
  getStats() {
    const nodeTypes = new Map<NodeType, number>();
    const edgeTypes = new Map<EdgeType, number>();

    this.getAllNodes().forEach(node => {
      nodeTypes.set(node.type, (nodeTypes.get(node.type) || 0) + 1);
    });

    this.getAllEdges().forEach(edge => {
      edgeTypes.set(edge.type, (edgeTypes.get(edge.type) || 0) + 1);
    });

    return {
      totalNodes: this.nodes.size,
      totalEdges: this.edges.size,
      nodeTypes: Object.fromEntries(nodeTypes),
      edgeTypes: Object.fromEntries(edgeTypes)
    };
  }

  /**
   * 导出为 JSON
   */
  toJSON(metadata: KnowledgeGraph['metadata']): KnowledgeGraph {
    return {
      nodes: this.getAllNodes(),
      edges: this.getAllEdges(),
      metadata
    };
  }

  /**
   * 从 JSON 导入
   */
  fromJSON(data: KnowledgeGraph): void {
    this.nodes.clear();
    this.edges.clear();
    
    data.nodes.forEach(node => this.nodes.set(node.id, node));
    data.edges.forEach(edge => this.edges.set(edge.id, edge));
  }

  /**
   * 清空图谱
   */
  clear(): void {
    this.nodes.clear();
    this.edges.clear();
  }
}