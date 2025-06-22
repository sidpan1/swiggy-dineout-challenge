# Analyze Performance Trends

## Description
**DETERMINISTIC WORKFLOW**: This workflow has been replaced by a Python script for efficient execution.

Analyzes 30-day restaurant performance trends to identify patterns, calculate key metrics, and detect significant changes in booking behavior, revenue generation, and customer satisfaction.

## Execution
Use the existing Python script instead of Claude command:
```bash
uv run python tools/analyze_performance_trends.py {session_id} --artifacts-dir artifacts
```

## Artifact Management
This script integrates with the artifact management protocol:
- **Input**: Loads restaurant data from `/artifacts/{session_id}/restaurant_data.json`
- **Output**: Saves analysis results to `/artifacts/{session_id}/performance_trends.json`
- **Logging**: Updates workflow execution automatically
- **Context**: Compatible with session-based artifact management

## Steps

### 1. Initialize Session Context
- Extract SESSION_ID from prompt or environment variables
- Verify session directory exists at `/artifacts/{session_id}/`
- Load session context from `/artifacts/{session_id}/session_context.md`
- Update workflow execution log: mark analyze-performance-trends as started

### 2. Load Restaurant Performance Data
Load restaurant data from the artifact store:
```bash
# Load restaurant data from shared artifact
RESTAURANT_DATA=$(cat /artifacts/{session_id}/restaurant_data.json)
```
- Extract daily bookings, cancellations, covers, revenue over 30 days
- Load customer ratings and review trends
- Extract average spend per cover trends

### 3. Calculate Key Performance Indicators

#### Booking Metrics
- **Total Bookings (30d)**: Sum of all confirmed reservations
- **Average Daily Bookings**: Total bookings / 30 days
- **Booking Growth Rate**: Compare first 15 days vs last 15 days
- **Booking Volatility**: Standard deviation of daily bookings
- **Peak Booking Days**: Identify highest performing days

#### Revenue Metrics  
- **Total Revenue (30d)**: Sum of all revenue generated
- **Average Daily Revenue**: Total revenue / 30 days
- **Revenue per Booking**: Total revenue / total bookings
- **Revenue Growth Rate**: Compare first 15 days vs last 15 days
- **Revenue Trend**: Linear regression slope over 30 days

#### Customer Experience Metrics
- **Average Rating Trend**: Track rating changes over time
- **Cancellation Rate**: Cancellations / total bookings
- **Covers per Booking**: Average party size trend
- **Spend per Cover Trend**: Average spend evolution

### 4. Identify Significant Trends

#### Growth Patterns
- **Increasing Trend**: >10% growth in last 15 days vs first 15 days
- **Declining Trend**: >10% decline in last 15 days vs first 15 days  
- **Stable Performance**: <10% variation between periods
- **Seasonal Patterns**: Weekly or weekend performance variations

#### Performance Shifts
- **Rating Improvements**: Rating increase >0.2 points
- **Rating Declines**: Rating decrease >0.2 points
- **Spend Pattern Changes**: >15% change in average spend per cover
- **Booking Behavior Changes**: Significant shifts in booking frequency

### 5. Calculate Statistical Measures

#### Trend Analysis
```python
# Calculate trend direction and strength
booking_trend = linear_regression_slope(daily_bookings)
revenue_trend = linear_regression_slope(daily_revenue)
rating_trend = linear_regression_slope(daily_ratings)

# Determine trend significance
trend_strength = abs(booking_trend) > booking_volatility * 0.5
```

#### Performance Consistency
- **Booking Consistency**: Coefficient of variation for daily bookings
- **Revenue Stability**: Standard deviation of daily revenue
- **Rating Stability**: Variance in customer ratings

### 6. Benchmark Against Historical Performance
Compare current 30-day performance with:
- Previous 30-day period (if data available)
- Restaurant's historical average
- Seasonal expectations based on cuisine/locality

### 7. Generate Trend Insights and Save Artifacts

#### Performance Summary
- Overall performance direction (improving/declining/stable)
- Key strength areas and concerning metrics
- Most significant changes identified

#### Notable Patterns
- Day-of-week performance variations
- Weekend vs weekday performance
- Rating correlation with other metrics
- Booking-to-revenue efficiency trends

### 8. Save Analysis Results to Artifacts
Save structured analysis results to the shared artifact directory:

```bash
# Save trend analysis results
cat > /artifacts/{session_id}/performance_trends.json << EOF
{
  "analysis_metadata": {
    "restaurant_id": "{restaurant_id}",
    "analysis_period": "30 days",
    "generated_at": "$(date -Iseconds)"
  },
  "trend_summary": {
    "overall_trend": "improving",
    "confidence_level": 0.85,
    "key_insights": [
      "Bookings increased 15% in last 2 weeks",
      "Average rating improved from 4.1 to 4.3",
      "Revenue per booking decreased 5%"
    ]
  },
  "performance_metrics": {
    "total_bookings": 245,
    "avg_daily_bookings": 8.2,
    "booking_growth_rate": 0.15,
    "total_revenue": 180500,
    "revenue_per_booking": 737,
    "avg_rating": 4.2,
    "cancellation_rate": 0.08
  },
  "trend_indicators": {
    "booking_trend": "increasing",
    "revenue_trend": "stable", 
    "rating_trend": "improving",
    "consistency_score": 0.78
  }
}
EOF

# Update workflow execution log
echo "### analyze-performance-trends - completed" >> /artifacts/{session_id}/workflow_execution.md
echo "- **Started**: $(date)" >> /artifacts/{session_id}/workflow_execution.md
echo "- **Completed**: $(date)" >> /artifacts/{session_id}/workflow_execution.md
echo "- **Artifacts Created**: performance_trends.json" >> /artifacts/{session_id}/workflow_execution.md
echo "- **Notes**: Trend analysis completed, identified 15% booking growth" >> /artifacts/{session_id}/workflow_execution.md
echo "" >> /artifacts/{session_id}/workflow_execution.md
```

## Output Format

### Trend Analysis Summary
```json
{
  "restaurant_id": "R001",
  "analysis_period": "30 days",
  "overall_trend": "improving",
  "key_insights": [
    "Bookings increased 15% in last 2 weeks",
    "Average rating improved from 4.1 to 4.3",
    "Revenue per booking decreased 5%"
  ],
  "performance_metrics": {
    "total_bookings": 245,
    "avg_daily_bookings": 8.2,
    "booking_growth_rate": 0.15,
    "total_revenue": 180500,
    "revenue_per_booking": 737,
    "avg_rating": 4.2,
    "cancellation_rate": 0.08
  },
  "trend_indicators": {
    "booking_trend": "increasing",
    "revenue_trend": "stable", 
    "rating_trend": "improving",
    "consistency_score": 0.78
  }
}
```

### Detailed Findings
- **Booking Analysis**: Daily booking patterns, growth trajectory, volatility assessment
- **Revenue Analysis**: Revenue trends, per-booking efficiency, spend pattern changes
- **Customer Satisfaction**: Rating trends, feedback patterns, service quality indicators
- **Operational Efficiency**: Cancellation trends, capacity utilization, performance consistency

### Risk and Opportunity Identification
- **Emerging Risks**: Declining metrics, increasing volatility, rating concerns
- **Growth Opportunities**: Positive trends to amplify, underutilized capacity
- **Stability Indicators**: Consistent performance areas, predictable patterns

## Error Handling

### Insufficient Data
```json
{
  "warning": "Limited trend analysis possible",
  "days_available": 15,
  "recommendation": "Extend analysis period when more data becomes available"
}
```

### Data Quality Issues
```json
{
  "warning": "Data gaps detected",
  "missing_days": 3,
  "impact": "Trend calculations may be less accurate"
}
```

### Statistical Significance
```json
{
  "note": "Trend not statistically significant",
  "confidence_level": 0.65,
  "recommendation": "Continue monitoring for more definitive patterns"
}
```

## Dependencies
- Restaurant performance data from collect-restaurant-data workflow
- Historical baseline data for comparison
- Statistical analysis capabilities for trend calculation

## Success Criteria
- Comprehensive trend analysis completed
- Key performance indicators calculated accurately
- Significant patterns and changes identified
- Statistical significance assessed for trends
- Clear insights provided for decision-making
- Analysis completed within 20 seconds