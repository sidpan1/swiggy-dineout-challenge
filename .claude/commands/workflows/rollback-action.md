# Rollback Action: $ARGUMENTS

Execute intelligent rollback for a failed action.

## Steps

1. Parse the failed action details and current system state
2. Determine the appropriate rollback strategy based on:
   - Action type and parameters
   - How far the action progressed before failing
   - Current system state
   - Dependencies on other actions
3. Generate specific rollback commands
4. Execute rollback with verification
5. Log rollback completion

## Expected Output

- Rollback execution status
- System state after rollback
- Any manual interventions required

## Usage

```bash
claude /rollback-action \
  --action "DISCOUNT|30% weekend special|FAILED" \
  --reason "API timeout" \
  --state "partial_creation"
```