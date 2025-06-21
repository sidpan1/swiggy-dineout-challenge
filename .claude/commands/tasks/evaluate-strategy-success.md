# Evaluate Strategy Success: $ARGUMENTS

Evaluate the success of a previously executed strategy against its defined metrics.

## Steps

1. Load the original strategy definition and execution details
2. Fetch current performance metrics for the evaluation period
3. Compare actual results against target metrics
4. Calculate success scores for each metric
5. Analyze patterns and identify contributing factors
6. Generate recommendations for strategy refinement
7. Update strategy learning database

## Expected Output

An evaluation report containing:
- Overall success score (0-100%)
- Individual metric performance
- Key insights and patterns
- Recommendations for optimization
- Suggested parameter adjustments

## Usage

```bash
# Evaluate a specific execution
claude /evaluate-strategy-success \
  --execution-id "abc-123" \
  --strategy "lunch_rush.md"

# Batch evaluate all pending
claude /evaluate-strategy-success --pending
```