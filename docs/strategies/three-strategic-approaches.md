# Three Strategic Approaches for Restaurant Classification & Intervention
## Swiggy Dineout GenAI Co-Pilot Research Analysis

---

## Executive Summary

This document presents three complementary strategic approaches for restaurant classification and intervention:

1. **Multi-Dimensional Classification** (Current Framework)
2. **ARPU-Occupancy Based Classification** (Business Metrics Focus)
3. **Anomaly-Based Detection & Intervention** (Proactive Alert System)

Each strategy serves a distinct purpose and can be used independently or in combination for comprehensive restaurant management.

---

## Strategy 1: Multi-Dimensional Classification Framework

### Overview
The existing framework from the restaurant classification SOP that uses multiple dimensions to create a holistic view of restaurant performance.

### Core Components
- **Performance vs Potential Matrix**: Stars, Hidden Gems, Workhorses, Strugglers
- **10 Classification Dimensions**: Performance trajectory, maturity, ad responsiveness, etc.
- **Composite Scoring**: Weighted combination of OPD, Revenue, Ad ROI, Rating

### Best Use Cases
- Long-term strategic planning
- Portfolio-level analysis
- Sales team quarterly reviews
- New restaurant onboarding

### Strengths
- Comprehensive view of restaurant health
- Multiple perspectives for nuanced understanding
- Proven framework with established thresholds

### Limitations
- Complex to implement and maintain
- May overwhelm with too many dimensions
- Slower to detect sudden changes

---

## Strategy 2: ARPU-Occupancy Based Classification

### Overview
A simplified yet powerful approach focusing on two critical business metrics that directly impact profitability.

### Core Components
- **ARPU (Average Revenue Per User)**: Monetization efficiency metric
- **Occupancy Rate**: Operational utilization metric
- **New Quadrants**: Premium Stars, Volume Plays, Luxury Niche, Strugglers

### Matrix Redefinition
```
                    ARPU (Revenue Efficiency)
                    Low (<₹500)      High (>₹800)
           ┌─────────────────┬─────────────────┐
High (>70%)│  VOLUME PLAYS   │  PREMIUM STARS  │
Occupancy  ├─────────────────┼─────────────────┤
Low (<40%) │  STRUGGLERS     │  LUXURY NICHE   │
           └─────────────────┴─────────────────┘
```

### Best Use Cases
- Daily operational decisions
- Quick restaurant health checks
- Revenue optimization initiatives
- Capacity planning

### Strengths
- Simple and intuitive
- Directly tied to business outcomes
- Easy to track and measure
- Clear action triggers

### Limitations
- May miss nuanced factors
- Doesn't capture growth trajectory
- Limited view of competitive context

---

## Strategy 3: Anomaly-Based Detection & Intervention

### Overview
A proactive monitoring system that identifies unusual patterns and triggers immediate interventions.

### Core Components
- **Statistical Anomaly Detection**: Time series analysis, outlier detection
- **Business Rule Anomalies**: Predefined thresholds and patterns
- **Real-time Alerts**: Immediate notification system
- **Contextual Analysis**: Competitive, seasonal, operational factors

### Anomaly Types & Detection

#### 1. Statistical Anomalies
```python
# Time Series Anomalies
- Sudden ARPU drops (>25% WoW)
- Occupancy vacuums (<20% on busy days)
- Booking pattern disruptions

# Multi-variate Anomalies
- Revenue-occupancy mismatch
- Rating-revenue divergence
- Cost-revenue imbalance
```

#### 2. Business Logic Anomalies
| Pattern | Detection Rule | Action |
|---------|----------------|---------|
| Revenue Cliff | Daily revenue < 0.5 × 7-day MA | Investigate immediately |
| Ghost Hours | Zero bookings during peak | Check operations |
| Cancellation Spike | Cancel rate > 30% | Contact restaurant |
| Competition Impact | Market share drop > 15% | Competitive response |

#### 3. Contextual Anomalies
- **Seasonal**: Underperformance during festivals
- **Weather**: Low occupancy despite good weather
- **Event-based**: Missing local event opportunities

### Alert Framework
```yaml
severity_levels:
  critical:
    response_time: < 2 hours
    escalation: Sales Head + Restaurant Owner
    examples: 
      - ARPU drop > 40%
      - Complete booking failure
      - Mass cancellations
  
  high:
    response_time: < 24 hours
    escalation: Account Manager
    examples:
      - Occupancy anomaly (3σ)
      - Competitive loss pattern
      - Rating decline > 0.5
  
  medium:
    response_time: < 48 hours
    escalation: Sales Executive
    examples:
      - Gradual metric decline
      - Efficiency degradation
```

### Best Use Cases
- Real-time problem detection
- Preventing revenue loss
- Early warning system
- Crisis management

### Strengths
- Proactive vs reactive
- Catches issues early
- Automated monitoring
- Reduces manual oversight

### Limitations
- Can generate false positives
- Requires fine-tuning
- May miss slow degradation
- Needs historical data

---

## Integrated Implementation Strategy

### Phase 1: Foundation (Week 1-2)
1. Implement ARPU-Occupancy tracking (Strategy 2)
2. Set up basic anomaly detection (Strategy 3)
3. Map to existing classifications (Strategy 1)

### Phase 2: Enhancement (Week 3-4)
1. Refine anomaly detection algorithms
2. Create unified dashboard
3. Develop intervention playbooks

### Phase 3: Intelligence (Week 5-6)
1. Train ML models on all three approaches
2. Create recommendation engine
3. Automate alert-to-action pipeline

### Phase 4: Optimization (Week 7-8)
1. A/B test intervention strategies
2. Fine-tune thresholds
3. Scale to full restaurant base

---

## Choosing the Right Strategy

### Decision Framework

```
IF goal == "Quarterly Strategic Review":
    USE Strategy 1 (Multi-Dimensional)
    
ELIF goal == "Daily Operations":
    USE Strategy 2 (ARPU-Occupancy)
    
ELIF goal == "Real-time Monitoring":
    USE Strategy 3 (Anomaly Detection)
    
ELSE goal == "Comprehensive Management":
    USE All Three Strategies
    - Strategy 1 for strategic planning
    - Strategy 2 for operational decisions  
    - Strategy 3 for proactive alerts
```

### Integration Points

1. **Classification → Anomaly Detection**
   - Different anomaly thresholds per quadrant
   - Tailored alerts based on restaurant type

2. **ARPU-Occupancy → Multi-Dimensional**
   - Use ARPU-Occupancy as primary metrics
   - Add dimensions for deeper analysis

3. **Anomaly → Classification**
   - Anomaly patterns indicate classification changes
   - Trigger reclassification on persistent anomalies

---

## Success Metrics Across Strategies

### Unified KPIs
1. **Revenue Impact**: 15-20% improvement in 60 days
2. **Operational Efficiency**: 50% reduction in issue resolution time
3. **Prediction Accuracy**: >85% for all classification methods
4. **Alert Effectiveness**: <15% false positive rate
5. **Sales Productivity**: 70% reduction in analysis time

### Strategy-Specific Metrics

| Strategy | Primary Metric | Target |
|----------|---------------|---------|
| Multi-Dimensional | Classification stability | <10% monthly change |
| ARPU-Occupancy | Metric improvement | 15% ARPU, 10% Occupancy |
| Anomaly Detection | Detection speed | <2 hours for critical |

---

## Conclusion

These three strategies provide a comprehensive toolkit for restaurant management:

1. **Use Multi-Dimensional** for strategic decisions and long-term planning
2. **Use ARPU-Occupancy** for daily operations and quick health checks
3. **Use Anomaly Detection** for proactive monitoring and crisis prevention

The real power comes from combining all three approaches into an integrated system that provides both strategic insights and operational alerts, ensuring no restaurant falls through the cracks while maximizing revenue potential across the portfolio.