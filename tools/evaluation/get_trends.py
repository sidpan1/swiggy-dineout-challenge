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
import os
from pathlib import Path
from typing import Dict, Any

# Project root and default database path
PROJECT_ROOT = Path(__file__).parent.parent.parent
DEFAULT_DB_PATH = PROJECT_ROOT / ".db" / "swiggy_dineout.db"


def get_evaluation_trends(workflow_type: str = None, target_entity_id: str = None, limit: int = 10, db_path: str = None) -> Dict[str, Any]:
    """
    Retrieve recent evaluations and calculate performance trends from the generic evaluation table.
    
    Analyzes evaluation history to identify performance trends, calculate statistics,
    and provide insights into evaluation patterns. Supports filtering by workflow type
    and target entity.
    
    Args:
        workflow_type (str, optional): Filter evaluations for specific workflow type.
            If None, returns trends across all workflow types.
        target_entity_id (str, optional): Filter evaluations for specific target entity.
            If None, returns trends across all entities.
        limit (int): Maximum number of recent evaluations to analyze. Default: 10
        db_path (str): Path to SQLite database file. Default: ".db/swiggy_dineout.db"
        
    Returns:
        Dict[str, any]: Comprehensive trend analysis containing:
            - total_evaluations (int): Number of evaluations analyzed
            - average_score (float): Mean evaluation score
            - highest_score (float): Best evaluation score
            - lowest_score (float): Worst evaluation score  
            - latest_score (float): Most recent evaluation score
            - trend (str): Overall trend direction ("improving", "declining", "stable")
            - score_range (float): Difference between highest and lowest scores
            - latest_rubric_breakdown (Dict): Score breakdown by rubric dimension from latest evaluation
            - evaluations (List[Dict]): Full evaluation records
            
    Raises:
        sqlite3.Error: If database query fails
        
    Example:
        >>> # Get trends for specific workflow type
        >>> trends = get_evaluation_trends(workflow_type="restaurant-analysis", limit=5)
        >>> print(f"Restaurant analysis trend: {trends['trend']}")
        >>> print(f"Latest score: {trends['latest_score']}")
        >>> 
        >>> # Get overall trends across all workflows
        >>> all_trends = get_evaluation_trends(limit=20)
        >>> print(f"Average score: {all_trends['average_score']}")
        >>>
        >>> # Check if no evaluations found
        >>> if trends.get('message'):
        ...     print(f"No data: {trends['message']}")
    """
    # Use default path if none provided
    if db_path is None:
        db_path = str(DEFAULT_DB_PATH)
    
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Build query with optional filters
        conditions = []
        params = []
        
        if workflow_type:
            conditions.append("workflow_type = ?")
            params.append(workflow_type)
        
        if target_entity_id:
            conditions.append("JSON_EXTRACT(details, '$.target_entity_id') = ?")
            params.append(target_entity_id)
        
        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)
        
        query = f"""
            SELECT * FROM evaluations 
            {where_clause}
            ORDER BY created_at DESC 
            LIMIT ?
        """
        params.append(limit)
        
        cursor.execute(query, params)
        evaluations = [dict(row) for row in cursor.fetchall()]
        
        if not evaluations:
            return {
                "message": "No evaluations found",
                "total_evaluations": 0,
                "evaluations": []
            }
        
        # Extract scores for trend analysis
        scores = [eval['evaluation_score'] for eval in evaluations]
        
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
        rubric_breakdown = {}
        
        try:
            # Parse the latest evaluation's rubric JSON
            latest_rubric = json.loads(latest_eval.get('evaluation_rubric', '{}'))
            for dimension, data in latest_rubric.items():
                if isinstance(data, dict) and 'score' in data:
                    rubric_breakdown[dimension] = data['score']
                elif isinstance(data, (int, float)):
                    rubric_breakdown[dimension] = data
        except json.JSONDecodeError:
            rubric_breakdown = {"error": "Unable to parse rubric data"}
        
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
    parser = argparse.ArgumentParser(description="Analyze evaluation trends and statistics from generic evaluation table")
    parser.add_argument("--workflow-type", help="Filter by workflow type (e.g., restaurant-analysis, code-review)")
    parser.add_argument("--target-entity-id", help="Filter by target entity ID (e.g., R001)")
    parser.add_argument("--limit", type=int, default=10, help="Number of recent evaluations to analyze (default: 10)")
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH), help="Database file path")
    parser.add_argument("--detailed", action="store_true", help="Show detailed evaluation records")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    
    args = parser.parse_args()
    
    try:
        trends = get_evaluation_trends(args.workflow_type, args.target_entity_id, args.limit, args.db_path)
        
        if args.json:
            # Output as JSON
            print(json.dumps(trends, indent=2))
        elif trends.get('message'):
            print(f"📭 {trends['message']}")
        else:
            # Formatted output
            print("📊 EVALUATION TRENDS ANALYSIS")
            print("=" * 50)
            
            if args.workflow_type:
                print(f"🔧 Workflow: {args.workflow_type}")
            else:
                print("🌐 Scope: All workflow types")
            
            if args.target_entity_id:
                print(f"🎯 Target Entity: {args.target_entity_id}")
            
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
            if rubric:
                for dimension, score in rubric.items():
                    print(f"  {dimension.replace('_', ' ').title()}: {score}")
            else:
                print("  No rubric data available")
            
            if args.detailed:
                print(f"\n📋 DETAILED RECORDS (latest {args.limit})")
                print("-" * 50)
                for i, eval_record in enumerate(trends['evaluations'][:5], 1):
                    print(f"{i}. ID: {eval_record['evaluation_id']} | Score: {eval_record['evaluation_score']} | Session: {eval_record['session_id']} | Workflow: {eval_record['workflow_type']}")
        
    except Exception as e:
        print(f"❌ Error analyzing trends: {str(e)}")
        exit(1)