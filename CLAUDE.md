# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Swiggy Dineout Challenge** - an AI-powered co-pilot system for restaurant performance analytics. The system provides sales intelligence briefings for restaurant partners by analyzing performance data across multiple dimensions (revenue, campaigns, operations, risk, and competitive positioning).

## Architecture

### Core System Design
- **Multi-Agent Orchestration**: Senior Sales Manager coordinates specialized data analysts
- **Prompt-Based Architecture**: System uses structured prompts for different analysis categories
- **Database-Driven**: SQLite database (`swiggy_dineout.db`) stores restaurant performance data
- **File-Based Workflow**: Generates structured reports and analyses in markdown format

### Key Components
- **Orchestration Layer** (`prompts/0. orchestration.md`): Coordinates analyst team deployment
- **Specialized Analysts**: Revenue optimization, risk/quality, campaign performance, financial health, competitive intelligence
- **Tool System** (`tools/`): Utilities for database operations, session management, and evaluation
- **Prompt System** (`prompts/`): Structured prompts for different analysis categories

## Development Commands

### Package Management
```bash
# Install dependencies
uv sync

# Add new dependency
uv add <package-name>

# Development dependencies
uv add --dev <package-name>
```

### Code Quality
```bash
# Format code
uv run black .

# Lint code
uv run ruff check .

# Type checking
uv run mypy .

# Run tests
uv run pytest
```

### Tool Usage
```bash
# Discover available tools
uv run tools/utils/get_tools.py

# Initialize session for restaurant analysis
uv run tools/utils/initialize_session.py R001

# Run evaluation tools
uv run tools/evaluation/initialize_db.py
uv run tools/evaluation/get_trends.py
```

### Database Operations
```bash
# Initialize database
uv run tools/utils/init_database.py

# Check database status
sqlite3 swiggy_dineout.db ".tables"
```

## System Architecture

### Data Flow
1. **Input**: Restaurant ID (e.g., R001)
2. **Orchestration**: Senior Sales Manager deploys specialized analysts
3. **Parallel Analysis**: 5 specialized analysts generate reports
4. **Synthesis**: Integration of findings into comprehensive briefing
5. **Output**: Structured sales intelligence briefing

### Prompt Engineering Structure
- **Session Management** (`prompts/1. session.md`): Handles session initialization
- **Analysis Categories** (`prompts/3. analysis-categories.md`): Defines specialized analyst roles
- **Data Sources** (`prompts/4. data-sources.md`): Specifies available data tables
- **Artifacts Protocol** (`prompts/5. artifacts-protocol.md`): Standardizes output formats

### File Organization
- `docs/`: Technical documentation and PRDs
- `prompts/`: System prompts for different analysis categories
- `tools/`: Utility scripts and evaluation tools
- `artifacts/`: Generated analysis outputs (git-ignored)

## Key Technical Details

### Database Schema
- Restaurant performance data stored in SQLite
- Tables include: restaurants, bookings, campaigns, reviews, settlements
- Use `tools/utils/init_database.py` to initialize schema

### Evaluation System
- Performance tracking via `tools/evaluation/`
- Metrics: accuracy, completeness, insight quality
- Run evaluations with `uv run tools/evaluation/save_score.py`

### Session Management
- Each analysis session has unique ID
- Artifacts stored in session-specific directories
- Use `tools/utils/initialize_session.py` for setup

## Development Workflow

### Adding New Analysis Categories
1. Create new prompt in `prompts/` directory
2. Update orchestration prompt to include new analyst
3. Add corresponding tool if needed
4. Update evaluation metrics

### Extending Data Sources
1. Add new tables to database schema
2. Update `prompts/4. data-sources.md`
3. Modify analyst prompts to use new data
4. Test with evaluation tools

### Running System End-to-End
1. Initialize database: `uv run tools/utils/init_database.py`
2. Create session: `uv run tools/utils/initialize_session.py R001`
3. Run analysis through prompt system
4. Evaluate results: `uv run tools/evaluation/save_score.py`

## Important Notes

- System generates extensive markdown reports - manage file sizes carefully
- Database operations should use transactions for data integrity
- Prompt engineering is critical - test changes thoroughly
- Evaluation metrics track both accuracy and business relevance
- Tool discovery system helps navigate available utilities

## Testing Strategy

- Unit tests for individual tools and utilities
- Integration tests for end-to-end workflow
- Evaluation framework for AI-generated insights
- Performance benchmarks for analysis speed and accuracy