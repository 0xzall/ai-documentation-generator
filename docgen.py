#!/usr/bin/env python3
"""AI Documentation Generator - Auto-generates docs from codebases."""
import os
import sys
import json
import argparse
import ast
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class FunctionDoc:
    name: str
    args: List[str]
    returns: str
    docstring: str
    complexity: int


class PythonParser:
    """Parse Python source files."""
    
    def parse_file(self, file_path: str) -> Dict:
        with open(file_path, 'r') as f:
            source = f.read()
        
        tree = ast.parse(source)
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func = FunctionDoc(
                    name=node.name,
                    args=[arg.arg for arg in node.args.args],
                    returns=ast.unparse(node.returns) if node.returns else "Any",
                    docstring=ast.get_docstring(node) or "",
                    complexity=self._calc_complexity(node)
                )
                functions.append(func)
            elif isinstance(node, ast.ClassDef):
                classes.append({
                    "name": node.name,
                    "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                    "docstring": ast.get_docstring(node) or ""
                })
        
        return {
            "file": file_path,
            "functions": functions,
            "classes": classes,
            "imports": [n.names[0].name for n in ast.walk(tree) if isinstance(n, ast.Import)]
        }
    
    def _calc_complexity(self, node: ast.FunctionDef) -> int:
        count = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                count += 1
        return count


class APIDocAgent:
    """Generate API documentation."""
    
    def generate(self, parsed: Dict) -> str:
        md = f"# API Documentation\n\n## File: `{parsed['file']}`\n\n"
        
        for cls in parsed["classes"]:
            md += f"### Class: `{cls['name']}`\n\n"
            if cls["docstring"]:
                md += f"{cls['docstring']}\n\n"
            md += f"**Methods:** {', '.join(cls['methods'])}\n\n"
        
        for func in parsed["functions"]:
            md += f"#### `{func.name}({', '.join(func.args)}) -> {func.returns}`\n\n"
            if func.docstring:
                md += f"{func.docstring}\n\n"
            md += f"- **Complexity:** {func.complexity}\n\n"
        
        return md


class TutorialAgent:
    """Generate tutorial content."""
    
    def generate(self, project_name: str, files: List[Dict]) -> str:
        md = f"# {project_name} Tutorial\n\n"
        md += "## Quick Start\n\n```bash\n"
        md += f"pip install {project_name.lower()}\n"
        md += "```\n\n"
        
        md += "## Basic Usage\n\n"
        for f in files[:3]:
            for func in f["functions"][:2]:
                md += f"### {func.name}\n\n```python\n"
                md += f"from {Path(f['file']).stem} import {func.name}\n\n"
                md += f"result = {func.name}()\n"
                md += "```\n\n"
        
        return md


class DocOrchestrator:
    """Main orchestrator."""
    
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.parser = PythonParser()
        self.api_doc = APIDocAgent()
        self.tutorial = TutorialAgent()
    
    def run(self, repo_path: str, output_dir: str) -> Dict:
        print(f"[📚] Scanning {repo_path}")
        
        all_files = []
        for py_file in Path(repo_path).rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            try:
                parsed = self.parser.parse_file(str(py_file))
                all_files.append(parsed)
            except SyntaxError:
                continue
        
        print(f"    Parsed {len(all_files)} Python files")
        
        # Generate docs
        os.makedirs(output_dir, exist_ok=True)
        
        print("[📝] Generating API docs...")
        api_md = ""
        for f in all_files:
            api_md += self.api_doc.generate(f) + "\n"
        
        with open(os.path.join(output_dir, "api_reference.md"), 'w') as f:
            f.write(api_md)
        
        print("[📖] Generating tutorial...")
        tutorial_md = self.tutorial.generate(Path(repo_path).name, all_files)
        
        with open(os.path.join(output_dir, "tutorial.md"), 'w') as f:
            f.write(tutorial_md)
        
        total_funcs = sum(len(f["functions"]) for f in all_files)
        total_classes = sum(len(f["classes"]) for f in all_files)
        
        return {
            "files_parsed": len(all_files),
            "functions_documented": total_funcs,
            "classes_documented": total_classes,
            "output_dir": output_dir,
            "generated_files": ["api_reference.md", "tutorial.md"]
        }


def main():
    parser = argparse.ArgumentParser(description="AI Documentation Generator")
    parser.add_argument("--repo", required=True, help="Repository path")
    parser.add_argument("--output", default="./docs", help="Output directory")
    args = parser.parse_args()
    
    orchestrator = DocOrchestrator()
    result = orchestrator.run(args.repo, args.output)
    
    print(f"\n[✓] Generated {len(result['generated_files'])} doc files")
    print(f"    Functions: {result['functions_documented']}")
    print(f"    Classes: {result['classes_documented']}")
    print(f"    Output: {result['output_dir']}")


if __name__ == "__main__":
    main()
