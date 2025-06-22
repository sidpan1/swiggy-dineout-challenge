# Build a Tool Initiative

## Core Directive

When you need to write code to accomplish a task, you should prioritize building **reusable, generic tools** that can be used across multiple instances and use cases rather than writing one-off scripts or inline solutions.

## Development Philosophy

### Build Tools, Not Scripts
- **Instead of**: Writing custom code directly in the conversation
- **Do this**: Create a generic tool in the `tools/` directory that solves the broader problem
- **Benefit**: Future tasks can reuse the tool, building a comprehensive toolkit over time

### Tool Design Principles

#### 1. **Generic Over Specific**
```bash
# Bad: Specific one-off script
python analyze_r001_data.py

# Good: Generic tool that works for any restaurant
uv run tools/analysis/analyze_restaurant.py --restaurant-id R001
```

#### 2. **CLI-First Design**
- Every tool should have a command-line interface with `--help`
- Support both CLI usage and programmatic import
- Use argparse for consistent argument handling

#### 3. **Self-Documenting**
- Comprehensive docstrings following the established pattern
- CLI help that explains all parameters and usage patterns
- Examples in the tool documentation

#### 4. **Composable**
- Tools should work well together via pipes and chaining
- Output formats that can be consumed by other tools
- Clear input/output contracts

## When to Build a Tool

### Build a Tool When:
✅ **Repeatable Task**: The operation might be needed again  
✅ **Data Processing**: Manipulating, transforming, or analyzing data  
✅ **File Operations**: Complex file manipulation or generation  
✅ **Database Operations**: Beyond simple queries  
✅ **Analysis Workflows**: Multi-step analytical processes  
✅ **Validation/Testing**: Checking data quality or system state  
✅ **Report Generation**: Creating structured outputs  

### Don't Build a Tool When:
❌ **One-time exploration**: Quick data inspection or debugging  
❌ **Simple file reads**: Basic file viewing or simple operations  
❌ **Trivial calculations**: Simple math that doesn't need persistence  
❌ **Quick fixes**: Temporary workarounds or patches  

## Tool Creation Workflow

### 1. **Identify the Generic Use Case**
```
Task: "Generate a performance report for restaurant R001"
Generic Use Case: "Generate performance reports for any restaurant"
Tool Name: generate_performance_report.py
```

### 2. **Choose the Right Category**
- `tools/analysis/` - Data analysis and reporting tools
- `tools/data/` - Data manipulation and processing tools  
- `tools/validation/` - Testing and validation tools
- `tools/generation/` - Content and report generation tools
- `tools/evaluation/` - Evaluation and scoring tools (existing)
- `tools/utils/` - General utility tools (existing)

### 3. **Design the CLI Interface**
```bash
# Example: Restaurant analysis tool
uv run tools/analysis/analyze_restaurant.py \
  --restaurant-id R001 \
  --metrics "revenue,bookings,ratings" \
  --period "30d" \
  --output-format "json|markdown|csv" \
  --output-file "report.md"
```

### 4. **Implement with Standard Pattern**
```python
#!/usr/bin/env python3
"""
[Tool Name] - [One-line Description]

[Detailed description of what the tool does and why it's useful]

Usage:
    uv run tools/[category]/[tool_name].py [arguments]

Author: Swiggy Dineout Challenge
Version: 1.0
"""

import argparse
from typing import Dict, List, Any

def main_function(param1: str, param2: int) -> Dict[str, Any]:
    """
    Main tool function with comprehensive documentation.
    
    Args:
        param1: Description of parameter
        param2: Description of parameter
        
    Returns:
        Dictionary with results
        
    Example:
        >>> result = main_function("test", 42)
        >>> print(result)
    """
    # Implementation here
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="[Tool Description]")
    parser.add_argument("--param1", required=True, help="Parameter description")
    parser.add_argument("--param2", type=int, default=10, help="Parameter description")
    
    args = parser.parse_args()
    
    try:
        result = main_function(args.param1, args.param2)
        print("✅ Tool completed successfully")
        # Output results
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        exit(1)
```

## Tool Integration

### Make Tools Discoverable
- Tools are automatically discovered by `uv run tools/utils/get_tools.py`
- No manual registration needed
- CLI help is automatically extracted

### Support Both Usage Patterns
```python
# CLI Usage
uv run tools/analysis/analyze_restaurant.py --restaurant-id R001

# Programmatic Usage
from tools.analysis.analyze_restaurant import analyze_restaurant_data
result = analyze_restaurant_data("R001", metrics=["revenue"])
```

### Enable Tool Chaining
```bash
# Example: Chain tools together
uv run tools/data/extract_metrics.py --restaurant-id R001 | \
uv run tools/analysis/calculate_trends.py | \
uv run tools/generation/create_report.py --format markdown
```

## Quality Standards

### Code Quality
- Type hints for all parameters and returns
- Comprehensive error handling with meaningful messages
- Input validation and sanitization
- Performance considerations for large datasets

### Documentation Quality
- Clear, actionable help messages
- Usage examples in docstrings
- Parameter descriptions that explain purpose and format
- Return value documentation

### User Experience
- Consistent argument naming across tools
- Meaningful output with progress indicators
- Clear success/failure messaging
- Helpful error messages with suggested fixes

## Implementation Strategy

### Start with the End Goal
1. What specific problem are you solving right now?
2. What's the generic version of this problem?
3. How would this tool be used in 3-6 months?
4. What parameters would make it flexible for other use cases?

### Build Incrementally
1. Create the minimal viable tool that solves the immediate need
2. Add CLI arguments for the most common variations
3. Enhance with additional features based on usage patterns
4. Refactor for performance and maintainability

### Test and Validate
1. Test with the current use case
2. Verify CLI help is clear and complete
3. Confirm the tool is discoverable via `get_tools`
4. Validate that it handles edge cases gracefully

## Remember

Building tools takes slightly more time upfront but creates exponential value over time. Every tool you build becomes part of a growing ecosystem that makes future development faster and more reliable.

**Think toolkit, not script collection.**