# Execute Scheduled Strategy: $ARGUMENTS

Main orchestrator for natural language strategy execution using recursive Claude commands and artifact-based communication.

## Overview

This command processes a natural language strategy through a pipeline of intelligent subtasks, with each step reading from and writing to a shared artifact directory.

## Steps

1. **Create execution artifact directory**
   ```bash
   TIMESTAMP=$(date +%Y%m%d_%H%M%S)
   EXEC_DIR="./artifacts/execution_${TIMESTAMP}"
   mkdir -p "$EXEC_DIR/results"
   echo "Created execution context: $EXEC_DIR"
   ```

2. **Copy strategy to artifact directory**
   ```bash
   # Find strategy file
   if [[ -f "./strategies/$ARGUMENTS" ]]; then
     STRATEGY_FILE="./strategies/$ARGUMENTS"
   elif [[ -f "$ARGUMENTS" ]]; then
     STRATEGY_FILE="$ARGUMENTS"
   else
     echo "Error: Strategy file not found: $ARGUMENTS"
     exit 1
   fi
   
   cp "$STRATEGY_FILE" "$EXEC_DIR/strategy.md"
   echo "Strategy copied to artifact directory"
   ```

3. **Parse strategy using Claude's understanding**
   ```bash
   echo "Parsing natural language strategy..."
   claude /project:parse-strategy "$EXEC_DIR"
   
   # Check if parsing succeeded
   if [[ ! -f "$EXEC_DIR/parsed.json" ]]; then
     echo "Error: Strategy parsing failed"
     exit 1
   fi
   ```

4. **Check execution conditions**
   ```bash
   echo "Evaluating execution conditions..."
   claude /project:check-strategy-conditions "$EXEC_DIR"
   
   # Read decision
   DECISION=$(jq -r '.decision' "$EXEC_DIR/conditions.json")
   
   if [[ "$DECISION" != "EXECUTE" ]]; then
     echo "Conditions not met. Reason: $(jq -r '.reason' "$EXEC_DIR/conditions.json")"
     echo "$DECISION" > "$EXEC_DIR/execution_status.txt"
     exit 0
   fi
   ```

5. **Generate executable actions**
   ```bash
   echo "Generating actions from strategy..."
   claude /project:generate-strategy-actions "$EXEC_DIR"
   
   if [[ ! -f "$EXEC_DIR/actions.json" ]]; then
     echo "Error: Action generation failed"
     exit 1
   fi
   ```

6. **Execute each action (if not dry run)**
   ```bash
   if [[ "$DRY_RUN" == "1" ]]; then
     echo "DRY RUN MODE - Actions that would be executed:"
     jq -r '.actions[] | "- \(.type): \(.description)"' "$EXEC_DIR/actions.json"
   else
     echo "Executing actions..."
     # Process each action through the execute-action command
     ACTION_COUNT=$(jq -r '.actions | length' "$EXEC_DIR/actions.json")
     
     for i in $(seq 0 $((ACTION_COUNT - 1))); do
       echo "Executing action $((i + 1))/$ACTION_COUNT..."
       echo "$i" > "$EXEC_DIR/current_action_index.txt"
       claude /project:execute-action "$EXEC_DIR"
     done
   fi
   ```

7. **Log execution results**
   ```bash
   echo "Logging execution..."
   claude /project:log-strategy-execution "$EXEC_DIR"
   ```

8. **Generate comprehensive report**
   ```bash
   echo "Generating execution report..."
   claude /project:generate-execution-report "$EXEC_DIR"
   
   # Display report location
   echo ""
   echo "Execution complete! Report available at:"
   echo "$EXEC_DIR/report.md"
   echo ""
   cat "$EXEC_DIR/report.md"
   ```

## Expected Artifact Structure

After execution, the artifact directory contains:
```
./artifacts/execution_20241220_143022/
├── strategy.md          # Original natural language strategy
├── parsed.json          # Claude's understanding of the strategy
├── conditions.json      # Evaluation of execution conditions
├── actions.json         # Generated executable actions
├── current_action_index.txt  # Tracking for action execution
├── results/
│   ├── action_0.json   # Result of first action
│   ├── action_1.json   # Result of second action
│   └── ...
├── execution_log.json   # Detailed execution log
└── report.md           # Human-readable execution report
```

## Usage

```bash
# Execute a strategy from strategies directory
claude /project:execute-scheduled-strategy lunch_rush.md

# Execute with full path
claude /project:execute-scheduled-strategy ./strategies/weekend_optimizer.md

# Dry run mode - analyze without executing
DRY_RUN=1 claude /project:execute-scheduled-strategy flash_sale.md

# Verbose mode
VERBOSE=1 claude /project:execute-scheduled-strategy happy_hour.md
```

## Error Handling

- Creates timestamped artifact directory for each execution
- Validates strategy file exists before processing
- Checks for successful completion of each pipeline stage
- Preserves partial results if pipeline fails
- All errors are logged to artifact directory

## Benefits

This natural language pipeline approach provides:
- **Traceability**: Complete execution history in artifacts
- **Debuggability**: Each step's output is preserved
- **Flexibility**: Strategies written in plain English
- **Intelligence**: Claude interprets intent at each stage
- **Modularity**: Each command focuses on one task