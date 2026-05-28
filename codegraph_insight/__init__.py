"""
CodeGraph-Insight: A lightweight code knowledge graph visualization tool.

Transform your codebase into an interactive knowledge graph.
Supports Python, JavaScript, TypeScript, Java, Go, and more.
"""

__version__ = "1.0.0"
__author__ = "CodeGraph Team"
__license__ = "MIT"

from .parser import CodeParser
from .graph_builder import GraphBuilder
from .visualizer import Visualizer
from .server import start_server

__all__ = ["CodeParser", "GraphBuilder", "Visualizer", "start_server"]
