#!/usr/bin/env python3
"""
Validate marimo notebooks.

Usage:
    python validate_nb.py notebooks/Tests-and-demos.py
"""

import sys
import ast
import subprocess

def validate_python_syntax(filepath):
    """Validate Python syntax of a marimo notebook."""
    try:
        with open(filepath, 'r') as f:
            code = f.read()
        ast.parse(code)
        return True, "Syntax OK"
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"

def validate_marimo_notebook(filepath):
    """Validate a marimo notebook by checking if marimo can parse it."""
    try:
        # Try to run marimo info command to validate the notebook
        result = subprocess.run(
            ["marimo", "info", filepath],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, "Marimo validation OK"
        else:
            return False, f"Marimo validation failed: {result.stderr}"
    except FileNotFoundError:
        # marimo not installed, fall back to syntax check
        return validate_python_syntax(filepath)
    except subprocess.TimeoutExpired:
        return False, "Validation timeout"
    except Exception as e:
        return False, f"Validation error: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: validate_nb.py <notebook.py>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    # First check Python syntax
    ok, msg = validate_python_syntax(filepath)
    if not ok:
        print(f"==> ERROR: {msg}")
        sys.exit(1)
    
    # Then check marimo structure if available
    ok, msg = validate_marimo_notebook(filepath)
    print(f"==> {msg}")
    sys.exit(0 if ok else 1)
