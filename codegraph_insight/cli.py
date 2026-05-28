"""
CLI Module - Command-line interface for CodeGraph-Insight.
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import Optional

from .parser import CodeParser
from .graph_builder import GraphBuilder
from .visualizer import Visualizer
from .server import start_server

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI."""
    parser = argparse.ArgumentParser(
        prog='codegraph-insight',
        description='🔍 CodeGraph-Insight: Transform your codebase into an interactive knowledge graph',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  codegraph-insight analyze ./my-project
  codegraph-insight visualize ./my-project -o graph.html
  codegraph-insight serve ./my-project -p 8080
  codegraph-insight export ./my-project -f json -o data.json
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser(
        'analyze',
        help='Analyze codebase and print summary'
    )
    analyze_parser.add_argument(
        'path',
        help='Path to codebase directory'
    )
    analyze_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    # Visualize command
    visualize_parser = subparsers.add_parser(
        'visualize',
        help='Generate interactive HTML visualization'
    )
    visualize_parser.add_argument(
        'path',
        help='Path to codebase directory'
    )
    visualize_parser.add_argument(
        '-o', '--output',
        default='codegraph.html',
        help='Output HTML file path (default: codegraph.html)'
    )
    visualize_parser.add_argument(
        '--open', '-O',
        action='store_true',
        help='Open in browser after generation'
    )
    
    # Serve command
    serve_parser = subparsers.add_parser(
        'serve',
        help='Start web server for interactive visualization'
    )
    serve_parser.add_argument(
        'path',
        help='Path to codebase directory'
    )
    serve_parser.add_argument(
        '-p', '--port',
        type=int,
        default=8080,
        help='Server port (default: 8080)'
    )
    serve_parser.add_argument(
        '--no-browser',
        action='store_true',
        help='Do not open browser automatically'
    )
    
    # Export command
    export_parser = subparsers.add_parser(
        'export',
        help='Export graph data to various formats'
    )
    export_parser.add_argument(
        'path',
        help='Path to codebase directory'
    )
    export_parser.add_argument(
        '-f', '--format',
        choices=['json', 'd3', 'dot'],
        default='json',
        help='Export format (default: json)'
    )
    export_parser.add_argument(
        '-o', '--output',
        default='codegraph.json',
        help='Output file path'
    )
    
    # Search command
    search_parser = subparsers.add_parser(
        'search',
        help='Search for code entities'
    )
    search_parser.add_argument(
        'path',
        help='Path to codebase directory'
    )
    search_parser.add_argument(
        'query',
        help='Search query'
    )
    search_parser.add_argument(
        '--type', '-t',
        choices=['module', 'class', 'function', 'method', 'variable', 'import'],
        help='Filter by node type'
    )
    
    # Version command
    subparsers.add_parser(
        'version',
        help='Show version information'
    )
    
    return parser


def cmd_analyze(args) -> int:
    """Execute analyze command."""
    path = Path(args.path)
    if not path.exists():
        logger.error(f"❌ Path not found: {path}")
        return 1
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info(f"🔍 Analyzing codebase: {path}")
    
    parser = CodeParser(str(path))
    nodes, edges = parser.parse_project()
    builder = GraphBuilder(nodes, edges)
    
    print(builder.get_summary())
    
    return 0


def cmd_visualize(args) -> int:
    """Execute visualize command."""
    path = Path(args.path)
    if not path.exists():
        logger.error(f"❌ Path not found: {path}")
        return 1
    
    logger.info(f"🔍 Parsing codebase: {path}")
    parser = CodeParser(str(path))
    nodes, edges = parser.parse_project()
    builder = GraphBuilder(nodes, edges)
    
    logger.info(f"🎨 Generating visualization...")
    visualizer = Visualizer(builder)
    output_path = visualizer.generate_html(args.output)
    
    logger.info(f"✅ Visualization saved to: {output_path}")
    
    if args.open:
        visualizer.open_in_browser(output_path)
    
    return 0


def cmd_serve(args) -> int:
    """Execute serve command."""
    path = Path(args.path)
    if not path.exists():
        logger.error(f"❌ Path not found: {path}")
        return 1
    
    logger.info(f"🔍 Parsing codebase: {path}")
    parser = CodeParser(str(path))
    nodes, edges = parser.parse_project()
    builder = GraphBuilder(nodes, edges)
    
    start_server(builder, port=args.port, open_browser=not args.no_browser)
    
    return 0


def cmd_export(args) -> int:
    """Execute export command."""
    path = Path(args.path)
    if not path.exists():
        logger.error(f"❌ Path not found: {path}")
        return 1
    
    logger.info(f"🔍 Parsing codebase: {path}")
    parser = CodeParser(str(path))
    nodes, edges = parser.parse_project()
    builder = GraphBuilder(nodes, edges)
    
    logger.info(f"📦 Exporting to {args.format.upper()} format...")
    
    if args.format == 'json':
        builder.export_to_json(args.output)
    elif args.format == 'd3':
        import json
        data = builder.export_to_d3()
        with open(args.output, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"✅ Exported to: {args.output}")
    elif args.format == 'dot':
        # Export to GraphViz DOT format
        dot_content = generate_dot_format(builder)
        with open(args.output, 'w') as f:
            f.write(dot_content)
        logger.info(f"✅ Exported to: {args.output}")
    
    return 0


def cmd_search(args) -> int:
    """Execute search command."""
    path = Path(args.path)
    if not path.exists():
        logger.error(f"❌ Path not found: {path}")
        return 1
    
    logger.info(f"🔍 Parsing codebase: {path}")
    parser = CodeParser(str(path))
    nodes, edges = parser.parse_project()
    builder = GraphBuilder(nodes, edges)
    
    logger.info(f"🔎 Searching for: {args.query}")
    results = builder.search_nodes(args.query, args.type)
    
    if not results:
        print("No results found.")
        return 0
    
    print(f"\n📊 Found {len(results)} results:\n")
    print(f"{'Name':<30} {'Type':<12} {'File':<30} {'Line'}")
    print("-" * 80)
    
    for result in results:
        name = result['name'][:28] + '..' if len(result['name']) > 30 else result['name']
        file_name = result['file'][:28] + '..' if len(result['file']) > 30 else result['file']
        print(f"{name:<30} {result['type']:<12} {file_name:<30} {result['line']}")
    
    return 0


def cmd_version(args) -> int:
    """Execute version command."""
    from . import __version__
    print(f"CodeGraph-Insight v{__version__}")
    print("Transform your codebase into an interactive knowledge graph")
    print("\nSupported languages:")
    print("  • Python (.py)")
    print("  • JavaScript (.js, .jsx)")
    print("  • TypeScript (.ts, .tsx)")
    print("  • Java (.java)")
    print("  • Go (.go)")
    print("  • Rust (.rs)")
    print("  • C/C++ (.c, .cpp, .h, .hpp)")
    print("  • Ruby (.rb)")
    print("  • PHP (.php)")
    print("  • Swift (.swift)")
    print("  • Kotlin (.kt)")
    print("  • Scala (.scala)")
    return 0


def generate_dot_format(builder: GraphBuilder) -> str:
    """Generate GraphViz DOT format."""
    lines = ['digraph CodeGraph {']
    lines.append('  rankdir=TB;')
    lines.append('  node [shape=box, style=filled];')
    
    # Color mapping
    colors = {
        'module': '#4A90E2',
        'class': '#F5A623',
        'function': '#7ED321',
        'method': '#BD10E0',
        'variable': '#9013FE',
        'import': '#50E3C2',
        'decorator': '#B8E986',
        'comment': '#9B9B9B'
    }
    
    # Add nodes
    for node_id, node in builder.nodes.items():
        color = colors.get(node.node_type.value, '#999999')
        label = node.name.replace('"', '\\"')
        lines.append(f'  "{node_id}" [label="{label}", fillcolor="{color}"];')
    
    # Add edges
    for edge in builder.edges:
        lines.append(f'  "{edge.source}" -> "{edge.target}";')
    
    lines.append('}')
    return '\n'.join(lines)


def main(argv: Optional[list] = None) -> int:
    """Main entry point for CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if args.command is None:
        parser.print_help()
        return 0
    
    commands = {
        'analyze': cmd_analyze,
        'visualize': cmd_visualize,
        'serve': cmd_serve,
        'export': cmd_export,
        'search': cmd_search,
        'version': cmd_version,
    }
    
    if args.command in commands:
        return commands[args.command](args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
