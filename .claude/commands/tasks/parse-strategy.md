# Parse Strategy: $ARGUMENTS

Parse natural language strategy into structured format using Claude's language understanding.

## Input

- `$ARGUMENTS`: Path to artifact directory containing `strategy.md`

## Steps

1. **Read the natural language strategy**
   ```bash
   EXEC_DIR="$ARGUMENTS"
   STRATEGY_FILE="$EXEC_DIR/strategy.md"
   
   if [[ ! -f "$STRATEGY_FILE" ]]; then
     echo "Error: Strategy file not found at $STRATEGY_FILE"
     exit 1
   fi
   
   # Read the strategy content
   STRATEGY_CONTENT=$(cat "$STRATEGY_FILE")
   ```

2. **Analyze and extract key components using natural language understanding**
   
   I will analyze the strategy to identify:
   - **Name**: The strategy's title or primary identifier
   - **Triggers**: Conditions that should activate this strategy (time, metrics, events)
   - **Actions**: What should be done (discounts, notifications, campaigns)
   - **Success Criteria**: How to measure if the strategy worked
   - **Rollback Conditions**: When to reverse or modify actions
   - **Priority**: Urgency level based on language cues
   - **Constraints**: Any limitations or boundaries mentioned

3. **Generate structured JSON output**
   
   Based on my analysis, I'll create a JSON structure that captures:
   ```json
   {
     "name": "extracted strategy name",
     "description": "brief summary of intent",
     "triggers": [
       {
         "type": "time|metric|event",
         "condition": "natural language condition",
         "parameters": {}
       }
     ],
     "actions": [
       {
         "type": "discount|notification|ad_campaign|etc",
         "description": "what to do",
         "parameters": {
           "extracted": "from natural language"
         },
         "priority": "high|medium|low"
       }
     ],
     "success_criteria": {
       "metric": "what to measure",
       "target": "desired outcome",
       "timeframe": "when to check"
     },
     "rollback": {
       "condition": "when to rollback",
       "actions": ["what to do"]
     },
     "constraints": {
       "budget": "if mentioned",
       "time": "if mentioned",
       "other": "any other limits"
     }
   }
   ```

4. **Save parsed output to artifact directory**
   ```bash
   # Save the parsed JSON to the artifact directory
   echo "$PARSED_JSON" > "$EXEC_DIR/parsed.json"
   
   # Also create a human-readable summary
   echo "# Strategy Analysis Summary" > "$EXEC_DIR/parsed_summary.md"
   echo "" >> "$EXEC_DIR/parsed_summary.md"
   echo "**Strategy Name**: $STRATEGY_NAME" >> "$EXEC_DIR/parsed_summary.md"
   echo "**Intent**: $STRATEGY_INTENT" >> "$EXEC_DIR/parsed_summary.md"
   echo "" >> "$EXEC_DIR/parsed_summary.md"
   echo "## Identified Actions" >> "$EXEC_DIR/parsed_summary.md"
   # ... add action summaries
   
   echo "Strategy successfully parsed and saved to artifact directory"
   ```

## Output

Creates two files in the artifact directory:
- `parsed.json`: Structured representation of the strategy
- `parsed_summary.md`: Human-readable analysis summary

## Example

For a strategy like:
```markdown
# Lunch Rush Booster

When we're approaching lunch time (11:30 AM - 2:00 PM) and the restaurant 
isn't at least 80% full, I want to attract more diners by offering a 
25% discount on lunch combos and increasing our social media ad spend 
by $50 for the next 2 hours. Send push notifications to app users 
within 1 mile.

Success: Reach 85% capacity by 12:30 PM
Rollback: If we hit 95% capacity, reduce discount to 15%
```

Would produce parsed.json with:
- Time-based trigger (11:30 AM - 2:00 PM)
- Metric condition (occupancy < 80%)
- Three actions (discount, ad boost, notifications)
- Clear success metrics and rollback plan

## Error Handling

- Validates artifact directory and strategy file exist
- Uses Claude's robust language understanding to handle various formats
- Provides clear error messages if parsing fails
- Always attempts to extract as much information as possible