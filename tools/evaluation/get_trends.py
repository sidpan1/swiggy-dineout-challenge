#!/usr/bin/env python3
"""
Evaluation Trends Analysis Tool

Retrieves and analyzes evaluation trends from the database. Provides insights into
evaluation patterns, performance trends, and scoring statistics.

Usage:
    uv run tools/evaluation/get_trends.py [--restaurant-id ID] [--limit N] [--db-path PATH]

Author: Swiggy Dineout Challenge
Version: 1.0
"""

import sqlite3
import json
import argparse
from typing import Dict, Any


def get_evaluation_trends(restaurant_id: str = None, limit: int = 10, db_path: str = "swiggy_dineout.db") -> Dict[str, Any]:
    """
    Retrieve recent evaluations and calculate performance trends.
    
    Analyzes evaluation history to identify performance trends, calculate statistics,
    and provide insights into evaluation patterns. Supports filtering by restaurant
    and configurable result limits.
    
    Args:
        restaurant_id (str, optional): Filter evaluations for specific restaurant.
            If None, returns trends across all restaurants.
        limit (int): Maximum number of recent evaluations to analyze. Default: 10
        db_path (str): Path to SQLite database file. Default: "swiggy_dineout.db"
        
    Returns:
        Dict[str, any]: Comprehensive trend analysis containing:
            - total_evaluations (int): Number of evaluations analyzed
            - average_score (float): Mean evaluation score
            - highest_score (float): Best evaluation score
            - lowest_score (float): Worst evaluation score  
            - latest_score (float): Most recent evaluation score
            - trend (str): Overall trend direction ("improving", "declining", "stable")
            - score_range (float): Difference between highest and lowest scores
            - latest_rubric_breakdown (Dict): Score breakdown by rubric dimension
            - evaluations (List[Dict]): Full evaluation records
            
    Raises:
        sqlite3.Error: If database query fails
        
    Example:
        >>> # Get trends for specific restaurant
        >>> trends = get_evaluation_trends(restaurant_id="R001", limit=5)
        >>> print(f"Restaurant R001 trend: {trends['trend']}")
        >>> print(f"Latest score: {trends['latest_score']}")
        >>> 
        >>> # Get overall trends across all restaurants
        >>> all_trends = get_evaluation_trends(limit=20)
        >>> print(f"Average score: {all_trends['average_score']}")
        >>>
        >>> # Check if no evaluations found
        >>> if trends.get('message'):
        ...     print(f"No data: {trends['message']}")
    """
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Build query
        if restaurant_id:
            query = """
                SELECT * FROM evaluations 
                WHERE restaurant_id = ? 
                ORDER BY evaluation_timestamp DESC 
                LIMIT ?
            """
            params = (restaurant_id, limit)
        else:
            query = """
                SELECT * FROM evaluations 
                ORDER BY evaluation_timestamp DESC 
                LIMIT ?
            """
            params = (limit,)
        
        cursor.execute(query, params)
        evaluations = [dict(row) for row in cursor.fetchall()]
        
        if not evaluations:
            return {
                "message": "No evaluations found",
                "total_evaluations": 0,
                "evaluations": []
            }
        
        # Extract scores for trend analysis
        scores = [eval['overall_score'] for eval in evaluations]
        
        # Calculate trend
        trend = "stable"
        if len(scores) > 1:
            if scores[0] > scores[-1]:  # Latest vs oldest
                trend = "improving"
            elif scores[0] < scores[-1]:
                trend = "declining"
        
        # Calculate score statistics
        avg_score = round(sum(scores) / len(scores), 2)
        max_score = max(scores)
        min_score = min(scores)
        
        # Score distribution by rubric dimensions (from latest evaluation)
        latest_eval = evaluations[0]
        rubric_breakdown = {
            "data_accuracy": latest_eval.get('data_accuracy_score', 0),
            "insight_quality": latest_eval.get('insight_quality_score', 0),
            "completeness": latest_eval.get('completeness_score', 0),
            "confidence_calibration": latest_eval.get('confidence_calibration_score', 0)
        }
        
        return {
            "total_evaluations": len(evaluations),
            "average_score": avg_score,
            "highest_score": max_score,
            "lowest_score": min_score,
            "latest_score": scores[0],
            "trend": trend,
            "score_range": max_score - min_score,
            "latest_rubric_breakdown": rubric_breakdown,
            "evaluations": evaluations
        }


if __name__ == "__main__":
    """Command-line interface for trend analysis."""
    parser = argparse.ArgumentParser(description="Analyze evaluation trends and statistics")
    parser.add_argument("--restaurant-id", help="Filter by restaurant ID (e.g., R001)")
    parser.add_argument("--limit", type=int, default=10, help="Number of recent evaluations to analyze (default: 10)")
    parser.add_argument("--db-path", default="swiggy_dineout.db", help="Database file path")
    parser.add_argument("--detailed", action="store_true", help="Show detailed evaluation records")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    
    args = parser.parse_args()
    
    try:
        trends = get_evaluation_trends(args.restaurant_id, args.limit, args.db_path)
        
        if args.json:
            # Output as JSON
            print(json.dumps(trends, indent=2))
        elif trends.get('message'):
            print(f"📭 {trends['message']}")
        else:
            # Formatted output
            print("📊 EVALUATION TRENDS ANALYSIS")
            print("=" * 50)
            
            if args.restaurant_id:
                print(f"🏪 Restaurant: {args.restaurant_id}")
            else:
                print("🌐 Scope: All restaurants")
            
            print(f"📈 Total evaluations: {trends['total_evaluations']}")
            print(f"🎯 Latest score: {trends['latest_score']}")
            print(f"📊 Average score: {trends['average_score']}")
            print(f"🏆 Highest score: {trends['highest_score']}")
            print(f"📉 Lowest score: {trends['lowest_score']}")
            print(f"📏 Score range: {trends['score_range']}")
            print(f"📈 Trend: {trends['trend'].upper()}")
            
            print("\n🎯 LATEST RUBRIC BREAKDOWN")
            print("-" * 30)
            rubric = trends['latest_rubric_breakdown']
            print(f"  Data Accuracy: {rubric['data_accuracy']}")
            print(f"  Insight Quality: {rubric['insight_quality']}")
            print(f"  Completeness: {rubric['completeness']}")
            print(f"  Confidence Calibration: {rubric['confidence_calibration']}")
            
            if args.detailed:
                print(f"\n📋 DETAILED RECORDS (latest {args.limit})")
                print("-" * 50)
                for i, eval_record in enumerate(trends['evaluations'][:5], 1):
                    print(f"{i}. ID: {eval_record['id']} | Score: {eval_record['overall_score']} | Session: {eval_record['session_id']}")
        
    except Exception as e:
        print(f"❌ Error analyzing trends: {str(e)}")
        exit(1)