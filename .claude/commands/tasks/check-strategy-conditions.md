# Check Strategy Conditions: $ARGUMENTS

Evaluate whether conditions are met for strategy execution using natural language understanding and contextual analysis.

## Input

- `$ARGUMENTS`: Path to artifact directory containing `parsed.json`

## Steps

1. **Read parsed strategy from artifact**
   ```bash
   EXEC_DIR="$ARGUMENTS"
   PARSED_FILE="$EXEC_DIR/parsed.json"
   
   if [[ ! -f "$PARSED_FILE" ]]; then
     echo "Error: Parsed strategy not found at $PARSED_FILE"
     exit 1
   fi
   
   # Read the parsed strategy
   PARSED_STRATEGY=$(cat "$PARSED_FILE")
   ```

2. **Evaluate each trigger condition**
   
   I will analyze the triggers from the parsed strategy and check:
   
   - **Time-based triggers**: Compare current time with specified windows
   - **Metric-based triggers**: Evaluate restaurant metrics against thresholds
   - **Event-based triggers**: Check for specific events or states
   - **Combined conditions**: Handle AND/OR logic in natural language

3. **Consider business context and constraints**
   
   Beyond the explicit triggers, I'll evaluate:
   
   - **Execution history**: Has this strategy run recently? Too frequently?
   - **Resource availability**: Are discounts/budgets within limits?
   - **Conflict detection**: Would this interfere with other active strategies?
   - **Safety checks**: Is it safe to execute given current conditions?

4. **Make execution decision**
   
   Based on all factors, I'll determine:
   ```json
   {
     "decision": "EXECUTE|SKIP|DEFER",
     "reason": "Natural language explanation",
     "details": {
       "triggers_met": ["list of satisfied conditions"],
       "triggers_not_met": ["list of unsatisfied conditions"],
       "constraints": ["any limiting factors"],
       "recommendations": ["suggestions if skipping"]
     },
     "confidence": 0.95,
     "next_check": "when to re-evaluate if deferred"
   }
   ```

5. **Save decision to artifact**
   ```bash
   # Save the decision to artifact directory
   echo "$DECISION_JSON" > "$EXEC_DIR/conditions.json"
   
   # Create human-readable evaluation summary
   echo "# Condition Evaluation Report" > "$EXEC_DIR/conditions_summary.md"
   echo "" >> "$EXEC_DIR/conditions_summary.md"
   echo "**Decision**: $DECISION" >> "$EXEC_DIR/conditions_summary.md"
   echo "**Reason**: $REASON" >> "$EXEC_DIR/conditions_summary.md"
   echo "" >> "$EXEC_DIR/conditions_summary.md"
   echo "## Detailed Analysis" >> "$EXEC_DIR/conditions_summary.md"
   # ... add detailed evaluation
   
   echo "Condition evaluation complete: $DECISION"
   ```

## Decision Logic

### EXECUTE
- All required triggers are satisfied
- No blocking constraints exist
- Resources are available
- No conflicts with other strategies

### SKIP  
- One or more required conditions not met
- Explicit constraints violated
- Recently executed (cooldown period)

### DEFER
- Conditions might be met soon
- Waiting for better timing
- Resource temporarily unavailable

## Example Evaluations

**Scenario 1: Time + Metric Trigger**
```
Strategy: "Lunch rush when occupancy < 80%"
Current: 11:45 AM, occupancy at 65%
Decision: EXECUTE - Both conditions met
```

**Scenario 2: Budget Constraint**
```
Strategy: "Offer 30% discount"
Current: Daily discount budget 90% used
Decision: SKIP - Budget constraint would be exceeded
```

**Scenario 3: Recent Execution**
```
Strategy: "Happy hour promotion"
Current: Same strategy ran 2 hours ago
Decision: DEFER - Wait for cooldown period (4 hours)
```

## Output

Creates in artifact directory:
- `conditions.json`: Structured decision and reasoning
- `conditions_summary.md`: Human-readable evaluation report

## Error Handling

- Validates artifact directory and parsed strategy exist
- Handles missing or incomplete trigger data gracefully
- Provides clear reasoning for all decisions
- Defaults to SKIP with explanation if uncertain