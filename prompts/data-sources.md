# Data Sources
## Data Architecture

### Core Data Entities

The system is built around twelve data tables that capture comprehensive restaurant performance and business intelligence:

1. `restaurant_master` - Core restaurant information with enhanced profiling (includes veg/non-veg type, exclusivity status, parent type, seating capacity, NPS score)
2. `restaurant_metrics` - Daily performance tracking
3. `ads_data` - Campaign performance metrics with financial details (includes total investment, fund consumption rate, YoY/MoM changes, campaign category)
4. `peer_benchmarks` - Locality and cuisine-based averages
5. `discount_history` - Promotional discount tracking
6. `operational_metrics` - Hourly operational intelligence
7. `service_quality_tracking` - Customer satisfaction metrics
8. `financial_settlements` - Financial relationship tracking
9. `competitive_intelligence` - Market positioning analysis
10. `revenue_volatility_tracking` - Anomaly detection and stability monitoring
11. `performance_feedback_loop` - Sales team feedback integration
12. `kpi_goals_tracking` - Goal setting and achievement monitoring

### Entity Relationship Model

```
restaurant_master (1) ──┬──< (N) restaurant_metrics
  (enhanced with           ├──< (N) ads_data (enhanced with financial details)
   profile extensions)     ├──< (N) discount_history
                          ├──< (N) operational_metrics
                          ├──< (N) service_quality_tracking
                          ├──< (N) financial_settlements
                          ├──< (N) revenue_volatility_tracking
                          ├──< (N) performance_feedback_loop
                          └──< (N) kpi_goals_tracking

peer_benchmarks (standalone reference table)
competitive_intelligence (standalone reference table - locality/cuisine based)
```

## Detailed Data Requirements

### 1. Restaurant Master Data (`restaurant_master`)

**Purpose**: Serves as the central registry for all restaurant partners.

**Business Justification**: Foundation table for all restaurant relationships, enabling geographic and cuisine-based segmentation for targeted strategies.

| Column | Type | Business Relevance | Sales Impact |
|--------|------|-------------------|--------------|
| `restaurant_id` | TEXT (PK) | Unique identifier for each restaurant partner | Primary key for all restaurant relationships and data linking |
| `restaurant_name` | TEXT | Restaurant brand identity and recognition | Brand-specific strategies and relationship personalization |
| `city` | TEXT | Geographic market segmentation | City-level market strategies and regional performance analysis |
| `locality` | TEXT | Micro-market segmentation within cities | Hyper-local competitive positioning and area-specific campaigns |
| `cuisine` | TEXT | Cuisine-based market categorization | Cuisine-specific benchmarking and targeted promotional strategies |
| `onboarded_date` | DATE | Partnership lifecycle and tenure tracking | Relationship maturity-based strategies and milestone recognition |
| `veg_nonveg_type` | TEXT | Market segmentation by dietary preferences | Enables targeted campaigns for specific customer segments |
| `online_order_enabled` | BOOLEAN | Digital transformation indicator | Identifies restaurants ready for digital marketing strategies |
| `establishment_date` | DATE | Restaurant maturity and market presence | Age-based strategies: new vs established restaurant approaches |
| `exclusivity_status` | TEXT | Partnership depth and commitment level | Exclusive partners get premium support and marketing |
| `parent_type` | TEXT | Business model and decision-making structure | Franchise vs independent requires different sales approaches |
| `seating_capacity` | INTEGER | Operational scale and volume potential | Capacity-based performance expectations and goals |
| `nps_score` | REAL | Customer loyalty and satisfaction indicator | Quality metric for premium positioning strategies |

**Data Quality Considerations**:
- Restaurant IDs must be immutable
- Locality names should be standardized
- Cuisine categories should follow a controlled vocabulary

### 2. Restaurant Performance Metrics (`restaurant_metrics`)

**Purpose**: Tracks daily operational performance for trend analysis.

**Business Justification**: Core performance tracking enables trend analysis, goal setting, and performance optimization strategies for restaurant partners.

| Column | Type | Business Relevance | Sales Impact |
|--------|------|-------------------|--------------|
| `id` | INTEGER (PK) | Auto-increment primary key | Technical identifier for efficient database operations |
| `restaurant_id` | TEXT (FK) | Links to restaurant master data | Performance tracking per restaurant partner |
| `restaurant_name` | TEXT | Restaurant brand identity for easy reference | Brand recognition in performance reports |
| `locality` | TEXT | Geographic context for performance | Location-based performance analysis |
| `cuisine` | TEXT | Cuisine context for peer comparison | Cuisine-specific performance benchmarking |
| `date` | DATE | Daily performance granularity | Time-based trend analysis and seasonal pattern identification |
| `bookings` | INTEGER | Core demand indicator (Orders Per Day) | Primary performance metric for demand assessment |
| `cancellations` | INTEGER | Service quality and operational efficiency indicator | Customer experience and operational improvement opportunities |
| `covers` | INTEGER | Actual customer volume served | Revenue potential and capacity utilization measurement |
| `avg_spend_per_cover` | REAL | Customer value and pricing effectiveness | Revenue optimization and pricing strategy insights |
| `revenue` | REAL | Direct business value metric (covers × avg_spend) | Financial performance and growth tracking |
| `avg_rating` | REAL | Customer satisfaction and quality indicator | Quality positioning and customer retention strategies |

**Critical Metrics**:
- **OPD (Orders Per Day)**: Core demand indicator
- **Cancellation Rate**: Operational efficiency metric
- **Cover Multiplier**: Average party size indicator
- **Revenue**: Direct business value metric

### 3. Advertising Campaign Data (`ads_data`)

**Purpose**: Measures marketing effectiveness and ROI with comprehensive financial tracking.

**Business Justification**: Campaign performance tracking enables marketing optimization, budget allocation, and ROI-driven advertising strategies. Enhanced with financial details for better budget planning and trend analysis.

| Column | Type | Business Relevance | Sales Impact |
|--------|------|-------------------|--------------|
| `id` | INTEGER (PK) | Auto-increment primary key | Technical identifier for efficient database operations |
| `restaurant_id` | TEXT (FK) | Links campaigns to specific restaurants | Campaign performance per restaurant partner |
| `campaign_id` | TEXT | Unique campaign identifier | Campaign-specific analysis and optimization |
| `campaign_start` | DATE | Campaign timing and duration tracking | Temporal performance analysis and seasonality insights |
| `campaign_end` | DATE | Campaign completion and duration calculation | Campaign length impact on performance |
| `impressions` | INTEGER | Brand visibility and reach indicator | Awareness building and market penetration measurement |
| `clicks` | INTEGER | Engagement and interest indicator | Click-through rate optimization and targeting effectiveness |
| `conversions` | INTEGER | Actual business impact (bookings generated) | Direct revenue attribution and campaign effectiveness |
| `spend` | REAL | Marketing investment per campaign | Budget allocation and cost optimization strategies |
| `revenue_generated` | REAL | Direct revenue attribution from campaign | ROI calculation and campaign profitability assessment |
| `total_investment` | REAL | Planned budget allocation | Budget planning and expectation setting |
| `fund_consumption_rate` | REAL | Spending velocity indicator | Campaign pacing and optimization |
| `yoy_funding_change` | REAL | Year-over-year investment trend | Growth trajectory and investment patterns |
| `mom_funding_change` | REAL | Month-over-month spend variance | Short-term investment optimization |
| `campaign_category` | TEXT | Detailed campaign classification | Campaign type effectiveness analysis |

**ROI Calculation**:
```
ROI = revenue_generated / spend
```

### 4. Peer Benchmark Data (`peer_benchmarks`)

**Purpose**: Enables comparative analysis within similar restaurant cohorts.

**Business Justification**: Peer benchmarking enables competitive positioning, performance gap identification, and market-appropriate goal setting for restaurant partners.

| Column | Type | Business Relevance | Sales Impact |
|--------|------|-------------------|--------------|
| `id` | INTEGER (PK) | Auto-increment primary key | Technical identifier for efficient database operations |
| `locality` | TEXT | Geographic peer grouping | Location-based competitive analysis and positioning |
| `cuisine` | TEXT | Cuisine-based peer grouping | Cuisine-specific performance benchmarking |
| `avg_bookings` | REAL | Peer average for daily bookings | Performance gap analysis and goal setting |
| `avg_conversion_rate` | REAL | Peer average for campaign conversion rates | Marketing effectiveness benchmarking |
| `avg_ads_spend` | REAL | Peer average for advertising investment | Budget allocation guidance and spend optimization |
| `avg_roi` | REAL | Peer average for return on advertising investment | ROI expectation setting and performance evaluation |
| `avg_revenue` | REAL | Peer average for daily revenue | Revenue performance positioning and growth targets |
| `avg_rating` | REAL | Peer average for customer ratings | Quality positioning and service improvement priorities |

**Benchmark Metrics**:
- Average bookings
- Average conversion rate
- Average ad spend
- Average ROI
- Average revenue
- Average rating

### 5. Discount History (`discount_history`)

**Purpose**: Tracks promotional effectiveness over time.

**Business Justification**: Discount performance tracking enables promotional strategy optimization, ROI assessment, and data-driven pricing decisions.

| Column | Type | Business Relevance | Sales Impact |
|--------|------|-------------------|--------------|
| `id` | INTEGER (PK) | Auto-increment primary key | Technical identifier for efficient database operations |
| `restaurant_id` | TEXT (FK) | Links discounts to specific restaurants | Promotional strategy tracking per restaurant partner |
| `start_date` | DATE | Discount period beginning | Promotional timing and seasonality analysis |
| `end_date` | DATE | Discount period end | Discount duration impact on effectiveness |
| `discount_type` | TEXT | Promotional strategy categorization | Discount type effectiveness comparison and optimization |
| `discount_percent` | REAL | Discount depth and customer value proposition | Price sensitivity analysis and discount optimization |
| `roi_from_discount` | REAL | Promotional return on investment | Discount profitability and strategic value assessment |

**Key Requirements**:
- Time-bound discount configurations
- Discount type categorization
- ROI impact measurement

---

### 6. Operational Metrics (`operational_metrics`)

**Purpose**: Granular operational intelligence for efficiency optimization and capacity management.

**Business Justification**: Understanding peak hours, capacity utilization, and booking patterns enables precise operational recommendations and revenue optimization strategies.

| Column | Type | Business Relevance | Sales Impact |
|--------|------|-------------------|--------------|
| `restaurant_id` | TEXT (FK) | Restaurant identifier | Links operational data to specific partner |
| `date` | DATE | Temporal tracking | Time-based trend analysis and seasonal patterns |
| `hour_slot` | INTEGER | Hourly granularity | Peak hour identification and slot optimization |
| `capacity_utilization` | REAL | Efficiency metric (% of seats filled) | Identifies under-utilized periods for promotions |
| `overbooking_incidents` | INTEGER | Service quality risk indicator | Customer experience protection strategies |
| `underbooking_slots` | INTEGER | Revenue opportunity loss | Marketing intervention opportunities |
| `online_bookings` | INTEGER | Digital channel performance | Digital marketing effectiveness measurement |
| `offline_bookings` | INTEGER | Traditional channel performance | Channel balance optimization strategies |
| `service_delay_minutes` | REAL | Operational efficiency indicator | Quality improvement action planning |

### 7. Service Quality Tracking (`service_quality_tracking`)

**Purpose**: Customer satisfaction monitoring and service excellence measurement.

**Business Justification**: Service quality directly impacts customer retention and restaurant reputation. Tracking trends enables proactive intervention and quality improvement strategies.

| Column | Type | Business Relevance | Sales Impact |
|--------|------|-------------------|--------------|
| `restaurant_id` | TEXT (FK) | Restaurant identifier | Quality performance per partner |
| `date` | DATE | Temporal tracking | Service quality trend monitoring |
| `reviews_count` | INTEGER | Customer engagement volume | Review acquisition strategies |
| `avg_service_rating` | REAL | Service-specific quality metric | Service improvement focus areas |
| `complaints_count` | INTEGER | Service failure frequency | Intervention threshold identification |
| `complaint_categories` | TEXT/JSON | Specific issue classification | Targeted improvement recommendations |
| `resolution_time_hours` | REAL | Response efficiency metric | Customer service excellence measurement |

### 8. Financial Settlements (`financial_settlements`)

**Purpose**: Financial relationship tracking and cash flow management.

**Business Justification**: Settlement patterns indicate financial health and operational efficiency. Delays or issues can signal partnership stress requiring intervention.

| Column | Type | Business Relevance | Sales Impact |
|--------|------|-------------------|--------------|
| `restaurant_id` | TEXT (FK) | Restaurant identifier | Financial relationship tracking |
| `settlement_date` | DATE | Transaction timing | Cash flow pattern analysis |
| `settlement_amount` | REAL | Financial transaction value | Revenue tracking and verification |
| `settlement_type` | TEXT | Transaction classification | Different settlement types require different handling |
| `processing_time_days` | INTEGER | Operational efficiency metric | Service quality indicator for financial operations |
| `outstanding_amount` | REAL | Pending obligations | Financial health and relationship stress indicator |

### 9. Competitive Intelligence (`competitive_intelligence`)

**Purpose**: Market positioning and competitive landscape analysis.

**Business Justification**: Understanding competitive context enables strategic positioning, pricing strategies, and differentiation approaches for restaurant partners.

| Column | Type | Business Relevance | Sales Impact |
|--------|------|-------------------|--------------|
| `locality` | TEXT | Geographic market segment | Location-based competitive strategies |
| `cuisine` | TEXT | Cuisine-based competition | Cuisine-specific positioning strategies |
| `capacity_range` | TEXT | Size-based market segment | Scale-appropriate competitive analysis |
| `competitor_count` | INTEGER | Market saturation indicator | Competition intensity assessment |
| `market_share_estimate` | REAL | Relative market position | Growth potential and strategy prioritization |
| `avg_competitor_rating` | REAL | Quality benchmark | Competitive quality positioning |
| `price_positioning` | TEXT | Price tier classification | Pricing strategy recommendations |
| `competitive_advantage_score` | REAL | Calculated advantage metric | Unique selling proposition identification |

### 10. Revenue Volatility Tracking (`revenue_volatility_tracking`)

**Purpose**: Revenue stability monitoring and anomaly detection for proactive intervention.

**Business Justification**: Revenue volatility indicates business stability. Early detection of anomalies enables proactive support and intervention strategies.

| Column | Type | Business Relevance | Sales Impact |
|--------|------|-------------------|--------------|
| `restaurant_id` | TEXT (FK) | Restaurant identifier | Individual volatility tracking |
| `date` | DATE | Temporal tracking | Anomaly detection timeline |
| `revenue_volatility_index` | REAL | Calculated stability metric | Risk assessment and intervention priority |
| `anomaly_detected` | BOOLEAN | Automated anomaly flag | Alert system for account managers |
| `anomaly_category` | TEXT | Anomaly type classification | Specific intervention strategies by anomaly type |
| `volatility_trend_7d` | REAL | Short-term volatility trend | Immediate intervention assessment |
| `volatility_trend_30d` | REAL | Medium-term volatility trend | Strategic stability evaluation |

### 11. Performance Feedback Loop (`performance_feedback_loop`)

**Purpose**: Sales team feedback integration and continuous improvement tracking.

**Business Justification**: Sales team insights and restaurant feedback create a continuous improvement loop, enabling strategy refinement and relationship optimization.

| Column | Type | Business Relevance | Sales Impact |
|--------|------|-------------------|--------------|
| `restaurant_id` | TEXT (FK) | Restaurant identifier | Feedback tracking per partner |
| `feedback_date` | DATE | Temporal feedback tracking | Feedback timeline and frequency |
| `sales_team_rating` | TEXT | Qualitative sales assessment | Team satisfaction with restaurant performance |
| `prr_score` | REAL | Performance Review Rating | Structured performance evaluation |
| `nrr_score` | REAL | Net Revenue Retention | Financial relationship health indicator |
| `feedback_notes` | TEXT | Qualitative observations | Contextual insights and specific issues |
| `action_items` | JSON | Structured follow-up tasks | Actionable improvement tracking |

### 12. KPI Goals Tracking (`kpi_goals_tracking`)

**Purpose**: Goal setting and achievement monitoring for sales team performance management.

**Business Justification**: Structured goal tracking enables performance management, expectation setting, and achievement recognition for both sales teams and restaurant partners.

| Column | Type | Business Relevance | Sales Impact |
|--------|------|-------------------|--------------|
| `restaurant_id` | TEXT (FK) | Restaurant identifier | Goal tracking per partner |
| `goal_period` | TEXT | Time-bound goal tracking | Quarterly/monthly performance cycles |
| `kpi_type` | TEXT | Metric classification | Different KPIs require different strategies |
| `target_value` | REAL | Goal definition | Clear expectations and targets |
| `actual_value` | REAL | Achievement measurement | Performance evaluation |
| `goal_phase` | TEXT | Goal timeline segmentation | Phased goal achievement tracking |
| `achievement_percentage` | REAL | Performance ratio | Success rate measurement and recognition |

## Querying

### Database Connection

The database connection details are stored in the session context. Always read the session context to get the correct database URL and the type of database.

### Example Queries (SQLite)
Use sqlite bash tool to query the database with the URL from session context:

```bash
# Example: Query ads data for restaurant R001
sqlite3 {db_url_from_session} "SELECT restaurant_id, campaign_id, spend, total_investment, campaign_category FROM ads_data WHERE restaurant_id = 'R001' LIMIT 2;"

# Example: Get restaurant performance metrics
sqlite3 {db_url_from_session} "SELECT restaurant_id, date, bookings, revenue, avg_rating FROM restaurant_metrics WHERE restaurant_id = 'R001' ORDER BY date DESC LIMIT 5;"
```

**Note**: Replace `{db_url_from_session}` with the actual database URL from the session context.