"""
Graph Builder Module - Build and analyze code knowledge graph.
Uses NetworkX for graph operations and analysis.
"""

import json
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import asdict
import logging

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    logging.warning("NetworkX not available. Graph analysis features disabled.")

from .parser import CodeNode, CodeEdge, NodeType

logger = logging.getLogger(__name__)


class GraphBuilder:
    """
    Build and analyze code knowledge graph.
    Provides graph algorithms and metrics.
    """
    
    def __init__(self, nodes: Dict[str, CodeNode], edges: List[CodeEdge]):
        self.nodes = nodes
        self.edges = edges
        self.graph = None
        self._build_graph()
    
    def _build_graph(self) -> None:
        """Build NetworkX graph from nodes and edges."""
        if not NETWORKX_AVAILABLE:
            logger.warning("NetworkX not available. Using basic graph structure.")
            return
        
        self.graph = nx.DiGraph()
        
        # Add nodes
        for node_id, node in self.nodes.items():
            self.graph.add_node(
                node_id,
                name=node.name,
                node_type=node.node_type.value,
                file_path=node.file_path,
                line_start=node.line_start,
                line_end=node.line_end,
                docstring=node.docstring,
                metadata=node.metadata
            )
        
        # Add edges
        for edge in self.edges:
            if edge.source in self.nodes and edge.target in self.nodes:
                self.graph.add_edge(
                    edge.source,
                    edge.target,
                    edge_type=edge.edge_type,
                    metadata=edge.metadata
                )
        
        logger.info(f"Built graph with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics and metrics."""
        stats = {
            'total_nodes': len(self.nodes),
            'total_edges': len(self.edges),
            'node_types': {},
            'edge_types': {},
            'files': set(),
            'languages': set()
        }
        
        # Count node types
        for node in self.nodes.values():
            node_type = node.node_type.value
            stats['node_types'][node_type] = stats['node_types'].get(node_type, 0) + 1
            stats['files'].add(node.file_path)
            if 'language' in node.metadata:
                stats['languages'].add(node.metadata['language'])
        
        # Count edge types
        for edge in self.edges:
            edge_type = edge.edge_type
            stats['edge_types'][edge_type] = stats['edge_types'].get(edge_type, 0) + 1
        
        stats['total_files'] = len(stats['files'])
        stats['languages'] = list(stats['languages'])
        del stats['files']  # Remove set for JSON serialization
        
        # NetworkX metrics
        if NETWORKX_AVAILABLE and self.graph is not None:
            try:
                stats['density'] = nx.density(self.graph)
                if nx.is_strongly_connected(self.graph):
                    stats['avg_shortest_path'] = nx.average_shortest_path_length(self.graph)
                
                # Centrality metrics (top 10)
                degree_centrality = nx.degree_centrality(self.graph)
                stats['most_connected'] = sorted(
                    degree_centrality.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10]
            except Exception as e:
                logger.warning(f"Could not compute all metrics: {e}")
        
        return stats
    
    def find_entry_points(self) -> List[Dict[str, Any]]:
        """Find potential entry points (nodes with no incoming edges)."""
        entry_points = []
        
        if NETWORKX_AVAILABLE and self.graph is not None:
            for node_id in self.graph.nodes():
                if self.graph.in_degree(node_id) == 0:
                    node = self.nodes.get(node_id)
                    if node and node.node_type in (NodeType.FUNCTION, NodeType.CLASS, NodeType.MODULE):
                        entry_points.append({
                            'id': node_id,
                            'name': node.name,
                            'type': node.node_type.value,
                            'file': node.file_path
                        })
        else:
            # Manual calculation without NetworkX
            incoming = set()
            for edge in self.edges:
                incoming.add(edge.target)
            
            for node_id, node in self.nodes.items():
                if node_id not in incoming:
                    if node.node_type in (NodeType.FUNCTION, NodeType.CLASS, NodeType.MODULE):
                        entry_points.append({
                            'id': node_id,
                            'name': node.name,
                            'type': node.node_type.value,
                            'file': node.file_path
                        })
        
        return sorted(entry_points, key=lambda x: x['name'])
    
    def find_complex_nodes(self, threshold: int = 5) -> List[Dict[str, Any]]:
        """Find nodes with high complexity (many children)."""
        complex_nodes = []
        
        for node_id, node in self.nodes.items():
            if len(node.children) >= threshold:
                complex_nodes.append({
                    'id': node_id,
                    'name': node.name,
                    'type': node.node_type.value,
                    'file': node.file_path,
                    'children_count': len(node.children),
                    'children': [self.nodes.get(cid, CodeNode(cid, 'unknown', NodeType.VARIABLE, '', 0, 0)).name 
                                for cid in node.children[:10]]
                })
        
        return sorted(complex_nodes, key=lambda x: x['children_count'], reverse=True)
    
    def search_nodes(self, query: str, node_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for nodes by name or content."""
        results = []
        query_lower = query.lower()
        
        for node_id, node in self.nodes.items():
            match = False
            
            # Check name
            if query_lower in node.name.lower():
                match = True
            
            # Check code
            if query_lower in node.code.lower():
                match = True
            
            # Check docstring
            if node.docstring and query_lower in node.docstring.lower():
                match = True
            
            # Filter by type if specified
            if node_type and node.node_type.value != node_type:
                match = False
            
            if match:
                results.append({
                    'id': node_id,
                    'name': node.name,
                    'type': node.node_type.value,
                    'file': node.file_path,
                    'line': node.line_start,
                    'preview': node.code[:100] if node.code else ''
                })
        
        return sorted(results, key=lambda x: x['name'])[:50]  # Limit to 50 results
    
    def get_node_neighbors(self, node_id: str, depth: int = 1) -> Dict[str, Any]:
        """Get neighbors of a node up to specified depth."""
        if node_id not in self.nodes:
            return {'error': f'Node {node_id} not found'}
        
        node = self.nodes[node_id]
        result = {
            'node': {
                'id': node_id,
                'name': node.name,
                'type': node.node_type.value,
                'file': node.file_path,
                'line': node.line_start,
                'code': node.code[:500] if node.code else ''
            },
            'parents': [],
            'children': [],
            'dependencies': []
        }
        
        # Get immediate relationships
        for edge in self.edges:
            if edge.source == node_id:
                target = self.nodes.get(edge.target)
                if target:
                    result['children'].append({
                        'id': edge.target,
                        'name': target.name,
                        'type': target.node_type.value,
                        'relationship': edge.edge_type
                    })
            elif edge.target == node_id:
                source = self.nodes.get(edge.source)
                if source:
                    result['parents'].append({
                        'id': edge.source,
                        'name': source.name,
                        'type': source.node_type.value,
                        'relationship': edge.edge_type
                    })
        
        return result
    
    def get_call_graph(self) -> Dict[str, List[str]]:
        """Extract call graph showing function/method relationships."""
        call_graph = {}
        
        for node_id, node in self.nodes.items():
            if node.node_type in (NodeType.FUNCTION, NodeType.METHOD):
                calls = []
                for edge in self.edges:
                    if edge.source == node_id and edge.edge_type == 'calls':
                        target = self.nodes.get(edge.target)
                        if target:
                            calls.append(target.name)
                if calls:
                    call_graph[node.name] = calls
        
        return call_graph
    
    def export_to_d3(self) -> Dict[str, Any]:
        """Export graph in D3.js compatible format."""
        nodes_list = []
        links_list = []
        
        # Color mapping for node types
        color_map = {
            'module': '#4A90E2',
            'class': '#F5A623',
            'function': '#7ED321',
            'method': '#BD10E0',
            'variable': '#9013FE',
            'import': '#50E3C2',
            'decorator': '#B8E986',
            'comment': '#9B9B9B'
        }
        
        for node_id, node in self.nodes.items():
            node_data = {
                'id': node_id,
                'name': node.name,
                'type': node.node_type.value,
                'file': node.file_path,
                'line': node.line_start,
                'color': color_map.get(node.node_type.value, '#999'),
                'radius': self._calculate_node_size(node),
                'metadata': node.metadata
            }
            nodes_list.append(node_data)
        
        for edge in self.edges:
            if edge.source in self.nodes and edge.target in self.nodes:
                links_list.append({
                    'source': edge.source,
                    'target': edge.target,
                    'type': edge.edge_type
                })
        
        return {
            'nodes': nodes_list,
            'links': links_list
        }
    
    def _calculate_node_size(self, node: CodeNode) -> int:
        """Calculate visual size for a node based on importance."""
        base_size = 5
        
        # Increase size based on node type
        if node.node_type == NodeType.MODULE:
            base_size += 10
        elif node.node_type == NodeType.CLASS:
            base_size += 7
        elif node.node_type in (NodeType.FUNCTION, NodeType.METHOD):
            base_size += 5
        
        # Increase size based on number of children
        base_size += min(len(node.children) * 0.5, 10)
        
        return int(base_size)
    
    def export_to_json(self, output_path: str) -> None:
        """Export graph to JSON file."""
        data = self.export_to_d3()
        data['statistics'] = self.get_statistics()
        data['entry_points'] = self.find_entry_points()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported graph to {output_path}")
    
    def get_summary(self) -> str:
        """Get a text summary of the codebase."""
        stats = self.get_statistics()
        
        lines = [
            "=" * 60,
            "📊 CodeGraph-Insight Analysis Summary",
            "=" * 60,
            "",
            f"📁 Total Files: {stats.get('total_files', 0)}",
            f"🔹 Total Nodes: {stats.get('total_nodes', 0)}",
            f"🔗 Total Edges: {stats.get('total_edges', 0)}",
            f"🌐 Languages: {', '.join(stats.get('languages', []))}",
            "",
            "📈 Node Types:",
        ]
        
        for node_type, count in sorted(stats.get('node_types', {}).items(), 
                                       key=lambda x: x[1], reverse=True):
            lines.append(f"   • {node_type}: {count}")
        
        lines.extend([
            "",
            "🔗 Edge Types:",
        ])
        
        for edge_type, count in sorted(stats.get('edge_types', {}).items(),
                                       key=lambda x: x[1], reverse=True):
            lines.append(f"   • {edge_type}: {count}")
        
        # Entry points
        entry_points = self.find_entry_points()
        if entry_points:
            lines.extend([
                "",
                "🚪 Top Entry Points:",
            ])
            for ep in entry_points[:5]:
                lines.append(f"   • {ep['name']} ({ep['type']}) - {ep['file']}")
        
        # Complex nodes
        complex_nodes = self.find_complex_nodes(threshold=3)
        if complex_nodes:
            lines.extend([
                "",
                "🏗️  Most Complex Components:",
            ])
            for cn in complex_nodes[:5]:
                lines.append(f"   • {cn['name']} - {cn['children_count']} children")
        
        lines.extend(["", "=" * 60])
        
        return '\n'.join(lines)


if __name__ == "__main__":
    # Test graph builder
    from parser import CodeParser
    import sys
    
    if len(sys.argv) > 1:
        parser = CodeParser(sys.argv[1])
        nodes, edges = parser.parse_project()
        builder = GraphBuilder(nodes, edges)
        print(builder.get_summary())
