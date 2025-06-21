# Log Strategy Execution: $ARGUMENTS

Log strategy execution details and schedule success evaluation.

## Steps

1. Accept execution results and metadata:
   - Execution ID
   - Strategy name
   - Trigger type (scheduled/event)
   - Action results
   - Timestamp
2. Format and append to strategy execution log
3. Extract success metrics from strategy definition
4. Calculate when to evaluate success based on metric requirements
5. Schedule evaluation job if needed
6. Update execution counters and statistics

## Expected Output

- Log entry confirmation with execution ID
- Scheduled evaluation time (if applicable)
- Updated execution statistics

## Usage

```bash
# Log a completed execution
claude /log-strategy-execution \
  --execution-id "abc-123" \
  --strategy "lunch_rush.md" \
  --results "results.json"
```