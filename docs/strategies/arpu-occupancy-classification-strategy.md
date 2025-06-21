# ARPU & Occupancy-Based Restaurant Classification Strategy
## Swiggy Dineout GenAI Co-Pilot Enhancement

---

## 1. Executive Summary

This strategy redefines the restaurant classification framework by centering on two critical business metrics:
- **ARPU (Average Revenue Per User)**: Measures monetization efficiency
- **Occupancy Rate**: Measures demand fulfillment and operational efficiency

These metrics directly correlate to restaurant health and provide actionable insights for sales interventions.

---

## 2. Redefined Performance vs Potential Matrix

### 2.1 New Matrix Definition

```
                    ARPU (Revenue Efficiency)
                    Low                High
           ┌─────────────────┬─────────────────┐
      High │                 │                 │
           │  VOLUME PLAYS   │   PREMIUM STARS │
Occupancy  │                 │                 │
   Rate    ├─────────────────┼─────────────────┤
           │                 │                 │
      Low  │  STRUGGLERS     │  LUXURY NICHE   │
           │                 │                 │
           └─────────────────┴─────────────────┘
```

### 2.2 Quadrant Definitions with ARPU & Occupancy

#### 🌟 PREMIUM STARS (High ARPU + High Occupancy)
- **Metrics**: ARPU > ₹800, Occupancy > 70%
- **Characteristics**: Premium positioning with strong demand
- **Strategy**: Scale while maintaining premium experience
- **Actions**: 
  - Expand capacity during peak hours
  - Introduce premium offerings
  - Dynamic pricing optimization

#### 📊 VOLUME PLAYS (Low ARPU + High Occupancy)
- **Metrics**: ARPU < ₹500, Occupancy > 70%
- **Characteristics**: Mass market appeal, thin margins
- **Strategy**: Optimize for efficiency and upsell
- **Actions**:
  - Menu engineering for higher margins
  - Table turnover optimization
  - Add-on sales campaigns

#### 💎 LUXURY NICHE (High ARPU + Low Occupancy)
- **Metrics**: ARPU > ₹800, Occupancy < 40%
- **Characteristics**: Premium but underutilized
- **Strategy**: Increase footfall without diluting brand
- **Actions**:
  - Targeted marketing to HNI segments
  - Exclusive events and experiences
  - Strategic time-based offers

#### ⚠️ STRUGGLERS (Low ARPU + Low Occupancy)
- **Metrics**: ARPU < ₹500, Occupancy < 40%
- **Characteristics**: Fundamental business model issues
- **Strategy**: Complete repositioning needed
- **Actions**:
  - Concept pivot evaluation
  - Cost structure overhaul
  - Channel strategy revision

---

## 3. Metric Calculation Framework

### 3.1 ARPU Calculation
```python
# Daily ARPU
daily_arpu = total_revenue / total_unique_customers

# Weighted ARPU (accounts for party size)
weighted_arpu = total_revenue / total_covers

# Time-segmented ARPU
lunch_arpu = lunch_revenue / lunch_customers
dinner_arpu = dinner_revenue / dinner_customers
```

### 3.2 Occupancy Rate Calculation
```python
# Basic Occupancy
occupancy_rate = (seats_occupied_hours / total_available_seat_hours) * 100

# Peak Hour Occupancy
peak_occupancy = (peak_seats_occupied / total_seats) * 100

# Weighted Occupancy (by revenue potential)
weighted_occupancy = sum(hourly_occupancy * hourly_revenue_weight)
```

### 3.3 Composite Scoring

**Performance Score = 0.6 × ARPU_normalized + 0.4 × Occupancy_normalized**

**Potential Score Factors:**
- Locality average ARPU ceiling
- Competitive occupancy benchmarks
- Historical growth trajectory
- Market expansion opportunities

---

## 4. Anomaly Detection System

### 4.1 Statistical Anomaly Detection

#### Time Series Decomposition
```python
# Detect anomalies in ARPU
arpu_components = seasonal_decompose(daily_arpu, period=7)
arpu_anomalies = detect_outliers(arpu_components.resid, method='isolation_forest')

# Detect anomalies in Occupancy
occupancy_components = seasonal_decompose(hourly_occupancy, period=24)
occupancy_anomalies = detect_outliers(occupancy_components.resid, method='mad')
```

#### Multi-variate Detection
```python
# Combined anomaly score
features = [arpu, occupancy, bookings, cancellations]
anomaly_score = isolation_forest.decision_function(features)
```

### 4.2 Business Logic Anomalies

| Anomaly Type | Detection Rule | Alert Priority |
|--------------|----------------|----------------|
| ARPU Cliff | Drop > 25% WoW | Critical |
| Occupancy Vacuum | < 20% on typically busy day | High |
| Revenue-Occupancy Mismatch | High occupancy + Low revenue | Medium |
| Booking-Show Discrepancy | Show rate < 70% | High |
| Rating-Revenue Divergence | Rating up + Revenue down | Medium |

### 4.3 Contextual Anomaly Patterns

#### Competitive Anomalies
- Restaurant ARPU drops while locality average rises
- Occupancy falls during competitor promotions

#### Seasonal Anomalies
- Festival period underperformance
- Weather-adjusted occupancy drops

#### Operational Anomalies
- Kitchen capacity vs occupancy mismatch
- Staff shortage indicators

---

## 5. Real-time Monitoring & Alert System

### 5.1 Monitoring Dashboard Metrics

**Primary KPIs**
- Current ARPU vs 7-day MA
- Current Occupancy vs same hour last week
- Anomaly score (0-100)
- Alert count by severity

**Drill-down Metrics**
- ARPU by meal period
- Occupancy heatmap (day × hour)
- Cancellation impact on metrics
- Competition benchmark overlay

### 5.2 Alert Framework

```yaml
alerts:
  critical:
    - metric: arpu_drop
      threshold: -25%
      window: 7_days
      action: immediate_intervention
    
  high:
    - metric: occupancy_anomaly
      threshold: 3_sigma
      window: same_hour_comparison
      action: investigate_causes
    
  medium:
    - metric: arpu_occupancy_divergence
      threshold: correlation < 0.3
      window: 14_days
      action: strategy_review
```

---

## 6. Implementation Strategy

### 6.1 Phase 1: Data Foundation (Weeks 1-2)
- [ ] Set up ARPU calculation pipeline
- [ ] Implement occupancy tracking system
- [ ] Historical data backfill (90 days)
- [ ] Baseline metric establishment

### 6.2 Phase 2: Classification System (Weeks 3-4)
- [ ] Implement quadrant classification
- [ ] Calculate performance & potential scores
- [ ] Validate against manual classifications
- [ ] Fine-tune thresholds

### 6.3 Phase 3: Anomaly Detection (Weeks 5-6)
- [ ] Deploy statistical models
- [ ] Implement business rule engine
- [ ] Set up alert mechanisms
- [ ] Train ML models on historical anomalies

### 6.4 Phase 4: Actionable Intelligence (Weeks 7-8)
- [ ] Build recommendation engine
- [ ] Create intervention playbooks
- [ ] Integrate with sales tools
- [ ] Launch pilot with select restaurants

---

## 7. Intervention Playbooks by Classification

### 7.1 PREMIUM STARS Interventions
**When ARPU/Occupancy Drops Detected:**
1. Check competitive landscape for new entrants
2. Analyze menu price perception
3. Review service quality metrics
4. Implement VIP retention program

### 7.2 VOLUME PLAYS Interventions
**When Margins Compress:**
1. Menu engineering workshop
2. Implement dynamic pricing
3. Optimize table turnover time
4. Launch combo/bundle offers

### 7.3 LUXURY NICHE Interventions
**When Occupancy Stagnates:**
1. Create exclusive experiences
2. Partner with luxury brands
3. Implement referral programs
4. Strategic PR campaigns

### 7.4 STRUGGLERS Interventions
**When Both Metrics Decline:**
1. Comprehensive audit
2. Concept pivot evaluation
3. Cost reduction plan
4. Alternative channel focus

---

## 8. Success Metrics & KPIs

### 8.1 Classification Accuracy
- Quadrant stability: <10% monthly movement
- Prediction accuracy: >85% for 30-day trajectory

### 8.2 Anomaly Detection Performance
- True positive rate: >90%
- False positive rate: <15%
- Mean time to detection: <2 hours

### 8.3 Business Impact
- ARPU improvement: 15% in 60 days post-intervention
- Occupancy improvement: 10% in 30 days post-intervention
- Sales efficiency: 50% reduction in analysis time

---

## 9. Technical Architecture

### 9.1 Data Pipeline
```
Raw Data → ETL → Feature Engineering → Classification → Anomaly Detection → Recommendations
    ↓         ↓            ↓                ↓                ↓                    ↓
 Bookings   Clean      ARPU/Occupancy   Quadrants      Alerts            Interventions
```

### 9.2 ML Model Stack
- **Classification**: XGBoost for quadrant prediction
- **Anomaly Detection**: Isolation Forest + Prophet
- **Recommendation**: Collaborative filtering + Rule engine

### 9.3 Real-time Processing
- Stream processing for live metrics
- 5-minute aggregation windows
- Sub-minute alert generation

---

## 10. Advanced Analytics Opportunities

### 10.1 Predictive Capabilities
- 7-day ARPU forecast
- Occupancy prediction by hour
- Churn risk scoring

### 10.2 Prescriptive Analytics
- Optimal pricing recommendations
- Capacity planning suggestions
- Marketing spend allocation

### 10.3 Cross-dimensional Insights
- ARPU × Occupancy × Customer Satisfaction
- Revenue optimization surfaces
- Multi-restaurant portfolio optimization

---

## Appendix A: Metric Formulas

### ARPU Variations
```
Base ARPU = Revenue / Unique Customers
Seat ARPU = Revenue / (Seats × Operating Hours)
Cover ARPU = Revenue / Total Covers
Adjusted ARPU = (Revenue - Discounts) / Paying Customers
```

### Occupancy Variations
```
Seat Occupancy = Occupied Seats / Total Seats
Revenue Occupancy = Actual Revenue / Max Potential Revenue
Cover Occupancy = Actual Covers / Max Capacity Covers
Time-weighted Occupancy = Σ(Hourly Occupancy × Hour Weight)
```

### Anomaly Scores
```
Z-Score = (Value - Mean) / StdDev
MAD Score = |Value - Median| / MAD
IQR Score = Value outside (Q1 - 1.5×IQR, Q3 + 1.5×IQR)
ML Score = Model.predict_proba(anomaly)
```

---

## Appendix B: Quick Decision Tree

```
IF occupancy < 40% AND arpu < 500:
    → STRUGGLER: Major intervention needed
ELIF occupancy > 70% AND arpu > 800:
    → PREMIUM STAR: Scale & defend
ELIF occupancy > 70% AND arpu < 500:
    → VOLUME PLAY: Optimize margins
ELIF occupancy < 40% AND arpu > 800:
    → LUXURY NICHE: Increase footfall
ELSE:
    → TRANSITIONAL: Monitor closely
```