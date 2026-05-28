"""
Visualizer Module - Generate interactive HTML visualization.
Uses D3.js for interactive graph visualization.
"""

import os
import json
import webbrowser
from pathlib import Path
from typing import Dict, Any, Optional
import logging

from .graph_builder import GraphBuilder

logger = logging.getLogger(__name__)


class Visualizer:
    """
    Generate interactive HTML visualization of code graph.
    Creates a standalone HTML file with embedded D3.js.
    """
    
    def __init__(self, graph_builder: GraphBuilder):
        self.graph_builder = graph_builder
        self.template_dir = Path(__file__).parent / 'templates'
    
    def generate_html(self, output_path: Optional[str] = None) -> str:
        """
        Generate interactive HTML visualization.
        
        Args:
            output_path: Path to save HTML file. If None, uses 'codegraph.html'
        
        Returns:
            Path to generated HTML file
        """
        if output_path is None:
            output_path = 'codegraph.html'
        
        # Get graph data
        graph_data = self.graph_builder.export_to_d3()
        stats = self.graph_builder.get_statistics()
        
        # Generate HTML
        html_content = self._generate_html_content(graph_data, stats)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Generated visualization: {output_path}")
        return output_path
    
    def _generate_html_content(self, graph_data: Dict, stats: Dict) -> str:
        """Generate complete HTML content with embedded D3.js."""
        
        html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeGraph-Insight Visualization</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            overflow: hidden;
        }
        
        #container {
            display: flex;
            height: 100vh;
        }
        
        #sidebar {
            width: 320px;
            background: rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            padding: 20px;
            overflow-y: auto;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        #graph-container {
            flex: 1;
            position: relative;
        }
        
        h1 {
            font-size: 1.5rem;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #4A90E2, #F5A623);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .subtitle {
            font-size: 0.85rem;
            color: #888;
            margin-bottom: 20px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 12px;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #4A90E2;
        }
        
        .stat-label {
            font-size: 0.75rem;
            color: #888;
            text-transform: uppercase;
        }
        
        .legend {
            margin-top: 20px;
        }
        
        .legend-title {
            font-size: 0.9rem;
            margin-bottom: 10px;
            color: #ccc;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            margin-bottom: 8px;
            font-size: 0.85rem;
        }
        
        .legend-color {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            margin-right: 10px;
        }
        
        #search-box {
            width: 100%;
            padding: 10px 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.05);
            color: #fff;
            font-size: 0.9rem;
            margin-bottom: 15px;
        }
        
        #search-box:focus {
            outline: none;
            border-color: #4A90E2;
        }
        
        #search-box::placeholder {
            color: #666;
        }
        
        .controls {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .control-btn {
            width: 100%;
            padding: 10px;
            margin-bottom: 8px;
            border: none;
            border-radius: 6px;
            background: rgba(74, 144, 226, 0.2);
            color: #4A90E2;
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.3s;
        }
        
        .control-btn:hover {
            background: rgba(74, 144, 226, 0.4);
        }
        
        #tooltip {
            position: absolute;
            padding: 12px;
            background: rgba(0, 0, 0, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s;
            max-width: 300px;
            z-index: 1000;
        }
        
        #tooltip h4 {
            margin-bottom: 5px;
            color: #4A90E2;
        }
        
        #tooltip p {
            font-size: 0.8rem;
            color: #ccc;
            margin: 3px 0;
        }
        
        svg {
            width: 100%;
            height: 100%;
        }
        
        .node {
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .node:hover {
            filter: brightness(1.3);
        }
        
        .link {
            stroke-opacity: 0.4;
            transition: all 0.3s;
        }
        
        .node-label {
            font-size: 10px;
            fill: #fff;
            pointer-events: none;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8);
        }
        
        .node-label-bg {
            fill: rgba(0, 0, 0, 0.6);
        }
        
        .info-panel {
            position: absolute;
            bottom: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(10px);
            padding: 15px;
            border-radius: 10px;
            max-width: 300px;
            max-height: 300px;
            overflow-y: auto;
            display: none;
        }
        
        .info-panel.active {
            display: block;
        }
        
        .info-panel h4 {
            margin-bottom: 10px;
            color: #4A90E2;
        }
        
        .info-panel p {
            font-size: 0.8rem;
            color: #ccc;
            margin: 5px 0;
        }
        
        .zoom-controls {
            position: absolute;
            bottom: 20px;
            left: 20px;
            display: flex;
            gap: 5px;
        }
        
        .zoom-btn {
            width: 36px;
            height: 36px;
            border: none;
            border-radius: 8px;
            background: rgba(0, 0, 0, 0.6);
            color: #fff;
            cursor: pointer;
            font-size: 1.2rem;
            transition: all 0.3s;
        }
        
        .zoom-btn:hover {
            background: rgba(74, 144, 226, 0.6);
        }
    </style>
</head>
<body>
    <div id="container">
        <div id="sidebar">
            <h1>🔍 CodeGraph-Insight</h1>
            <p class="subtitle">Interactive Code Knowledge Graph</p>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{total_nodes}</div>
                    <div class="stat-label">Nodes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_edges}</div>
                    <div class="stat-label">Edges</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_files}</div>
                    <div class="stat-label">Files</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{languages}</div>
                    <div class="stat-label">Languages</div>
                </div>
            </div>
            
            <input type="text" id="search-box" placeholder="🔍 Search nodes...">
            
            <div class="legend">
                <div class="legend-title">Node Types</div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #4A90E2;"></div>
                    <span>Module</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #F5A623;"></div>
                    <span>Class</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #7ED321;"></div>
                    <span>Function</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #BD10E0;"></div>
                    <span>Method</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #50E3C2;"></div>
                    <span>Import</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #9013FE;"></div>
                    <span>Variable</span>
                </div>
            </div>
            
            <div class="controls">
                <button class="control-btn" onclick="resetZoom()">🔄 Reset View</button>
                <button class="control-btn" onclick="togglePhysics()">⚡ Toggle Physics</button>
                <button class="control-btn" onclick="exportData()">💾 Export Data</button>
            </div>
        </div>
        
        <div id="graph-container">
            <svg id="graph"></svg>
            <div id="tooltip"></div>
            <div id="info-panel" class="info-panel">
                <h4>Node Details</h4>
                <div id="info-content"></div>
            </div>
            <div class="zoom-controls">
                <button class="zoom-btn" onclick="zoomIn()">+</button>
                <button class="zoom-btn" onclick="zoomOut()">−</button>
            </div>
        </div>
    </div>
    
    <script>
        // Graph data
        const graphData = {graph_data_json};
        
        // Setup SVG
        const container = document.getElementById('graph-container');
        const width = container.clientWidth;
        const height = container.clientHeight;
        
        const svg = d3.select('#graph')
            .attr('viewBox', [0, 0, width, height]);
        
        // Add zoom behavior
        const g = svg.append('g');
        
        const zoom = d3.zoom()
            .scaleExtent([0.1, 4])
            .on('zoom', (event) => {
                g.attr('transform', event.transform);
            });
        
        svg.call(zoom);
        
        // Create force simulation
        let simulation = d3.forceSimulation(graphData.nodes)
            .force('link', d3.forceLink(graphData.links).id(d => d.id).distance(100))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(d => d.radius + 10));
        
        // Create links
        const link = g.append('g')
            .attr('class', 'links')
            .selectAll('line')
            .data(graphData.links)
            .join('line')
            .attr('class', 'link')
            .attr('stroke', '#999')
            .attr('stroke-width', 1.5);
        
        // Create nodes
        const node = g.append('g')
            .attr('class', 'nodes')
            .selectAll('circle')
            .data(graphData.nodes)
            .join('circle')
            .attr('class', 'node')
            .attr('r', d => d.radius)
            .attr('fill', d => d.color)
            .attr('stroke', '#fff')
            .attr('stroke-width', 1.5)
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended));
        
        // Add labels
        const labels = g.append('g')
            .attr('class', 'labels')
            .selectAll('text')
            .data(graphData.nodes)
            .join('text')
            .attr('class', 'node-label')
            .attr('text-anchor', 'middle')
            .attr('dy', d => d.radius + 12)
            .text(d => d.name.length > 20 ? d.name.substring(0, 20) + '...' : d.name)
            .style('opacity', d => d.radius > 8 ? 1 : 0);
        
        // Tooltip
        const tooltip = d3.select('#tooltip');
        
        node.on('mouseover', function(event, d) {{
            tooltip.style('opacity', 1)
                .html(`
                    <h4>${{d.name}}</h4>
                    <p><strong>Type:</strong> ${{d.type}}</p>
                    <p><strong>File:</strong> ${{d.file}}</p>
                    <p><strong>Line:</strong> ${{d.line}}</p>
                `)
                .style('left', (event.pageX + 10) + 'px')
                .style('top', (event.pageY - 10) + 'px');
        }})
        .on('mouseout', function() {{
            tooltip.style('opacity', 0);
        }})
        .on('click', function(event, d) {{
            showNodeInfo(d);
        }});
        
        // Update positions
        simulation.on('tick', () => {{
            link
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
            
            node
                .attr('cx', d => d.x)
                .attr('cy', d => d.y);
            
            labels
                .attr('x', d => d.x)
                .attr('y', d => d.y);
        }});
        
        // Drag functions
        function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }}
        
        function dragged(event, d) {{
            d.fx = event.x;
            d.fy = event.y;
        }}
        
        function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }}
        
        // Search functionality
        document.getElementById('search-box').addEventListener('input', function(e) {{
            const query = e.target.value.toLowerCase();
            
            node.style('opacity', d => {{
                if (!query) return 1;
                return d.name.toLowerCase().includes(query) ? 1 : 0.1;
            }});
            
            link.style('opacity', d => {{
                if (!query) return 0.4;
                const sourceMatch = d.source.name.toLowerCase().includes(query);
                const targetMatch = d.target.name.toLowerCase().includes(query);
                return (sourceMatch || targetMatch) ? 0.6 : 0.05;
            }});
            
            labels.style('opacity', d => {{
                if (!query) return d.radius > 8 ? 1 : 0;
                return d.name.toLowerCase().includes(query) ? 1 : 0;
            }});
        }});
        
        // Control functions
        function resetZoom() {{
            svg.transition().duration(750).call(
                zoom.transform,
                d3.zoomIdentity
            );
        }}
        
        let physicsEnabled = true;
        function togglePhysics() {{
            physicsEnabled = !physicsEnabled;
            if (physicsEnabled) {{
                simulation.restart();
            }} else {{
                simulation.stop();
            }}
        }}
        
        function zoomIn() {{
            svg.transition().duration(300).call(zoom.scaleBy, 1.3);
        }}
        
        function zoomOut() {{
            svg.transition().duration(300).call(zoom.scaleBy, 0.7);
        }}
        
        function showNodeInfo(d) {{
            const panel = document.getElementById('info-panel');
            const content = document.getElementById('info-content');
            
            content.innerHTML = `
                <p><strong>Name:</strong> ${{d.name}}</p>
                <p><strong>Type:</strong> ${{d.type}}</p>
                <p><strong>File:</strong> ${{d.file}}</p>
                <p><strong>Line:</strong> ${{d.line}}</p>
                ${{d.metadata ? `<p><strong>Metadata:</strong> ${{JSON.stringify(d.metadata, null, 2)}}</p>` : ''}}
            `;
            
            panel.classList.add('active');
        }}
        
        function exportData() {{
            const dataStr = JSON.stringify(graphData, null, 2);
            const blob = new Blob([dataStr], {{type: 'application/json'}});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'codegraph-data.json';
            a.click();
            URL.revokeObjectURL(url);
        }}
        
        // Close info panel on background click
        svg.on('click', function(event) {{
            if (event.target.tagName === 'svg') {{
                document.getElementById('info-panel').classList.remove('active');
            }}
        }});
    </script>
</body>
</html>'''
        
        # Format statistics
        total_nodes = stats.get('total_nodes', 0)
        total_edges = stats.get('total_edges', 0)
        total_files = stats.get('total_files', 0)
        languages = len(stats.get('languages', []))
        
        # Escape and embed graph data
        graph_data_json = json.dumps(graph_data, ensure_ascii=False)
        
        # Fill template
        html = html_template.format(
            total_nodes=total_nodes,
            total_edges=total_edges,
            total_files=total_files,
            languages=languages,
            graph_data_json=graph_data_json
        )
        
        return html
    
    def open_in_browser(self, html_path: str) -> None:
        """Open visualization in default browser."""
        abs_path = os.path.abspath(html_path)
        webbrowser.open(f'file://{abs_path}')
        logger.info(f"Opened visualization in browser: {abs_path}")


if __name__ == "__main__":
    # Test visualizer
    from parser import CodeParser
    import sys
    
    if len(sys.argv) > 1:
        parser = CodeParser(sys.argv[1])
        nodes, edges = parser.parse_project()
        builder = GraphBuilder(nodes, edges)
        visualizer = Visualizer(builder)
        html_path = visualizer.generate_html()
        print(f"Generated: {html_path}")
        visualizer.open_in_browser(html_path)
