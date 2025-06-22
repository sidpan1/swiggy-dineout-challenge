# Tools Documentation

## How to Run Tools

All tools in this project should be executed using `uv run` for proper dependency management:

```bash
uv run tools/[tool_name].py [arguments]
```uv run

## How to Discover Available Tools

Use the tool discovery utility to find all available tools and their documentation:

```bash
# List all available tools
uv run tools/utils/get_tools.py

# Get detailed help for a specific tool
uv run tools/utils/get_tools.py [tool_name]

This tool discovery system will show you each tool's CLI interface, usage patterns, and help documentation automatically.