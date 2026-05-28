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
        
        # Format statistics
        total_nodes = stats.get('total_nodes', 0)
        total_edges = stats.get('total_edges', 0)
        total_files = stats.get('total_files', 0)
        languages = len(stats.get('languages', []))
        
        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="en">')
        html_parts.append('<head>')
        html_parts.append('    <meta charset="UTF-8">')
        html_parts.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html_parts.append('    <title>CodeGraph-Insight Visualization</title>')
        html_parts.append('    <script src="https://d3js.org/d3.v7.min.js"></script>')
        html_parts.append('    <style>')
        html_parts.append('        * { margin: 0; padding: 0; box-sizing: border-box; }')
        html_parts.append('        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #fff; overflow: hidden; }')
        html_parts.append('        #container { display: flex; height: 100vh; }')
        html_parts.append('        #sidebar { width: 320px; background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px); padding: 20px; overflow-y: auto; border-right: 1px solid rgba(255, 255, 255, 0.1); }')
        html_parts.append('        #graph-container { flex: 1; position: relative; }')
        html_parts.append('        h1 { font-size: 1.5rem; margin-bottom: 10px; background: linear-gradient(90deg, #4A90E2, #F5A623); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }')
        html_parts.append('        .subtitle { font-size: 0.85rem; color: #888; margin-bottom: 20px; }')
        html_parts.append('        .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }')
        html_parts.append('        .stat-card { background: rgba(255, 255, 255, 0.05); padding: 12px; border-radius: 8px; text-align: center; }')
        html_parts.append('        .stat-value { font-size: 1.5rem; font-weight: bold; color: #4A90E2; }')
        html_parts.append('        .stat-label { font-size: 0.75rem; color: #888; text-transform: uppercase; }')
        html_parts.append('        .legend { margin-top: 20px; }')
        html_parts.append('        .legend-title { font-size: 0.9rem; margin-bottom: 10px; color: #ccc; }')
        html_parts.append('        .legend-item { display: flex; align-items: center; margin-bottom: 8px; font-size: 0.85rem; }')
        html_parts.append('        .legend-color { width: 16px; height: 16px; border-radius: 50%; margin-right: 10px; }')
        html_parts.append('        #search-box { width: 100%; padding: 10px 15px; border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 8px; background: rgba(255, 255, 255, 0.05); color: #fff; font-size: 0.9rem; margin-bottom: 15px; }')
        html_parts.append('        #search-box:focus { outline: none; border-color: #4A90E2; }')
        html_parts.append('        .controls { margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.1); }')
        html_parts.append('        .control-btn { width: 100%; padding: 10px; margin-bottom: 8px; border: none; border-radius: 6px; background: rgba(74, 144, 226, 0.2); color: #4A90E2; cursor: pointer; font-size: 0.85rem; transition: all 0.3s; }')
        html_parts.append('        .control-btn:hover { background: rgba(74, 144, 226, 0.4); }')
        html_parts.append('        #tooltip { position: absolute; padding: 12px; background: rgba(0, 0, 0, 0.9); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 8px; pointer-events: none; opacity: 0; transition: opacity 0.2s; max-width: 300px; z-index: 1000; }')
        html_parts.append('        svg { width: 100%; height: 100%; }')
        html_parts.append('        .node { cursor: pointer; }')
        html_parts.append('        .node:hover { filter: brightness(1.3); }')
        html_parts.append('        .link { stroke-opacity: 0.4; }')
        html_parts.append('        .node-label { font-size: 10px; fill: #fff; pointer-events: none; text-shadow: 0 1px 3px rgba(0, 0, 0, 0.8); }')
        html_parts.append('        .info-panel { position: absolute; bottom: 20px; right: 20px; background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(10px); padding: 15px; border-radius: 10px; max-width: 300px; max-height: 300px; overflow-y: auto; display: none; }')
        html_parts.append('        .info-panel.active { display: block; }')
        html_parts.append('        .zoom-controls { position: absolute; bottom: 20px; left: 20px; display: flex; gap: 5px; }')
        html_parts.append('        .zoom-btn { width: 36px; height: 36px; border: none; border-radius: 8px; background: rgba(0, 0, 0, 0.6); color: #fff; cursor: pointer; font-size: 1.2rem; }')
        html_parts.append('    </style>')
        html_parts.append('</head>')
        html_parts.append('<body>')
        html_parts.append('    <div id="container">')
        html_parts.append('        <div id="sidebar">')
        html_parts.append('            <h1>CodeGraph-Insight</h1>')
        html_parts.append('            <p class="subtitle">Interactive Code Knowledge Graph</p>')
        html_parts.append('            <div class="stats-grid">')
        html_parts.append('                <div class="stat-card"><div class="stat-value">' + str(total_nodes) + '</div><div class="stat-label">Nodes</div></div>')
        html_parts.append('                <div class="stat-card"><div class="stat-value">' + str(total_edges) + '</div><div class="stat-label">Edges</div></div>')
        html_parts.append('                <div class="stat-card"><div class="stat-value">' + str(total_files) + '</div><div class="stat-label">Files</div></div>')
        html_parts.append('                <div class="stat-card"><div class="stat-value">' + str(languages) + '</div><div class="stat-label">Languages</div></div>')
        html_parts.append('            </div>')
        html_parts.append('            <input type="text" id="search-box" placeholder="Search nodes...">')
        html_parts.append('            <div class="legend">')
        html_parts.append('                <div class="legend-title">Node Types</div>')
        html_parts.append('                <div class="legend-item"><div class="legend-color" style="background: #4A90E2;"></div><span>Module</span></div>')
        html_parts.append('                <div class="legend-item"><div class="legend-color" style="background: #F5A623;"></div><span>Class</span></div>')
        html_parts.append('                <div class="legend-item"><div class="legend-color" style="background: #7ED321;"></div><span>Function</span></div>')
        html_parts.append('                <div class="legend-item"><div class="legend-color" style="background: #BD10E0;"></div><span>Method</span></div>')
        html_parts.append('                <div class="legend-item"><div class="legend-color" style="background: #50E3C2;"></div><span>Import</span></div>')
        html_parts.append('            </div>')
        html_parts.append('            <div class="controls">')
        html_parts.append('                <button class="control-btn" onclick="resetZoom()">Reset View</button>')
        html_parts.append('                <button class="control-btn" onclick="togglePhysics()">Toggle Physics</button>')
        html_parts.append('                <button class="control-btn" onclick="exportData()">Export Data</button>')
        html_parts.append('            </div>')
        html_parts.append('        </div>')
        html_parts.append('        <div id="graph-container">')
        html_parts.append('            <svg id="graph"></svg>')
        html_parts.append('            <div id="tooltip"></div>')
        html_parts.append('            <div id="info-panel" class="info-panel"><h4>Node Details</h4><div id="info-content"></div></div>')
        html_parts.append('            <div class="zoom-controls"><button class="zoom-btn" onclick="zoomIn()">+</button><button class="zoom-btn" onclick="zoomOut()">-</button></div>')
        html_parts.append('        </div>')
        html_parts.append('    </div>')
        html_parts.append('    <script>')
        html_parts.append('        const graphData = ' + json.dumps(graph_data, ensure_ascii=False) + ';')
        html_parts.append('        const container = document.getElementById("graph-container");')
        html_parts.append('        const width = container.clientWidth;')
        html_parts.append('        const height = container.clientHeight;')
        html_parts.append('        const svg = d3.select("#graph").attr("viewBox", [0, 0, width, height]);')
        html_parts.append('        const g = svg.append("g");')
        html_parts.append('        const zoom = d3.zoom().scaleExtent([0.1, 4]).on("zoom", (e) => g.attr("transform", e.transform));')
        html_parts.append('        svg.call(zoom);')
        html_parts.append('        let simulation = d3.forceSimulation(graphData.nodes)')
        html_parts.append('            .force("link", d3.forceLink(graphData.links).id(d => d.id).distance(100))')
        html_parts.append('            .force("charge", d3.forceManyBody().strength(-300))')
        html_parts.append('            .force("center", d3.forceCenter(width / 2, height / 2))')
        html_parts.append('            .force("collision", d3.forceCollide().radius(d => d.radius + 10));')
        html_parts.append('        const link = g.append("g").selectAll("line").data(graphData.links).join("line").attr("class", "link").attr("stroke", "#999").attr("stroke-width", 1.5);')
        html_parts.append('        const node = g.append("g").selectAll("circle").data(graphData.nodes).join("circle").attr("class", "node").attr("r", d => d.radius).attr("fill", d => d.color).attr("stroke", "#fff").attr("stroke-width", 1.5).call(d3.drag().on("start", dragstarted).on("drag", dragged).on("end", dragended));')
        html_parts.append('        const labels = g.append("g").selectAll("text").data(graphData.nodes).join("text").attr("class", "node-label").attr("text-anchor", "middle").attr("dy", d => d.radius + 12).text(d => d.name.length > 20 ? d.name.substring(0, 20) + "..." : d.name).style("opacity", d => d.radius > 8 ? 1 : 0);')
        html_parts.append('        const tooltip = d3.select("#tooltip");')
        html_parts.append('        node.on("mouseover", function(event, d) { tooltip.style("opacity", 1).html("<h4>" + d.name + "</h4><p><strong>Type:</strong> " + d.type + "</p><p><strong>File:</strong> " + d.file + "</p><p><strong>Line:</strong> " + d.line + "</p>").style("left", (event.pageX + 10) + "px").style("top", (event.pageY - 10) + "px"); })')
        html_parts.append('            .on("mouseout", function() { tooltip.style("opacity", 0); })')
        html_parts.append('            .on("click", function(event, d) { showNodeInfo(d); });')
        html_parts.append('        simulation.on("tick", () => { link.attr("x1", d => d.source.x).attr("y1", d => d.source.y).attr("x2", d => d.target.x).attr("y2", d => d.target.y); node.attr("cx", d => d.x).attr("cy", d => d.y); labels.attr("x", d => d.x).attr("y", d => d.y); });')
        html_parts.append('        function dragstarted(event, d) { if (!event.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; }')
        html_parts.append('        function dragged(event, d) { d.fx = event.x; d.fy = event.y; }')
        html_parts.append('        function dragended(event, d) { if (!event.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; }')
        html_parts.append('        document.getElementById("search-box").addEventListener("input", function(e) { const query = e.target.value.toLowerCase(); node.style("opacity", d => !query ? 1 : d.name.toLowerCase().includes(query) ? 1 : 0.1); link.style("opacity", d => !query ? 0.4 : (d.source.name.toLowerCase().includes(query) || d.target.name.toLowerCase().includes(query)) ? 0.6 : 0.05); labels.style("opacity", d => !query ? (d.radius > 8 ? 1 : 0) : d.name.toLowerCase().includes(query) ? 1 : 0); });')
        html_parts.append('        function resetZoom() { svg.transition().duration(750).call(zoom.transform, d3.zoomIdentity); }')
        html_parts.append('        let physicsEnabled = true; function togglePhysics() { physicsEnabled = !physicsEnabled; if (physicsEnabled) simulation.restart(); else simulation.stop(); }')
        html_parts.append('        function zoomIn() { svg.transition().duration(300).call(zoom.scaleBy, 1.3); }')
        html_parts.append('        function zoomOut() { svg.transition().duration(300).call(zoom.scaleBy, 0.7); }')
        html_parts.append('        function showNodeInfo(d) { const panel = document.getElementById("info-panel"); const content = document.getElementById("info-content"); content.innerHTML = "<p><strong>Name:</strong> " + d.name + "</p><p><strong>Type:</strong> " + d.type + "</p><p><strong>File:</strong> " + d.file + "</p><p><strong>Line:</strong> " + d.line + "</p>" + (d.metadata ? "<p><strong>Metadata:</strong> " + JSON.stringify(d.metadata, null, 2) + "</p>" : ""); panel.classList.add("active"); }')
        html_parts.append('        function exportData() { const dataStr = JSON.stringify(graphData, null, 2); const blob = new Blob([dataStr], {type: "application/json"}); const url = URL.createObjectURL(blob); const a = document.createElement("a"); a.href = url; a.download = "codegraph-data.json"; a.click(); URL.revokeObjectURL(url); }')
        html_parts.append('        svg.on("click", function(event) { if (event.target.tagName === "svg") document.getElementById("info-panel").classList.remove("active"); });')
        html_parts.append('    </script>')
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        return '\n'.join(html_parts)
    
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
