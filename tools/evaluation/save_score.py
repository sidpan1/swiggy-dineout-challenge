#!/usr/bin/env python3
"""
Evaluation Score Saving Tool

Saves evaluation scores and metadata to the database. This tool handles the insertion
of evaluation records with rubric breakdowns and session context.

Usage:
    uv run tools/evaluation/save_score.py --session-id SESSION --solution-path PATH --score SCORE [options]

Author: Swiggy Dineout Challenge
Version: 1.0
"""

import sqlite3
import json
import argparse
from datetime import datetime
from typing import Dict, Any


def insert_evaluation_record(
    session_id: str,
    solution_document_path: str,
    overall_score: float,
    rubric_scores: Dict[str, Dict[str, float]],
    evaluation_details: Dict[str, Any],
    db_path: str = "swiggy_dineout.db"
) -> int:
    """
    Insert a new evaluation record into the database.
    
    Stores comprehensive evaluation data including overall score, rubric dimension
    breakdowns, and associated metadata. Automatically timestamps the evaluation
    and links it to the current session.
    
    Args:
        session_id (str): Unique identifier for the current evaluation session
        solution_document_path (str): File path to the solution document being evaluated
        overall_score (float): Weighted overall evaluation score (0.0-100.0)
        rubric_scores (Dict[str, Dict[str, float]]): Rubric dimension scores and weights.
            Expected format:
            {
                'data_accuracy': {'score': 85.0, 'weight': 0.35},
                'insight_quality': {'score': 75.0, 'weight': 0.30},
                'completeness': {'score': 90.0, 'weight': 0.20},
                'confidence_calibration': {'score': 40.0, 'weight': 0.15}
            }
        evaluation_details (Dict[str, any]): Additional metadata including:
            - restaurant_id (str): Restaurant being evaluated
            - artifacts_folder (str): Session artifacts directory
            - notes (str): Evaluation notes
            - strengths (List[str]): Identified strengths
            - weaknesses (List[str]): Identified weaknesses  
            - recommendations (List[str]): Improvement recommendations
        db_path (str): Path to SQLite database file
        
    Returns:
        int: Database ID of the inserted evaluation record
        
    Raises:
        sqlite3.Error: If database insertion fails
        ValueError: If required rubric dimensions are missing
        
    Example:
        >>> eval_id = insert_evaluation_record(
        ...     session_id="session_001",
        ...     solution_document_path="analysis_workspace/R001_report.md",
        ...     overall_score=76.25,
        ...     rubric_scores={
        ...         'data_accuracy': {'score': 85.0, 'weight': 0.35},
        ...         'insight_quality': {'score': 75.0, 'weight': 0.30},
        ...         'completeness': {'score': 90.0, 'weight': 0.20},
        ...         'confidence_calibration': {'score': 40.0, 'weight': 0.15}
        ...     },
        ...     evaluation_details={
        ...         'restaurant_id': 'R001',
        ...         'strengths': ['Comprehensive analysis'],
        ...         'weaknesses': ['Too verbose'],
        ...         'recommendations': ['Compress to 1-pager']
        ...     }
        ... )
        >>> print(f"Saved evaluation with ID: {eval_id}")
    """
    
    # Extract rubric scores
    data_accuracy = rubric_scores.get('data_accuracy', {})
    insight_quality = rubric_scores.get('insight_quality', {})
    completeness = rubric_scores.get('completeness', {})
    confidence_calibration = rubric_scores.get('confidence_calibration', {})
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO evaluations (
                session_id, solution_document_path, overall_score, evaluation_timestamp,
                data_accuracy_score, data_accuracy_weight,
                insight_quality_score, insight_quality_weight,
                completeness_score, completeness_weight,
                confidence_calibration_score, confidence_calibration_weight,
                evaluation_notes, strengths, weaknesses, recommendations,
                restaurant_id, artifacts_folder
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            solution_document_path,
            overall_score,
            datetime.now().isoformat(),
            data_accuracy.get('score', 0.0),
            data_accuracy.get('weight', 0.0),
            insight_quality.get('score', 0.0),
            insight_quality.get('weight', 0.0),
            completeness.get('score', 0.0),
            completeness.get('weight', 0.0),
            confidence_calibration.get('score', 0.0),
            confidence_calibration.get('weight', 0.0),
            evaluation_details.get('notes', ''),
            json.dumps(evaluation_details.get('strengths', [])),
            json.dumps(evaluation_details.get('weaknesses', [])),
            json.dumps(evaluation_details.get('recommendations', [])),
            evaluation_details.get('restaurant_id', ''),
            evaluation_details.get('artifacts_folder', '')
        ))
        
        evaluation_id = cursor.lastrowid
        conn.commit()
        return evaluation_id


if __name__ == "__main__":
    """Command-line interface for saving evaluation scores."""
    parser = argparse.ArgumentParser(description="Save evaluation score to database")
    parser.add_argument("--session-id", required=True, help="Session identifier")
    parser.add_argument("--solution-path", required=True, help="Path to solution document")
    parser.add_argument("--score", type=float, required=True, help="Overall evaluation score (0-100)")
    parser.add_argument("--restaurant-id", help="Restaurant ID (e.g., R001)")
    parser.add_argument("--notes", default="", help="Evaluation notes")
    parser.add_argument("--db-path", default="swiggy_dineout.db", help="Database file path")
    
    # Rubric scores
    parser.add_argument("--data-accuracy", type=float, default=0.0, help="Data accuracy score")
    parser.add_argument("--insight-quality", type=float, default=0.0, help="Insight quality score")
    parser.add_argument("--completeness", type=float, default=0.0, help="Completeness score")
    parser.add_argument("--confidence-calibration", type=float, default=0.0, help="Confidence calibration score")
    
    args = parser.parse_args()
    
    try:
        # Prepare rubric scores with standard weights
        rubric_scores = {
            'data_accuracy': {'score': args.data_accuracy, 'weight': 0.35},
            'insight_quality': {'score': args.insight_quality, 'weight': 0.30},
            'completeness': {'score': args.completeness, 'weight': 0.20},
            'confidence_calibration': {'score': args.confidence_calibration, 'weight': 0.15}
        }
        
        evaluation_details = {
            'restaurant_id': args.restaurant_id or '',
            'notes': args.notes,
            'strengths': [],
            'weaknesses': [],
            'recommendations': []
        }
        
        eval_id = insert_evaluation_record(
            session_id=args.session_id,
            solution_document_path=args.solution_path,
            overall_score=args.score,
            rubric_scores=rubric_scores,
            evaluation_details=evaluation_details,
            db_path=args.db_path
        )
        
        print(f"✅ Evaluation record saved with ID: {eval_id}")
        print(f"📊 Session: {args.session_id}")
        print(f"📄 Solution: {args.solution_path}")
        print(f"🎯 Score: {args.score}")
        
    except Exception as e:
        print(f"❌ Error saving evaluation: {str(e)}")
        exit(1)