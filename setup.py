#!/usr/bin/env python
"""
Fallback setup.py for compatibility.
Modern installations should use pyproject.toml.
"""
try:
    from setuptools import setup
    setup()
except ImportError:
    # If setuptools is not available, try using build backend directly
    import sys
    print("Error: setuptools is not installed.", file=sys.stderr)
    print("Please install it with: pip install setuptools", file=sys.stderr)
    sys.exit(1)
