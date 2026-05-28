"""
Code Parser Module - Parse source code and extract AST information.
Supports Python, JavaScript, TypeScript, Java, Go, and more.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NodeType(Enum):
    """Types of code entities."""
    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"
    VARIABLE = "variable"
    IMPORT = "import"
    DECORATOR = "decorator"
    COMMENT = "comment"


@dataclass
class CodeNode:
    """Represents a node in the code graph."""
    id: str
    name: str
    node_type: NodeType
    file_path: str
    line_start: int
    line_end: int
    code: str = ""
    docstring: str = ""
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CodeEdge:
    """Represents an edge/relationship in the code graph."""
    source: str
    target: str
    edge_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class CodeParser:
    """
    Universal code parser supporting multiple languages.
    Uses regex-based parsing for lightweight operation.
    """
    
    SUPPORTED_EXTENSIONS = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.go': 'go',
        '.rs': 'rust',
        '.cpp': 'cpp',
        '.c': 'c',
        '.h': 'c',
        '.hpp': 'cpp',
        '.rb': 'ruby',
        '.php': 'php',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.scala': 'scala',
    }
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path).resolve()
        self.nodes: Dict[str, CodeNode] = {}
        self.edges: List[CodeEdge] = []
        self.files_processed = 0
        self.node_counter = 0
        
    def _generate_id(self) -> str:
        """Generate unique node ID."""
        self.node_counter += 1
        return f"node_{self.node_counter}"
    
    def parse_project(self) -> Tuple[Dict[str, CodeNode], List[CodeEdge]]:
        """
        Parse entire project and build code graph.
        
        Returns:
            Tuple of (nodes dict, edges list)
        """
        logger.info(f"🔍 Starting to parse project: {self.root_path}")
        
        # Find all source files
        source_files = self._find_source_files()
        logger.info(f"📁 Found {len(source_files)} source files")
        
        # Parse each file
        for file_path in source_files:
            try:
                self._parse_file(file_path)
                self.files_processed += 1
            except Exception as e:
                logger.warning(f"⚠️  Failed to parse {file_path}: {e}")
        
        # Build cross-file dependencies
        self._build_dependencies()
        
        logger.info(f"✅ Parsing complete! Processed {self.files_processed} files")
        logger.info(f"📊 Found {len(self.nodes)} nodes and {len(self.edges)} edges")
        
        return self.nodes, self.edges
    
    def _find_source_files(self) -> List[Path]:
        """Find all supported source files in project."""
        source_files = []
        
        # Skip common non-source directories
        skip_dirs = {
            'node_modules', 'venv', '.git', '__pycache__', '.venv',
            'dist', 'build', '.idea', '.vscode', 'target', 'vendor',
            'coverage', '.pytest_cache', '.mypy_cache', '.tox'
        }
        
        for path in self.root_path.rglob('*'):
            if path.is_file() and path.suffix in self.SUPPORTED_EXTENSIONS:
                # Check if file is in skipped directory
                if any(skip_dir in str(path) for skip_dir in skip_dirs):
                    continue
                source_files.append(path)
        
        return sorted(source_files)
    
    def _parse_file(self, file_path: Path) -> None:
        """Parse a single source file."""
        language = self.SUPPORTED_EXTENSIONS.get(file_path.suffix, 'unknown')
        relative_path = file_path.relative_to(self.root_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            logger.warning(f"Cannot read {file_path}: {e}")
            return
        
        # Create module node
        module_id = self._generate_id()
        module_node = CodeNode(
            id=module_id,
            name=str(relative_path),
            node_type=NodeType.MODULE,
            file_path=str(relative_path),
            line_start=1,
            line_end=len(content.splitlines()),
            code=content[:500],  # First 500 chars
            metadata={'language': language, 'size': len(content)}
        )
        self.nodes[module_id] = module_node
        
        # Parse based on language
        if language == 'python':
            self._parse_python(content, str(relative_path), module_id)
        elif language in ('javascript', 'typescript'):
            self._parse_javascript(content, str(relative_path), module_id, language)
        elif language == 'java':
            self._parse_java(content, str(relative_path), module_id)
        elif language == 'go':
            self._parse_go(content, str(relative_path), module_id)
        else:
            self._parse_generic(content, str(relative_path), module_id, language)
    
    def _parse_python(self, content: str, file_path: str, module_id: str) -> None:
        """Parse Python source code."""
        lines = content.splitlines()
        current_class = None
        
        # Pattern for class definitions
        class_pattern = re.compile(r'^class\s+(\w+)\s*(?:\([^)]*\))?:')
        # Pattern for function definitions
        func_pattern = re.compile(r'^(?:\s*)def\s+(\w+)\s*\(')
        # Pattern for imports
        import_pattern = re.compile(r'^(?:from\s+(\S+)\s+)?import\s+(.+)$')
        # Pattern for docstrings
        docstring_pattern = re.compile(r'^[\'\"]{3}(.*?)[\'\"]{3}', re.DOTALL)
        
        for line_num, line in enumerate(lines, 1):
            # Check for class
            class_match = class_pattern.match(line)
            if class_match:
                class_name = class_match.group(1)
                node_id = self._generate_id()
                node = CodeNode(
                    id=node_id,
                    name=class_name,
                    node_type=NodeType.CLASS,
                    file_path=file_path,
                    line_start=line_num,
                    line_end=line_num,
                    parent=module_id,
                    metadata={'line': line_num}
                )
                self.nodes[node_id] = node
                self.nodes[module_id].children.append(node_id)
                self.edges.append(CodeEdge(module_id, node_id, 'contains'))
                current_class = node_id
                continue
            
            # Check for function
            func_match = func_pattern.match(line)
            if func_match:
                func_name = func_match.group(1)
                node_id = self._generate_id()
                node_type = NodeType.METHOD if current_class else NodeType.FUNCTION
                node = CodeNode(
                    id=node_id,
                    name=func_name,
                    node_type=node_type,
                    file_path=file_path,
                    line_start=line_num,
                    line_end=line_num,
                    parent=current_class if current_class else module_id,
                    metadata={'line': line_num, 'signature': line.strip()}
                )
                self.nodes[node_id] = node
                parent_id = current_class if current_class else module_id
                self.nodes[parent_id].children.append(node_id)
                self.edges.append(CodeEdge(parent_id, node_id, 'contains'))
                continue
            
            # Check for imports
            import_match = import_pattern.match(line)
            if import_match:
                node_id = self._generate_id()
                node = CodeNode(
                    id=node_id,
                    name=line.strip(),
                    node_type=NodeType.IMPORT,
                    file_path=file_path,
                    line_start=line_num,
                    line_end=line_num,
                    code=line.strip(),
                    parent=module_id,
                    metadata={'line': line_num}
                )
                self.nodes[node_id] = node
                self.nodes[module_id].children.append(node_id)
                self.edges.append(CodeEdge(module_id, node_id, 'imports'))
    
    def _parse_javascript(self, content: str, file_path: str, module_id: str, language: str) -> None:
        """Parse JavaScript/TypeScript source code."""
        lines = content.splitlines()
        
        # Patterns for JS/TS
        class_pattern = re.compile(r'(?:export\s+)?class\s+(\w+)')
        func_pattern = re.compile(r'(?:export\s+)?(?:async\s+)?function\s+(\w+)')
        arrow_func_pattern = re.compile(r'(?:export\s+)?const\s+(\w+)\s*=\s*(?:async\s+)?\(')
        import_pattern = re.compile(r'import\s+.*?from\s+[\'"](.+?)[\'"]')
        require_pattern = re.compile(r'require\s*\(\s*[\'"](.+?)[\'"]\s*\)')
        
        for line_num, line in enumerate(lines, 1):
            # Class
            class_match = class_pattern.search(line)
            if class_match:
                node_id = self._generate_id()
                node = CodeNode(
                    id=node_id,
                    name=class_match.group(1),
                    node_type=NodeType.CLASS,
                    file_path=file_path,
                    line_start=line_num,
                    line_end=line_num,
                    parent=module_id,
                    metadata={'line': line_num, 'language': language}
                )
                self.nodes[node_id] = node
                self.nodes[module_id].children.append(node_id)
                self.edges.append(CodeEdge(module_id, node_id, 'contains'))
                continue
            
            # Function
            func_match = func_pattern.search(line)
            if func_match:
                node_id = self._generate_id()
                node = CodeNode(
                    id=node_id,
                    name=func_match.group(1),
                    node_type=NodeType.FUNCTION,
                    file_path=file_path,
                    line_start=line_num,
                    line_end=line_num,
                    parent=module_id,
                    metadata={'line': line_num, 'signature': line.strip()}
                )
                self.nodes[node_id] = node
                self.nodes[module_id].children.append(node_id)
                self.edges.append(CodeEdge(module_id, node_id, 'contains'))
    
    def _parse_java(self, content: str, file_path: str, module_id: str) -> None:
        """Parse Java source code."""
        lines = content.splitlines()
        
        class_pattern = re.compile(r'(?:public\s+|private\s+|protected\s+)?(?:abstract\s+)?class\s+(\w+)')
        method_pattern = re.compile(r'(?:public\s+|private\s+|protected\s+)?(?:static\s+)?(?:\w+\s+)+(\w+)\s*\(')
        import_pattern = re.compile(r'import\s+([\w.]+);')
        
        for line_num, line in enumerate(lines, 1):
            class_match = class_pattern.search(line)
            if class_match:
                node_id = self._generate_id()
                node = CodeNode(
                    id=node_id,
                    name=class_match.group(1),
                    node_type=NodeType.CLASS,
                    file_path=file_path,
                    line_start=line_num,
                    line_end=line_num,
                    parent=module_id,
                    metadata={'line': line_num}
                )
                self.nodes[node_id] = node
                self.nodes[module_id].children.append(node_id)
                self.edges.append(CodeEdge(module_id, node_id, 'contains'))
    
    def _parse_go(self, content: str, file_path: str, module_id: str) -> None:
        """Parse Go source code."""
        lines = content.splitlines()
        
        func_pattern = re.compile(r'^func\s+(?:\([^)]+\)\s+)?(\w+)')
        struct_pattern = re.compile(r'^type\s+(\w+)\s+struct')
        import_pattern = re.compile(r'import\s+\(\s*([^)]+)\)')
        
        for line_num, line in enumerate(lines, 1):
            struct_match = struct_pattern.match(line)
            if struct_match:
                node_id = self._generate_id()
                node = CodeNode(
                    id=node_id,
                    name=struct_match.group(1),
                    node_type=NodeType.CLASS,  # Treat struct as class
                    file_path=file_path,
                    line_start=line_num,
                    line_end=line_num,
                    parent=module_id,
                    metadata={'line': line_num}
                )
                self.nodes[node_id] = node
                self.nodes[module_id].children.append(node_id)
                self.edges.append(CodeEdge(module_id, node_id, 'contains'))
            
            func_match = func_pattern.match(line)
            if func_match:
                node_id = self._generate_id()
                node = CodeNode(
                    id=node_id,
                    name=func_match.group(1),
                    node_type=NodeType.FUNCTION,
                    file_path=file_path,
                    line_start=line_num,
                    line_end=line_num,
                    parent=module_id,
                    metadata={'line': line_num, 'signature': line.strip()}
                )
                self.nodes[node_id] = node
                self.nodes[module_id].children.append(node_id)
                self.edges.append(CodeEdge(module_id, node_id, 'contains'))
    
    def _parse_generic(self, content: str, file_path: str, module_id: str, language: str) -> None:
        """Generic parser for unsupported languages - extracts basic info."""
        lines = content.splitlines()
        
        # Generic patterns that work across many languages
        func_pattern = re.compile(r'(?:function|func|def|void|int|string)\s+(\w+)\s*\(')
        
        for line_num, line in enumerate(lines[:100], 1):  # Only first 100 lines
            func_match = func_pattern.search(line)
            if func_match:
                node_id = self._generate_id()
                node = CodeNode(
                    id=node_id,
                    name=func_match.group(1),
                    node_type=NodeType.FUNCTION,
                    file_path=file_path,
                    line_start=line_num,
                    line_end=line_num,
                    parent=module_id,
                    metadata={'line': line_num, 'language': language}
                )
                self.nodes[node_id] = node
                self.nodes[module_id].children.append(node_id)
                self.edges.append(CodeEdge(module_id, node_id, 'contains'))
    
    def _build_dependencies(self) -> None:
        """Build cross-file dependencies based on imports and references."""
        # This is a simplified version - in production would use more sophisticated analysis
        module_nodes = {nid: node for nid, node in self.nodes.items() 
                       if node.node_type == NodeType.MODULE}
        
        for node_id, node in self.nodes.items():
            if node.node_type == NodeType.IMPORT:
                # Try to match imports to modules
                import_text = node.code.lower()
                for mod_id, mod_node in module_nodes.items():
                    mod_name = Path(mod_node.name).stem.lower()
                    if mod_name in import_text and mod_id != node.parent:
                        self.edges.append(CodeEdge(node.parent, mod_id, 'depends_on'))


if __name__ == "__main__":
    # Test parser
    import sys
    if len(sys.argv) > 1:
        parser = CodeParser(sys.argv[1])
        nodes, edges = parser.parse_project()
        print(f"Parsed {len(nodes)} nodes and {len(edges)} edges")
