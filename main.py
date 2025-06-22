#!/usr/bin/env python3
"""
Swiggy Dineout Challenge - Restaurant Performance Analysis System

This script orchestrates two modes of operation:
1. Generate Mode: Creates restaurant improvement recommendations
2. Evaluate Mode: Evaluates existing session results against PRD criteria

Usage:
    # Generate mode (default)
    python main.py generate R001
    python main.py generate R001 --artifacts-dir ./custom_artifacts
    python main.py generate R001 --session-id custom123
    
    # Evaluate mode
    python main.py evaluate --session-id abc123def456

Features:
- Dual mode operation with mode-specific system prompts
- Automatic session initialization for generate mode
- Evaluation capabilities for existing sessions
- Structured output with session tracking
- Error handling and cleanup

Author: Swiggy Dineout Challenge
Version: 2.0
"""

import argparse
import glob
import json
import subprocess
import sys
from pathlib import Path

from tools.utils.initialize_session import create_session_context, generate_session_id

# Mode-specific prompt whitelists
GENERATE_MODE_PROMPTS = [
    "orchestration.md",
    "analysis-categories.md", 
    "data-sources.md",
    "artifacts-protocol.md",
    "instructions.md",
    "output-format.md",
    "tools.md",
    "tools-build.md"
]

EVALUATE_MODE_PROMPTS = [
    "evaluation/evaluate-solution.md"
]


def initialize_session(restaurant_id, artifacts_dir="./.artifacts", session_id=None):
    """
    Initialize a new analysis session for the restaurant.

    Args:
        restaurant_id (str): Restaurant ID (e.g., R001)
        artifacts_dir (str): Directory for artifacts storage
        session_id (str): Optional custom session ID

    Returns:
        dict: Session information including session_id and artifacts_directory

    Raises:
        Exception: If session initialization fails
    """
    print(f"🚀 Initializing session for restaurant {restaurant_id}...")

    try:
        # Generate session ID if not provided
        if not session_id:
            session_id = generate_session_id()

        # Create session context directly
        session_context = create_session_context(
            session_id, restaurant_id, artifacts_dir
        )

        print(f"✅ Session initialized: {session_context}")

        return session_context

    except Exception as e:
        print(f"❌ Error during session initialization: {str(e)}")
        raise


def load_system_prompts(mode="generate"):
    """
    Load and concatenate system prompts based on the specified mode.

    Args:
        mode (str): Operation mode - "generate" or "evaluate"

    Returns:
        str: Combined system prompt content

    Raises:
        FileNotFoundError: If prompts directory or files don't exist
        ValueError: If invalid mode or no valid prompts found
    """
    print(f"📄 Loading system prompts for {mode} mode...")

    prompts_dir = Path("prompts")
    if not prompts_dir.exists():
        raise FileNotFoundError("Prompts directory not found")

    # Get whitelisted prompts based on mode
    if mode == "generate":
        allowed_prompts = GENERATE_MODE_PROMPTS
    elif mode == "evaluate":
        allowed_prompts = EVALUATE_MODE_PROMPTS
    else:
        raise ValueError(f"Invalid mode: {mode}. Must be 'generate' or 'evaluate'")

    combined_prompts = []
    loaded_count = 0

    for prompt_filename in allowed_prompts:
        prompt_path = prompts_dir / prompt_filename
        
        if not prompt_path.exists():
            print(f"  ⚠️  Warning: Prompt file not found: {prompt_path}")
            continue
            
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    # Use the filename without extension as the header
                    header = Path(prompt_filename).stem
                    combined_prompts.append(f"# {header}\n\n{content}")
                    print(f"  ✓ Loaded: {prompt_filename}")
                    loaded_count += 1
        except Exception as e:
            print(f"  ⚠️  Warning: Could not load {prompt_filename}: {e}")

    if not combined_prompts:
        raise ValueError(f"No valid prompt content loaded for {mode} mode")

    system_prompt = "\n\n---\n\n".join(combined_prompts)
    print(
        f"✅ Loaded {loaded_count} prompt files for {mode} mode ({len(system_prompt)} characters)"
    )

    return system_prompt


def run_claude_analysis(mode, restaurant_id, session_info, system_prompt, session_id=None):
    """
    Call Claude to perform analysis based on the specified mode.

    Args:
        mode (str): Analysis mode - "generate" or "evaluate"
        restaurant_id (str): Restaurant ID (for generate mode)
        session_info (dict): Session information from initialization
        system_prompt (str): Combined system prompt content
        session_id (str): Session ID (for evaluate mode)

    Returns:
        subprocess.CompletedProcess: Claude command result

    Raises:
        subprocess.CalledProcessError: If Claude command fails
    """
    if mode == "generate":
        print(f"🤖 Generating improvement recommendations for {restaurant_id}...")
        user_prompt = f"Generate improvement recommendations for restaurant {restaurant_id}"
        log_prefix = restaurant_id
    elif mode == "evaluate":
        print(f"📊 Evaluating session results for session {session_id}...")
        user_prompt = f"Evaluate the solution document for session {session_id}"
        log_prefix = f"eval_{session_id}"
    else:
        raise ValueError(f"Invalid mode: {mode}")

    # Enhance system prompt with session context
    enhanced_system_prompt = system_prompt
    if session_info:
        session_context = f"""
# Session Context
You need to maintain session state across interactions.

## Current Session Context
```json
{json.dumps(session_info, indent=2)}
```

## Instructions
Use the session context for any run-time information. 
---

"""
        print(f"Session Context: {session_context}")
        enhanced_system_prompt = session_context + system_prompt

    # Build Claude command
    cmd = [
        "claude",
        "-p",
        user_prompt,
        "--output-format",
        "stream-json",
        "--verbose",
        "--dangerously-skip-permissions",
        "--system-prompt",
        enhanced_system_prompt,
    ]

    try:
        # Create logs directory
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)

        # Determine log filename
        if session_info and "session_id" in session_info:
            log_filename = f"{session_info['session_id']}_{mode}.log"
        else:
            log_filename = f"{log_prefix}_{mode}.log"

        log_file_path = logs_dir / log_filename

        # Run Claude command
        print("🔄 Executing Claude analysis...")
        print(f"📝 Output will be logged to: {log_file_path}")

        # Run command and capture output
        result = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"
        )

        if result.returncode != 0:
            print(f"❌ Claude command failed with return code: {result.returncode}")
            print(f"STDERR: {result.stderr}")
            raise subprocess.CalledProcessError(result.returncode, cmd, result.stderr)

        # Clean the output
        clean_output = (
            result.stdout.replace("\x00", "").replace("\r\n", "\n").replace("\r", "\n")
        )

        # Save to log file
        with open(log_file_path, "w", encoding="utf-8") as log_file:
            log_file.write(clean_output)
            if result.stderr:
                log_file.write(f"\n--- STDERR ---\n{result.stderr}")

        print("✅ Analysis completed successfully")
        print(f"📄 Full output logged to: {log_file_path}")

        # Save output to session artifacts directory
        if session_info and "artifacts_directory" in session_info:
            if mode == "generate":
                output_file = f"{session_info['artifacts_directory']}/improvement_recommendations.json"
            else:  # evaluate mode
                output_file = f"{session_info['artifacts_directory']}/evaluation_results.json"
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(clean_output)
            print(f"💾 Output also saved to: {output_file}")

        return result

    except subprocess.CalledProcessError as e:
        print(f"❌ Claude command failed: {e.stderr}")
        raise
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        raise


def run_evaluation_mode(session_id):
    """
    Run evaluation mode for an existing session.
    
    Args:
        session_id (str): Session ID to evaluate
        
    Returns:
        subprocess.CompletedProcess: Claude command result
        
    Raises:
        FileNotFoundError: If session artifacts don't exist
        subprocess.CalledProcessError: If Claude command fails
    """
    print(f"📊 Starting evaluation mode for session: {session_id}")
    
    # Check if session artifacts exist
    artifacts_dir = Path(".artifacts") / session_id
    if not artifacts_dir.exists():
        raise FileNotFoundError(f"Session artifacts not found for session {session_id}")
    
    # Create session info for evaluation
    session_info = {
        "session_id": session_id,
        "artifacts_directory": str(artifacts_dir),
        "mode": "evaluate"
    }
    
    # Load evaluation system prompts
    system_prompt = load_system_prompts("evaluate")
    
    # Run Claude analysis in evaluate mode
    result = run_claude_analysis("evaluate", None, session_info, system_prompt, session_id)
    
    return result


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Swiggy Dineout Challenge - Restaurant Performance Analysis System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Generate mode (default)
    python main.py generate R001
    python main.py generate R001 --artifacts-dir ./custom_artifacts
    python main.py generate R001 --session-id custom123
    python main.py generate R001 --no-session
    
    # Evaluate mode
    python main.py evaluate --session-id abc123def456
        """,
    )

    subparsers = parser.add_subparsers(dest="mode", help="Operation mode")
    
    # Generate mode subparser
    generate_parser = subparsers.add_parser(
        "generate", 
        help="Generate improvement recommendations for a restaurant"
    )
    generate_parser.add_argument(
        "restaurant_id", 
        help="Restaurant ID (e.g., R001, R002, etc.)"
    )
    generate_parser.add_argument(
        "--artifacts-dir",
        default="./.artifacts",
        help="Directory for artifact storage (default: ./.artifacts)",
    )
    generate_parser.add_argument(
        "--session-id", 
        help="Use specific session ID instead of generating one"
    )
    generate_parser.add_argument(
        "--no-session",
        action="store_true",
        help="Skip session initialization (not recommended)",
    )
    
    # Evaluate mode subparser
    evaluate_parser = subparsers.add_parser(
        "evaluate",
        help="Evaluate existing session results against PRD criteria"
    )
    evaluate_parser.add_argument(
        "--session-id",
        required=True,
        help="Session ID to evaluate (required)"
    )

    args = parser.parse_args()
    
    # Default to generate mode if no mode specified
    if args.mode is None:
        args.mode = "generate"
        # If no subcommand provided, try to parse restaurant_id as first argument
        if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
            args.restaurant_id = sys.argv[1]
        else:
            parser.print_help()
            sys.exit(1)

    try:
        if args.mode == "generate":
            # Generate mode execution
            session_info = None
            
            # Step 1: Initialize session (unless skipped)
            if not args.no_session:
                session_info = initialize_session(
                    args.restaurant_id, args.artifacts_dir, args.session_id
                )
            else:
                print("⚠️  Skipping session initialization (--no-session flag)")

            # Step 2: Load system prompts for generate mode
            system_prompt = load_system_prompts("generate")

            # Step 3: Generate recommendations
            result = run_claude_analysis(
                "generate", args.restaurant_id, session_info, system_prompt
            )

            # Step 4: Display results
            print("\n" + "=" * 80)
            print("📊 GENERATION RESULTS")
            print("=" * 80)
            print(result.stdout)

            if session_info:
                print(
                    f"\n📁 Session artifacts saved to: {session_info['artifacts_directory']}"
                )
                print(f"🆔 Session ID: {session_info['session_id']}")

            print("\n✅ Recommendation generation completed successfully!")
            
        elif args.mode == "evaluate":
            # Evaluate mode execution
            result = run_evaluation_mode(args.session_id)
            
            # Display results
            print("\n" + "=" * 80)
            print("📊 EVALUATION RESULTS")
            print("=" * 80)
            print(result.stdout)
            
            print(f"\n🆔 Evaluated Session ID: {args.session_id}")
            print("\n✅ Evaluation completed successfully!")

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
