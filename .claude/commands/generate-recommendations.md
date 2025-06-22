# Generate Recommendations

## Description
Intelligent recommendation engine that synthesizes insights from performance analysis, ad evaluation, peer benchmarking, and anomaly detection to generate prioritized, actionable improvement suggestions with quantified impact estimates.

## Inputs
Natural language prompt with session context requesting recommendations:
- "SESSION_ID=abc123 Generate improvement recommendations for restaurant R001"
- "SESSION_ID=def456 Suggest actionable steps to boost Spice Garden performance"
- "SESSION_ID=ghi789 Create data-backed recommendations for restaurant R002 optimization"

## Artifact Management
This workflow integrates with the artifact management protocol:
- **Input**: Loads all analysis results from `/artifacts/{session_id}/` directory
- **Output**: Saves recommendations to `/artifacts/{session_id}/recommendations.json`
- **Logging**: Updates `/artifacts/{session_id}/workflow_execution.md` with completion status
- **Context**: Reads session configuration from `/artifacts/{session_id}/session_context.md`

## Steps

### 1. Initialize Session Context
- Extract SESSION_ID from prompt or environment variables
- Verify session directory exists at `/artifacts/{session_id}/`
- Load session context from `/artifacts/{session_id}/session_context.md`
- Update workflow execution log: mark generate-recommendations as started

### 2. Synthesize Analysis Results
Load insights from all previous analysis workflows:
```bash
# Load all analysis results from shared artifacts
PERFORMANCE_TRENDS=$(cat /artifacts/{session_id}/performance_trends.json)
AD_EVALUATION=$(cat /artifacts/{session_id}/ad_evaluation.json)
PEER_INSIGHTS=$(cat /artifacts/{session_id}/peer_insights.json)
ANOMALIES=$(cat /artifacts/{session_id}/anomalies.json)
RESTAURANT_DATA=$(cat /artifacts/{session_id}/restaurant_data.json)
```
- **Performance Trends**: Key findings from trend analysis
- **Ad Campaign Results**: Effectiveness gaps and opportunities
- **Peer Insights**: Performance gaps vs competitors
- **Anomaly Findings**: Critical issues requiring attention

### 3. Identify Improvement Opportunities

#### Revenue Optimization Opportunities
- **Booking Volume Increase**: Based on peer gap analysis
- **Revenue per Booking Improvement**: Price optimization potential
- **Capacity Utilization**: Better covers per booking ratios
- **Upselling Opportunities**: Increase average spend per cover

#### Marketing Effectiveness Opportunities
- **Ad Spend Optimization**: Budget reallocation based on ROI analysis
- **Campaign Targeting**: Audience and timing improvements
- **Creative Optimization**: Message and content improvements
- **Channel Mix**: Balance between organic and paid acquisition

#### Operational Excellence Opportunities
- **Service Quality**: Customer satisfaction improvements
- **Cancellation Reduction**: Process improvements to reduce cancellations
- **Consistency**: Reduce performance variability
- **Efficiency**: Operational streamlining for better margins

#### Competitive Positioning Opportunities
- **Market Share Growth**: Strategies to capture competitor traffic
- **Differentiation**: Unique value proposition development
- **Premium Positioning**: Leverage existing strengths
- **Defensive Strategies**: Protect against competitive threats

### 4. Prioritize Recommendations by Impact and Feasibility

#### High-Impact, High-Feasibility (Quick Wins)
- **Low Effort, High Return**: Immediate implementation possible
- **Resource Requirements**: Minimal additional investment needed
- **Timeline**: Can be implemented within 2-4 weeks
- **Risk Level**: Low risk of negative consequences

#### High-Impact, Medium-Feasibility (Strategic Initiatives)
- **Moderate Effort, High Return**: Requires some planning and resources
- **Resource Requirements**: Moderate investment needed
- **Timeline**: Implementation within 1-3 months
- **Risk Level**: Medium risk, manageable with proper execution

#### Medium-Impact, High-Feasibility (Efficiency Gains)
- **Low Effort, Medium Return**: Easy improvements with modest gains
- **Resource Requirements**: Minimal investment required
- **Timeline**: Quick implementation possible
- **Risk Level**: Very low risk

### 5. Calculate Expected Impact

#### Quantified Impact Estimates
For each recommendation:
- **Revenue Impact**: Expected additional monthly revenue
- **Booking Impact**: Expected increase in daily bookings
- **ROI Impact**: Expected improvement in advertising ROI
- **Rating Impact**: Expected customer satisfaction improvement
- **Implementation Cost**: Estimated investment required

#### Confidence Levels
- **High Confidence (80-90%)**: Based on strong peer data and clear gaps
- **Medium Confidence (60-80%)**: Based on industry best practices
- **Low Confidence (40-60%)**: Based on general optimization principles

### 6. Generate Specific Action Items

#### Immediate Actions (0-2 weeks)
- **Ad Campaign Adjustments**: Specific budget and targeting changes
- **Pricing Optimizations**: Menu or service pricing adjustments
- **Operational Fixes**: Address identified service issues
- **Promotional Campaigns**: Launch specific offers or discounts

#### Short-term Initiatives (1-2 months)
- **Marketing Strategy**: Comprehensive campaign optimization
- **Service Improvements**: Staff training or process enhancements
- **Menu Optimization**: Dish or offering modifications
- **Technology Upgrades**: System or platform improvements

#### Long-term Strategy (3-6 months)
- **Market Positioning**: Brand and positioning evolution
- **Competitive Strategy**: Long-term competitive advantages
- **Capacity Planning**: Expansion or optimization planning
- **Partnership Development**: Strategic alliances or collaborations

### 7. Create Implementation Roadmap

#### Phase 1: Foundation (Weeks 1-2)
- **Critical Issue Resolution**: Address high-severity anomalies
- **Quick Win Implementation**: Deploy easiest high-impact changes
- **Baseline Establishment**: Set measurement framework
- **Team Alignment**: Ensure stakeholder buy-in

#### Phase 2: Optimization (Weeks 3-8)
- **Marketing Enhancement**: Implement ad and campaign optimizations
- **Service Excellence**: Deploy customer experience improvements
- **Operational Efficiency**: Streamline processes and workflows
- **Performance Monitoring**: Track progress and adjust strategies

#### Phase 3: Growth (Weeks 9-24)
- **Market Expansion**: Implement growth strategies
- **Competitive Advantage**: Build sustainable differentiation
- **Continuous Improvement**: Establish ongoing optimization cycles
- **Strategic Evolution**: Adapt to market changes and opportunities

### 8. Save Recommendations to Artifacts
Save structured recommendations to the shared artifact directory:

```bash
# Save recommendations results
cat > /artifacts/{session_id}/recommendations.json << EOF
{
  "recommendations_metadata": {
    "restaurant_id": "{restaurant_id}",
    "restaurant_name": "{restaurant_name}",
    "session_id": "{session_id}",
    "generated_at": "$(date -Iseconds)",
    "analysis_period": "{analysis_period}",
    "data_sources": [
      "performance_trends.json",
      "ad_evaluation.json", 
      "peer_insights.json",
      "anomalies.json",
      "restaurant_data.json"
    ]
  },
  "executive_summary": {
    "overall_performance": "{performance_status}",
    "key_strengths": [
      "{strength_1}",
      "{strength_2}",
      "{strength_3}"
    ],
    "critical_issues": [
      "{issue_1}",
      "{issue_2}",
      "{issue_3}"
    ],
    "strategic_priority": "{priority_focus}"
  },
  "high_priority_actions": {
    "immediate_actions": [
      {
        "priority": "critical",
        "action": "{action_title}",
        "description": "{detailed_description}",
        "timeline": "{implementation_timeline}",
        "owner": "{responsible_team}",
        "kpi_target": "{measurable_target}",
        "business_impact": "{expected_impact}",
        "implementation_steps": [
          "{step_1}",
          "{step_2}",
          "{step_3}"
        ]
      }
    ]
  },
  "strategic_recommendations": {
    "leverage_strengths": [
      {
        "area": "{strength_area}",
        "current_performance": "{current_metrics}",
        "recommendation": "{recommendation_title}",
        "rationale": "{data_backed_reasoning}",
        "action_plan": [
          "{action_1}",
          "{action_2}",
          "{action_3}"
        ],
        "expected_impact": "{quantified_outcome}",
        "investment_required": "{cost_estimate}",
        "roi_projection": "{expected_roi}"
      }
    ],
    "address_weaknesses": [
      {
        "area": "{weakness_area}",
        "current_issue": "{problem_description}",
        "recommendation": "{solution_title}",
        "priority": "{priority_level}",
        "action_plan": [
          "{action_1}",
          "{action_2}",
          "{action_3}"
        ],
        "success_metrics": "{measurement_criteria}",
        "timeline": "{implementation_schedule}"
      }
    ]
  },
  "marketing_recommendations": {
    "advertisement_optimization": [
      {
        "campaign_type": "{campaign_category}",
        "current_performance": "{current_metrics}",
        "recommendation": "{optimization_approach}",
        "budget_allocation": "{spending_recommendation}",
        "optimization_tactics": [
          "{tactic_1}",
          "{tactic_2}",
          "{tactic_3}"
        ],
        "expected_outcomes": "{projected_results}"
      }
    ],
    "targeting_refinement": [
      {
        "objective": "{targeting_goal}",
        "current_gap": "{performance_gap}",
        "tactics": [
          "{targeting_tactic_1}",
          "{targeting_tactic_2}",
          "{targeting_tactic_3}"
        ],
        "measurement": "{tracking_approach}"
      }
    ]
  },
  "operational_recommendations": {
    "revenue_management": [
      {
        "initiative": "{revenue_initiative}",
        "rationale": "{business_justification}",
        "implementation": [
          "{implementation_step_1}",
          "{implementation_step_2}",
          "{implementation_step_3}"
        ],
        "expected_impact": "{revenue_projection}"
      }
    ],
    "customer_experience": [
      {
        "initiative": "{experience_initiative}",
        "rationale": "{customer_impact_reasoning}",
        "implementation": [
          "{experience_step_1}",
          "{experience_step_2}",
          "{experience_step_3}"
        ],
        "expected_impact": "{satisfaction_improvement}"
      }
    ]
  },
  "financial_projections": {
    "current_baseline": {
      "monthly_revenue": "{current_revenue}",
      "monthly_ad_spend": "{current_ad_spend}",
      "current_roi": "{current_roi}",
      "avg_spend_per_cover": "{current_spend_per_cover}"
    },
    "optimized_projections": {
      "scenario_1_conservative": {
        "description": "{conservative_approach}",
        "monthly_revenue": "{conservative_revenue}",
        "revenue_increase": "{conservative_increase_percent}",
        "ad_spend": "{conservative_ad_spend}",
        "projected_roi": "{conservative_roi}",
        "implementation_timeline": "{conservative_timeline}"
      },
      "scenario_2_aggressive": {
        "description": "{aggressive_approach}",
        "monthly_revenue": "{aggressive_revenue}",
        "revenue_increase": "{aggressive_increase_percent}",
        "ad_spend": "{aggressive_ad_spend}",
        "projected_roi": "{aggressive_roi}",
        "implementation_timeline": "{aggressive_timeline}"
      }
    }
  },
  "implementation_roadmap": {
    "week_1_2": [
      "{week_1_action_1}",
      "{week_1_action_2}",
      "{week_1_action_3}"
    ],
    "week_3_4": [
      "{week_3_action_1}",
      "{week_3_action_2}",
      "{week_3_action_3}"
    ],
    "month_2": [
      "{month_2_action_1}",
      "{month_2_action_2}",
      "{month_2_action_3}"
    ],
    "month_3": [
      "{month_3_action_1}",
      "{month_3_action_2}",
      "{month_3_action_3}"
    ]
  },
  "risk_mitigation": {
    "identified_risks": [
      {
        "risk": "{risk_description}",
        "probability": "{risk_probability}",
        "impact": "{risk_impact}",
        "mitigation": [
          "{mitigation_step_1}",
          "{mitigation_step_2}",
          "{mitigation_step_3}"
        ]
      }
    ]
  },
  "success_metrics": {
    "primary_kpis": [
      {
        "metric": "{kpi_name}",
        "current": "{current_value}",
        "target": "{target_value}",
        "timeline": "{achievement_timeline}"
      }
    ],
    "secondary_kpis": [
      {
        "metric": "{secondary_kpi_name}",
        "current": "{current_value}",
        "target": "{target_value}",
        "timeline": "{achievement_timeline}"
      }
    ]
  },
  "conclusion": {
    "strategic_assessment": "{overall_strategic_summary}",
    "key_success_factors": [
      "{success_factor_1}",
      "{success_factor_2}",
      "{success_factor_3}"
    ],
    "expected_outcomes": "{projected_business_outcomes}",
    "next_steps": "{immediate_next_actions}"
  }
}
EOF

# Update workflow execution log
echo "### generate-recommendations - completed" >> /artifacts/{session_id}/workflow_execution.md
echo "- **Started**: $(date)" >> /artifacts/{session_id}/workflow_execution.md
echo "- **Completed**: $(date)" >> /artifacts/{session_id}/workflow_execution.md
echo "- **Artifacts Created**: recommendations.json" >> /artifacts/{session_id}/workflow_execution.md
echo "- **Notes**: Generated structured recommendations with quantified impact estimates" >> /artifacts/{session_id}/workflow_execution.md
echo "" >> /artifacts/{session_id}/workflow_execution.md
```

## Output Format

### Recommendation Summary
```json
{
  "restaurant_id": "R001",
  "total_recommendations": 6,
  "priority_distribution": {
    "high": 2,
    "medium": 3,
    "low": 1
  },
  "estimated_impact": {
    "monthly_revenue_increase": 45000,
    "daily_booking_increase": 3.8,
    "roi_improvement": 0.7,
    "implementation_cost": 12000
  },
  "top_recommendation": {
    "title": "Optimize Ad Spend Allocation",
    "impact": "₹18,000 additional monthly revenue",
    "effort": "low",
    "timeline": "2 weeks"
  }
}
```

### Prioritized Recommendations

#### High-Priority Recommendations
1. **Increase Ad Budget for High-ROI Campaigns**
   - **Current Gap**: ROI 25% below peer average (2.1x vs 2.8x)
   - **Action**: Increase budget for weekend campaigns by ₹2,000/month
   - **Expected Impact**: +15 monthly bookings, +₹18,000 monthly revenue
   - **Implementation**: Reallocate ad spend within existing budget
   - **Timeline**: 2 weeks
   - **Confidence**: High (85%)

2. **Optimize Booking Process for Higher Conversion**
   - **Current Gap**: Conversion rate 15% below peers
   - **Action**: Simplify booking flow and reduce friction points
   - **Expected Impact**: +8% conversion rate improvement
   - **Implementation**: UX improvements and process optimization
   - **Timeline**: 4 weeks
   - **Confidence**: Medium (75%)

#### Medium-Priority Recommendations
3. **Implement Happy Hour Pricing Strategy**
   - **Opportunity**: Low afternoon occupancy compared to peers
   - **Action**: 20% discount for 2-5 PM bookings
   - **Expected Impact**: +12 afternoon bookings/week
   - **Implementation**: Promotional campaign and menu updates
   - **Timeline**: 3 weeks
   - **Confidence**: Medium (70%)

4. **Enhance Customer Experience Quality**
   - **Current Gap**: Rating stable but improvement potential exists
   - **Action**: Staff training focused on service excellence
   - **Expected Impact**: +0.2 rating improvement over 2 months
   - **Implementation**: Training program and service standards
   - **Timeline**: 6 weeks
   - **Confidence**: Medium (65%)

### Implementation Guide

#### Week 1-2: Foundation
- [ ] Reallocate ad budget to high-performing campaigns
- [ ] Address any critical anomalies identified
- [ ] Set up enhanced performance monitoring
- [ ] Communicate strategy to restaurant team

#### Week 3-6: Core Optimizations
- [ ] Implement booking process improvements
- [ ] Launch happy hour promotional strategy
- [ ] Begin customer service enhancement program
- [ ] Monitor and adjust ad campaign performance

#### Week 7-12: Advanced Strategies
- [ ] Evaluate initial results and refine strategies
- [ ] Implement additional peer-gap closing initiatives
- [ ] Develop long-term competitive positioning
- [ ] Plan next phase of optimization initiatives

### Success Metrics and Monitoring

#### Key Performance Indicators
- **Daily Bookings**: Target increase from 8.2 to 12+ (peer level)
- **Monthly Revenue**: Target increase of ₹45,000+ within 3 months
- **Ad ROI**: Target improvement from 2.1x to 2.5x+ within 6 weeks
- **Customer Rating**: Target improvement from 4.2 to 4.4+ within 8 weeks

#### Monitoring Frequency
- **Weekly**: Ad performance and booking trends
- **Bi-weekly**: Revenue and customer satisfaction metrics
- **Monthly**: Comprehensive performance review vs targets
- **Quarterly**: Strategic assessment and next phase planning

## Error Handling

### Insufficient Analysis Data
```json
{
  "warning": "Limited recommendation scope",
  "missing_analysis": ["peer_insights"],
  "impact": "Recommendations based on available data only",
  "recommendation": "Gather additional comparative data for enhanced insights"
}
```

### Conflicting Optimization Objectives
```json
{
  "note": "Trade-offs identified between recommendations",
  "conflict": "Revenue optimization vs customer satisfaction",
  "recommendation": "Prioritize based on business objectives and implement sequentially"
}
```

### High Implementation Risk
```json
{
  "warning": "Some recommendations carry execution risk",
  "risk_factors": ["market_volatility", "competitive_response"],
  "mitigation": "Implement with careful monitoring and rollback plans"
}
```

## Dependencies
- Results from all analysis workflows (trends, ads, peers, anomalies)
- Session context from `/artifacts/{session_id}/session_context.md`
- Restaurant data from `/artifacts/{session_id}/restaurant_data.json`
- Peer benchmark data for gap identification

## Success Criteria
- Structured recommendations saved to `/artifacts/{session_id}/recommendations.json`
- All analysis results synthesized into actionable recommendations
- Recommendations prioritized by impact and feasibility
- Specific implementation guidance provided with timelines
- Expected outcomes quantified with confidence levels
- Success metrics and monitoring plan established
- Workflow execution logged with completion status
- Recommendation generation completed within 35 seconds