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
import anyio
import json
import sys
from abc import ABC, abstractmethod
from pathlib import Path

from claude_code_sdk import ClaudeCodeOptions, Message, query

from tools.utils.initialize_session import (
    create_session_context,
    generate_session_id,
    read_session_context,
)

# Mode-specific prompt whitelists
GENERATE_MODE_PROMPTS = [
    "orchestration.md",
    "artifacts-protocol.md",
    "instructions.md",
    "analysis-categories.md",
    "data-sources.md",
    "output-format.md",
    "tools.md",
    "tools-build.md",
]

EVALUATE_MODE_PROMPTS = [
    "evaluation/evaluate-solution.md",
]


class ModeCommand(ABC):
    """Abstract base class for mode-specific commands."""

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @abstractmethod
    def get_user_prompt(self) -> str:
        """Get the user prompt for this mode."""
        pass

    @abstractmethod
    def get_log_prefix(self) -> str:
        """Get the log filename prefix for this mode."""
        pass

    @abstractmethod
    def get_mode_name(self) -> str:
        """Get the mode name for logging."""
        pass

    def enhance_system_prompt(self, base_prompt: str, session_context: dict) -> str:
        """Enhance the system prompt with session context (default implementation)."""
        if not session_context:
            return base_prompt

        session_context = f"""
# Session Context
You need to maintain session state across interactions.

## Current Session Context
```json
{json.dumps(session_context, indent=2)}
```

## Instructions
Use the session context for any run-time information. 
---

"""
        return session_context + base_prompt


class GenerateCommand(ModeCommand):
    """Command for generate mode."""

    def __init__(
        self,
        restaurant_id: str,
        artifacts_dir: str = "./.artifacts",
        session_id: str = None,
        no_session: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.restaurant_id = restaurant_id
        self.artifacts_dir = artifacts_dir
        self.session_id = session_id
        self.no_session = no_session

    def get_user_prompt(self) -> str:
        return (
            f"Generate improvement recommendations for restaurant {self.restaurant_id}"
        )

    def get_log_prefix(self) -> str:
        return self.restaurant_id

    def get_mode_name(self) -> str:
        return "generate"

    async def execute(self):
        """Execute the generate mode logic."""
        print(f"🚀 Starting generate mode for restaurant: {self.restaurant_id}")

        session_context = None

        # Step 1: Initialize session (unless skipped)
        if not self.no_session:
            session_context = initialize_session(
                self.restaurant_id, self.artifacts_dir, self.session_id
            )
        else:
            print("⚠️  Skipping session initialization (--no-session flag)")

        # Step 2: Load system prompts for generate mode
        system_prompt = load_system_prompts(GENERATE_MODE_PROMPTS)

        # Step 3: Run Claude analysis
        output_file = None
        if session_context and "artifacts_directory" in session_context:
            output_file = f"{session_context['artifacts_directory']}/logs/run_log.json"

        result = await run_claude(self, session_context, system_prompt, output_file)

        return result


class EvaluateCommand(ModeCommand):
    """Command for evaluate mode."""

    def __init__(self, session_id: str, **kwargs):
        super().__init__(**kwargs)
        self.session_id = session_id

    def get_user_prompt(self) -> str:
        return f"Evaluate the solution document for session {self.session_id}"

    def get_log_prefix(self) -> str:
        return f"eval_{self.session_id}"

    def get_mode_name(self) -> str:
        return "evaluate"

    def enhance_system_prompt(self, base_prompt: str, session_context: dict) -> str:
        """Enhance system prompt with inspection prompts for evaluate mode."""
        # First apply the default session context enhancement
        enhanced_prompt = super().enhance_system_prompt(base_prompt, session_context)

        # Add inspection prompts specific to evaluate mode
        inspection_prompts = f"""
    # The following prompts are used by the main agent to generate the output:
    {", ".join(GENERATE_MODE_PROMPTS)}. They will be found in the following directory: {Path("prompts")}
    """

        return enhanced_prompt + "\n\n" + inspection_prompts

    async def execute(self):
        """Execute the evaluate mode logic."""
        print(f"📊 Starting evaluation mode for session: {self.session_id}")

        # Check if session artifacts exist
        artifacts_dir = Path(".artifacts") / self.session_id
        if not artifacts_dir.exists():
            raise FileNotFoundError(
                f"Session artifacts not found for session {self.session_id}"
            )

        # Create session info for evaluation
        session_context = read_session_context(self.session_id)

        # Load evaluation system prompts
        system_prompt = load_system_prompts(EVALUATE_MODE_PROMPTS)

        # Run Claude analysis in evaluate mode
        output_file = f"{session_context['artifacts_directory']}/logs/eval_log.json"
        result = await run_claude(self, session_context, system_prompt, output_file)

        return result


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
        session_context, _ = create_session_context(
            session_id, restaurant_id, artifacts_dir
        )

        print(f"✅ Session initialized: {session_context}")

        return session_context

    except Exception as e:
        print(f"❌ Error during session initialization: {str(e)}")
        raise


def load_system_prompts(prompt_files):
    """
    Load and concatenate system prompts from the specified list of markdown files.

    Args:
        prompt_files (list): List of markdown file names to load

    Returns:
        str: Combined system prompt content

    Raises:
        FileNotFoundError: If prompts directory doesn't exist
        ValueError: If no valid prompts found
    """
    print(f"📄 Loading {len(prompt_files)} system prompt files...")

    prompts_dir = Path("prompts")
    if not prompts_dir.exists():
        raise FileNotFoundError("Prompts directory not found")

    combined_prompts = []
    loaded_count = 0

    for prompt_filename in prompt_files:
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
        raise ValueError("No valid prompt content loaded")

    system_prompt = "\n\n---\n\n".join(combined_prompts)
    print(f"✅ Loaded {loaded_count} prompt files ({len(system_prompt)} characters)")

    return system_prompt


async def run_claude(
    command: ModeCommand,
    session_context: dict,
    system_prompt: str,
    output_file: str = None,
):
    """
    Call Claude using the provided command and session information.

    Args:
        command (ModeCommand): Command object containing mode-specific logic
        session_context (dict): Session information from initialization
        system_prompt (str): Combined system prompt content
        output_file (str): Optional path to save artifacts output file

    Returns:
        dict: Analysis result with output and metadata

    Raises:
        Exception: If Claude analysis fails
    """
    mode_name = command.get_mode_name()
    user_prompt = command.get_user_prompt()
    log_prefix = command.get_log_prefix()

    print(f"🤖 Running {mode_name} mode...")

    # Enhance system prompt with session context and mode-specific enhancements
    enhanced_system_prompt = command.enhance_system_prompt(
        system_prompt, session_context
    )

    # print(f"System Prompt: {enhanced_system_prompt}")

    try:
        # Create logs directory
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)

        # Determine log filename
        if session_context and "session_id" in session_context:
            log_filename = f"{session_context['session_id']}_{mode_name}.log"
        else:
            log_filename = f"{log_prefix}_{mode_name}.log"

        log_file_path = logs_dir / log_filename

        print("🔄 Executing Claude analysis...")
        print(f"📝 Output will be logged to: {log_file_path}")

        # Set up Claude Code options with session directory as working directory
        if session_context and "artifacts_directory" in session_context:
            # Use the session artifacts directory as the working directory
            working_dir = Path(session_context["artifacts_directory"])
            print(
                f"📁 Using session artifacts directory as working directory: {working_dir}"
            )
        else:
            # Fallback to current directory if no session info
            working_dir = Path.cwd()
            print(f"📁 Using current directory as working directory: {working_dir}")

        options = ClaudeCodeOptions(
            system_prompt=enhanced_system_prompt,
            cwd=working_dir,
            permission_mode="bypassPermissions",
        )

        # Collect all messages from the SDK
        messages: list[Message] = []
        output_content = []

        async for message in query(prompt=user_prompt, options=options):
            messages.append(message)

            # Log the message as JSON for compatibility
            message_json = json.dumps(message, default=str, indent=2)
            output_content.append(message_json)

            # Print progress for assistant messages
            if hasattr(message, "type") and message.get("type") == "assistant":
                print("📝 Received assistant response...")

        # Combine all output
        full_output = "\n".join(output_content)

        # Save to log file
        with open(log_file_path, "w", encoding="utf-8") as log_file:
            log_file.write(full_output)

        print("✅ Analysis completed successfully")
        print(f"📄 Full output logged to: {log_file_path}")

        # Save output to artifacts directory if specified
        if output_file:
            # Ensure the directory exists
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(full_output)
            print(f"💾 Output also saved to: {output_file}")

        # Return result in similar format to subprocess.CompletedProcess
        return {"stdout": full_output, "messages": messages, "returncode": 0}

    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        raise e


async def async_main():
    """Async main entry point for the script."""
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
        "generate", help="Generate improvement recommendations for a restaurant"
    )
    generate_parser.add_argument(
        "restaurant_id", help="Restaurant ID (e.g., R001, R002, etc.)"
    )
    generate_parser.add_argument(
        "--artifacts-dir",
        default="./.artifacts",
        help="Directory for artifact storage (default: ./.artifacts)",
    )
    generate_parser.add_argument(
        "--session-id", help="Use specific session ID instead of generating one"
    )
    generate_parser.add_argument(
        "--no-session",
        action="store_true",
        help="Skip session initialization (not recommended)",
    )

    # Evaluate mode subparser
    evaluate_parser = subparsers.add_parser(
        "evaluate", help="Evaluate existing session results against PRD criteria"
    )
    evaluate_parser.add_argument(
        "--session-id", required=True, help="Session ID to evaluate (required)"
    )

    args = parser.parse_args()

    # Default to generate mode if no mode specified
    if args.mode is None:
        args.mode = "generate"
        # If no subcommand provided, try to parse restaurant_id as first argument
        if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
            args.restaurant_id = sys.argv[1]
        else:
            parser.print_help()
            sys.exit(1)

    try:
        if args.mode == "generate":
            # Generate mode execution
            command = GenerateCommand(
                restaurant_id=args.restaurant_id,
                artifacts_dir=args.artifacts_dir,
                session_id=args.session_id,
                no_session=args.no_session,
            )
            result = await command.execute()

            # Display results
            print("\n" + "=" * 80)
            print("📊 GENERATION RESULTS")
            print("=" * 80)
            print(result["stdout"])

            # Show session info if available
            if not args.no_session:
                print("\n📁 Session artifacts saved")
                if args.session_id:
                    print(f"🆔 Session ID: {args.session_id}")

            print("\n✅ Recommendation generation completed successfully!")

        elif args.mode == "evaluate":
            # Evaluate mode execution
            command = EvaluateCommand(session_id=args.session_id)
            result = await command.execute()

            # Display results
            print("\n" + "=" * 80)
            print("📊 EVALUATION RESULTS")
            print("=" * 80)
            print(result["stdout"])

            print(f"\n🆔 Evaluated Session ID: {args.session_id}")
            print("\n✅ Evaluation completed successfully!")

            print(f"\n🆔 Evaluated Session ID: {args.session_id}")
            print("\n✅ Evaluation completed successfully!")

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


def main():
    """Main entry point for the script."""
    anyio.run(async_main)


if __name__ == "__main__":
    main()
