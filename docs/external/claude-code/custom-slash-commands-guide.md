# Custom Slash Commands in Claude Code

## Overview

Claude Code supports project-specific custom slash commands that allow you to create reusable, intelligent workflows tailored to your project's needs. These commands enable Claude to execute complex, multi-step operations with natural language understanding and decision-making capabilities.

## What Are Custom Slash Commands?

Custom slash commands are project-specific instructions stored in `.claude/commands/` directory that Claude can execute when invoked with the `/project:command-name` syntax. They act as intelligent macros that can:

- Parse and understand context
- Make decisions based on conditions
- Execute multi-step workflows
- Generate reports and outputs
- Handle errors gracefully

## Creating Custom Commands

### 1. File Structure

```
.claude/
└── commands/
    ├── README.md                 # Documentation for your commands
    ├── command-one.md           # Individual command file
    ├── command-two.md           # Another command
    └── subcommands/             # Optional subdirectory for grouped commands
        └── sub-command.md
```

### 2. Command File Format

Each command is a markdown file with:
- Clear description of what the command does
- Step-by-step instructions for Claude
- Expected inputs and outputs
- Error handling guidance

Example structure:
```markdown
# Command Name

## Description
Brief description of what this command does.

## Inputs
- Parameter 1: Description
- Parameter 2: Description (optional)

## Steps
1. First step with specific instructions
2. Second step with decision logic
3. Generate output in specified format

## Output
Description of expected output format

## Error Handling
How to handle common error scenarios
```

### 3. Command Naming Convention

- Use descriptive, action-oriented names
- Use hyphens for multi-word commands: `parse-strategy.md`
- Group related commands in subdirectories: `actions/create-discount.md`
- Invoke with `/project:` prefix: `/project:parse-strategy`

## Key Features

### 1. Modularity
Commands can call other commands, enabling composition:
```bash
/project:main-workflow
    ├── /project:parse-input
    ├── /project:validate-data
    └── /project:generate-output
```

### 2. Context Awareness
Claude maintains context between command steps, allowing for intelligent decision-making based on previous results.

### 3. Natural Language Processing
Commands can include instructions for Claude to:
- Parse unstructured text
- Extract relevant information
- Make context-aware decisions
- Generate human-readable outputs

### 4. Error Recovery
Commands can include rollback procedures and error handling logic.

## Best Practices

### 1. Single Responsibility
Each command should do one thing well. Complex workflows should be broken into multiple commands.

### 2. Clear Documentation
- Describe inputs and outputs explicitly
- Include usage examples
- Document error scenarios

### 3. Idempotency
Where possible, commands should be safe to run multiple times without side effects.

### 4. Composability
Design commands to work well in pipelines:
```bash
claude /project:command-one | claude /project:command-two
```

### 5. Testing
Include dry-run modes for commands that make changes:
```bash
DRY_RUN=1 claude /project:dangerous-command
```

## Example: Simple Command

```markdown
# analyze-file.md

## Description
Analyzes a code file and provides insights about its structure and purpose.

## Inputs
- File path (required)
- Analysis depth (optional: "basic" | "detailed")

## Steps
1. Read the specified file
2. Identify the programming language
3. Extract key components:
   - Functions/methods
   - Classes/modules
   - Dependencies
4. Generate analysis based on depth parameter
5. Format output as markdown

## Output
Markdown report with:
- File overview
- Component list
- Complexity metrics
- Suggestions for improvement

## Error Handling
- If file not found: Return error message
- If file too large: Analyze first 1000 lines with warning
```

## Advanced Features

### 1. Conditional Logic
Commands can include decision points:
```markdown
3. If condition X is met:
   - Execute action A
   Otherwise:
   - Execute action B
```

### 2. Data Transformation
Commands can parse and transform data between formats:
```markdown
2. Parse JSON input and convert to:
   - CSV for reporting
   - Markdown for documentation
   - SQL for database insertion
```

### 3. External Integration
Commands can interact with external systems through Claude's available tools:
```markdown
4. Use web search to find latest API documentation
5. Fetch current data from specified endpoint
6. Generate code based on API response
```

## Common Patterns

### 1. Parser Pattern
```
/project:parse-[format] - Converts from one format to another
```

### 2. Generator Pattern
```
/project:generate-[output] - Creates new content based on inputs
```

### 3. Validator Pattern
```
/project:validate-[target] - Checks correctness of data/code
```

### 4. Executor Pattern
```
/project:execute-[action] - Performs specific actions
```

### 5. Monitor Pattern
```
/project:monitor-[resource] - Tracks and reports on resources
```

## Limitations and Considerations

1. **Scope**: Commands have access to the project directory and Claude's standard tools
2. **State**: Commands are stateless between invocations unless explicitly saving state to files
3. **Performance**: Complex commands may take time to execute
4. **Security**: Avoid hardcoding sensitive information in commands

## Getting Started

1. Create `.claude/commands/` directory in your project
2. Add your first command as a markdown file
3. Test with: `claude /project:your-command-name`
4. Iterate and refine based on results
5. Document in `.claude/commands/README.md`

## Conclusion

Custom slash commands in Claude Code provide a powerful way to create project-specific automation and workflows. By leveraging Claude's natural language understanding and decision-making capabilities, you can build intelligent tools that adapt to your project's needs while maintaining clarity and reusability.