5# Product Requirements Document: Restaurant Performance Co-Pilot Agent

## 1. Product Overview

### Agent Identity & Purpose
- **Agent Name**: Restaurant Performance Co-Pilot
- **Primary Function**: Automatically generates structured, contextual performance summaries for restaurant partners based on restaurant_id input to enable data-driven sales conversations
- **Target Users**: Sales Executives and Account Managers managing restaurant partnerships at Swiggy Dineout
- **Business Value**: Reduces manual data gathering time from 30 minutes-3 hours to ~10 minutes per restaurant done autonomously, enabling scalable partner management across hundreds of restaurants per city

### Agent Context & Mental Model
- **User's Mental Model**: Users expect this agent to function like a "smart research assistant" that instantly compiles the same insights they would manually gather from multiple dashboards, presented in a sales-ready format
- **Boundaries of Trust**: Agent outputs are treated as starting points for sales conversations, not absolute truth. Users expect 85%+ accuracy with clear confidence indicators for uncertain data points
- **Expectations of Control**: Users need ability to drill down into specific metrics, request additional analysis, and override/edit recommendations before sharing with restaurant partners

## 2. User Stories

### Story 1: Pre-Meeting Performance Summary **[CORE - Problem Statement]**
```
As a Sales Executive preparing for a restaurant partner meeting,
I want the agent to generate a structured performance summary covering recent performance, ad campaign effectiveness, and peer benchmarking,
So that I can arrive at meetings fully prepared with relevant data and talking points in under 30 seconds instead of manually gathering data for 30 minutes to 3 hours,
With the understanding that this directly addresses the core challenge outlined in the problem statement: "Sales Executives manually gather performance metrics across multiple dashboards and reports."
```
*Based on Problem Statement Requirements:*
- Restaurant's Recent Performance (bookings, cancellations, revenue, ratings over 30 days)
- Ad Campaign Effectiveness (spend, impressions, clicks, conversions, ROI) 
- Peer Benchmarking (locality + cuisine comparison)
- Recommended Next Steps (ad spend, discounting, campaign timing)

### Story 2: Revenue Optimization & Upsell Identification **[EXTENDED - Enhanced Intelligence]**
```
As a Sales Executive targeting 15% quarterly growth across my restaurant portfolio,
I want the agent to identify specific revenue optimization opportunities (capacity utilization gaps, campaign efficiency improvements, pricing adjustments),
So that I can present concrete upsell proposals with projected ROI and timeline for implementation,
With the understanding that recommendations must account for seasonal patterns and the partner's current financial capacity for increased investment.
```
*Extended Capabilities Beyond Problem Statement:*
- Capacity utilization analysis from operational metrics
- Financial health assessment from settlement patterns
- Advanced ROI projections with implementation timelines

### Story 3: Risk Mitigation & Relationship Health Monitoring **[EXTENDED - Proactive Intelligence]**
```
As an Account Manager responsible for partner retention and satisfaction,
I want the agent to detect early warning signals (revenue volatility, service quality decline, competitive pressure),
So that I can proactively intervene with support strategies before partnership health deteriorates,
With the understanding that I'll need to correlate technical metrics with qualitative feedback from recent partner interactions.
```
*Extended Capabilities Beyond Problem Statement:*
- Revenue volatility tracking and anomaly detection
- Service quality monitoring through complaint analysis
- Early warning systems for relationship risk assessment

### Story 4: Competitive Response & Market Positioning **[EXTENDED - Market Intelligence]**
```
As a Sales Executive responding to competitive threats or market changes in a specific locality,
I want the agent to analyze competitive positioning gaps and identify differentiation opportunities for my restaurant partners,
So that I can help partners defend market share and capitalize on competitive advantages through targeted campaigns and positioning strategies,
With the understanding that competitive intelligence requires validation through market research and partner feedback on local competitive dynamics.
```
*Extended Capabilities Beyond Problem Statement:*
- Advanced competitive intelligence beyond basic peer benchmarking
- Market share analysis and competitive advantage identification
- Strategic positioning recommendations based on competitive landscape

### Story 5: Campaign Budget Optimization & Performance Coaching **[CORE+ - Enhanced Problem Statement]**
```
As an Account Manager working with partners to optimize their marketing spend efficiency,
I want the agent to provide specific campaign performance coaching recommendations with budget reallocation suggestions,
So that I can guide partners toward achieving their target ROI while maximizing booking volume and revenue growth,
With the understanding that recommendations must align with the partner's seasonal business patterns and cash flow constraints.
```
*Core Problem Statement Enhanced:*
- Builds on required "Ad Campaign Effectiveness" analysis
- Extends "Recommended Next Steps" with advanced optimization strategies
- Incorporates financial capacity assessment for practical implementation



## 3. Bounded Acceptance Criteria

### Must (Hard Requirements)
- Generate comprehensive sales briefing within 10 minutes of restaurant_id input
- Achieve ≥85% accuracy on financial metrics (revenue, ROI, settlement patterns) and ≥90% accuracy on operational metrics (bookings, capacity utilization)
- Return structured output optimized for sales conversations with executive summary, key talking points, and specific action items
- Provide risk scoring (High/Medium/Low) for relationship health based on revenue volatility, service quality trends, and competitive pressure
- Include trend analysis with clear performance trajectory indicators and seasonal context
- Calculate competitive positioning across 5+ dimensions (revenue efficiency, market share, service quality, pricing, campaign performance)
- Generate at least 5 specific, ROI-quantified recommendations with implementation priority and effort estimates
- Detect and flag revenue anomalies, service quality degradation, or competitive threats within 24 hours of occurrence
- Provide capacity utilization insights identifying underperforming time slots and revenue recovery opportunities

### Should (Expected Behaviors)
- Escalate high-risk accounts (volatility score >70%) for immediate account manager attention
- Customize insights based on restaurant profile (capacity, exclusivity status, franchise vs independent)
- Pre-populate campaign optimization suggestions based on peer ROI benchmarks and seasonal patterns
- Generate meeting talking points tailored to partner's current business phase and recent performance trends
- Provide drill-down capability for operational metrics (hourly utilization, service delay patterns, complaint categories)
- Include financial health indicators (settlement processing times, outstanding amounts, investment trends)
- Surface competitive advantages and market positioning opportunities specific to locality and cuisine
- Suggest specific budget reallocation amounts based on campaign performance gaps vs benchmarks

### Must Not (Safety Rails)
- Fabricate operational data or financial metrics when insufficient data exists
- Recommend budget increases >25% without flagging as "requires validation"
- Make partnership health assessments without incorporating both quantitative metrics and qualitative feedback scores
- Suggest competitive strategies without sufficient local market intelligence
- Auto-trigger account escalations without clear risk threshold documentation
- Recommend operational changes affecting customer experience without service quality context
- Make revenue projections beyond current trend confidence intervals

### Edge Case Handling
- **Ambiguous Input**: "restaurant ABC" → "I need a specific restaurant_id (format R###) to generate an accurate performance summary. Could you provide the restaurant_id for ABC?"
- **Low Confidence**: Missing peer data → "⚠️ Limited peer data available for this locality/cuisine combination. Benchmarking confidence: Low. Consider expanding comparison to broader geographic area."
- **Error State**: Data unavailable → "Unable to generate complete summary due to missing campaign data for this period. Would you like me to create a partial summary with available metrics and flag data gaps for follow-up?"

## 7. Evaluation Rubric

| Criteria | Weight | Description | Measurement |
|----------|--------|-------------|-------------|
| **Data Accuracy** | 35% | Correctness of extracted metrics and calculations | % of metrics within 5% of ground truth in test dataset |
| **Insight Quality** | 30% | Usefulness and actionability of generated recommendations | Sales team acceptance rate without major modifications |
| **Completeness** | 20% | Coverage of all required summary sections | % of summaries containing all core components |
| **Confidence Calibration** | 15% | Accuracy of confidence level predictions | Correlation between flagged low-confidence items and actual errors |

## 8. Data & Privacy Considerations

- **Data Retention**: Sales intelligence briefings generated on-demand with no persistent storage; audit logs retained for 90 days for compliance and performance analysis
- **Audit Trail**: All restaurant_id queries logged with user_id, timestamp, and generated recommendations for accountability and feedback loop improvement
- **Business Data Sensitivity**: Restaurant performance metrics, financial settlements, and competitive intelligence classified as business-confidential with appropriate access controls
- **User Consent & Training**: Sales team requires certification on appropriate use of AI-generated insights, competitive intelligence handling, and partner data confidentiality
- **Data Sources**: Mock datasets for MVP development; production integration requires data governance approval across 14 extended data tables including operational metrics, service quality, and financial intelligence
- **Competitive Intelligence Ethics**: Clear guidelines on appropriate use of peer benchmarking data and competitive positioning insights in partner conversations

## 9. Success Metrics

### Business Impact Metrics (mock numbers)
- **Revenue Growth**: 25% increase in monthly revenue growth across agent-supported accounts
- **Partnership Retention**: 95% retention rate vs 88% baseline
- **Upsell Success**: 40% success rate on recommended opportunities vs 25% baseline
- **Campaign ROI**: 30% improvement in average ROI through optimizations

### Product Performance Metrics (mock numbers)
- **Time Savings**: 70 minutes saved per meeting × 100 meetings/month = 116 hours/month saved
- **Insight Accuracy**: >90% accuracy on revenue projections and risk assessments
- **Recommendation Adoption**: 80% of recommendations implemented within 30 days
- **Partner Satisfaction**: 90% rate agent-supported management as "highly valuable"
