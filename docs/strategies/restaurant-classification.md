# Restaurant Classification SOP - Swiggy Dineout GenAI Co-Pilot

## Document Information
- **Version**: 1.0
- **Created**: June 2025
- **Purpose**: Standardize restaurant classification for personalized AI-driven recommendations
- **Audience**: Data Science Team, Product Managers, Sales Operations

---

## 1. Executive Summary

This SOP defines the multi-dimensional classification framework for restaurants on Swiggy Dineout. The framework enables the GenAI Co-Pilot to generate personalized, actionable insights for Sales Executives by understanding each restaurant's unique context and potential.

### Core Principle
Every restaurant is classified across multiple dimensions, ultimately mapped to a Performance vs Potential matrix that drives recommendation strategies.

---

## 2. Primary Classification Framework: Performance vs Potential Matrix

### 2.1 Matrix Overview

```
                    Current Performance
                    Low                High
           ┌─────────────────┬─────────────────┐
      High │                 │                 │
           │  HIDDEN GEMS    │     STARS       │
Potential  │                 │                 │
           ├─────────────────┼─────────────────┤
           │                 │                 │
      Low  │  STRUGGLERS     │   WORKHORSES    │
           │                 │                 │
           └─────────────────┴─────────────────┘
```

### 2.2 Quadrant Definitions

#### 🌟 STARS (High Performance + High Potential)
- **Definition**: Top performers with room for growth
- **Strategy**: "Protect and scale"
- **Key Actions**: Maintain quality, increase capacity, defend market position

#### 💎 HIDDEN GEMS (Low Performance + High Potential)
- **Definition**: Underperformers in high-opportunity contexts
- **Strategy**: "Unlock demand"
- **Key Actions**: Aggressive marketing, discover barriers, capture market share

#### 🐴 WORKHORSES (High Performance + Low Potential)
- **Definition**: Maximized performers within constraints
- **Strategy**: "Optimize efficiency"
- **Key Actions**: Focus on margins, retention, operational excellence

#### ⚠️ STRUGGLERS (Low Performance + Low Potential)
- **Definition**: Poor performers with structural challenges
- **Strategy**: "Fundamental pivot"
- **Key Actions**: Major repositioning, cuisine change, or channel shift

### 2.3 Scoring Methodology

#### Performance Score (0-100)
- **OPD (Orders per day)**: 40% weight
- **Revenue**: 30% weight
- **Ad ROI**: 20% weight
- **Average Rating**: 10% weight

#### Potential Score (0-100)
- **Locality Demand**: 30% weight
- **Cuisine-Locality Fit**: 25% weight
- **Competition Gap**: 25% weight
- **Market Growth Rate**: 20% weight

---

## 3. Multi-Dimensional Classification System

### 3.1 Performance Trajectory Classifications

| Classification | Definition | Threshold | Action Focus |
|---------------|------------|-----------|--------------|
| Rising Stars | Consistent growth | >20% MoM | Scale rapidly |
| Plateaued | Stable performance | ±5% for 3+ months | Find new levers |
| Declining | Negative trajectory | <-10% MoM | Urgent intervention |
| Volatile | Unpredictable patterns | >30% variance | Stabilize first |
| Seasonal | Clear temporal patterns | >50% peak variance | Leverage patterns |

### 3.2 Maturity Stages

| Stage | Duration | Characteristics | Primary Focus |
|-------|----------|----------------|---------------|
| New Launch | <3 months | Building awareness | Adoption strategies |
| Growth Phase | 3-12 months | Rapid scaling | Capacity & quality |
| Mature | 1-3 years | Stable operations | Optimization |
| Legacy | 3+ years | Market saturation | Reinvention |

### 3.3 Ad Responsiveness Categories

| Category | ROI Pattern | Spend Level | Recommendation |
|----------|-------------|-------------|----------------|
| Ad Champions | >3x consistent | Optimal | Scale smartly |
| Ad Learners | Improving trend | Sub-optimal | Test & optimize |
| Ad Skeptics | <1x returns | Minimal | Strategy overhaul |
| Ad Virgins | No history | Zero | Education & pilot |
| Ad Churners | Stopped after losses | Zero | Targeted revival |

### 3.4 Operational Excellence Types

| Type | Key Metric | Threshold | Intervention |
|------|------------|-----------|--------------|
| Capacity Constrained | Utilization | >85% | Expand capacity |
| Under-utilized | Utilization | <40% | Demand generation |
| Peak Dependent | Weekend revenue | >70% | Weekday strategies |
| Cancellation Prone | Cancel rate | >15% | Process improvement |
| Rating Champions | Avg rating | >4.5 | Leverage for marketing |

### 3.5 Customer Behavior Archetypes

| Archetype | Booking Pattern | Marketing Focus |
|-----------|----------------|-----------------|
| Date Night Destinations | Couples, weekends | Romance angle |
| Business Lunch Hubs | Weekday noon | Corporate packages |
| Family Favorites | Large groups, early | Kids amenities |
| Party Places | Late night, groups | Event hosting |
| Solo Diner Friendly | Single bookings | Quick service |

---

## 4. Classification Correlation Matrix

### 4.1 Signal Mapping to Quadrants

| Input Signals | Likely Quadrant | Confidence |
|--------------|-----------------|------------|
| Rising Star + Ad Champion + High Locality Demand | STAR | High |
| New Launch + Under-utilized + Prime Location | HIDDEN GEM | High |
| Plateaued + Capacity Max + Legacy | WORKHORSE | High |
| Declining + Ad Churner + Poor Rating | STRUGGLER | High |

### 4.2 Multi-Signal Validation Rules

```python
# Pseudo-code for classification
if (growth_rate > 20% AND ad_roi > 3 AND locality_score > 70):
    quadrant = "STAR"
    confidence = "HIGH"
elif (current_performance < 40 AND locality_score > 70 AND cuisine_fit > 60):
    quadrant = "HIDDEN_GEM"
    confidence = "MEDIUM-HIGH"
# ... additional rules
```

---

## 5. Implementation Guidelines

### 5.1 Data Requirements

#### Required Metrics (Daily Granularity)
- Bookings count
- Revenue
- Cancellations
- Average rating
- Ad spend and attributed revenue

#### Required Context
- Restaurant locality and cuisine
- Competitor performance
- Historical patterns (min 90 days)

### 5.2 Classification Process

1. **Calculate Base Scores**
   - Performance Score (0-100)
   - Potential Score (0-100)

2. **Apply Dimensional Classifications**
   - Run through all 10 classification dimensions
   - Store classification with confidence scores

3. **Determine Primary Quadrant**
   - Plot on 2x2 matrix
   - Validate with multi-signal rules

4. **Generate Composite Profile**
   - Primary classification
   - 2-3 supporting factors
   - Confidence level

5. **Create Recommendations**
   - Strategy based on quadrant
   - Tactics based on dimensions
   - Priority based on impact potential

### 5.3 Quality Checks

- **Consistency Check**: Ensure dimensional classifications align with quadrant
- **Peer Validation**: Compare with manually classified samples
- **Temporal Stability**: Classifications shouldn't flip daily
- **Business Logic**: Recommendations must be actionable

---

## 6. Recommendation Templates by Quadrant

### 6.1 STARS Template
```
Focus: Maintain momentum while scaling
1. Increase ad spend by 20% to capture growing demand
2. Add capacity for peak hours (Fri-Sat 7-10 PM)
3. Launch loyalty program to defend against new competition
```

### 6.2 HIDDEN GEMS Template
```
Focus: Unlock latent demand
1. Launch discovery campaign with ₹X budget
2. Target [specific customer archetype] with tailored messaging
3. Optimize pricing to match locality expectations
```

### 6.3 WORKHORSES Template
```
Focus: Maximize efficiency
1. Reduce ad spend on saturated segments
2. Increase average order value through upselling
3. Focus on repeat customer rate (current: X%, target: Y%)
```

### 6.4 STRUGGLERS Template
```
Focus: Fundamental changes needed
1. Consider adding [popular cuisine] options
2. Pivot focus to delivery channel
3. Reduce fixed costs while testing new positioning
```

---

## 7. Edge Cases and Exceptions

### 7.1 New Restaurants (<30 days data)
- Use locality and cuisine benchmarks
- Focus on potential score
- Default to "Hidden Gem" strategies

### 7.2 Seasonal Businesses
- Adjust performance windows
- Use YoY comparisons
- Factor in seasonal potential

### 7.3 Multi-Concept Restaurants
- Classify each concept separately
- Aggregate for overall strategy
- Highlight best performing concept

---

## 8. Success Metrics

### 8.1 Classification Accuracy
- **Target**: 85% agreement with expert classification
- **Measure**: Quarterly validation sample

### 8.2 Recommendation Impact
- **Target**: 30% improvement in key metrics within 60 days
- **Measure**: A/B tests on recommendation adoption

### 8.3 Sales Efficiency
- **Target**: 70% reduction in prep time
- **Measure**: Sales team time tracking

---

## 9. Governance and Updates

### 9.1 Review Cycle
- **Monthly**: Threshold adjustments based on market changes
- **Quarterly**: New classification dimensions
- **Annually**: Complete framework review

### 9.2 Ownership
- **Primary**: Data Science Team Lead
- **Stakeholders**: Sales Ops, Product, Account Management

### 9.3 Change Management
- All changes require impact analysis
- A/B test new classification logic
- Maintain version history

---

## 10. Appendix: Quick Reference

### Classification Checklist
- [ ] Calculate Performance Score
- [ ] Calculate Potential Score
- [ ] Determine primary quadrant
- [ ] Apply all dimensional classifications
- [ ] Validate with multi-signal rules
- [ ] Generate composite profile
- [ ] Create prioritized recommendations
- [ ] Add confidence scores
- [ ] Review for business logic

### Common Pitfalls to Avoid
1. Over-relying on single metrics
2. Ignoring temporal patterns
3. Missing locality context
4. Generic recommendations
5. Extreme classification changes

---

## Document Control
- **Next Review Date**: September 2025
- **Distribution**: Internal - Swiggy Data Science and Sales Operations
- **Classification**: Confidential