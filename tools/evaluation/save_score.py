#!/usr/bin/env python3
"""
Evaluation Score Saving Tool

Saves evaluation scores and metadata to the generic evaluation database. This tool handles 
the insertion of evaluation records with flexible rubric dimensions and use-case specific details.

Usage:
    uv run tools/evaluation/save_score.py --session-id SESSION --workflow-type TYPE --score SCORE [options]

Author: Swiggy Dineout Challenge
Version: 2.0
"""

import sqlite3
import json
import argparse
from pathlib import Path
from typing import Dict, Any

# Project root and default database path
PROJECT_ROOT = Path(__file__).parent.parent.parent
DEFAULT_DB_PATH = PROJECT_ROOT / ".db" / "swiggy_dineout.db"


def insert_evaluation_record(
    session_id: str,
    workflow_type: str,
    evaluation_score: float,
    evaluation_rubric: Dict[str, Any] = None,
    details: Dict[str, Any] = None,
    db_path: str = None
) -> int:
    """
    Insert a new evaluation record into the generic evaluations table.
    
    Stores evaluation data in a completely generic format that can handle any workflow type
    and any rubric structure through JSON fields.
    
    Args:
        session_id (str): Unique identifier for the evaluation session
        workflow_type (str): Type of workflow being evaluated (e.g., "restaurant-analysis", "code-review")
        evaluation_score (float): Final evaluation score (0.0-100.0)
        evaluation_rubric (Dict[str, Any], optional): Rubric dimensions and scores as JSON.
            Example: {
                'data_accuracy': {'score': 85.0, 'weight': 0.35},
                'insight_quality': {'score': 75.0, 'weight': 0.30},
                'overall_weighted_score': 78.5
            }
        details (Dict[str, Any], optional): Use-case specific details as JSON.
            Example: {
                'restaurant_id': 'R001',
                'solution_path': 'artifacts/analysis.md',
                'artifacts_folder': 'session_001',
                'notes': 'Strong analysis but missing integration',
                'strengths': ['Comprehensive data analysis'],
                'weaknesses': ['Missing unified format'],
                'recommendations': ['Create integrated briefing']
            }
        db_path (str, optional): Path to SQLite database file
        
    Returns:
        int: evaluation_id of the inserted record
        
    Raises:
        sqlite3.Error: If database insertion fails
        
    Example:
        >>> eval_id = insert_evaluation_record(
        ...     session_id="acad9e9a",
        ...     workflow_type="restaurant-analysis",
        ...     evaluation_score=78.0,
        ...     evaluation_rubric={
        ...         'data_accuracy': {'score': 82.0, 'weight': 0.35},
        ...         'insight_quality': {'score': 85.0, 'weight': 0.30},
        ...         'completeness': {'score': 68.0, 'weight': 0.20},
        ...         'confidence_calibration': {'score': 75.0, 'weight': 0.15}
        ...     },
        ...     details={
        ...         'restaurant_id': 'R001',
        ...         'solution_path': '.artifacts/acad9e9a',
        ...         'notes': 'Strong analytical depth but missing unified format'
        ...     }
        ... )
        >>> print(f"Saved evaluation with ID: {eval_id}")
    """
    # Use default path if none provided
    if db_path is None:
        db_path = str(DEFAULT_DB_PATH)
    
    # Ensure JSON fields have default values
    if evaluation_rubric is None:
        evaluation_rubric = {}
    if details is None:
        details = {}
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO evaluations (
                session_id, workflow_type, evaluation_score, 
                evaluation_rubric, details
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            session_id,
            workflow_type,
            evaluation_score,
            json.dumps(evaluation_rubric),
            json.dumps(details)
        ))
        
        evaluation_id = cursor.lastrowid
        conn.commit()
        return evaluation_id


if __name__ == "__main__":
    """Command-line interface for saving evaluation scores."""
    parser = argparse.ArgumentParser(description="Save evaluation score to generic evaluation database")
    parser.add_argument("--session-id", required=True, help="Session identifier")
    parser.add_argument("--workflow-type", required=True, help="Workflow type (e.g., restaurant-analysis, code-review)")
    parser.add_argument("--score", type=float, required=True, help="Overall evaluation score (0-100)")
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH), help="Database file path")
    
    # Generic fields (optional)
    parser.add_argument("--rubric-json", help="JSON string containing rubric structure")
    parser.add_argument("--details-json", help="JSON string containing details/metadata")
    parser.add_argument("--target-entity-id", help="Target entity being evaluated")
    parser.add_argument("--notes", help="Evaluation notes")
    
    args = parser.parse_args()
    
    try:
        # Parse rubric JSON if provided, otherwise empty
        evaluation_rubric = {}
        if args.rubric_json:
            evaluation_rubric = json.loads(args.rubric_json)
        
        # Parse details JSON if provided, otherwise build from individual args
        details = {}
        if args.details_json:
            details = json.loads(args.details_json)
        else:
            # Build from individual arguments
            if args.target_entity_id:
                details['target_entity_id'] = args.target_entity_id
            if args.notes:
                details['notes'] = args.notes
        
        eval_id = insert_evaluation_record(
            session_id=args.session_id,
            workflow_type=args.workflow_type,
            evaluation_score=args.score,
            evaluation_rubric=evaluation_rubric,
            details=details,
            db_path=args.db_path
        )
        
        print(f"✅ Evaluation record saved with ID: {eval_id}")
        print(f"📊 Session: {args.session_id}")
        print(f"🔧 Workflow: {args.workflow_type}")
        print(f"🎯 Score: {args.score}")
        
    except Exception as e:
        print(f"❌ Error saving evaluation: {str(e)}")
        exit(1)