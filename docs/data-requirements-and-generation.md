# Data Requirements and Mock Data Generation Process

## Overview

This document outlines the comprehensive data requirements for the Swiggy Dineout GenAI Co-Pilot Challenge and details the mock data generation process implemented in `init_database.py`. The data architecture is designed to support real-time performance analytics, peer benchmarking, and actionable insights generation for Sales Executives and Account Managers.

## Data Architecture

### Core Data Entities

The system is built around five primary data tables that capture different aspects of restaurant performance:

1. **Restaurant Master** - Core restaurant information
2. **Restaurant Metrics** - Daily performance tracking
3. **Ads Data** - Campaign performance metrics
4. **Peer Benchmarks** - Locality and cuisine-based averages
5. **Discount History** - Promotional discount tracking

### Entity Relationship Model

```
restaurant_master (1) ──┬──< (N) restaurant_metrics
                       ├──< (N) ads_data
                       └──< (N) discount_history

peer_benchmarks (standalone reference table)
```

## Detailed Data Requirements

### 1. Restaurant Master Data

**Purpose**: Serves as the central registry for all restaurant partners.

**Key Requirements**:
- Unique identifier for each restaurant
- Geographic segmentation (city, locality)
- Cuisine classification for peer grouping
- Onboarding date for lifecycle analysis

**Data Quality Considerations**:
- Restaurant IDs must be immutable
- Locality names should be standardized
- Cuisine categories should follow a controlled vocabulary

### 2. Restaurant Performance Metrics

**Purpose**: Tracks daily operational performance for trend analysis.

**Key Requirements**:
- Daily granularity for 30-day rolling analysis
- Booking lifecycle tracking (bookings → cancellations → covers)
- Revenue calculation components (covers × avg_spend)
- Quality metric through ratings

**Critical Metrics**:
- **OPD (Orders Per Day)**: Core demand indicator
- **Cancellation Rate**: Operational efficiency metric
- **Cover Multiplier**: Average party size indicator
- **Revenue**: Direct business value metric

### 3. Advertising Campaign Data

**Purpose**: Measures marketing effectiveness and ROI.

**Key Requirements**:
- Campaign-level granularity
- Full funnel tracking (impressions → clicks → conversions)
- Financial metrics (spend, revenue_generated)
- Date range tracking for temporal analysis

**ROI Calculation**:
```
ROI = revenue_generated / spend
```

### 4. Peer Benchmark Data

**Purpose**: Enables comparative analysis within similar restaurant cohorts.

**Key Requirements**:
- Locality + Cuisine combination as grouping key
- Aggregated metrics across peer groups
- Same metric definitions as individual restaurant data

**Benchmark Metrics**:
- Average bookings
- Average conversion rate
- Average ad spend
- Average ROI
- Average revenue
- Average rating

### 5. Discount History

**Purpose**: Tracks promotional effectiveness over time.

**Key Requirements**:
- Time-bound discount configurations
- Discount type categorization
- ROI impact measurement

## Mock Data Generation Strategy

### 1. Data Volume and Distribution

The mock data generator creates:
- 5 restaurants across 3 cities
- 31 days of daily metrics per restaurant (155 total records)
- 2-4 ad campaigns per restaurant (10-20 total campaigns)
- 25 locality-cuisine benchmark combinations
- 1-3 discount periods per restaurant

### 2. Realistic Data Patterns

#### Restaurant Performance Patterns
```python
# Base performance with daily variations
base_bookings = random.randint(8, 25)  # Restaurant-specific baseline
daily_bookings = base_bookings + random.randint(-5, 8)  # Daily fluctuation

# Realistic cancellation rates (5-15%)
cancellations = int(bookings * random.uniform(0.05, 0.15))

# Cover multiplier (2-4 people per booking)
covers = bookings * random.randint(2, 4)
```

#### Ad Campaign Patterns
```python
# Realistic funnel metrics
CTR = 5-12%  # Click-through rate from impressions
Conversion Rate = 6-15%  # Booking rate from clicks

# Campaign types reflecting real scenarios
campaign_types = ['visibility_boost', 'weekend_special', 'lunch_deals', 'dinner_prime']
```

### 3. Data Consistency Rules

1. **Temporal Consistency**: All dates are generated relative to current date
2. **Metric Relationships**: Revenue = covers × avg_spend_per_cover
3. **Rating Constraints**: Ratings bounded between 1.0 and 5.0
4. **Foreign Key Integrity**: All references to restaurant_id are valid

### 4. Business Logic Embedded in Mock Data

#### Performance Variations
- Restaurants have consistent "personality" (base metrics)
- Daily variations simulate real-world fluctuations
- Rating variations are small (±0.3) to reflect stability

#### Campaign Effectiveness
- Higher spend generally correlates with more impressions
- Conversion rates vary by campaign type (implicit)
- ROI ranges from 2.2x to 3.8x (profitable campaigns)

#### Discount Impact
- Discount percentages range from 5% to 25%
- ROI from discounts (2.0x to 4.2x) shows positive impact

## Data Quality Assurance

### 1. Validation Rules

- **Unique Constraints**: (restaurant_id, date) for metrics, (restaurant_id, campaign_id) for ads
- **Check Constraints**: Ratings between 1.0 and 5.0
- **Foreign Key Constraints**: All restaurant_id references validated
- **Non-negative Values**: All counts and monetary values ≥ 0

### 2. Data Completeness

- Every restaurant has 31 days of metrics
- Every restaurant has at least 2 ad campaigns
- All locality-cuisine combinations have benchmarks
- No null values in required fields

### 3. Business Rule Compliance

- Cancellations never exceed bookings
- Revenue calculations are consistent
- Campaign dates don't overlap for same restaurant
- Discount periods are realistic (2-6 weeks)

## Usage Guidelines for AI/ML Applications

### 1. Feature Engineering Opportunities

- **Trend Analysis**: 30-day rolling averages, week-over-week growth
- **Seasonality**: Day-of-week patterns, weekend vs weekday
- **Campaign Attribution**: Pre/during/post campaign performance
- **Peer Positioning**: Performance indices relative to benchmarks

### 2. Insight Generation Patterns

- **Performance Anomalies**: Identify days with unusual metrics
- **Campaign Effectiveness**: Compare campaign ROI to peer averages
- **Growth Opportunities**: Gap analysis vs peer benchmarks
- **Optimization Targets**: Underperforming metrics identification

### 3. Prompt Engineering Considerations

When using this data with LLMs:
- Provide clear metric definitions
- Include temporal context (last 30 days)
- Reference peer benchmarks for comparison
- Focus on actionable insights

## Future Enhancements

### 1. Additional Data Sources
- Customer demographics
- Menu item performance
- Seasonal event calendars
- Competitor presence data

### 2. Advanced Metrics
- Customer lifetime value
- Repeat booking rate
- Time-slot optimization data
- Weather impact correlations

### 3. Real-time Capabilities
- Streaming data ingestion
- Live dashboard updates
- Predictive alerts
- Dynamic benchmarking

## Conclusion

The mock data generation process creates a realistic, self-consistent dataset that mirrors real-world restaurant performance patterns. This foundation enables the development and testing of AI-powered insights that can meaningfully impact sales conversations and drive business growth for restaurant partners.