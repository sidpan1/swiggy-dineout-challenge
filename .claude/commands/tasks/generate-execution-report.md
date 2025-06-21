# Generate Execution Report: $ARGUMENTS

Create a comprehensive report for a strategy execution.

## Steps

1. Gather all execution data:
   - Strategy definition
   - Execution context and trigger
   - Actions taken and their results
   - Current impact metrics
   - Any errors or rollbacks
2. Analyze the execution effectiveness
3. Identify patterns or insights
4. Generate recommendations for future executions
5. Format as a readable markdown report

## Expected Output

A markdown report containing:
- Executive summary
- Execution details and timeline
- Actions taken with results
- Performance impact (if measurable)
- Issues encountered and resolutions
- Recommendations for optimization
- Next scheduled execution

## Usage

```bash
claude /generate-execution-report \
  --execution-id "abc-123" \
  --include-metrics
```