#!/usr/bin/env python3
"""
Session Initialization Script for Restaurant Intelligence System
Generates unique session ID and creates session context with proper artifact directory structure.
"""

import json
import os
import uuid
from datetime import datetime
import argparse

def generate_session_id():
    """Generate a unique 8-character session ID"""
    return str(uuid.uuid4())[:8]

def create_session_context(session_id, restaurant_id, artifacts_dir="artifacts"):
    """Create session context JSON file"""
    
    # Create artifacts directory structure
    session_dir = f"{artifacts_dir}/{session_id}"
    os.makedirs(session_dir, exist_ok=True)
    
    # Create session context
    session_context = {
        "session_id": session_id,
        "restaurant_id": restaurant_id,
        "timestamp": datetime.now().isoformat(),
        "workflow": "generate-restaurant-insights",
        "status": "initialized",
        "artifacts_directory": f"/{artifacts_dir}/{session_id}/"
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

def main():
    parser = argparse.ArgumentParser(description="Initialize restaurant analysis session")
    parser.add_argument("restaurant_id", help="Restaurant ID (e.g., R001)")
    parser.add_argument("--artifacts-dir", default="artifacts", help="Directory for artifact storage")
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