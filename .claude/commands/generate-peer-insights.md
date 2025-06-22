# Generate Peer Insights

## Description
Comprehensive peer benchmarking analysis that compares restaurant performance against similar establishments in the same locality and cuisine category to identify competitive positioning and improvement opportunities.

## Inputs
Natural language prompt with session context and comparison requirements:
- "SESSION_ID=abc123 Compare restaurant R001 with similar restaurants in the area"
- "SESSION_ID=def456 Generate peer benchmarking insights for Spice Garden restaurant"
- "SESSION_ID=ghi789 Analyze how restaurant R002 performs against competitors"

## Artifact Management
This workflow integrates with the artifact management protocol:
- **Input**: Loads restaurant data from `/artifacts/{session_id}/restaurant_data.json`
- **Output**: Saves analysis results to `/artifacts/{session_id}/peer_insights.json`
- **Logging**: Updates `/artifacts/{session_id}/workflow_execution.md` with completion status
- **Context**: Reads session configuration from `/artifacts/{session_id}/session_context.md`

## Steps

### 1. Initialize Session Context
- Extract SESSION_ID from prompt or environment variables
- Verify session directory exists at `/artifacts/{session_id}/`
- Load session context from `/artifacts/{session_id}/session_context.md`
- Update workflow execution log: mark generate-peer-insights as started

### 2. Load Restaurant and Peer Data
Load restaurant and peer data from the artifact store:
```bash
# Load restaurant data including peer benchmarks
RESTAURANT_DATA=$(cat /artifacts/{session_id}/restaurant_data.json)
```
- Extract restaurant performance metrics
- Load peer benchmark data for same locality/cuisine
- Extract industry averages for broader context

### 3. Identify Peer Restaurant Group
Define peer group based on loaded data:
- **Same Locality**: Restaurants in identical locality/area
- **Same Cuisine**: Restaurants serving identical cuisine type
- **Peer Group Size**: Determine number of comparable restaurants
- **Peer Validity**: Ensure sufficient peers for meaningful comparison

### 4. Calculate Peer Comparison Metrics

#### Booking Performance Comparison
- **Bookings vs Peer Average**: Target bookings / Peer average bookings
- **Booking Rank**: Percentile ranking within peer group
- **Booking Gap**: Absolute difference from peer average
- **Market Share**: Restaurant's booking share within locality

#### Revenue Performance Comparison
- **Revenue vs Peer Average**: Target revenue / Peer average revenue
- **Revenue per Booking vs Peers**: Efficiency comparison
- **Revenue Rank**: Percentile ranking for revenue generation
- **Revenue Premium/Discount**: Pricing position vs competitors

#### Customer Satisfaction Comparison
- **Rating vs Peer Average**: Target rating - Peer average rating
- **Rating Rank**: Position in peer group by customer satisfaction
- **Rating Gap Analysis**: Distance from top-rated peer
- **Review Sentiment vs Peers**: Qualitative comparison if data available

#### Advertising Effectiveness Comparison
- **ROI vs Peer Average**: Ad ROI compared to peer benchmark
- **Ad Spend vs Peers**: Investment level comparison
- **Conversion Rate vs Peers**: Ad effectiveness comparison
- **CTR vs Peer Average**: Campaign engagement comparison

### 5. Identify Performance Gaps and Opportunities

#### Overperforming Areas
Identify metrics where restaurant exceeds peer average by >20%:
- **Strength Categories**: Areas of competitive advantage
- **Success Factors**: Potential reasons for outperformance
- **Leverage Opportunities**: Ways to maximize strong performance

#### Underperforming Areas
Identify metrics where restaurant trails peer average by >20%:
- **Gap Categories**: Areas needing improvement
- **Improvement Potential**: Quantified upside opportunity
- **Catch-up Strategies**: Pathways to peer-level performance

#### Competitive Positioning
- **Market Position**: Overall ranking within peer group
- **Differentiation Factors**: Unique positioning elements
- **Competitive Threats**: Close competitors and risks
- **White Space Opportunities**: Underserved market segments

### 6. Analyze Top and Bottom Performers

#### Top Performer Analysis
Study the highest-performing peer restaurant:
- **Best Practice Identification**: What drives their success
- **Performance Gap**: Distance from top performer
- **Learnable Strategies**: Applicable insights for target restaurant

#### Bottom Performer Analysis
Understand lowest-performing peer restaurant:
- **Avoidable Pitfalls**: Common failure patterns
- **Risk Mitigation**: How to avoid similar performance issues
- **Relative Safety**: Target restaurant's distance from bottom

### 7. Generate Competitive Intelligence

#### Market Dynamics
- **Peer Group Trends**: Overall market direction
- **Competitive Intensity**: Level of competition in peer group
- **Growth Opportunities**: Market expansion potential
- **Saturation Assessment**: Market capacity analysis

#### Strategic Positioning
- **Value Proposition Analysis**: Positioning vs competitors
- **Price-Performance Matrix**: Value positioning assessment
- **Service Level Comparison**: Operational excellence benchmarking

### 8. Save Analysis Results to Artifacts
Save peer benchmarking results to the shared artifact directory:

```bash
# Save peer insights results
cat > /artifacts/{session_id}/peer_insights.json << EOF
{
  "analysis_metadata": {
    "restaurant_id": "{restaurant_id}",
    "peer_group": {
      "locality": "Koramangala",
      "cuisine": "Indian",
      "peer_count": 8,
      "comparison_period": "30 days"
    },
    "generated_at": "$(date -Iseconds)"
  },
  "performance_ranking": {
    "overall_rank": 5,
    "total_peers": 8,
    "percentile": 62.5
  },
  "key_insights": [
    "Bookings 15% below peer average",
    "Revenue per booking 10% above peers",
    "Customer rating matches peer average",
    "Ad ROI significantly below peer benchmark"
  ],
  "competitive_position": "middle_performer",
  "improvement_opportunities": {
    "booking_volume": {
      "current_gap": -34.4,
      "upside_potential": 4.3,
      "revenue_impact": 95000
    },
    "ad_effectiveness": {
      "roi_gap": -25.0,
      "optimization_potential": "₹3,500 additional revenue per ₹5,000 spent"
    }
  }
}
EOF

# Update workflow execution log
echo "### generate-peer-insights - completed" >> /artifacts/{session_id}/workflow_execution.md
echo "- **Started**: $(date)" >> /artifacts/{session_id}/workflow_execution.md
echo "- **Completed**: $(date)" >> /artifacts/{session_id}/workflow_execution.md
echo "- **Artifacts Created**: peer_insights.json" >> /artifacts/{session_id}/workflow_execution.md
echo "- **Notes**: Peer analysis completed, identified booking volume gap" >> /artifacts/{session_id}/workflow_execution.md
echo "" >> /artifacts/{session_id}/workflow_execution.md
```

## Output Format

### Peer Comparison Summary
```json
{
  "restaurant_id": "R001",
  "peer_group": {
    "locality": "Koramangala",
    "cuisine": "Indian", 
    "peer_count": 8,
    "comparison_period": "30 days"
  },
  "performance_ranking": {
    "overall_rank": 5,
    "total_peers": 8,
    "percentile": 62.5
  },
  "key_insights": [
    "Bookings 15% below peer average",
    "Revenue per booking 10% above peers",
    "Customer rating matches peer average",
    "Ad ROI significantly below peer benchmark"
  ],
  "competitive_position": "middle_performer"
}
```

### Detailed Peer Analysis
#### Performance Comparison Matrix
```json
{
  "booking_metrics": {
    "target_performance": 8.2,
    "peer_average": 12.5,
    "gap_percentage": -34.4,
    "rank": 6,
    "status": "underperforming"
  },
  "revenue_metrics": {
    "target_performance": 737,
    "peer_average": 670,
    "gap_percentage": 10.0,
    "rank": 3,
    "status": "overperforming"
  },
  "satisfaction_metrics": {
    "target_performance": 4.2,
    "peer_average": 4.1,
    "gap_percentage": 2.4,
    "rank": 4,
    "status": "at_par"
  }
}
```

### Opportunity Analysis
#### High-Impact Improvement Areas
1. **Booking Volume Optimization**
   - **Current Gap**: 34% below peer average
   - **Upside Potential**: +4.3 bookings per day to reach peer average
   - **Revenue Impact**: ~₹95,000 additional monthly revenue

2. **Ad Campaign Effectiveness**
   - **Current Gap**: ROI 25% below peers
   - **Optimization Potential**: Improve ROI from 2.1x to 2.8x
   - **Efficiency Gain**: ₹3,500 additional revenue per ₹5,000 spent

#### Competitive Advantages to Leverage
1. **Premium Pricing Power**
   - **Advantage**: 10% higher revenue per booking
   - **Strategy**: Maintain quality while increasing volume
   - **Opportunity**: Expand premium positioning

### Strategic Recommendations
#### Short-term Actions (1-2 months)
- **Booking Volume**: Focus on visibility and accessibility improvements
- **Ad Optimization**: Adopt peer best practices for campaign management
- **Service Consistency**: Maintain current customer satisfaction levels

#### Medium-term Strategy (3-6 months)
- **Market Share Growth**: Target peer-average booking levels
- **Differentiation**: Strengthen premium positioning
- **Competitive Intelligence**: Monitor top performer strategies

## Error Handling

### Insufficient Peer Data
```json
{
  "warning": "Limited peer comparison possible",
  "peer_count": 2,
  "minimum_recommended": 5,
  "impact": "Benchmarking less statistically significant"
}
```

### No Direct Peers
```json
{
  "warning": "No exact locality+cuisine peers found",
  "alternative_comparison": "Using broader locality or cuisine comparison",
  "recommendation": "Interpret results with caution"
}
```

### Data Quality Variations
```json
{
  "note": "Peer data quality varies",
  "data_coverage": 0.85,
  "impact": "Some peer comparisons may be incomplete"
}
```

## Dependencies
- Restaurant performance data from collect-restaurant-data workflow
- Peer benchmark data for locality and cuisine comparisons
- Restaurant master data for peer group identification
- Statistical analysis capabilities for ranking and gap analysis

## Success Criteria
- Comprehensive peer group identified and analyzed
- Performance gaps and opportunities clearly quantified
- Competitive positioning assessment completed
- Actionable insights for closing performance gaps
- Strategic recommendations aligned with peer analysis
- Analysis completed within 30 seconds