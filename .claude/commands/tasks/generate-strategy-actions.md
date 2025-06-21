# Generate Strategy Actions: $ARGUMENTS

Transform strategy intent into specific executable actions using natural language understanding.

## Input

- `$ARGUMENTS`: Path to artifact directory containing `parsed.json` and `conditions.json`

## Steps

1. **Read context from artifacts**
   ```bash
   EXEC_DIR="$ARGUMENTS"
   
   # Validate required files exist
   if [[ ! -f "$EXEC_DIR/parsed.json" ]] || [[ ! -f "$EXEC_DIR/conditions.json" ]]; then
     echo "Error: Required files not found in $EXEC_DIR"
     exit 1
   fi
   
   # Read strategy and conditions
   PARSED_STRATEGY=$(cat "$EXEC_DIR/parsed.json")
   CONDITIONS=$(cat "$EXEC_DIR/conditions.json")
   ```

2. **Analyze strategy intent and generate specific actions**
   
   Based on the natural language strategy, I'll create concrete actions:
   
   - **Interpret action descriptions**: Convert intent to executable steps
   - **Extract parameters**: Determine values from natural language
   - **Set priorities**: Infer urgency from context and language
   - **Add safety limits**: Include reasonable constraints
   - **Sequence actions**: Order for optimal execution

3. **Create detailed action specifications**
   
   For each action identified, generate:
   ```json
   {
     "actions": [
       {
         "id": "action_1",
         "type": "discount|notification|ad_campaign|menu_update|etc",
         "description": "Human-readable description",
         "parameters": {
           "specific": "values extracted from strategy",
           "percentage": 25,
           "duration_minutes": 120,
           "target_audience": "derived from context"
         },
         "priority": "high|medium|low",
         "timeout_seconds": 300,
         "rollback_enabled": true,
         "validation": {
           "max_impact": "safety limit",
           "requires_approval": false
         }
       }
     ],
     "execution_order": ["action_1", "action_2"],
     "estimated_impact": "Expected outcomes",
     "total_cost_estimate": "If applicable"
   }
   ```

4. **Save actions to artifact**
   ```bash
   # Save generated actions
   echo "$ACTIONS_JSON" > "$EXEC_DIR/actions.json"
   
   # Create action summary
   echo "# Generated Actions Plan" > "$EXEC_DIR/actions_summary.md"
   echo "" >> "$EXEC_DIR/actions_summary.md"
   echo "Based on the strategy intent, I've generated the following actions:" >> "$EXEC_DIR/actions_summary.md"
   echo "" >> "$EXEC_DIR/actions_summary.md"
   
   # List each action with details
   for action in actions; do
     echo "## Action: $ACTION_TYPE" >> "$EXEC_DIR/actions_summary.md"
     echo "- **Description**: $DESCRIPTION" >> "$EXEC_DIR/actions_summary.md"
     echo "- **Priority**: $PRIORITY" >> "$EXEC_DIR/actions_summary.md"
     echo "- **Parameters**: $PARAMS" >> "$EXEC_DIR/actions_summary.md"
     echo "" >> "$EXEC_DIR/actions_summary.md"
   done
   
   echo "Actions generated successfully"
   ```

## Action Type Mapping

Natural language intent maps to action types:

| Intent Language | Action Type | Parameters |
|----------------|-------------|------------|
| "offer discount", "reduce price" | `discount` | percentage, items, duration |
| "notify customers", "send alert" | `notification` | message, audience, channel |
| "boost ads", "increase marketing" | `ad_campaign` | budget, platform, duration |
| "update menu", "feature items" | `menu_update` | items, prominence |
| "adjust staffing" | `staff_schedule` | count, roles, shift |

## Example Transformations

**Input**: "Offer 25% discount on lunch combos"
**Output**: 
```json
{
  "type": "discount",
  "parameters": {
    "percentage": 25,
    "applicable_items": ["lunch_combo_*"],
    "duration_minutes": 120,
    "max_uses_per_customer": 1
  }
}
```

**Input**: "Send push notifications to nearby customers"
**Output**:
```json
{
  "type": "notification",
  "parameters": {
    "channel": "push",
    "radius_km": 2,
    "message": "Special lunch offer at [Restaurant]!",
    "include_discount_code": true
  }
}
```

## Output

Creates in artifact directory:
- `actions.json`: Structured action specifications
- `actions_summary.md`: Human-readable action plan

## Error Handling

- Validates all required context files exist
- Ensures all actions have required parameters
- Sets reasonable defaults for missing values
- Includes safety constraints on all actions