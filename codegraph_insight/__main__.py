"""
Entry point for running CodeGraph-Insight as a module.
Usage: python -m codegraph_insight
"""

from .cli import main
import sys

if __name__ == "__main__":
    sys.exit(main())
