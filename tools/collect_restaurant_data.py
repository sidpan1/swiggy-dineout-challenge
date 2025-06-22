#!/usr/bin/env python3

import json
import os
import sys
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import argparse

class RestaurantDataCollector:
    def __init__(self, db_path: str = "swiggy_dineout.db"):
        self.db_path = db_path
        self.connection = None
    
    def connect_db(self):
        """Connect to the SQLite database"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False
    
    def close_db(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute SQL query and return results as list of dictionaries"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            return []
    
    def get_restaurant_info(self, restaurant_id: str) -> Optional[Dict[str, Any]]:
        """Get basic restaurant information"""
        query = "SELECT * FROM restaurant_master WHERE restaurant_id = ?"
        results = self.execute_query(query, (restaurant_id,))
        return results[0] if results else None
    
    def get_restaurant_metrics(self, restaurant_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get restaurant metrics for the last N days"""
        query = """
        SELECT * FROM restaurant_metrics 
        WHERE restaurant_id = ? AND date >= date('now', '-{} days') 
        ORDER BY date DESC
        """.format(days)
        return self.execute_query(query, (restaurant_id,))
    
    def get_ads_data(self, restaurant_id: str, days: int = 60) -> List[Dict[str, Any]]:
        """Get advertising data for the restaurant"""
        query = """
        SELECT * FROM ads_data 
        WHERE restaurant_id = ? AND campaign_end >= date('now', '-{} days') 
        ORDER BY campaign_end DESC
        """.format(days)
        return self.execute_query(query, (restaurant_id,))
    
    def get_peer_benchmarks(self, locality: str, cuisine: str) -> List[Dict[str, Any]]:
        """Get peer benchmark data for the restaurant's locality and cuisine"""
        query = "SELECT * FROM peer_benchmarks WHERE locality = ? AND cuisine = ?"
        return self.execute_query(query, (locality, cuisine))
    
    def get_discount_history(self, restaurant_id: str, days: int = 90) -> List[Dict[str, Any]]:
        """Get discount history for the restaurant"""
        query = """
        SELECT * FROM discount_history 
        WHERE restaurant_id = ? AND end_date >= date('now', '-{} days') 
        ORDER BY end_date DESC
        """.format(days)
        return self.execute_query(query, (restaurant_id,))
    
    def calculate_metrics_summary(self, metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate summary statistics from daily metrics"""
        if not metrics:
            return {
                'total_bookings_30d': 0,
                'avg_daily_bookings': 0,
                'total_revenue_30d': 0,
                'avg_rating': 0,
                'cancellation_rate': 0,
                'total_covers': 0,
                'avg_covers_per_booking': 0
            }
        
        total_bookings = sum(m.get('bookings', 0) for m in metrics)
        total_revenue = sum(m.get('revenue', 0) for m in metrics)
        total_cancellations = sum(m.get('cancellations', 0) for m in metrics)
        total_covers = sum(m.get('covers', 0) for m in metrics)
        
        # Calculate averages
        avg_daily_bookings = total_bookings / len(metrics)
        avg_rating = sum(m.get('avg_rating', 0) for m in metrics if m.get('avg_rating')) / len([m for m in metrics if m.get('avg_rating')])
        cancellation_rate = total_cancellations / total_bookings if total_bookings > 0 else 0
        avg_covers_per_booking = total_covers / total_bookings if total_bookings > 0 else 0
        
        return {
            'total_bookings_30d': total_bookings,
            'avg_daily_bookings': round(avg_daily_bookings, 1),
            'total_revenue_30d': round(total_revenue, 2),
            'avg_rating': round(avg_rating, 1) if avg_rating else 0,
            'cancellation_rate': round(cancellation_rate, 3),
            'total_covers': total_covers,
            'avg_covers_per_booking': round(avg_covers_per_booking, 1)
        }
    
    def calculate_ads_summary(self, ads_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate summary statistics from ads data"""
        if not ads_data:
            return {
                'total_spend': 0,
                'total_impressions': 0,
                'total_clicks': 0,
                'total_conversions': 0,
                'avg_ctr': 0,
                'avg_conversion_rate': 0,
                'avg_roi': 0
            }
        
        total_spend = sum(ad.get('spend', 0) for ad in ads_data)
        total_impressions = sum(ad.get('impressions', 0) for ad in ads_data)
        total_clicks = sum(ad.get('clicks', 0) for ad in ads_data)
        total_conversions = sum(ad.get('conversions', 0) for ad in ads_data)
        
        avg_ctr = total_clicks / total_impressions if total_impressions > 0 else 0
        avg_conversion_rate = total_conversions / total_clicks if total_clicks > 0 else 0
        roi_values = [ad.get('roi', 0) for ad in ads_data if ad.get('roi')]
        avg_roi = sum(roi_values) / len(roi_values) if roi_values else 0
        
        return {
            'total_spend': round(total_spend, 2),
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'total_conversions': total_conversions,
            'avg_ctr': round(avg_ctr, 4),
            'avg_conversion_rate': round(avg_conversion_rate, 4),
            'avg_roi': round(avg_roi, 2)
        }
    
    def validate_data_quality(self, metrics: List[Dict[str, Any]], ads_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate data quality and completeness"""
        metrics_completeness = len(metrics) / 30.0
        missing_days = max(0, 30 - len(metrics))
        
        validation_status = 'complete' if len(metrics) >= 20 else 'incomplete'
        has_ads_data = len(ads_data) > 0
        
        return {
            'metrics_completeness': round(metrics_completeness, 2),
            'missing_days': missing_days,
            'validation_status': validation_status,
            'has_ads_data': has_ads_data,
            'total_data_points': len(metrics) + len(ads_data)
        }
    
    def collect_data(self, restaurant_id: str, session_id: str, artifacts_dir: str = "artifacts") -> Dict[str, Any]:
        """Main data collection method"""
        
        # Connect to database
        if not self.connect_db():
            return {"error": "Database connection failed", "suggestion": "Run 'python init_database.py' to initialize database"}
        
        try:
            # Get restaurant info
            restaurant_info = self.get_restaurant_info(restaurant_id)
            if not restaurant_info:
                available_restaurants = self.execute_query("SELECT restaurant_id, restaurant_name FROM restaurant_master LIMIT 10")
                return {
                    "error": "Restaurant not found",
                    "restaurant_id": restaurant_id,
                    "available_restaurants": available_restaurants
                }
            
            # Collect all data
            metrics = self.get_restaurant_metrics(restaurant_id)
            ads_data = self.get_ads_data(restaurant_id)
            peer_benchmarks = self.get_peer_benchmarks(restaurant_info['locality'], restaurant_info['cuisine'])
            discount_history = self.get_discount_history(restaurant_id)
            
            # Calculate summaries
            metrics_summary = self.calculate_metrics_summary(metrics)
            ads_summary = self.calculate_ads_summary(ads_data)
            data_quality = self.validate_data_quality(metrics, ads_data)
            
            # Check for insufficient data
            if data_quality['validation_status'] == 'incomplete':
                warning = {
                    "warning": "Insufficient recent data",
                    "metrics_days_available": len(metrics),
                    "minimum_required": 20,
                    "recommendation": "Analysis will proceed with available data"
                }
                print(json.dumps(warning, indent=2))
            
            # Compile final result
            result = {
                'restaurant_info': {
                    'restaurant_id': restaurant_info['restaurant_id'],
                    'restaurant_name': restaurant_info['restaurant_name'],
                    'locality': restaurant_info['locality'],
                    'cuisine': restaurant_info['cuisine'],
                    'onboarded_date': restaurant_info['onboarded_date']
                },
                'metrics_summary': metrics_summary,
                'daily_metrics': [
                    {
                        'date': m['date'],
                        'bookings': m.get('bookings', 0),
                        'revenue': m.get('revenue', 0),
                        'rating': m.get('avg_rating', 0),
                        'covers': m.get('covers', 0),
                        'cancellations': m.get('cancellations', 0)
                    } for m in metrics
                ],
                'ads_summary': ads_summary,
                'ads_data': ads_data,
                'peer_benchmarks': peer_benchmarks,
                'discount_history': discount_history,
                'data_quality': data_quality,
                'collection_timestamp': datetime.now().isoformat()
            }
            
            # Save to artifacts directory
            os.makedirs(f"{artifacts_dir}/{session_id}", exist_ok=True)
            
            # Save main restaurant data
            with open(f"{artifacts_dir}/{session_id}/restaurant_data.json", 'w') as f:
                json.dump(result, f, indent=2)
            
            # Save separate artifact files as per protocol
            with open(f"{artifacts_dir}/{session_id}/peer_benchmarks.json", 'w') as f:
                json.dump(peer_benchmarks, f, indent=2)
            
            with open(f"{artifacts_dir}/{session_id}/ads_data.json", 'w') as f:
                json.dump(ads_data, f, indent=2)
            
            # Update workflow execution log
            self.update_workflow_log(session_id, artifacts_dir, "collect-restaurant-data", "completed")
            
            return result
            
        finally:
            self.close_db()
    
    def update_workflow_log(self, session_id: str, artifacts_dir: str, workflow_name: str, status: str):
        """Update workflow execution log"""
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
            "artifacts_created": ["restaurant_data.json", "peer_benchmarks.json", "ads_data.json"]
        }
        
        # Remove existing entry for this workflow if it exists
        log_data["workflows"] = [w for w in log_data["workflows"] if w["workflow"] != workflow_name]
        log_data["workflows"].append(workflow_entry)
        
        # Save updated log
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Collect restaurant data for analysis")
    parser.add_argument("restaurant_id", help="Restaurant ID to collect data for")
    parser.add_argument("session_id", help="Session ID for artifact management")
    parser.add_argument("--db-path", default="swiggy_dineout.db", help="Path to SQLite database")
    parser.add_argument("--artifacts-dir", default="artifacts", help="Directory for artifact storage")
    parser.add_argument("--output-format", choices=["json", "summary"], default="json", help="Output format")
    
    args = parser.parse_args()
    
    collector = RestaurantDataCollector(args.db_path)
    result = collector.collect_data(args.restaurant_id, args.session_id, args.artifacts_dir)
    
    if args.output_format == "json":
        print(json.dumps(result, indent=2))
    else:
        # Summary output
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Data collection completed for {result['restaurant_info']['restaurant_name']}")
            print(f"Metrics: {result['data_quality']['total_data_points']} data points collected")
            print(f"Status: {result['data_quality']['validation_status']}")

if __name__ == "__main__":
    main()