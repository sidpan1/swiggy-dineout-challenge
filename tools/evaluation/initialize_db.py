#!/usr/bin/env python3
"""
Evaluation Database Initialization Tool

Creates the evaluation database schema for storing evaluation scores and metadata.
This tool sets up the necessary tables for the evaluation system with a generic,
scalable design that supports any rubric dimensions.

Usage:
    uv run tools/evaluation/initialize_db.py [--db-path PATH]

Author: Swiggy Dineout Challenge
Version: 2.0
"""

import sqlite3
import argparse
from pathlib import Path

# Project root and default database path
PROJECT_ROOT = Path(__file__).parent.parent.parent
DEFAULT_DB_PATH = PROJECT_ROOT / ".db" / "swiggy_dineout.db"


def initialize_tables(db_path: str = None):
    """
    Initialize a completely generic evaluation table that can handle any workflow type.
    
    Creates a single, simple table with:
    - evaluation_id (primary key)
    - session_id (links to evaluation session)
    - workflow_type (generic workflow identifier)
    - evaluation_score (final numeric score)
    - evaluation_rubric (JSON with all rubric dimensions and scores)
    - details (JSON with all use-case specific data)
    
    This function is idempotent and safe to call multiple times.
    
    Args:
        db_path (str): Path to SQLite database file. Defaults to project .db/swiggy_dineout.db
        
    Returns:
        None
        
    Raises:
        sqlite3.Error: If database creation fails
        
    Example:
        >>> initialize_tables()
        >>> initialize_tables("custom_db.db")
    """
    # Use default path if none provided
    if db_path is None:
        db_path = str(DEFAULT_DB_PATH)
    
    with sqlite3.connect(db_path) as conn:
        # Single, completely generic evaluations table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS evaluations (
                evaluation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                workflow_type TEXT NOT NULL,
                evaluation_score REAL NOT NULL,
                evaluation_rubric TEXT NOT NULL DEFAULT '{}',
                details TEXT NOT NULL DEFAULT '{}',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                
                -- Performance indexes
                UNIQUE(session_id, workflow_type, created_at)
            )
        """)
        
        # Create indexes for performance
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_evaluations_session_id 
            ON evaluations(session_id)
        """)
        
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_evaluations_workflow_type 
            ON evaluations(workflow_type)
        """)
        
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_evaluations_created_at 
            ON evaluations(created_at)
        """)
        
        conn.commit()


if __name__ == "__main__":
    """Command-line interface for database initialization."""
    parser = argparse.ArgumentParser(description="Initialize evaluation database tables with generic, scalable schema")
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH), help=f"Database file path (default: {DEFAULT_DB_PATH})")
    
    args = parser.parse_args()
    
    try:
        # Check if database file exists
        db_exists = Path(args.db_path).exists()
        
        # Initialize tables
        initialize_tables(args.db_path)
        
        if db_exists:
            print(f"✅ Evaluation tables verified/updated in {Path(args.db_path).name}")
        else:
            print(f"✅ New evaluation database created: {Path(args.db_path).name}")
        
        print("📋 Table created/verified:")
        print("   • evaluations (generic evaluation storage)")
        print("     - evaluation_id, session_id, workflow_type")
        print("     - evaluation_score, evaluation_rubric (JSON), details (JSON)")
        print("🔍 Indexes created for performance optimization")
        
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        exit(1)