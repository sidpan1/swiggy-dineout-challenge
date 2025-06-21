# Execute Action

## Description
Executes a single action from the natural language strategy pipeline, reading from the artifact directory and intelligently handling the action based on its type and description.

## Inputs
- Artifact directory path (required): Contains actions.json and optional current_action_index.txt
- Environment variables:
  - DRY_RUN: If set to "1", simulates execution without making changes

## Steps

1. Read the action context from the artifact directory
   - Check if current_action_index.txt exists to determine which action to execute
   - If not present, execute the first action in actions.json
   - Extract action type, description, and parameters

2. Understand the action intent using natural language processing
   - Analyze what the action is trying to achieve
   - Consider the restaurant context if available
   - Determine appropriate execution approach

3. Execute the action based on its type
   - For "discount" actions: Create appropriate discount campaigns
   - For "notification" actions: Simulate sending targeted messages
   - For "ad_campaign" actions: Adjust advertising parameters
   - For unknown types: Use description to infer intent

4. Generate and save results
   - Create action result in results/ directory
   - Include execution status, details, and rollback information
   - Update execution log

## Output
Creates files in the artifact directory:
- `results/action_N.json`: Detailed execution result
- Updates to `execution.log`: Running log of actions
- Console output showing action status

## Error Handling
- If artifact directory doesn't exist: Exit with clear error
- If actions.json is missing: Exit with error
- If action execution fails: Save failure details and rollback info
- Always attempt to save partial results

## Example Usage
```bash
# Execute action from artifact directory
claude /project:execute-action ./artifacts/execution_20241220_143022

# Dry run mode
DRY_RUN=1 claude /project:execute-action ./artifacts/execution_20241220_143022
```