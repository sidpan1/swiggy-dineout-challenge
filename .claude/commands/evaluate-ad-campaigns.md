# Evaluate Ad Campaigns

## Description
Comprehensive evaluation of restaurant advertising campaigns to assess effectiveness, ROI, and performance against benchmarks. Provides insights for optimizing ad spend and targeting strategies.

## Inputs
Natural language prompt with session context and evaluation scope:
- "SESSION_ID=abc123 Evaluate ad campaign effectiveness for restaurant R001"
- "SESSION_ID=def456 Analyze advertising ROI and performance for Spice Garden"
- "SESSION_ID=ghi789 Assess recent ad campaigns and suggest optimizations for restaurant R002"

## Artifact Management
This workflow integrates with the artifact management protocol:
- **Input**: Loads restaurant and ads data from `/artifacts/{session_id}/restaurant_data.json`
- **Output**: Saves analysis results to `/artifacts/{session_id}/ad_evaluation.json`
- **Logging**: Updates `/artifacts/{session_id}/workflow_execution.md` with completion status
- **Context**: Reads session configuration from `/artifacts/{session_id}/session_context.md`

## Steps

### 1. Initialize Session Context
- Extract SESSION_ID from prompt or environment variables
- Verify session directory exists at `/artifacts/{session_id}/`
- Load session context from `/artifacts/{session_id}/session_context.md`
- Update workflow execution log: mark evaluate-ad-campaigns as started

### 2. Load Campaign Performance Data
Load restaurant and ads data from the artifact store:
```bash
# Load restaurant data including ads performance
RESTAURANT_DATA=$(cat /artifacts/{session_id}/restaurant_data.json)
```
- Extract individual campaign metrics (impressions, clicks, conversions, spend)
- Load campaign duration and timing information
- Extract revenue attribution data

### 3. Calculate Campaign Performance Metrics

#### Campaign-Level Analysis
For each campaign:
- **Click-Through Rate (CTR)**: Clicks / Impressions × 100
- **Conversion Rate**: Conversions / Clicks × 100
- **Cost Per Click (CPC)**: Spend / Clicks
- **Cost Per Conversion**: Spend / Conversions
- **Return on Ad Spend (ROAS)**: Revenue Generated / Spend
- **Campaign Efficiency Score**: Weighted score of CTR, conversion rate, and ROAS

#### Aggregated Performance
Across all campaigns:
- **Total Ad Investment**: Sum of all campaign spend
- **Total Conversions Generated**: Sum of all conversions
- **Overall ROI**: Total Revenue from Ads / Total Ad Spend
- **Average Campaign Performance**: Mean metrics across campaigns
- **Campaign Success Rate**: Percentage of campaigns meeting ROI targets

### 4. Analyze Campaign Effectiveness

#### High-Performing Campaigns
Identify campaigns with:
- ROI > 3.0x
- Conversion rate > 10%
- CTR > 8%
- Cost per conversion < ₹50

#### Underperforming Campaigns
Flag campaigns with:
- ROI < 2.0x
- Conversion rate < 5%
- CTR < 3%
- Cost per conversion > ₹100

#### Campaign Timing Analysis
- **Day-of-week performance**: Best performing campaign days
- **Duration optimization**: Optimal campaign length analysis
- **Seasonal effectiveness**: Performance variation by time period

### 5. Benchmark Against Industry Standards

#### Peer Comparison
Compare restaurant's ad performance with peer benchmarks:
- **ROI vs Peer Average**: Restaurant ROI / Peer Average ROI
- **Conversion Rate Ranking**: Percentile within peer group
- **Spend Efficiency**: Cost per conversion vs peer average
- **Market Share**: Restaurant's ad presence relative to peers

#### Industry Benchmarks
Assess against standard performance metrics:
- **CTR Benchmark**: Industry average 6-8% for restaurant ads
- **Conversion Benchmark**: Industry average 8-12% for restaurant bookings
- **ROI Benchmark**: Industry average 2.5-3.5x for restaurant advertising

### 6. Identify Optimization Opportunities

#### Budget Allocation
- **High-ROI Campaign Types**: Campaign formats delivering best returns
- **Underinvested Channels**: Promising campaigns needing more budget
- **Overinvested Channels**: Campaigns with diminishing returns

#### Targeting Improvements
- **Audience Optimization**: Best-performing demographic segments
- **Geographic Optimization**: High-converting locality targeting
- **Timing Optimization**: Optimal campaign scheduling recommendations

#### Creative and Messaging
- **Top-Performing Ad Content**: Campaign themes with highest engagement
- **Message Effectiveness**: Promotional offers vs brand awareness campaigns
- **Seasonal Messaging**: Time-appropriate campaign themes

### 7. Generate Campaign Insights and Save Artifacts

#### Performance Summary
Overall advertising effectiveness assessment with key findings

#### Campaign Rankings
Rank all campaigns by performance metrics and identify patterns

#### Optimization Recommendations
Specific, actionable suggestions for improving ad performance

### 8. Save Analysis Results to Artifacts
Save ad campaign evaluation results to the shared artifact directory:

```bash
# Save ad evaluation results
cat > /artifacts/{session_id}/ad_evaluation.json << EOF
{
  "analysis_metadata": {
    "restaurant_id": "{restaurant_id}",
    "evaluation_period": "60 days",
    "generated_at": "$(date -Iseconds)"
  },
  "overall_performance": {
    "total_spend": 15000,
    "total_conversions": 89,
    "overall_roi": 2.1,
    "avg_ctr": 7.2,
    "avg_conversion_rate": 8.5
  },
  "peer_comparison": {
    "roi_vs_peers": "below_average",
    "peer_avg_roi": 2.8,
    "performance_ranking": "bottom_quartile"
  },
  "key_insights": [
    "ROI 25% below peer average",
    "Weekend campaigns outperform weekday by 40%", 
    "Lunch promotion campaigns show highest conversion rates"
  ],
  "optimization_recommendations": {
    "high_priority": [
      "Increase weekend campaign budget by ₹2000",
      "Pause underperforming weekday campaigns"
    ],
    "medium_priority": [
      "Test lunch-specific promotional content",
      "Optimize targeting for local demographics"
    ]
  }
}
EOF

# Update workflow execution log
echo "### evaluate-ad-campaigns - completed" >> /artifacts/{session_id}/workflow_execution.md
echo "- **Started**: $(date)" >> /artifacts/{session_id}/workflow_execution.md
echo "- **Completed**: $(date)" >> /artifacts/{session_id}/workflow_execution.md
echo "- **Artifacts Created**: ad_evaluation.json" >> /artifacts/{session_id}/workflow_execution.md
echo "- **Notes**: Ad campaign analysis completed, ROI below peer average" >> /artifacts/{session_id}/workflow_execution.md
echo "" >> /artifacts/{session_id}/workflow_execution.md
```

## Output Format

### Campaign Performance Summary
```json
{
  "restaurant_id": "R001",
  "evaluation_period": "60 days",
  "total_campaigns": 3,
  "overall_performance": {
    "total_spend": 15000,
    "total_conversions": 89,
    "overall_roi": 2.1,
    "avg_ctr": 7.2,
    "avg_conversion_rate": 8.5
  },
  "peer_comparison": {
    "roi_vs_peers": "below_average",
    "peer_avg_roi": 2.8,
    "performance_ranking": "bottom_quartile"
  },
  "key_insights": [
    "ROI 25% below peer average",
    "Weekend campaigns outperform weekday by 40%", 
    "Lunch promotion campaigns show highest conversion rates"
  ]
}
```

### Campaign-Specific Analysis
For each campaign:
- **Performance Metrics**: All calculated KPIs
- **Effectiveness Rating**: High/Medium/Low performance classification
- **Optimization Potential**: Specific improvement opportunities
- **Budget Recommendations**: Spend increase/decrease/maintain suggestions

### Optimization Recommendations
#### High-Priority Actions
1. **Increase Budget for High-ROI Campaigns**: Specific campaigns and amounts
2. **Pause Underperforming Campaigns**: Campaigns not meeting ROI thresholds
3. **Optimize Timing**: Best days/hours for campaign scheduling

#### Medium-Priority Actions
1. **Audience Targeting Refinement**: Demographic and geographic optimizations
2. **Creative Testing**: A/B test recommendations for ad content
3. **Bid Strategy Adjustments**: CPC and bidding optimization

#### Long-Term Strategic Changes
1. **Campaign Mix Optimization**: Balance between campaign types
2. **Seasonal Strategy Planning**: Year-round campaign calendar
3. **Competitive Positioning**: Differentiation strategies

## Error Handling

### No Recent Campaigns
```json
{
  "warning": "No recent ad campaigns found",
  "recommendation": "Consider launching advertising campaigns to increase visibility",
  "suggested_budget": "₹5000 for initial test campaigns"
}
```

### Insufficient Campaign Data
```json
{
  "warning": "Limited campaign performance data",
  "campaigns_analyzed": 1,
  "recommendation": "Analysis based on single campaign may not be representative"
}
```

### Benchmark Data Unavailable
```json
{
  "note": "Peer benchmark data not available",
  "impact": "Relative performance assessment limited to industry averages"
}
```

## Dependencies
- Ad campaign data from collect-restaurant-data workflow
- Peer benchmark data for comparative analysis
- Industry standard benchmarks for performance assessment
- Revenue attribution data for ROI calculations

## Success Criteria
- All campaign performance metrics calculated accurately
- Peer and industry benchmarking completed
- Clear optimization recommendations provided
- High, medium, and underperforming campaigns identified
- Specific budget and targeting recommendations generated
- Analysis completed within 25 seconds