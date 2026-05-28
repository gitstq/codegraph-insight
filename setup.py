"""
Setup script for CodeGraph-Insight.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = [
        line.strip() for line in requirements_path.read_text().splitlines()
        if line.strip() and not line.startswith('#')
    ]

setup(
    name="codegraph-insight",
    version="1.0.0",
    author="CodeGraph Team",
    author_email="codegraph@example.com",
    description="Transform your codebase into an interactive knowledge graph",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/CodeGraph-Insight",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "codegraph-insight=codegraph_insight.cli:main",
            "cgi=codegraph_insight.cli:main",
        ],
    },
    keywords="code-analysis knowledge-graph visualization ast parser",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/CodeGraph-Insight/issues",
        "Source": "https://github.com/gitstq/CodeGraph-Insight",
    },
)
