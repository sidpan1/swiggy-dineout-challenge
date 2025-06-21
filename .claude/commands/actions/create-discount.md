# Create Discount

## Description
Creates a discount campaign for a restaurant based on natural language parameters from the strategy pipeline.

## Inputs
- Artifact directory path (required): Contains action details in actions.json
- Action index (optional): From current_action_index.txt, defaults to first action

## Steps

1. Read discount parameters from the artifact directory
   - Extract percentage, duration, applicable items
   - Understand the intent behind the discount

2. Generate appropriate discount configuration
   - Create memorable discount code (e.g., LUNCH25, WEEKEND20)
   - Set reasonable limits to prevent abuse
   - Define validity period
   - Specify applicable menu items or categories

3. Simulate discount creation
   - In production, this would call restaurant POS APIs
   - For now, generate realistic discount details
   - Consider restaurant context and current promotions

4. Save discount details for tracking and rollback
   - Discount ID and code
   - Configuration parameters
   - Activation and expiry times
   - Rollback instructions if needed

## Output
- Success/failure status with discount details
- Rollback information saved to results directory
- Human-readable summary of the created discount

## Error Handling
- Validate discount percentage is reasonable (5-50%)
- Check for conflicting active discounts
- Ensure applicable items exist
- Default to safe values if parameters are unclear

## Example Result
```json
{
  "status": "success",
  "discount_code": "LUNCH25",
  "percentage": 25,
  "valid_until": "2024-12-20T16:30:00Z",
  "applicable_items": ["lunch_special", "combo_meals"],
  "estimated_usage": "150-200 customers",
  "message": "Discount 'LUNCH25' created successfully!"
}
```