# Natural Language Pipeline Commands for Restaurant Strategy Execution

This directory contains Claude Code commands that implement a natural language pipeline system for restaurant optimization. The system uses recursive Claude execution with artifact-based communication between subtasks.

## Architecture Overview

The system processes natural language strategies through a pipeline of intelligent commands that communicate via a shared artifact directory:

```
Natural Language Strategy (./strategies/*.md)
                    │
                    ▼
    ┌──────────────────────────────┐
    │ Execution Artifact Directory  │
    │ ./artifacts/execution_<ts>/   │
    │                              │
    │ • strategy.md    (original)  │
    │ • parsed.json    (analysis)  │
    │ • conditions.json (decision) │
    │ • actions.json   (plan)      │
    │ • results/       (outcomes)  │
    │ • report.md      (summary)   │
    └──────────────────────────────┘
                    ↕
         Recursive Claude Execution
                    │
    ┌───────────────┴──────────────┐
    │                              │
/project:execute-scheduled-strategy │
    ├── /project:parse-strategy    │
    ├── /project:check-conditions  │
    ├── /project:generate-actions  │
    ├── /project:execute-action    │
    ├── /project:log-execution     │
    └── /project:generate-report   │
```

## Main Commands

### Core Workflow Commands

- **`/project:execute-scheduled-strategy`** - High-level orchestrator for strategy execution
- **`/project:parse-strategy`** - Parse markdown strategy files into structured JSON
- **`/project:check-strategy-conditions`** - Evaluate if conditions are met for execution
- **`/project:generate-strategy-actions`** - Generate specific executable actions
- **`/project:execute-action`** - Route and execute individual actions
- **`/project:log-strategy-execution`** - Log results and schedule evaluations
- **`/project:generate-execution-report`** - Create comprehensive execution reports

### Supporting Commands

- **`/project:rollback-action`** - Intelligent rollback for failed actions
- **`/project:evaluate-strategy-success`** - Measure strategy effectiveness
- **`/project:monitor-active-strategies`** - Real-time strategy dashboard

### Action Sub-Commands (in `actions/` directory)

- **`/project:actions/create-discount`** - Create discount campaigns
- **`/project:actions/adjust-ad-campaign`** - Modify advertising parameters
- **`/project:actions/send-notifications`** - Send targeted customer notifications

## Natural Language Strategy Format

Strategies are written in plain English in `./strategies/*.md` files. Example:

```markdown
# Lunch Rush Optimization Strategy

When it's approaching lunch time (11:30 AM - 2:00 PM) and the restaurant 
is not yet at 80% capacity, I want to attract more customers by:

1. Offering a 25% discount on lunch specials
2. Boosting our ad spending by 50% on food delivery apps  
3. Sending push notifications to customers within 2km radius

Success criteria: Achieve 85% capacity by 12:30 PM
Rollback: If capacity exceeds 95%, reduce discount to 15%
```

## Usage Examples

### Execute a Natural Language Strategy

```bash
# Execute a strategy - creates timestamped artifact directory
claude /project:execute-scheduled-strategy lunch_rush.md

# Dry run mode - analyze without executing
DRY_RUN=1 claude /project:execute-scheduled-strategy weekend_optimizer.md

# View execution artifacts
ls -la ./artifacts/execution_*/
```

### Direct Command Usage with Artifacts

```bash
# Create execution context
EXEC_DIR="./artifacts/execution_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$EXEC_DIR"

# Copy strategy to artifacts
cp ./strategies/lunch_rush.md "$EXEC_DIR/strategy.md"

# Run pipeline steps with artifact communication
claude /project:parse-strategy "$EXEC_DIR"
claude /project:check-strategy-conditions "$EXEC_DIR" 
claude /project:generate-strategy-actions "$EXEC_DIR"
claude /project:execute-action "$EXEC_DIR"
claude /project:generate-execution-report "$EXEC_DIR"
```

### Artifact-Based Pipeline

```bash
# Each command reads from and writes to the artifact directory
# enabling natural language understanding at each step
STRATEGY="lunch_rush"
claude /project:execute-scheduled-strategy "$STRATEGY.md"

# View the execution trace
cat ./artifacts/execution_*/report.md
```

## Adding New Commands

### To add a new action type:

1. Create a new command in `actions/` directory:
   ```bash
   # .claude/commands/actions/new-action-type.md
   ```

2. Update the `/project:execute-action` command to include the new case

3. No other changes needed - the system will automatically route to your new command

### To add a new top-level command:

1. Create the command file in `.claude/commands/`
2. Follow the existing pattern of clear steps and expected outputs
3. Use project-specific references (`/project:command-name`)

## Benefits of Natural Language Pipeline

- **Natural Language Strategies**: Write strategies in plain English without complex syntax
- **Recursive Intelligence**: Claude understands context at each pipeline stage
- **Artifact-Based Communication**: Full execution trace for debugging and auditing
- **Modularity**: Each command focuses on one aspect of understanding/execution
- **Flexibility**: Easy to modify strategies without changing code
- **Context Preservation**: Artifacts maintain full context between pipeline stages
- **Intelligent Decision Making**: Claude interprets intent rather than following rigid rules

## File Structure

```
.claude/commands/
├── README.md                          # This file
├── execute-scheduled-strategy.md      # Main orchestrator
├── parse-strategy.md                  # Strategy parser
├── check-strategy-conditions.md       # Condition evaluator
├── generate-strategy-actions.md       # Action generator
├── execute-action.md                  # Action router
├── log-strategy-execution.md          # Execution logger
├── generate-execution-report.md       # Report generator
├── rollback-action.md                 # Rollback handler
├── evaluate-strategy-success.md       # Success evaluator
├── monitor-active-strategies.md       # Dashboard monitor
└── actions/                          # Action sub-commands
    ├── create-discount.md
    ├── adjust-ad-campaign.md
    └── send-notifications.md
```

## Integration with Restaurant System

These commands implement a natural language pipeline system where:

### Input
- Natural language strategies in `./strategies/*.md`
- Restaurant context and metrics (when needed)

### Processing
- Recursive Claude execution for intelligent processing
- Artifact-based communication in `./artifacts/execution_<timestamp>/`
- Each command reads context and writes results to shared artifact directory

### Output
- Execution reports in artifact directories
- Action results and rollback information
- Complete audit trail of decisions and outcomes

### Key Principles
1. **Natural Language First**: Strategies describe intent, not implementation
2. **Recursive Intelligence**: Claude interprets and executes at each stage
3. **Artifact Communication**: All inter-command data flows through artifacts
4. **Contextual Understanding**: Each command has full context from artifacts
5. **Traceable Execution**: Complete history preserved in timestamped directories