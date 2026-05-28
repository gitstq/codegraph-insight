/**
 * 可视化仪表盘服务器
 */
import * as http from 'http';
import * as fs from 'fs';
import * as path from 'path';
import { WebSocketServer, WebSocket } from 'ws';
import { KnowledgeGraph, CodeNode } from '../types';

/**
 * 启动仪表盘服务器
 */
export function startDashboardServer(graph: KnowledgeGraph, port: number = 3000): void {
  // 创建 HTTP 服务器
  const server = http.createServer((req, res) => {
    if (req.url === '/' || req.url === '/index.html') {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(getDashboardHTML());
    } else if (req.url === '/api/graph') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(graph));
    } else if (req.url === '/api/stats') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(getGraphStats(graph)));
    } else {
      res.writeHead(404);
      res.end('Not Found');
    }
  });

  // 创建 WebSocket 服务器
  const wss = new WebSocketServer({ server });
  
  wss.on('connection', (ws: WebSocket) => {
    console.log('WebSocket 连接已建立');
    
    ws.on('message', (message: string) => {
      try {
        const data = JSON.parse(message);
        handleWebSocketMessage(ws, data, graph);
      } catch (error) {
        ws.send(JSON.stringify({ error: 'Invalid message format' }));
      }
    });
  });

  server.listen(port, () => {
    console.log(`\n🌐 仪表盘服务器已启动!`);
    console.log(`   本地访问: http://localhost:${port}`);
    console.log(`   API 端点: http://localhost:${port}/api/graph`);
    console.log(`   按 Ctrl+C 停止服务器\n`);
  });
}

/**
 * 处理 WebSocket 消息
 */
function handleWebSocketMessage(ws: WebSocket, data: any, graph: KnowledgeGraph): void {
  switch (data.action) {
    case 'search':
      const results = searchNodes(graph, data.query);
      ws.send(JSON.stringify({ action: 'searchResults', data: results }));
      break;
    
    case 'getNodeDetails':
      const node = graph.nodes.find(n => n.id === data.nodeId);
      const neighbors = node ? getNodeNeighbors(graph, node.id) : [];
      ws.send(JSON.stringify({ action: 'nodeDetails', data: { node, neighbors } }));
      break;
    
    case 'getStats':
      ws.send(JSON.stringify({ action: 'stats', data: getGraphStats(graph) }));
      break;
    
    default:
      ws.send(JSON.stringify({ error: 'Unknown action' }));
  }
}

/**
 * 搜索节点
 */
function searchNodes(graph: KnowledgeGraph, query: string): CodeNode[] {
  const lowerQuery = query.toLowerCase();
  return graph.nodes.filter(node => 
    node.name.toLowerCase().includes(lowerQuery) ||
    node.filePath.toLowerCase().includes(lowerQuery)
  ).slice(0, 20);
}

/**
 * 获取节点邻居
 */
function getNodeNeighbors(graph: KnowledgeGraph, nodeId: string): CodeNode[] {
  const neighborIds = new Set<string>();
  
  graph.edges.forEach(edge => {
    if (edge.source === nodeId) neighborIds.add(edge.target);
    if (edge.target === nodeId) neighborIds.add(edge.source);
  });

  return Array.from(neighborIds).map(id => 
    graph.nodes.find(n => n.id === id)
  ).filter(Boolean) as CodeNode[];
}

/**
 * 获取图谱统计信息
 */
function getGraphStats(graph: KnowledgeGraph) {
  const nodeTypes: Record<string, number> = {};
  const edgeTypes: Record<string, number> = {};

  graph.nodes.forEach(node => {
    nodeTypes[node.type] = (nodeTypes[node.type] || 0) + 1;
  });

  graph.edges.forEach(edge => {
    edgeTypes[edge.type] = (edgeTypes[edge.type] || 0) + 1;
  });

  return {
    totalNodes: graph.nodes.length,
    totalEdges: graph.edges.length,
    nodeTypes,
    edgeTypes,
    metadata: graph.metadata
  };
}

/**
 * 获取仪表盘 HTML
 */
function getDashboardHTML(): string {
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeGraph Insight - 代码知识图谱</title>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            height: 100vh;
            overflow: hidden;
        }
        .container { display: flex; height: 100vh; }
        .sidebar {
            width: 320px;
            background: #1e293b;
            border-right: 1px solid #334155;
            display: flex;
            flex-direction: column;
        }
        .header {
            padding: 20px;
            border-bottom: 1px solid #334155;
        }
        .header h1 {
            font-size: 1.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header p { font-size: 0.875rem; color: #94a3b8; margin-top: 4px; }
        .search-box {
            padding: 15px 20px;
            border-bottom: 1px solid #334155;
        }
        .search-box input {
            width: 100%;
            padding: 10px 15px;
            border: 1px solid #475569;
            border-radius: 8px;
            background: #0f172a;
            color: #e2e8f0;
            font-size: 0.875rem;
        }
        .search-box input:focus {
            outline: none;
            border-color: #667eea;
        }
        .stats {
            padding: 15px 20px;
            border-bottom: 1px solid #334155;
        }
        .stat-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            font-size: 0.875rem;
        }
        .stat-label { color: #94a3b8; }
        .stat-value { color: #667eea; font-weight: 600; }
        .node-details {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
        }
        .node-details h3 {
            font-size: 1rem;
            margin-bottom: 15px;
            color: #f8fafc;
        }
        .detail-item {
            padding: 10px 0;
            border-bottom: 1px solid #334155;
            font-size: 0.875rem;
        }
        .detail-label { color: #94a3b8; margin-bottom: 4px; }
        .detail-value { color: #e2e8f0; word-break: break-all; }
        .main-content {
            flex: 1;
            position: relative;
        }
        #graph-container {
            width: 100%;
            height: 100%;
        }
        .legend {
            position: absolute;
            bottom: 20px;
            right: 20px;
            background: rgba(30, 41, 59, 0.95);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #334155;
        }
        .legend h4 { font-size: 0.75rem; color: #94a3b8; margin-bottom: 10px; text-transform: uppercase; }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 6px 0;
            font-size: 0.75rem;
        }
        .legend-color {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }
        .loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
        }
        .spinner {
            width: 40px;
            height: 40px;
            border: 3px solid #334155;
            border-top-color: #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <div class="header">
                <h1>🔮 CodeGraph Insight</h1>
                <p>智能代码知识图谱分析工具</p>
            </div>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="搜索函数、类、文件...">
            </div>
            <div class="stats" id="stats">
                <div class="stat-item">
                    <span class="stat-label">总节点数</span>
                    <span class="stat-value" id="totalNodes">-</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">总边数</span>
                    <span class="stat-value" id="totalEdges">-</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">文件数</span>
                    <span class="stat-value" id="totalFiles">-</span>
                </div>
            </div>
            <div class="node-details" id="nodeDetails">
                <h3>👈 点击节点查看详情</h3>
            </div>
        </div>
        <div class="main-content">
            <div id="graph-container">
                <div class="loading">
                    <div class="spinner"></div>
                    <p>正在加载知识图谱...</p>
                </div>
            </div>
            <div class="legend">
                <h4>节点类型</h4>
                <div class="legend-item"><div class="legend-color" style="background:#f87171"></div>文件</div>
                <div class="legend-item"><div class="legend-color" style="background:#60a5fa"></div>函数</div>
                <div class="legend-item"><div class="legend-color" style="background:#34d399"></div>类</div>
                <div class="legend-item"><div class="legend-color" style="background:#fbbf24"></div>接口</div>
                <div class="legend-item"><div class="legend-color" style="background:#a78bfa"></div>方法</div>
                <div class="legend-item"><div class="legend-color" style="background:#f472b6"></div>变量</div>
            </div>
        </div>
    </div>

    <script>
        const ws = new WebSocket(\`ws://\${window.location.host}\`);
        let network = null;
        let graphData = null;

        const nodeColors = {
            file: '#f87171',
            function: '#60a5fa',
            class: '#34d399',
            interface: '#fbbf24',
            method: '#a78bfa',
            variable: '#f472b6',
            import: '#94a3b8',
            export: '#94a3b8',
            property: '#94a3b8'
        };

        // 加载图谱数据
        async function loadGraph() {
            try {
                const response = await fetch('/api/graph');
                graphData = await response.json();
                renderGraph(graphData);
                updateStats(graphData);
            } catch (error) {
                console.error('加载图谱失败:', error);
            }
        }

        // 渲染图谱
        function renderGraph(data) {
            const container = document.getElementById('graph-container');
            
            const nodes = new vis.DataSet(data.nodes.map(n => ({
                id: n.id,
                label: n.name.length > 20 ? n.name.substring(0, 20) + '...' : n.name,
                title: \`\${n.name}\\n类型: \${n.type}\\n文件: \${n.filePath}\`,
                color: nodeColors[n.type] || '#94a3b8',
                shape: n.type === 'file' ? 'box' : 'dot',
                size: n.type === 'file' ? 20 : 10,
                font: { color: '#e2e8f0', size: 12 }
            })));

            const edges = new vis.DataSet(data.edges.map(e => ({
                from: e.source,
                to: e.target,
                arrows: 'to',
                color: { color: '#475569' },
                width: 1
            })));

            const options = {
                nodes: {
                    borderWidth: 2,
                    borderWidthSelected: 3,
                    shadow: true
                },
                edges: {
                    smooth: { type: 'continuous' },
                    shadow: true
                },
                physics: {
                    stabilization: false,
                    barnesHut: {
                        gravitationalConstant: -2000,
                        centralGravity: 0.3,
                        springLength: 95,
                        springConstant: 0.04,
                        damping: 0.09
                    }
                },
                interaction: {
                    hover: true,
                    tooltipDelay: 200
                }
            };

            network = new vis.Network(container, { nodes, edges }, options);

            network.on('click', function(params) {
                if (params.nodes.length > 0) {
                    const nodeId = params.nodes[0];
                    ws.send(JSON.stringify({ action: 'getNodeDetails', nodeId }));
                }
            });
        }

        // 更新统计信息
        function updateStats(data) {
            document.getElementById('totalNodes').textContent = data.nodes.length;
            document.getElementById('totalEdges').textContent = data.edges.length;
            document.getElementById('totalFiles').textContent = data.metadata.totalFiles;
        }

        // 显示节点详情
        function showNodeDetails(data) {
            const container = document.getElementById('nodeDetails');
            if (!data.node) {
                container.innerHTML = '<h3>未找到节点信息</h3>';
                return;
            }

            const node = data.node;
            let html = \`
                <h3>📄 \${node.name}</h3>
                <div class="detail-item">
                    <div class="detail-label">类型</div>
                    <div class="detail-value">\${node.type}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">文件路径</div>
                    <div class="detail-value">\${node.filePath}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">行号</div>
                    <div class="detail-value">\${node.lineStart} - \${node.lineEnd}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">语言</div>
                    <div class="detail-value">\${node.language}</div>
                </div>
            \`;

            if (node.metadata && Object.keys(node.metadata).length > 0) {
                html += '<div class="detail-item"><div class="detail-label">元数据</div></div>';
                for (const [key, value] of Object.entries(node.metadata)) {
                    html += \`<div class="detail-item" style="padding-left: 15px;"><div class="detail-value">\${key}: \${JSON.stringify(value)}</div></div>\`;
                }
            }

            if (data.neighbors && data.neighbors.length > 0) {
                html += \`
                    <div class="detail-item">
                        <div class="detail-label">关联节点 (\${data.neighbors.length})</div>
                    </div>
                \`;
                data.neighbors.slice(0, 10).forEach(neighbor => {
                    html += \`<div class="detail-item" style="padding-left: 15px;"><div class="detail-value">\${neighbor.name} (\${neighbor.type})</div></div>\`;
                });
            }

            container.innerHTML = html;
        }

        // WebSocket 消息处理
        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            switch (message.action) {
                case 'nodeDetails':
                    showNodeDetails(message.data);
                    break;
                case 'searchResults':
                    // 高亮搜索结果
                    if (network && message.data.length > 0) {
                        const nodeIds = message.data.map(n => n.id);
                        network.selectNodes(nodeIds);
                        if (nodeIds.length > 0) {
                            network.focus(nodeIds[0], { scale: 1.2 });
                        }
                    }
                    break;
            }
        };

        // 搜索功能
        document.getElementById('searchInput').addEventListener('input', (e) => {
            const query = e.target.value.trim();
            if (query.length >= 2) {
                ws.send(JSON.stringify({ action: 'search', query }));
            }
        });

        // 初始化
        loadGraph();
    </script>
</body>
</html>`;
}