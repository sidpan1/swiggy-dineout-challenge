# Monitor Active Strategies: $ARGUMENTS

Display real-time dashboard of all active strategies and their status.

## Steps

1. List all strategies in `strategies/active/`
2. For each strategy:
   - Check if event monitor is running (for event-based)
   - Show next scheduled execution (for scheduled)
   - Display today's execution count vs limit
   - Show last execution status
3. Check system resource usage
4. Identify any strategies in error state
5. Format as a clear, readable dashboard

## Expected Output

A dashboard showing:
- Strategy name, type, priority, and status
- Execution statistics
- System health metrics
- Any alerts or warnings

## Usage

```bash
# One-time view
claude /monitor-active-strategies

# Continuous monitoring (refresh every 30s)
watch -n 30 claude /monitor-active-strategies

# Filter by status
claude /monitor-active-strategies --status error
```