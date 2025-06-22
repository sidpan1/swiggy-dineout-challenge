#!/usr/bin/env python3
"""
Session Initialization Tool for Restaurant Intelligence System

This tool creates and manages session contexts for restaurant performance analysis workflows.
It generates unique session IDs, sets up artifact directory structures, and initializes
session state with proper database configuration.

Main Functions:
- generate_session_id(): Create unique 8-character session identifier
- create_session_context(): Initialize session with artifacts and database config
- main(): Command-line interface for session initialization

Usage:
    # Initialize session for restaurant R001
    uv run tools/utils/initialize_session.py R001
    
    # Use custom artifacts directory
    uv run tools/utils/initialize_session.py R001 --artifacts-dir ./custom_artifacts
    
    # Use specific session ID
    uv run tools/utils/initialize_session.py R001 --session-id "custom123"

Author: Swiggy Dineout Challenge
Version: 1.0
"""

import json
import os
import uuid
from datetime import datetime
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_session_id():
    """
    Generate a unique 8-character session identifier.
    
    Creates a random UUID and truncates to first 8 characters for use as
    a short, unique session identifier.
    
    Returns:
        str: 8-character session ID (e.g., "a1b2c3d4")
        
    Example:
        >>> session_id = generate_session_id()
        >>> len(session_id)
        8
    """
    return str(uuid.uuid4())[:8]

def create_session_context(session_id, restaurant_id, artifacts_dir="./.artifacts"):
    """
    Create comprehensive session context with artifacts directory structure.
    
    Initializes a new session with proper directory structure, session metadata,
    database configuration, and logging files. Creates all necessary files for
    workflow execution tracking and error handling.
    
    Args:
        session_id (str): Unique session identifier
        restaurant_id (str): Restaurant being analyzed (e.g., "R001")
        artifacts_dir (str): Base directory for artifact storage. Default: "./.artifacts"
        
    Returns:
        Tuple[Dict, str]: Session context dictionary and session directory path
        
    Raises:
        OSError: If directory creation fails
        IOError: If file creation fails
        
    Example:
        >>> context, dir_path = create_session_context("abc12345", "R001")
        >>> print(context['session_id'])
        'abc12345'
        >>> print(context['restaurant_id'])
        'R001'
    """
    
    # Create artifacts directory structure with absolute path
    artifacts_dir_abs = os.path.abspath(artifacts_dir)
    session_dir = f"{artifacts_dir_abs}/{session_id}"
    os.makedirs(session_dir, exist_ok=True)
    
    # Create logs subdirectory
    logs_dir = f"{session_dir}/logs"
    os.makedirs(logs_dir, exist_ok=True)
    
    # Get database configuration from environment variables
    db_type = os.getenv("DATABASE_TYPE", "sqlite")
    db_url = os.getenv("DATABASE_URL", "sqlite:/Users/sid/Code/swiggy-dinout-challenge/.db/swiggy_dineout.db")
    
    # Create session context
    session_context = {
        "session_id": session_id,
        "restaurant_id": restaurant_id,
        "timestamp": datetime.now().isoformat(),
        "workflow": "generate-restaurant-insights",
        "status": "initialized",
        "artifacts_directory": f"{session_dir}/",
        "database": {
            "type": db_type,
            "url": db_url
        }
    }
    
    # Save session context
    context_file = f"{session_dir}/session_context.json"
    with open(context_file, 'w') as f:
        json.dump(session_context, f, indent=2)
    
    # Initialize workflow execution log
    workflow_log = {"workflows": []}
    workflow_file = f"{session_dir}/workflow_execution.json"
    with open(workflow_file, 'w') as f:
        json.dump(workflow_log, f, indent=2)
    
    # Initialize error log
    error_log = {"errors": []}
    error_file = f"{session_dir}/error_log.json"
    with open(error_file, 'w') as f:
        json.dump(error_log, f, indent=2)
    
    return session_context, session_dir

def read_session_context(session_id):
    """
    Read session context from file.
    """
    with open(f"./.artifacts/{session_id}/session_context.json", "r") as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Initialize restaurant analysis session")
    parser.add_argument("restaurant_id", help="Restaurant ID (e.g., R001)")
    parser.add_argument("--artifacts-dir", default="./.artifacts", help="Directory for artifact storage")
    parser.add_argument("--session-id", help="Use specific session ID instead of generating one")
    
    args = parser.parse_args()
    
    # Generate or use provided session ID
    session_id = args.session_id if args.session_id else generate_session_id()
    
    try:
        # Create session context and directory structure
        session_context, session_dir = create_session_context(session_id, args.restaurant_id, args.artifacts_dir)
        
        print(f"✅ Session initialized successfully!")
        print(f"📋 Session ID: {session_id}")
        print(f"🏪 Restaurant ID: {args.restaurant_id}")
        print(f"📁 Artifacts directory: {session_dir}")
        print(f"📄 Session context: {session_dir}/session_context.json")
        
        # Output session info for use by calling workflow
        return {
            "session_id": session_id,
            "restaurant_id": args.restaurant_id,
            "artifacts_directory": session_dir,
            "session_context_file": f"{session_dir}/session_context.json"
        }
        
    except Exception as e:
        print(f"❌ Error initializing session: {str(e)}")
        return None

if __name__ == "__main__":
    result = main()
    if result:
        # Print JSON output for script chaining
        print("\n" + json.dumps(result, indent=2))