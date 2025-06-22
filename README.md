# Swiggy Dineout Challenge - Restaurant Performance Analysis System

An AI-powered co-pilot that generates sales intelligence briefings for restaurant partners by analyzing performance data across multiple dimensions (revenue, campaigns, operations, risk, and competitive positioning).

## Overview

This system addresses the real challenge faced by Sales Executives and Account Managers who manually gather performance metrics across multiple dashboards (taking 30mins to 3 hours per restaurant). Our GenAI Co-Pilot automates this process, generating structured, contextual performance summaries tailored for each restaurant partner.

### Problem Solved
- **Current Pain**: Manual data gathering from multiple dashboards before restaurant meetings
- **Solution**: Automated AI-powered briefings with actionable insights
- **Impact**: Save 30min-3hrs per restaurant analysis while improving insight quality

## Quick Start

### Generate Mode - Sales Intelligence Briefings

Generate comprehensive performance analysis and improvement recommendations:

```bash
# Generate briefing for restaurant R001
python main.py generate R001

# Use custom artifacts directory
python main.py generate R001 --artifacts-dir ./custom_artifacts

# Use specific session ID for tracking
python main.py generate R001 --session-id custom123

# Skip session initialization (not recommended)
python main.py generate R001 --no-session
```

### Evaluate Mode - Quality Assessment

Evaluate existing session results against PRD criteria and scoring rubrics:

```bash
# Evaluate a specific session's output quality
python main.py evaluate --session-id abc123def456
```

## System Architecture

### 🤖 Multi-Agent Orchestration
- **Senior Sales Manager**: Coordinates specialized analyst deployment
- **5 Specialized Analysts**: Revenue optimization, risk/quality, campaign performance, financial health, competitive intelligence
- **Parallel Analysis**: Each analyst generates focused reports simultaneously
- **Synthesis**: Integration into comprehensive sales briefing

### 📊 Core Analysis Dimensions

1. **Recent Performance** (30-day trends)
   - Bookings, cancellations, revenue, ratings
   - Notable changes and trend analysis

2. **Ad Campaign Effectiveness**
   - Spend, impressions, clicks, conversions, ROI
   - Inefficiencies and optimization opportunities

3. **Peer Benchmarking**
   - Comparison with similar restaurants (locality + cuisine)
   - Performance gaps and advantages

4. **Actionable Recommendations**
   - Data-backed suggestions for performance improvement
   - Specific next steps for sales conversations

### 🎯 Key Metrics Tracked

| Metric | Purpose | Sales Use Case |
|--------|---------|----------------|
| **OPD** (Orders per day) | Demand signal | Growth tracking, benchmark vs peers |
| **Revenue/GOV** | Traffic quality | Identify high-potential partners |
| **Ads ROI** | Campaign effectiveness | Pitch/diagnose ads, counter objections |

## System Modes

### 🔧 Generate Mode
- **Purpose**: Creates restaurant sales intelligence briefings
- **System Prompts**: Multi-agent orchestration with specialized analysts
- **Data Sources**: Restaurant metrics, ads data, peer benchmarks, reviews, settlements
- **Output**: Structured markdown briefing ready for sales meetings

### 📊 Evaluate Mode  
- **Purpose**: Quality assessment against PRD evaluation rubric
- **System Prompts**: Evaluation-specific prompts only
- **Scoring**: Quantitative assessment with improvement recommendations
- **Output**: Detailed evaluation report with scores and actionable feedback

## Development Setup

### Prerequisites
```bash
# Install dependencies
uv sync

# Initialize database with sample data
uv run tools/utils/init_database.py

# Verify setup
sqlite3 swiggy_dineout.db ".tables"
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

### Tool Discovery
```bash
# See available tools
uv run tools/utils/get_tools.py

# Run evaluation tools
uv run tools/evaluation/initialize_db.py
uv run tools/evaluation/get_trends.py
```

## File Organization

```
├── main.py                 # Dual-mode entry point
├── prompts/               # System prompts by category
│   ├── orchestration.md   # Multi-agent coordination
│   ├── analysis-categories.md  # Specialist analyst roles
│   ├── data-sources.md    # Available data tables
│   └── evaluation/        # Assessment prompts
├── tools/                 # Utilities and evaluation
│   ├── utils/            # Session management, DB operations
│   └── evaluation/       # Quality assessment tools
├── docs/                 # Technical documentation
└── .artifacts/           # Generated session outputs
```

## Sample Output Structure

The system generates markdown briefings containing:

- **Executive Summary**: Key performance highlights
- **Performance Analysis**: 30-day trends and metrics
- **Campaign Assessment**: Ad effectiveness and ROI analysis  
- **Competitive Position**: Peer benchmarking insights
- **Recommended Actions**: Specific, data-backed next steps

## Evaluation Framework

Quality assessment based on:
- **Data Accuracy**: Correct interpretation of metrics
- **Insight Quality**: Actionable and relevant recommendations  
- **Completeness**: Coverage of all analysis dimensions
- **Confidence Calibration**: Appropriate uncertainty handling

## Legacy Commands

```bash
# Manual Claude commands (not recommended)
claude -p "Generate improvement recommendations for restaurant R001" \
  --output-format stream-json --verbose --dangerously-skip-permissions \
  --system-prompt "$(cat prompts/*.md)"
```

**Note**: Use `main.py` for proper session management, mode-specific prompt filtering, and structured artifact handling.