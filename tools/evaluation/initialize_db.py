#!/usr/bin/env python3
"""
Evaluation Database Initialization Tool

Creates the evaluation database schema for storing evaluation scores and metadata.
This tool sets up the necessary tables for the evaluation system.

Usage:
    uv run tools/evaluation/initialize_db.py [--db-path PATH]

Author: Swiggy Dineout Challenge
Version: 1.0
"""

import sqlite3
import argparse
from pathlib import Path


def initialize_table(db_path: str = "swiggy_dineout.db"):
    """
    Initialize evaluation tables in the SQLite database.
    
    Creates the 'evaluations' table with all necessary columns for storing
    evaluation scores, rubric breakdowns, and session metadata. This function
    is idempotent and safe to call multiple times.
    
    Args:
        db_path (str): Path to SQLite database file. Defaults to "swiggy_dineout.db"
        
    Returns:
        None
        
    Raises:
        sqlite3.Error: If database creation fails
        
    Example:
        >>> initialize_table()
        >>> initialize_table("custom_db.db")
    """
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                solution_document_path TEXT NOT NULL,
                overall_score REAL NOT NULL,
                evaluation_timestamp DATETIME NOT NULL,
                
                -- Rubric dimension scores
                data_accuracy_score REAL,
                data_accuracy_weight REAL,
                insight_quality_score REAL,
                insight_quality_weight REAL,
                completeness_score REAL,
                completeness_weight REAL,
                confidence_calibration_score REAL,
                confidence_calibration_weight REAL,
                
                -- Evaluation metadata
                evaluation_notes TEXT,
                strengths TEXT,
                weaknesses TEXT,
                recommendations TEXT,
                
                -- Session context
                restaurant_id TEXT,
                artifacts_folder TEXT
            )
        """)
        conn.commit()


if __name__ == "__main__":
    """Command-line interface for database initialization."""
    parser = argparse.ArgumentParser(description="Initialize evaluation database tables")
    parser.add_argument("--db-path", default="swiggy_dineout.db", help="Database file path (default: swiggy_dineout.db)")
    
    args = parser.parse_args()
    
    try:
        # Check if database file exists
        db_exists = Path(args.db_path).exists()
        
        # Initialize tables
        initialize_table(args.db_path)
        
        if db_exists:
            print(f"✅ Evaluation tables verified/updated in {args.db_path}")
        else:
            print(f"✅ New evaluation database created: {args.db_path}")
            print(f"📋 Tables created: evaluations")
        
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        exit(1)