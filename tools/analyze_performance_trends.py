#!/usr/bin/env python3
"""
Performance Trends Analysis for Restaurant Intelligence System
Analyzes 30-day performance trends, calculates key metrics, and identifies patterns.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import statistics

def load_restaurant_data(file_path: str) -> Dict[str, Any]:
    """Load restaurant data from JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def calculate_performance_trends(daily_metrics: List[Dict]) -> Dict[str, Any]:
    """Calculate performance trends from daily metrics."""
    
    # Sort by date to ensure chronological order
    sorted_metrics = sorted(daily_metrics, key=lambda x: x['date'])
    
    # Extract time series data
    dates = [item['date'] for item in sorted_metrics]
    bookings = [item['bookings'] for item in sorted_metrics]
    revenue = [item['revenue'] for item in sorted_metrics]
    ratings = [item.get('rating', item.get('avg_rating', 0)) for item in sorted_metrics]
    cancellations = [item.get('cancellations', 0) for item in sorted_metrics]
    covers = [item['covers'] for item in sorted_metrics]
    avg_spend = [item.get('avg_spend_per_cover', item['revenue']/item['covers'] if item['covers'] > 0 else 0) for item in sorted_metrics]
    
    # Calculate weekly trends (split into 4 weeks + 3 days)
    weekly_data = []
    week_size = 7
    
    for i in range(0, len(sorted_metrics), week_size):
        week_data = sorted_metrics[i:i+week_size]
        if len(week_data) > 0:
            week_bookings = sum(d['bookings'] for d in week_data)
            week_revenue = sum(d['revenue'] for d in week_data)
            week_covers = sum(d['covers'] for d in week_data)
            week_cancellations = sum(d.get('cancellations', 0) for d in week_data)
            avg_rating = statistics.mean(d.get('rating', d.get('avg_rating', 0)) for d in week_data)
            
            weekly_data.append({
                'week_number': len(weekly_data) + 1,
                'start_date': week_data[0]['date'],
                'end_date': week_data[-1]['date'],
                'total_bookings': week_bookings,
                'total_revenue': week_revenue,
                'total_covers': week_covers,
                'total_cancellations': week_cancellations,
                'avg_rating': round(avg_rating, 2),
                'days_in_week': len(week_data)
            })
    
    # Calculate growth rates
    def calculate_growth_rate(values: List[float]) -> float:
        if len(values) < 2:
            return 0.0
        first_half = values[:len(values)//2]
        second_half = values[len(values)//2:]
        
        avg_first = statistics.mean(first_half)
        avg_second = statistics.mean(second_half)
        
        if avg_first == 0:
            return 0.0
        return ((avg_second - avg_first) / avg_first) * 100
    
    # Performance metrics
    trends = {
        'booking_trends': {
            'total_bookings': sum(bookings),
            'avg_daily_bookings': round(statistics.mean(bookings), 2),
            'min_daily_bookings': min(bookings),
            'max_daily_bookings': max(bookings),
            'booking_growth_rate': round(calculate_growth_rate(bookings), 2),
            'booking_volatility': round(statistics.stdev(bookings), 2),
            'weekly_breakdown': weekly_data
        },
        'revenue_trends': {
            'total_revenue': round(sum(revenue), 2),
            'avg_daily_revenue': round(statistics.mean(revenue), 2),
            'min_daily_revenue': round(min(revenue), 2),
            'max_daily_revenue': round(max(revenue), 2),
            'revenue_growth_rate': round(calculate_growth_rate(revenue), 2),
            'revenue_volatility': round(statistics.stdev(revenue), 2)
        },
        'rating_trends': {
            'avg_rating': round(statistics.mean(ratings), 2),
            'min_rating': min(ratings),
            'max_rating': max(ratings),
            'rating_trend': round(calculate_growth_rate(ratings), 2),
            'rating_stability': round(statistics.stdev(ratings), 3)
        },
        'operational_metrics': {
            'total_covers': sum(covers),
            'avg_daily_covers': round(statistics.mean(covers), 2),
            'total_cancellations': sum(cancellations),
            'avg_cancellation_rate': round((sum(cancellations) / sum(bookings)) * 100, 2),
            'avg_spend_per_cover': round(statistics.mean(avg_spend), 2),
            'spend_per_cover_trend': round(calculate_growth_rate(avg_spend), 2)
        }
    }
    
    return trends

def identify_patterns(daily_metrics: List[Dict], trends: Dict[str, Any]) -> Dict[str, Any]:
    """Identify patterns in the performance data."""
    
    # Day of week analysis
    day_of_week_performance = {}
    for metric in daily_metrics:
        date_obj = datetime.strptime(metric['date'], '%Y-%m-%d')
        day_name = date_obj.strftime('%A')
        
        if day_name not in day_of_week_performance:
            day_of_week_performance[day_name] = {
                'bookings': [],
                'revenue': [],
                'ratings': []
            }
        
        day_of_week_performance[day_name]['bookings'].append(metric['bookings'])
        day_of_week_performance[day_name]['revenue'].append(metric['revenue'])
        day_of_week_performance[day_name]['ratings'].append(metric.get('rating', metric.get('avg_rating', 0)))
    
    # Calculate averages for each day
    day_averages = {}
    for day, data in day_of_week_performance.items():
        day_averages[day] = {
            'avg_bookings': round(statistics.mean(data['bookings']), 2),
            'avg_revenue': round(statistics.mean(data['revenue']), 2),
            'avg_rating': round(statistics.mean(data['ratings']), 2),
            'sample_size': len(data['bookings'])
        }
    
    # Find best and worst performing days
    best_booking_day = max(day_averages.items(), key=lambda x: x[1]['avg_bookings'])
    worst_booking_day = min(day_averages.items(), key=lambda x: x[1]['avg_bookings'])
    best_revenue_day = max(day_averages.items(), key=lambda x: x[1]['avg_revenue'])
    worst_revenue_day = min(day_averages.items(), key=lambda x: x[1]['avg_revenue'])
    
    # Anomaly detection (values beyond 2 standard deviations)
    bookings_mean = statistics.mean([m['bookings'] for m in daily_metrics])
    bookings_stdev = statistics.stdev([m['bookings'] for m in daily_metrics])
    
    revenue_mean = statistics.mean([m['revenue'] for m in daily_metrics])
    revenue_stdev = statistics.stdev([m['revenue'] for m in daily_metrics])
    
    anomalies = []
    for metric in daily_metrics:
        booking_z_score = abs(metric['bookings'] - bookings_mean) / bookings_stdev
        revenue_z_score = abs(metric['revenue'] - revenue_mean) / revenue_stdev
        
        if booking_z_score > 2 or revenue_z_score > 2:
            anomalies.append({
                'date': metric['date'],
                'bookings': metric['bookings'],
                'revenue': metric['revenue'],
                'booking_z_score': round(booking_z_score, 2),
                'revenue_z_score': round(revenue_z_score, 2),
                'anomaly_type': 'high' if (metric['bookings'] > bookings_mean and metric['revenue'] > revenue_mean) else 'low'
            })
    
    patterns = {
        'day_of_week_analysis': {
            'daily_averages': day_averages,
            'best_performing_days': {
                'bookings': {'day': best_booking_day[0], 'avg_bookings': best_booking_day[1]['avg_bookings']},
                'revenue': {'day': best_revenue_day[0], 'avg_revenue': best_revenue_day[1]['avg_revenue']}
            },
            'worst_performing_days': {
                'bookings': {'day': worst_booking_day[0], 'avg_bookings': worst_booking_day[1]['avg_bookings']},
                'revenue': {'day': worst_revenue_day[0], 'avg_revenue': worst_revenue_day[1]['avg_revenue']}
            }
        },
        'anomalies': {
            'total_anomalies': len(anomalies),
            'anomaly_details': anomalies
        },
        'performance_insights': {
            'consistent_performer': trends['rating_trends']['rating_stability'] < 0.2,
            'growth_trajectory': 'positive' if trends['booking_trends']['booking_growth_rate'] > 0 else 'negative',
            'revenue_efficiency': trends['revenue_trends']['avg_daily_revenue'] / trends['booking_trends']['avg_daily_bookings']
        }
    }
    
    return patterns

def calculate_comparative_metrics(data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate metrics compared to peer benchmarks."""
    
    restaurant_metrics = data['metrics_summary']
    peer_benchmarks = data['peer_benchmarks'][0] if data['peer_benchmarks'] else {}
    ads_performance = data.get('ads_summary', {})
    
    comparisons = {
        'vs_peers': {
            'bookings_performance': {
                'restaurant_avg': restaurant_metrics['avg_daily_bookings'],
                'peer_avg': peer_benchmarks.get('avg_bookings', 0),
                'performance_ratio': round(restaurant_metrics['avg_daily_bookings'] / peer_benchmarks.get('avg_bookings', 1), 2),
                'status': 'above_average' if restaurant_metrics['avg_daily_bookings'] > peer_benchmarks.get('avg_bookings', 0) else 'below_average'
            },
            'revenue_performance': {
                'restaurant_total': restaurant_metrics['total_revenue_30d'],
                'peer_avg': peer_benchmarks.get('avg_revenue', 0),
                'performance_ratio': round(restaurant_metrics['total_revenue_30d'] / peer_benchmarks.get('avg_revenue', 1), 2),
                'status': 'above_average' if restaurant_metrics['total_revenue_30d'] > peer_benchmarks.get('avg_revenue', 0) else 'below_average'
            },
            'rating_performance': {
                'restaurant_rating': restaurant_metrics['avg_rating'],
                'peer_avg_rating': peer_benchmarks.get('avg_rating', 0),
                'rating_advantage': round(restaurant_metrics['avg_rating'] - peer_benchmarks.get('avg_rating', 0), 2),
                'status': 'above_average' if restaurant_metrics['avg_rating'] > peer_benchmarks.get('avg_rating', 0) else 'below_average'
            }
        },
        'ads_effectiveness': {
            'roi_performance': {
                'restaurant_roi': ads_performance.get('avg_roi', 0),
                'peer_avg_roi': peer_benchmarks.get('avg_roi', 0),
                'roi_advantage': round(ads_performance.get('avg_roi', 0) - peer_benchmarks.get('avg_roi', 0), 2),
                'status': 'above_average' if ads_performance.get('avg_roi', 0) > peer_benchmarks.get('avg_roi', 0) else 'below_average'
            },
            'conversion_performance': {
                'restaurant_conversion': ads_performance.get('avg_conversion_rate', 0),
                'peer_avg_conversion': peer_benchmarks.get('avg_conversion_rate', 0),
                'conversion_advantage': round(ads_performance.get('avg_conversion_rate', 0) - peer_benchmarks.get('avg_conversion_rate', 0), 2),
                'status': 'above_average' if ads_performance.get('avg_conversion_rate', 0) > peer_benchmarks.get('avg_conversion_rate', 0) else 'below_average'
            }
        }
    }
    
    return comparisons

def update_workflow_log(session_id: str, artifacts_dir: str, workflow_name: str, status: str, error_msg: str = None):
    """Update workflow execution log and error log if needed"""
    import json
    
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
        "artifacts_created": ["performance_trends.json"] if status == "completed" else []
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
    """Main function to analyze performance trends."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze restaurant performance trends")
    parser.add_argument("session_id", help="Session ID for artifact management")
    parser.add_argument("--artifacts-dir", default="artifacts", help="Directory for artifact storage")
    
    args = parser.parse_args()
    
    # File paths
    input_file = f"{args.artifacts_dir}/{args.session_id}/restaurant_data.json"
    output_file = f"{args.artifacts_dir}/{args.session_id}/performance_trends.json"
    
    # Update workflow log - started
    update_workflow_log(args.session_id, args.artifacts_dir, "analyze-performance-trends", "started")
    
    try:
        # Load data
        print("Loading restaurant data...")
        data = load_restaurant_data(input_file)
        
        # Extract daily metrics
        daily_metrics = data.get('daily_metrics', data.get('raw_data', {}).get('daily_metrics', []))
        
        if not daily_metrics:
            error_msg = f"No daily metrics found in {input_file}"
            update_workflow_log(args.session_id, args.artifacts_dir, "analyze-performance-trends", "failed", error_msg)
            print(f"Error: {error_msg}")
            return None
        
        print(f"Analyzing {len(daily_metrics)} days of performance data...")
        
        # Calculate trends
        trends = calculate_performance_trends(daily_metrics)
        patterns = identify_patterns(daily_metrics, trends)
        comparisons = calculate_comparative_metrics(data)
        
        # Compile results
        results = {
            'analysis_metadata': {
                'restaurant_id': data['restaurant_info']['restaurant_id'],
                'restaurant_name': data['restaurant_info']['restaurant_name'],
                'analysis_period': {
                    'start_date': daily_metrics[0]['date'],
                    'end_date': daily_metrics[-1]['date'],
                    'total_days': len(daily_metrics)
                },
                'generated_at': datetime.now().isoformat(),
                'session_id': data.get('collection_metadata', {}).get('session_id', args.session_id)
            },
            'performance_trends': trends,
            'pattern_analysis': patterns,
            'competitive_analysis': comparisons,
            'key_insights': {
                'top_strengths': [
                    f"Strong ROI performance: {comparisons['ads_effectiveness']['roi_performance']['roi_advantage']:.1f}x above peer average",
                    f"Superior rating: {comparisons['vs_peers']['rating_performance']['rating_advantage']:.1f} points above peers",
                    f"Revenue outperforming peers by {((comparisons['vs_peers']['revenue_performance']['performance_ratio'] - 1) * 100):.1f}%"
                ],
                'areas_for_improvement': [
                    f"Booking volatility is {trends['booking_trends']['booking_volatility']:.1f} bookings/day",
                    f"Revenue volatility is ₹{trends['revenue_trends']['revenue_volatility']:,.0f}/day",
                    f"Cancellation rate at {trends['operational_metrics']['avg_cancellation_rate']:.1f}%"
                ],
                'growth_trajectory': {
                    'booking_growth': f"{trends['booking_trends']['booking_growth_rate']:.1f}%",
                    'revenue_growth': f"{trends['revenue_trends']['revenue_growth_rate']:.1f}%",
                    'overall_trend': patterns['performance_insights']['growth_trajectory']
                }
            }
        }
        
        # Save results
        print(f"Saving analysis results to {output_file}...")
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Update workflow log - completed
        update_workflow_log(args.session_id, args.artifacts_dir, "analyze-performance-trends", "completed")
        
        print("Performance trends analysis completed successfully!")
        print(f"Analysis covers {len(daily_metrics)} days of data")
        print(f"Key findings:")
        print(f"  - Average daily bookings: {trends['booking_trends']['avg_daily_bookings']}")
        print(f"  - Average daily revenue: ₹{trends['revenue_trends']['avg_daily_revenue']:,.0f}")
        print(f"  - Overall rating: {trends['rating_trends']['avg_rating']}")
        print(f"  - Growth trajectory: {patterns['performance_insights']['growth_trajectory']}")
        
        return results
        
    except FileNotFoundError as e:
        error_msg = f"Required input file not found: {e}"
        update_workflow_log(args.session_id, args.artifacts_dir, "analyze-performance-trends", "failed", error_msg)
        print(f"Error: {error_msg}")
        return None
    except Exception as e:
        error_msg = f"Analysis failed: {str(e)}"
        update_workflow_log(args.session_id, args.artifacts_dir, "analyze-performance-trends", "failed", error_msg)
        print(f"Error: {error_msg}")
        return None

if __name__ == "__main__":
    main()