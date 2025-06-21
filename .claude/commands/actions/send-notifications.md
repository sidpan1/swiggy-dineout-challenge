# Send Notifications

## Description
Sends targeted notifications to customers based on natural language parameters from the strategy pipeline.

## Inputs
- Artifact directory path (required): Contains action details in actions.json
- Action index (optional): From current_action_index.txt, defaults to first action

## Steps

1. Read notification parameters from the artifact directory
   - Extract target audience, message content, and radius/criteria
   - Understand the intent and urgency of the notification

2. Determine notification strategy
   - Identify target customer segment (nearby, loyal, lapsed, etc.)
   - Choose appropriate channel (push, SMS, email)
   - Craft compelling message based on context
   - Set delivery timing for maximum impact

3. Simulate notification sending
   - In production, this would call notification service APIs
   - Generate realistic delivery metrics
   - Consider time of day and customer preferences

4. Save notification details for tracking
   - Campaign ID and delivery statistics
   - Message content and targeting criteria
   - Expected response rates
   - Performance tracking setup

## Output
- Success/failure status with delivery metrics
- Notification campaign details saved to results directory
- Summary of expected reach and impact

## Error Handling
- Validate message content is appropriate
- Check targeting criteria are reasonable
- Ensure delivery time is optimal
- Respect customer notification preferences

## Example Result
```json
{
  "status": "success",
  "campaign_id": "notif_lunch_2024122014",
  "channel": "push",
  "message": "🍽️ Craving lunch? Enjoy 25% off our special combos until 2 PM today!",
  "target_audience": {
    "radius_km": 2,
    "segment": "lunch_regulars",
    "estimated_reach": 350
  },
  "delivery_time": "2024-12-20T11:30:00Z",
  "expected_open_rate": "22%",
  "expected_conversion": "8%"
}
```