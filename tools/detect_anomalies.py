#!/usr/bin/env python3
"""
Anomaly Detection Script for Restaurant Performance Data
Detects unusual patterns, outliers, and significant deviations in restaurant metrics
"""

import json
import numpy as np
from datetime import datetime
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def load_data(session_id, artifacts_dir="artifacts"):
    """Load performance data from artifacts directory"""
    try:
        with open(f'{artifacts_dir}/{session_id}/restaurant_data.json', 'r') as f:
            restaurant_data = json.load(f)
        
        with open(f'{artifacts_dir}/{session_id}/performance_trends.json', 'r') as f:
            performance_data = json.load(f)
        
        # Try to load ad evaluation data, but it's optional
        try:
            with open(f'{artifacts_dir}/{session_id}/ad_evaluation.json', 'r') as f:
                ad_data = json.load(f)
        except FileNotFoundError:
            # If ad evaluation doesn't exist, create empty structure
            ad_data = {"individual_campaign_analysis": []}
        
        return restaurant_data, performance_data, ad_data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Required data file not found: {e}")

def detect_statistical_anomalies(daily_data, metric_name, z_threshold=2.5):
    """Detect statistical anomalies using Z-score"""
    values = [day.get(metric_name, 0) for day in daily_data]
    
    # Calculate Z-scores
    z_scores = np.abs(stats.zscore(values))
    
    anomalies = []
    for i, (day, z_score) in enumerate(zip(daily_data, z_scores)):
        if z_score > z_threshold:
            anomalies.append({
                'date': day['date'],
                'metric': metric_name,
                'value': day.get(metric_name, 0),
                'z_score': float(z_score),
                'type': 'statistical_outlier',
                'severity': 'high' if z_score > 3.0 else 'medium'
            })
    
    return anomalies

def detect_pattern_anomalies(daily_data):
    """Detect pattern-based anomalies"""
    anomalies = []
    
    # Check for sudden drops/spikes
    for i in range(1, len(daily_data)):
        prev_day = daily_data[i-1]
        curr_day = daily_data[i]
        
        # Revenue spike/drop detection
        if prev_day['revenue'] > 0:
            revenue_change = (curr_day['revenue'] - prev_day['revenue']) / prev_day['revenue'] * 100
        else:
            revenue_change = 0
        if abs(revenue_change) > 50:  # 50% change threshold
            anomalies.append({
                'date': curr_day['date'],
                'metric': 'revenue',
                'value': curr_day['revenue'],
                'previous_value': prev_day['revenue'],
                'change_percent': float(revenue_change),
                'type': 'sudden_change',
                'severity': 'high' if abs(revenue_change) > 75 else 'medium'
            })
        
        # Booking pattern anomalies
        if prev_day['bookings'] > 0:
            booking_change = (curr_day['bookings'] - prev_day['bookings']) / prev_day['bookings'] * 100
        else:
            booking_change = 0
        if abs(booking_change) > 60:  # 60% change threshold
            anomalies.append({
                'date': curr_day['date'],
                'metric': 'bookings',
                'value': curr_day['bookings'],
                'previous_value': prev_day['bookings'],
                'change_percent': float(booking_change),
                'type': 'sudden_change',
                'severity': 'high' if abs(booking_change) > 80 else 'medium'
            })

    return anomalies

def detect_operational_anomalies(daily_data):
    """Detect operational anomalies"""
    anomalies = []
    
    for day in daily_data:
        # Unusual spend per cover patterns
        spend_per_cover = day.get('avg_spend_per_cover', day['revenue']/day['covers'] if day['covers'] > 0 else 0)
        if spend_per_cover > 800 or spend_per_cover < 300:
            anomalies.append({
                'date': day['date'],
                'metric': 'avg_spend_per_cover',
                'value': spend_per_cover,
                'type': 'operational_anomaly',
                'description': f"Unusual spend per cover: ₹{spend_per_cover:.2f}",
                'severity': 'high' if spend_per_cover > 900 or spend_per_cover < 250 else 'medium'
            })
        
        # Cancellation rate anomalies
        cancellations = day.get('cancellations', 0)
        if cancellations > 0 and day['bookings'] > 0:
            cancellation_rate = cancellations / day['bookings'] * 100
            if cancellation_rate > 15:  # >15% cancellation rate
                anomalies.append({
                    'date': day['date'],
                    'metric': 'cancellation_rate',
                    'value': float(cancellation_rate),
                    'type': 'operational_anomaly',
                    'description': f"High cancellation rate: {cancellation_rate:.1f}%",
                    'severity': 'high' if cancellation_rate > 25 else 'medium'
                })
        
        # Rating anomalies
        rating = day.get('rating', day.get('avg_rating', 0))
        if rating < 4.0 and rating > 0:
            anomalies.append({
                'date': day['date'],
                'metric': 'avg_rating',
                'value': rating,
                'type': 'quality_anomaly',
                'description': f"Low rating: {rating:.1f}",
                'severity': 'high' if rating < 3.5 else 'medium'
            })

    return anomalies

def detect_trend_anomalies(performance_data):
    """Detect trend-based anomalies"""
    anomalies = []
    
    # Check for negative growth trends
    booking_growth = performance_data['performance_trends']['booking_trends']['booking_growth_rate']
    revenue_growth = performance_data['performance_trends']['revenue_trends']['revenue_growth_rate']
    
    if booking_growth < -10:
        anomalies.append({
            'metric': 'booking_growth_rate',
            'value': booking_growth,
            'type': 'negative_trend',
            'description': f"Significant booking decline: {booking_growth:.1f}%",
            'severity': 'high' if booking_growth < -20 else 'medium'
        })
    
    if revenue_growth < -15:
        anomalies.append({
            'metric': 'revenue_growth_rate',
            'value': revenue_growth,
            'type': 'negative_trend',
            'description': f"Significant revenue decline: {revenue_growth:.1f}%",
            'severity': 'high' if revenue_growth < -25 else 'medium'
        })
    
    # Check for high volatility
    booking_volatility = performance_data['performance_trends']['booking_trends']['booking_volatility']
    revenue_volatility = performance_data['performance_trends']['revenue_trends']['revenue_volatility']
    
    if booking_volatility > 5:
        anomalies.append({
            'metric': 'booking_volatility',
            'value': booking_volatility,
            'type': 'high_volatility',
            'description': f"High booking volatility: {booking_volatility:.1f} bookings/day",
            'severity': 'medium'
        })
    
    if revenue_volatility > 15000:
        anomalies.append({
            'metric': 'revenue_volatility',
            'value': revenue_volatility,
            'type': 'high_volatility',
            'description': f"High revenue volatility: ₹{revenue_volatility:.0f}/day",
            'severity': 'medium'
        })

    return anomalies

def detect_competitive_anomalies(restaurant_data, performance_data):
    """Detect competitive positioning anomalies"""
    anomalies = []
    
    # Check for performance gaps vs peers
    peer_data = restaurant_data['peer_benchmarks'][0] if restaurant_data['peer_benchmarks'] else {}
    restaurant_metrics = restaurant_data['metrics_summary']
    
    if not peer_data:
        return anomalies
    
    # Revenue comparison
    restaurant_daily_revenue = restaurant_metrics.get('total_revenue_30d', 0) / 30
    peer_daily_revenue = peer_data.get('avg_revenue', 0) / 30 if peer_data.get('avg_revenue', 0) > 1000 else peer_data.get('avg_revenue', 0)  # Handle daily vs monthly
    
    if peer_daily_revenue > 0:
        revenue_ratio = restaurant_daily_revenue / peer_daily_revenue
    else:
        revenue_ratio = 0
    
    if revenue_ratio > 3.0:
        anomalies.append({
            'metric': 'revenue_vs_peers',
            'value': float(revenue_ratio),
            'type': 'competitive_outlier',
            'description': f"Revenue {revenue_ratio:.1f}x above peer average",
            'severity': 'low'  # This is actually positive
        })
    
    # Check for underperforming metrics
    restaurant_rating = restaurant_metrics.get('avg_rating', 0)
    peer_rating = peer_data.get('avg_rating', 0)
    
    if peer_rating > 0 and restaurant_rating < peer_rating - 0.2:
        anomalies.append({
            'metric': 'rating_vs_peers',
            'value': restaurant_rating,
            'peer_value': peer_rating,
            'type': 'competitive_underperformance',
            'description': f"Rating below peer average: {restaurant_rating} vs {peer_rating}",
            'severity': 'medium'
        })

    return anomalies

def detect_ad_campaign_anomalies(ad_data):
    """Detect advertising campaign anomalies"""
    anomalies = []
    
    campaigns = ad_data.get('individual_campaign_analysis', [])
    
    for campaign in campaigns:
        metrics = campaign['performance_metrics']
        
        # Check for unusual cost per conversion
        if metrics['cost_per_conversion'] > 25:
            anomalies.append({
                'campaign_id': campaign['campaign_id'],
                'metric': 'cost_per_conversion',
                'value': metrics['cost_per_conversion'],
                'type': 'ad_inefficiency',
                'description': f"High cost per conversion: ₹{metrics['cost_per_conversion']:.2f}",
                'severity': 'high' if metrics['cost_per_conversion'] > 30 else 'medium'
            })
        
        # Check for low ROI
        if metrics['roi'] < 3.0:
            anomalies.append({
                'campaign_id': campaign['campaign_id'],
                'metric': 'roi',
                'value': metrics['roi'],
                'type': 'ad_underperformance',
                'description': f"Low ROI: {metrics['roi']:.2f}",
                'severity': 'high' if metrics['roi'] < 2.0 else 'medium'
            })

    return anomalies

def categorize_anomalies(anomalies):
    """Categorize anomalies by type and severity"""
    categorized = {
        'critical': [],
        'high': [],
        'medium': [],
        'low': []
    }
    
    for anomaly in anomalies:
        severity = anomaly.get('severity', 'medium')
        if severity == 'critical':
            categorized['critical'].append(anomaly)
        elif severity == 'high':
            categorized['high'].append(anomaly)
        elif severity == 'medium':
            categorized['medium'].append(anomaly)
        else:
            categorized['low'].append(anomaly)
    
    return categorized

def generate_anomaly_insights(anomalies):
    """Generate insights and recommendations based on detected anomalies"""
    insights = []
    recommendations = []
    
    high_severity_count = len([a for a in anomalies if a.get('severity') == 'high'])
    medium_severity_count = len([a for a in anomalies if a.get('severity') == 'medium'])
    
    if high_severity_count > 0:
        insights.append(f"Found {high_severity_count} high-severity anomalies requiring immediate attention")
        recommendations.append("Investigate high-severity anomalies first - they may indicate operational issues")
    
    if medium_severity_count > 0:
        insights.append(f"Detected {medium_severity_count} medium-severity anomalies for monitoring")
        recommendations.append("Monitor medium-severity anomalies for patterns over time")
    
    # Type-specific insights
    anomaly_types = {}
    for anomaly in anomalies:
        anomaly_type = anomaly.get('type', 'unknown')
        anomaly_types[anomaly_type] = anomaly_types.get(anomaly_type, 0) + 1
    
    for anomaly_type, count in anomaly_types.items():
        if count > 1:
            insights.append(f"Multiple {anomaly_type} anomalies detected ({count} instances)")
    
    return insights, recommendations

def update_workflow_log(session_id: str, artifacts_dir: str, workflow_name: str, status: str, error_msg: str = None):
    """Update workflow execution log and error log if needed"""
    import json
    import os
    
    # Update workflow execution log
    log_file = f"{artifacts_dir}/{session_id}/workflow_execution.json"
    
    # Load existing log or create new one
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            log_data = json.load(f)
    else:
        log_data = {"workflows": []}
    
    # Add or update workflow entry
    workflow_entry = {
        "workflow": workflow_name,
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "artifacts_created": ["anomalies.json"] if status == "completed" else []
    }
    
    # Remove existing entry for this workflow if it exists
    log_data["workflows"] = [w for w in log_data["workflows"] if w["workflow"] != workflow_name]
    log_data["workflows"].append(workflow_entry)
    
    # Save updated log
    os.makedirs(f"{artifacts_dir}/{session_id}", exist_ok=True)
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)
    
    # Update error log if there's an error
    if error_msg:
        error_log_file = f"{artifacts_dir}/{session_id}/error_log.json"
        
        # Load existing error log or create new one
        if os.path.exists(error_log_file):
            with open(error_log_file, 'r') as f:
                error_data = json.load(f)
        else:
            error_data = {"errors": []}
        
        # Add error entry
        error_entry = {
            "workflow": workflow_name,
            "error_message": error_msg,
            "timestamp": datetime.now().isoformat(),
            "status": "unresolved"
        }
        
        error_data["errors"].append(error_entry)
        
        # Save error log
        with open(error_log_file, 'w') as f:
            json.dump(error_data, f, indent=2)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Detect anomalies in restaurant performance data")
    parser.add_argument("session_id", help="Session ID for artifact management")
    parser.add_argument("--artifacts-dir", default="artifacts", help="Directory for artifact storage")
    
    args = parser.parse_args()
    
    # Update workflow log - started
    update_workflow_log(args.session_id, args.artifacts_dir, "detect-anomalies", "started")
    
    try:
        print(f"🔍 Detecting anomalies for session {args.session_id}")
        
        # Load data
        restaurant_data, performance_data, ad_data = load_data(args.session_id, args.artifacts_dir)
        daily_data = restaurant_data.get('daily_metrics', restaurant_data.get('raw_data', {}).get('daily_metrics', []))
        
        if not daily_data:
            error_msg = "No daily metrics found in restaurant data"
            update_workflow_log(args.session_id, args.artifacts_dir, "detect-anomalies", "failed", error_msg)
            print(f"Error: {error_msg}")
            return None
        
        restaurant_id = restaurant_data['restaurant_info']['restaurant_id']
        
        all_anomalies = []
        
        # Detect different types of anomalies
        print("📊 Analyzing statistical anomalies...")
        all_anomalies.extend(detect_statistical_anomalies(daily_data, 'bookings'))
        all_anomalies.extend(detect_statistical_anomalies(daily_data, 'revenue'))
        
        print("📈 Analyzing pattern anomalies...")
        all_anomalies.extend(detect_pattern_anomalies(daily_data))
        
        print("⚙️ Analyzing operational anomalies...")
        all_anomalies.extend(detect_operational_anomalies(daily_data))
        
        print("📉 Analyzing trend anomalies...")
        all_anomalies.extend(detect_trend_anomalies(performance_data))
        
        print("🏆 Analyzing competitive anomalies...")
        all_anomalies.extend(detect_competitive_anomalies(restaurant_data, performance_data))
        
        print("📺 Analyzing ad campaign anomalies...")
        all_anomalies.extend(detect_ad_campaign_anomalies(ad_data))
        
        # Categorize anomalies
        categorized_anomalies = categorize_anomalies(all_anomalies)
        
        # Generate insights
        insights, recommendations = generate_anomaly_insights(all_anomalies)
        
        # Create final report
        anomaly_report = {
            'analysis_metadata': {
                'restaurant_id': restaurant_id,
                'session_id': args.session_id,
                'analysis_date': datetime.now().isoformat(),
                'total_anomalies_detected': len(all_anomalies),
                'analysis_period': {
                    'start_date': daily_data[-1]['date'] if daily_data else None,
                    'end_date': daily_data[0]['date'] if daily_data else None,
                    'total_days': len(daily_data)
                }
            },
            'anomaly_summary': {
                'total_anomalies': len(all_anomalies),
                'by_severity': {
                    'critical': len(categorized_anomalies['critical']),
                    'high': len(categorized_anomalies['high']),
                    'medium': len(categorized_anomalies['medium']),
                    'low': len(categorized_anomalies['low'])
                },
                'by_type': {
                    'statistical_outliers': len([a for a in all_anomalies if a.get('type') == 'statistical_outlier']),
                    'sudden_changes': len([a for a in all_anomalies if a.get('type') == 'sudden_change']),
                    'operational_anomalies': len([a for a in all_anomalies if a.get('type') == 'operational_anomaly']),
                    'trend_anomalies': len([a for a in all_anomalies if a.get('type') in ['negative_trend', 'high_volatility']]),
                    'competitive_anomalies': len([a for a in all_anomalies if 'competitive' in a.get('type', '')]),
                    'ad_campaign_anomalies': len([a for a in all_anomalies if 'ad_' in a.get('type', '')])
                }
            },
            'categorized_anomalies': categorized_anomalies,
            'all_anomalies': all_anomalies,
            'insights': insights,
            'recommendations': recommendations,
            'risk_assessment': {
                'overall_risk_level': 'high' if categorized_anomalies['critical'] or len(categorized_anomalies['high']) > 3 else 'medium' if categorized_anomalies['high'] else 'low',
                'immediate_action_required': len(categorized_anomalies['critical']) > 0 or len(categorized_anomalies['high']) > 2,
                'monitoring_recommended': len(categorized_anomalies['medium']) > 0
            }
        }
        
        # Save results
        output_file = f'{args.artifacts_dir}/{args.session_id}/anomalies.json'
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(anomaly_report, f, indent=2, default=str)
        
        # Update workflow log - completed
        update_workflow_log(args.session_id, args.artifacts_dir, "detect-anomalies", "completed")
        
        print("\n✅ Anomaly detection complete!")
        print(f"📄 Results saved to: {output_file}")
        print(f"🚨 Total anomalies detected: {len(all_anomalies)}")
        print(f"⚠️  High severity: {len(categorized_anomalies['high'])}")
        print(f"📊 Medium severity: {len(categorized_anomalies['medium'])}")
        print(f"💡 Key insights: {len(insights)}")
        
        return anomaly_report
        
    except FileNotFoundError as e:
        error_msg = f"Required input file not found: {e}"
        update_workflow_log(args.session_id, args.artifacts_dir, "detect-anomalies", "failed", error_msg)
        print(f"Error: {error_msg}")
        return None
    except Exception as e:
        error_msg = f"Anomaly detection failed: {str(e)}"
        update_workflow_log(args.session_id, args.artifacts_dir, "detect-anomalies", "failed", error_msg)
        print(f"Error: {error_msg}")
        return None

if __name__ == "__main__":
    main()