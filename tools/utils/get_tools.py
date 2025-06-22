#!/usr/bin/env python3
"""
CLI Tool Discovery Utility

Discovers and documents CLI tools by executing them with --help flag.
Provides information about available tools and their command-line interfaces.
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any


def discover_cli_tools(tools_dir: str = "tools") -> Dict[str, Dict[str, Any]]:
    """
    Discover all Python CLI tools in the tools directory and extract their help documentation.
    
    Args:
        tools_dir: Path to the tools directory (default: "tools")
        
    Returns:
        Dictionary mapping tool names to their CLI documentation and metadata
        
    Example:
        tools = discover_cli_tools()
        for tool_name, tool_info in tools.items():
            print(f"{tool_name}: {tool_info['description']}")
    """
    tools_info = {}
    tools_path = Path(tools_dir)
    
    if not tools_path.exists():
        return {"error": f"Tools directory '{tools_dir}' not found"}
    
    # Walk through tools directory
    for root, dirs, files in os.walk(tools_path):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                file_path = Path(root) / file
                tool_name = file_path.stem
                try:
                    relative_path = str(file_path.relative_to(Path.cwd()))
                except ValueError:
                    # If relative_to fails, use the path as-is
                    relative_path = str(file_path)
                
                # Try to get help documentation
                help_output = get_tool_help(relative_path)
                
                # Extract basic file info
                try:
                    with open(file_path, 'r') as f:
                        first_lines = f.readlines()[:20]  # Read first 20 lines for docstring
                    
                    # Extract module docstring
                    description = extract_module_docstring(first_lines)
                    
                except Exception as e:
                    description = f"Error reading file: {str(e)}"
                
                tool_info = {
                    "name": tool_name,
                    "path": str(file_path),
                    "relative_path": relative_path,
                    "description": description,
                    "help_output": help_output,
                    "executable": help_output.get("success", False),
                    "usage_command": f"uv run {relative_path}"
                }
                
                tools_info[tool_name] = tool_info
    
    return tools_info


def get_tool_help(tool_path: str) -> Dict[str, Any]:
    """
    Execute a tool with --help flag to get CLI documentation.
    
    Args:
        tool_path: Relative path to the tool file
        
    Returns:
        Dictionary with help output and execution status
    """
    try:
        # Try with --help flag
        result = subprocess.run(
            ["uv", "run", tool_path, "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return {
                "success": True,
                "help_text": result.stdout,
                "error": None
            }
        else:
            # Try with -h flag
            result_h = subprocess.run(
                ["uv", "run", tool_path, "-h"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result_h.returncode == 0:
                return {
                    "success": True,
                    "help_text": result_h.stdout,
                    "error": None
                }
            else:
                # Try running without arguments to see if it shows usage
                result_no_args = subprocess.run(
                    ["uv", "run", tool_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                return {
                    "success": False,
                    "help_text": result_no_args.stdout if result_no_args.stdout else result_no_args.stderr,
                    "error": f"No help available. Exit code: {result.returncode}"
                }
                
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "help_text": "",
            "error": "Tool execution timed out"
        }
    except Exception as e:
        return {
            "success": False,
            "help_text": "",
            "error": str(e)
        }


def extract_module_docstring(lines: List[str]) -> str:
    """
    Extract module docstring from the first few lines of a Python file.
    
    Args:
        lines: First few lines of the Python file
        
    Returns:
        Extracted docstring or fallback description
    """
    docstring_lines = []
    in_docstring = False
    docstring_delimiter = None
    
    for line in lines:
        line = line.strip()
        
        if not in_docstring:
            if line.startswith('"""') or line.startswith("'''"):
                docstring_delimiter = line[:3]
                in_docstring = True
                # Check if docstring starts and ends on same line
                if line.count(docstring_delimiter) >= 2 and len(line) > 3:
                    return line[3:-3].strip()
                else:
                    docstring_lines.append(line[3:])
            elif line.startswith('#') and 'usage' in line.lower():
                return line[1:].strip()
        else:
            if docstring_delimiter in line:
                # End of docstring
                break
            else:
                docstring_lines.append(line)
    
    if docstring_lines:
        return ' '.join(docstring_lines).strip()
    
    return "No description available"


def print_tool_documentation(tool_name: str = None, tools_dir: str = "tools") -> None:
    """
    Print formatted CLI documentation for a specific tool or all tools.
    
    Args:
        tool_name: Name of specific tool to document (optional)
        tools_dir: Path to tools directory
        
    Example:
        # Print all tools
        print_tool_documentation()
        
        # Print specific tool
        print_tool_documentation("evaluate")
    """
    tools = discover_cli_tools(tools_dir)
    
    if "error" in tools:
        print(f"Error: {tools['error']}")
        return
    
    if not tools:
        print("No tools found in the tools directory.")
        return
    
    if tool_name:
        # Print specific tool documentation
        if tool_name in tools:
            _print_single_tool(tools[tool_name])
        else:
            print(f"Tool '{tool_name}' not found.")
            print(f"Available tools: {', '.join(tools.keys())}")
    else:
        # Print all tools
        print("=" * 80)
        print("AVAILABLE CLI TOOLS")
        print("=" * 80)
        
        for name, info in sorted(tools.items()):
            if "error" not in info:
                _print_tool_summary(info)
                print("-" * 40)


def _print_single_tool(tool_info: Dict[str, Any]) -> None:
    """Print detailed CLI documentation for a single tool."""
    print("=" * 80)
    print(f"CLI TOOL: {tool_info['name'].upper()}")
    print("=" * 80)
    print(f"Path: {tool_info['relative_path']}")
    print(f"Usage: {tool_info['usage_command']}")
    print(f"Description: {tool_info['description']}")
    print(f"Executable: {'✅' if tool_info['executable'] else '❌'}")
    print()
    
    # Print CLI help output
    help_output = tool_info['help_output']
    if help_output['success'] and help_output['help_text']:
        print("CLI HELP:")
        print("-" * 40)
        print(help_output['help_text'])
    elif help_output['help_text']:
        print("OUTPUT (no help flag available):")
        print("-" * 40)
        print(help_output['help_text'])
    else:
        print("CLI HELP:")
        print("-" * 40)
        print("No help output available")
        if help_output['error']:
            print(f"Error: {help_output['error']}")


def _print_tool_summary(tool_info: Dict[str, Any]) -> None:
    """Print summary information for a CLI tool."""
    status = "✅" if tool_info['executable'] else "❌"
    print(f"Tool: {tool_info['name']} {status}")
    print(f"Path: {tool_info['relative_path']}")
    print(f"Usage: {tool_info['usage_command']}")
    
    description = tool_info['description']
    if len(description) > 100:
        description = description[:100] + "..."
    print(f"Description: {description}")


def get_tool_usage_examples() -> Dict[str, str]:
    """
    Provide CLI usage examples for common tools.
    
    Returns:
        Dictionary mapping tool names to CLI usage examples
    """
    return {
        "evaluate": """
# Run evaluation tool directly
uv run tools/evaluate.py

# Use evaluation functions in code
from tools.evaluate import initialize_table, insert_evaluation_record, get_evaluation_trends
        """,
        
        "initialize_session": """
# Initialize new session for restaurant R001
uv run tools/utils/initialize_session.py R001

# Use custom artifacts directory
uv run tools/utils/initialize_session.py R001 --artifacts-dir ./custom_artifacts

# Use specific session ID
uv run tools/utils/initialize_session.py R001 --session-id "abc12345"
        """,
        
        "get_tools": """
# List all available tools
uv run tools/utils/get_tools.py

# Get help for specific tool
uv run tools/utils/get_tools.py evaluate

# Show usage examples
uv run tools/utils/get_tools.py --examples
        """
    }


if __name__ == "__main__":
    """Command-line interface for tool discovery."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Discover and document available tools")
    parser.add_argument("tool", nargs="?", help="Specific tool to document")
    parser.add_argument("--examples", action="store_true", help="Show usage examples")
    parser.add_argument("--tools-dir", default="tools", help="Tools directory path")
    
    args = parser.parse_args()
    
    if args.examples:
        examples = get_tool_usage_examples()
        print("=" * 80)
        print("TOOL USAGE EXAMPLES")
        print("=" * 80)
        for tool_name, example in examples.items():
            print(f"\n{tool_name.upper()}:")
            print("-" * 40)
            print(example)
    else:
        print_tool_documentation(args.tool, args.tools_dir)