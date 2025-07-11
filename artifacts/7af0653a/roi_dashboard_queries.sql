-- ROI Dashboard SQL Queries for Spice Garden (R001)
-- Swiggy Dineout Smart Advertising Analytics

-- ============================================
-- 1. REAL-TIME CAMPAIGN PERFORMANCE
-- ============================================

-- Daily ROI Tracker
SELECT 
    DATE(campaign_start) as date,
    campaign_category,
    campaign_id,
    SUM(impressions) as impressions,
    SUM(clicks) as clicks,
    SUM(conversions) as conversions,
    SUM(spend) as spend,
    SUM(revenue_generated) as revenue,
    ROUND(SUM(revenue_generated) / NULLIF(SUM(spend), 0), 2) as roi,
    ROUND(100.0 * SUM(clicks) / NULLIF(SUM(impressions), 0), 2) as ctr,
    ROUND(100.0 * SUM(conversions) / NULLIF(SUM(clicks), 0), 2) as conv_rate,
    ROUND(SUM(spend) / NULLIF(SUM(conversions), 0), 2) as cpa
FROM ads_data
WHERE restaurant_id = 'R001'
    AND campaign_start >= DATE('now', '-30 days')
GROUP BY DATE(campaign_start), campaign_category, campaign_id
ORDER BY date DESC, roi DESC;

-- Hourly Performance Analysis
WITH hourly_bookings AS (
    SELECT 
        hour_slot,
        AVG(online_bookings + offline_bookings) as avg_bookings,
        AVG(capacity_utilization) as avg_utilization
    FROM operational_metrics
    WHERE restaurant_id = 'R001'
        AND date >= DATE('now', '-30 days')
    GROUP BY hour_slot
)
SELECT 
    hour_slot,
    CASE 
        WHEN hour_slot BETWEEN 12 AND 15 THEN 'Lunch Rush'
        WHEN hour_slot BETWEEN 19 AND 22 THEN 'Dinner Peak'
        ELSE 'Off-Peak'
    END as period,
    avg_bookings,
    avg_utilization,
    ROUND((100 - avg_utilization) * 0.01 * 100, 0) as available_capacity
FROM hourly_bookings
ORDER BY avg_bookings DESC;

-- ============================================
-- 2. CAMPAIGN COMPARISON & OPTIMIZATION
-- ============================================

-- Campaign Category Performance
SELECT 
    campaign_category,
    COUNT(DISTINCT campaign_id) as campaigns_run,
    SUM(spend) as total_spend,
    SUM(revenue_generated) as total_revenue,
    SUM(conversions) as total_conversions,
    ROUND(SUM(revenue_generated) / NULLIF(SUM(spend), 0), 2) as category_roi,
    ROUND(SUM(spend) / NULLIF(SUM(conversions), 0), 2) as avg_cpa,
    ROUND(SUM(revenue_generated) / NULLIF(SUM(conversions), 0), 2) as avg_order_value
FROM ads_data
WHERE restaurant_id = 'R001'
GROUP BY campaign_category
ORDER BY category_roi DESC;

-- Day of Week Performance
SELECT 
    CASE strftime('%w', date)
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        WHEN '6' THEN 'Saturday'
    END as day_name,
    strftime('%w', date) as day_number,
    AVG(bookings) as avg_bookings,
    AVG(revenue) as avg_revenue,
    AVG(covers) as avg_covers,
    COUNT(*) as days_in_sample
FROM restaurant_metrics
WHERE restaurant_id = 'R001'
    AND date >= DATE('now', '-30 days')
GROUP BY strftime('%w', date)
ORDER BY day_number;

-- ============================================
-- 3. COMPETITIVE BENCHMARKING
-- ============================================

-- Spice Garden vs Peer Performance
WITH restaurant_performance AS (
    SELECT 
        'R001' as restaurant_id,
        'Spice Garden' as name,
        AVG(bookings) as avg_bookings,
        AVG(revenue) as avg_revenue,
        AVG(revenue) / NULLIF(AVG(bookings), 0) as avg_check_size
    FROM restaurant_metrics
    WHERE restaurant_id = 'R001'
        AND date >= DATE('now', '-30 days')
),
peer_performance AS (
    SELECT 
        'Koramangala Indian Avg' as name,
        avg_bookings,
        avg_revenue,
        avg_revenue / NULLIF(avg_bookings, 0) as avg_check_size,
        avg_roi,
        avg_ads_spend
    FROM peer_benchmarks
    WHERE locality = 'Koramangala' AND cuisine = 'Indian'
)
SELECT 
    r.name,
    ROUND(r.avg_bookings, 1) as avg_daily_bookings,
    ROUND(r.avg_revenue, 0) as avg_daily_revenue,
    ROUND(r.avg_check_size, 0) as avg_check,
    ROUND((r.avg_bookings - p.avg_bookings) / p.avg_bookings * 100, 1) as bookings_vs_peer_pct,
    ROUND((r.avg_revenue - p.avg_revenue) / p.avg_revenue * 100, 1) as revenue_vs_peer_pct
FROM restaurant_performance r
CROSS JOIN peer_performance p
UNION ALL
SELECT 
    name,
    ROUND(avg_bookings, 1),
    ROUND(avg_revenue, 0),
    ROUND(avg_check_size, 0),
    0.0,
    0.0
FROM peer_performance;

-- ============================================
-- 4. CUSTOMER ACQUISITION & RETENTION
-- ============================================

-- Customer Acquisition Cost Trends
SELECT 
    strftime('%Y-%m', campaign_start) as month,
    SUM(spend) as monthly_spend,
    SUM(conversions) as new_customers,
    ROUND(SUM(spend) / NULLIF(SUM(conversions), 0), 2) as cac,
    ROUND(SUM(revenue_generated) / NULLIF(SUM(conversions), 0), 2) as first_order_value,
    ROUND((SUM(revenue_generated) / NULLIF(SUM(conversions), 0)) / 
          (SUM(spend) / NULLIF(SUM(conversions), 0)), 2) as first_order_roi
FROM ads_data
WHERE restaurant_id = 'R001'
GROUP BY strftime('%Y-%m', campaign_start)
ORDER BY month DESC;

-- Conversion Funnel Analysis
SELECT 
    campaign_category,
    SUM(impressions) as impressions,
    SUM(clicks) as clicks,
    SUM(conversions) as bookings,
    ROUND(100.0 * SUM(clicks) / NULLIF(SUM(impressions), 0), 2) as impression_to_click_pct,
    ROUND(100.0 * SUM(conversions) / NULLIF(SUM(clicks), 0), 2) as click_to_booking_pct,
    ROUND(100.0 * SUM(conversions) / NULLIF(SUM(impressions), 0), 4) as overall_conversion_pct
FROM ads_data
WHERE restaurant_id = 'R001'
    AND campaign_start >= DATE('now', '-30 days')
GROUP BY campaign_category;

-- ============================================
-- 5. ROI OPTIMIZATION OPPORTUNITIES
-- ============================================

-- Identify High-Potential Time Slots
WITH slot_performance AS (
    SELECT 
        hour_slot,
        AVG(capacity_utilization) as avg_utilization,
        AVG(online_bookings + offline_bookings) as avg_bookings,
        100 - AVG(capacity_utilization) as available_capacity_pct
    FROM operational_metrics
    WHERE restaurant_id = 'R001'
        AND date >= DATE('now', '-14 days')
    GROUP BY hour_slot
)
SELECT 
    hour_slot,
    ROUND(avg_utilization, 1) as current_utilization_pct,
    ROUND(avg_bookings, 1) as avg_bookings,
    ROUND(available_capacity_pct, 1) as growth_potential_pct,
    CASE 
        WHEN available_capacity_pct > 40 AND hour_slot BETWEEN 12 AND 15 THEN 'High Priority - Lunch'
        WHEN available_capacity_pct > 40 AND hour_slot BETWEEN 19 AND 22 THEN 'High Priority - Dinner'
        WHEN available_capacity_pct > 30 THEN 'Medium Priority'
        ELSE 'Low Priority'
    END as optimization_priority
FROM slot_performance
WHERE available_capacity_pct > 20
ORDER BY 
    CASE 
        WHEN hour_slot BETWEEN 12 AND 15 OR hour_slot BETWEEN 19 AND 22 
        THEN available_capacity_pct 
        ELSE 0 
    END DESC;

-- Budget Reallocation Recommendations
WITH campaign_efficiency AS (
    SELECT 
        campaign_category,
        SUM(spend) as total_spend,
        SUM(revenue_generated) as total_revenue,
        ROUND(SUM(revenue_generated) / NULLIF(SUM(spend), 0), 2) as roi,
        ROUND(100.0 * SUM(spend) / 
            (SELECT SUM(spend) FROM ads_data WHERE restaurant_id = 'R001'), 1) as spend_share_pct
    FROM ads_data
    WHERE restaurant_id = 'R001'
    GROUP BY campaign_category
)
SELECT 
    campaign_category,
    spend_share_pct as current_budget_pct,
    roi as current_roi,
    CASE 
        WHEN roi > 10 THEN spend_share_pct * 1.5
        WHEN roi > 8 THEN spend_share_pct * 1.2
        WHEN roi > 5 THEN spend_share_pct * 1.0
        ELSE spend_share_pct * 0.5
    END as recommended_budget_pct,
    CASE 
        WHEN roi > 10 THEN 'Scale Up 50%'
        WHEN roi > 8 THEN 'Scale Up 20%'
        WHEN roi > 5 THEN 'Maintain'
        ELSE 'Scale Down 50%'
    END as action
FROM campaign_efficiency
ORDER BY roi DESC;

-- ============================================
-- 6. PREDICTIVE ANALYTICS
-- ============================================

-- Revenue Projection Based on Ad Spend
WITH spend_revenue_correlation AS (
    SELECT 
        DATE(campaign_start) as date,
        SUM(spend) as daily_spend,
        SUM(revenue_generated) as ad_revenue,
        (SELECT SUM(revenue) FROM restaurant_metrics 
         WHERE restaurant_id = 'R001' 
         AND date = DATE(ads_data.campaign_start)) as total_revenue
    FROM ads_data
    WHERE restaurant_id = 'R001'
        AND campaign_start >= DATE('now', '-30 days')
    GROUP BY DATE(campaign_start)
)
SELECT 
    ROUND(AVG(daily_spend), 0) as avg_daily_spend,
    ROUND(AVG(ad_revenue), 0) as avg_ad_revenue,
    ROUND(AVG(total_revenue), 0) as avg_total_revenue,
    ROUND(AVG(ad_revenue) / NULLIF(AVG(daily_spend), 0), 2) as avg_roi,
    ROUND(100.0 * AVG(ad_revenue) / NULLIF(AVG(total_revenue), 0), 1) as ad_revenue_contribution_pct
FROM spend_revenue_correlation;

-- Weekly Performance Trend
SELECT 
    strftime('%Y-W%W', campaign_start) as week,
    SUM(spend) as weekly_spend,
    SUM(conversions) as weekly_conversions,
    SUM(revenue_generated) as weekly_revenue,
    ROUND(SUM(revenue_generated) / NULLIF(SUM(spend), 0), 2) as weekly_roi,
    ROUND(SUM(spend) / 7, 0) as avg_daily_spend,
    ROUND(SUM(conversions) / 7, 1) as avg_daily_conversions
FROM ads_data
WHERE restaurant_id = 'R001'
    AND campaign_start >= DATE('now', '-90 days')
GROUP BY strftime('%Y-W%W', campaign_start)
ORDER BY week DESC
LIMIT 12;

-- ============================================
-- 7. ALERTS & MONITORING
-- ============================================

-- Real-time Performance Alerts
SELECT 
    'ALERT' as status,
    CASE 
        WHEN roi < 5 THEN 'CRITICAL: ROI below 5x threshold'
        WHEN cpa > 20 THEN 'WARNING: CPA exceeds ₹20 limit'
        WHEN ctr < 3 THEN 'WARNING: CTR below 3% minimum'
        WHEN daily_spend > 500 THEN 'WARNING: Daily spend exceeds ₹500'
        ELSE 'OK: All metrics within range'
    END as alert_message,
    roi,
    cpa,
    ctr,
    daily_spend
FROM (
    SELECT 
        ROUND(SUM(revenue_generated) / NULLIF(SUM(spend), 0), 2) as roi,
        ROUND(SUM(spend) / NULLIF(SUM(conversions), 0), 2) as cpa,
        ROUND(100.0 * SUM(clicks) / NULLIF(SUM(impressions), 0), 2) as ctr,
        SUM(spend) as daily_spend
    FROM ads_data
    WHERE restaurant_id = 'R001'
        AND DATE(campaign_start) = DATE('now')
);

-- Campaign Health Score
SELECT 
    campaign_id,
    campaign_category,
    ROUND(
        (CASE WHEN roi > 10 THEN 30 ELSE roi * 3 END) +
        (CASE WHEN ctr > 10 THEN 25 ELSE ctr * 2.5 END) +
        (CASE WHEN conv_rate > 15 THEN 25 ELSE conv_rate * 1.67 END) +
        (CASE WHEN cpa < 10 THEN 20 ELSE 200 / cpa END)
    , 1) as health_score,
    roi,
    ctr,
    conv_rate,
    cpa
FROM (
    SELECT 
        campaign_id,
        campaign_category,
        ROUND(revenue_generated / NULLIF(spend, 0), 2) as roi,
        ROUND(100.0 * clicks / NULLIF(impressions, 0), 2) as ctr,
        ROUND(100.0 * conversions / NULLIF(clicks, 0), 2) as conv_rate,
        ROUND(spend / NULLIF(conversions, 0), 2) as cpa,
        revenue_generated,
        spend,
        clicks,
        impressions,
        conversions
    FROM ads_data
    WHERE restaurant_id = 'R001'
        AND campaign_end >= DATE('now')
)
ORDER BY health_score DESC;