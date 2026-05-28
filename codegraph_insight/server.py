"""
Server Module - Start local web server for interactive visualization.
"""

import os
import json
import logging
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import webbrowser

from .graph_builder import GraphBuilder

logger = logging.getLogger(__name__)


class GraphHandler(BaseHTTPRequestHandler):
    """HTTP request handler for serving graph visualization."""
    
    graph_data = {}
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)
        
        if path == '/' or path == '/index.html':
            self._serve_html()
        elif path == '/api/graph':
            self._serve_graph_data()
        elif path == '/api/stats':
            self._serve_stats()
        elif path == '/api/search':
            self._serve_search(query)
        elif path == '/api/node':
            self._serve_node(query)
        else:
            self._send_404()
    
    def _serve_html(self):
        """Serve main HTML page."""
        html_content = self._generate_html()
        self._send_response(200, 'text/html', html_content)
    
    def _serve_graph_data(self):
        """Serve graph data as JSON."""
        self._send_response(200, 'application/json', 
                           json.dumps(self.graph_data))
    
    def _serve_stats(self):
        """Serve graph statistics."""
        # This would be populated by the server
        stats = {'status': 'ok', 'nodes': len(self.graph_data.get('nodes', []))}
        self._send_response(200, 'application/json', json.dumps(stats))
    
    def _serve_search(self, query):
        """Handle search query."""
        q = query.get('q', [''])[0]
        # Simple search implementation
        results = []
        for node in self.graph_data.get('nodes', []):
            if q.lower() in node.get('name', '').lower():
                results.append(node)
        self._send_response(200, 'application/json', 
                           json.dumps({'results': results[:20]}))
    
    def _serve_node(self, query):
        """Get specific node details."""
        node_id = query.get('id', [''])[0]
        node = None
        for n in self.graph_data.get('nodes', []):
            if n.get('id') == node_id:
                node = n
                break
        self._send_response(200, 'application/json', 
                           json.dumps({'node': node}))
    
    def _send_response(self, status, content_type, content):
        """Send HTTP response."""
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        if isinstance(content, str):
            content = content.encode('utf-8')
        self.wfile.write(content)
    
    def _send_404(self):
        """Send 404 response."""
        self.send_response(404)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Not Found')
    
    def _generate_html(self) -> str:
        """Generate HTML content (simplified version)."""
        return '''<!DOCTYPE html>
<html>
<head>
    <title>CodeGraph-Insight Server</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body { margin: 0; font-family: sans-serif; background: #1a1a2e; color: white; }
        #graph { width: 100vw; height: 100vh; }
        .node { cursor: pointer; }
        .link { stroke: #999; stroke-opacity: 0.6; }
        .node-label { font-size: 10px; fill: white; pointer-events: none; }
    </style>
</head>
<body>
    <svg id="graph"></svg>
    <script>
        fetch('/api/graph')
            .then(r => r.json())
            .then(data => {
                const width = window.innerWidth;
                const height = window.innerHeight;
                const svg = d3.select('#graph').attr('viewBox', [0, 0, width, height]);
                const g = svg.append('g');
                
                const zoom = d3.zoom().on('zoom', e => g.attr('transform', e.transform));
                svg.call(zoom);
                
                const simulation = d3.forceSimulation(data.nodes)
                    .force('link', d3.forceLink(data.links).id(d => d.id).distance(100))
                    .force('charge', d3.forceManyBody().strength(-300))
                    .force('center', d3.forceCenter(width/2, height/2));
                
                const link = g.append('g').selectAll('line')
                    .data(data.links).join('line')
                    .attr('class', 'link');
                
                const node = g.append('g').selectAll('circle')
                    .data(data.nodes).join('circle')
                    .attr('class', 'node')
                    .attr('r', d => d.radius || 5)
                    .attr('fill', d => d.color || '#999')
                    .call(d3.drag()
                        .on('start', (e, d) => { if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
                        .on('drag', (e, d) => { d.fx = e.x; d.fy = e.y; })
                        .on('end', (e, d) => { if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; }));
                
                const labels = g.append('g').selectAll('text')
                    .data(data.nodes).join('text')
                    .attr('class', 'node-label')
                    .attr('dy', 15)
                    .text(d => d.name);
                
                simulation.on('tick', () => {
                    link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
                        .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
                    node.attr('cx', d => d.x).attr('cy', d => d.y);
                    labels.attr('x', d => d.x).attr('y', d => d.y);
                });
            });
    </script>
</body>
</html>'''


def start_server(graph_builder: GraphBuilder, port: int = 8080, 
                 open_browser: bool = True) -> None:
    """
    Start local web server for interactive visualization.
    
    Args:
        graph_builder: GraphBuilder instance with parsed code
        port: Port number for server
        open_browser: Whether to open browser automatically
    """
    # Set graph data for handler
    GraphHandler.graph_data = graph_builder.export_to_d3()
    
    # Create server
    server = HTTPServer(('localhost', port), GraphHandler)
    
    logger.info(f"🚀 Starting CodeGraph-Insight server on http://localhost:{port}")
    
    # Start server in separate thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # Open browser
    if open_browser:
        webbrowser.open(f'http://localhost:{port}')
    
    logger.info(f"✅ Server running! Press Ctrl+C to stop")
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("\n🛑 Shutting down server...")
        server.shutdown()
        logger.info("👋 Server stopped")


if __name__ == "__main__":
    # Test server
    from parser import CodeParser
    import sys
    
    if len(sys.argv) > 1:
        parser = CodeParser(sys.argv[1])
        nodes, edges = parser.parse_project()
        builder = GraphBuilder(nodes, edges)
        start_server(builder)
