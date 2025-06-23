# Swiggy Dineout Challenge - Restaurant Performance Analysis System

An AI-powered co-pilot that generates sales intelligence briefings for restaurant partners by analyzing performance data across multiple dimensions (revenue, campaigns, operations, risk, and competitive positioning).

## Recommended Reading Order

Follow this guided tour to understand the solution architecture and technical approach:

### 1. **Problem Statement** → [`docs/problem-statement.md`](docs/problem-statement.md)
Build an AI-powered Co-Pilot that generates structured performance summaries for restaurant partners.

### 2. **Problem Exploration** → [`docs/problem-exploration.md`](docs/problem-exploration.md)  
Explores the broader vision of replacing fragmented business processes with unified natural language workflows that can be compiled into code and executed by agentic systems.

### 3. **Data Requirements & Generation** → [`docs/data-requirements-and-generation.md`](docs/data-requirements-and-generation.md)
Detailed 12-table database schema with 4,180+ realistic records, including restaurant "personalities" that drive authentic performance patterns for AI analysis.

### 4. **Product Requirements Document (PRD)** → [`docs/restaurant-performance-agent-prd.md`](docs/restaurant-performance-agent-prd.md)
Comprehensive PRD with user stories, acceptance criteria, and evaluation rubrics targeting ≥85% accuracy and 75% reduction in meeting preparation time.

### 5. **System Architecture** → [`docs/system-architecture.md`](docs/system-architecture.md)
Multi-agent orchestration system with 5 specialized analysts coordinated by a Senior Sales Manager, built on Claude Code with modular prompts and self-improving capabilities.

### 6. **Sample Output**
- [artifacts/8e85652c](artifacts/8e85652c)
    - [restaurant_performance_briefing_R001_20241222.md](artifacts/8e85652c/restaurant_performance_briefing_R001_20241222.md)
    - [evaluation_results.md](artifacts/8e85652c/evaluation_results.md)
    - [dashboard.html](artifacts/8e85652c/dashboard.html) 
- [artifacts/8e85652c](artifacts/8e85652c)
    - [restaurant_performance_briefing_R001_20241222.md](artifacts/8e85652c/restaurant_performance_briefing_R001_20241222.md)
    - [evaluation_results.md](artifacts/8e85652c/evaluation_results.md)
    - [pizza_palace_dashboard.html](artifacts/fd0acfd4/pizza_palace_dashboard.html)

(HTML Dashboards need to be downloaded and opened in browser. A bit raw, not evaluated yet - check the prompt here : [dashboard-generator.md](prompts/dashboard-generator.md))

### 7. **Run the System** → [Quick Start Guide](#quick-start) (below)
Try the system yourself with the provided commands to see the AI-powered briefing generation in action.

## Limitations
This POC is a proof of concept and there are a lot of limitations.

- Currently it takes about 10 mins and ~ $3 to generate a briefing for a restaurant, there is a lot of room for optimization.
- The use cases and prompts generated are basic and built through intuition and exploration with AI. They are not validated by domain experts.
- The evaluations implemented are very basic and not comprehensive, they would need refining based on context from the domain experts.
- Currently the agent directly queries the database by constructing SQL queries on the fly, these can be abstracted by a layer of data access tools. (Raw access can still be provided if needed for edge cases)
- The system has no guardrails to prevent hallucinations and policy violations.
- The agents are not built to work with multi-LLM providers as of now (since I had a Claude Max subscription and wanted to use it), but it can be easily extended to work with other LLM providers.
- We don't use an LLM gateway to route requests to the appropriate LLM based on the request as of now.
- The system is not well observable, there isn't adequate tracing and monitoring.
- No deployment pipeline is implemented for cloud deployment.
- The system is not built to be scalable across multiple instances.
- A subset of the final system architecture is implemented in this POC.

---

## Overview

This system addresses the real challenge faced by Sales Executives and Account Managers who manually gather performance metrics across multiple dashboards (taking 30mins to 3 hours per restaurant). Our GenAI Co-Pilot automates this process, generating structured, contextual performance summaries tailored for each restaurant partner.

### Problem Solved
- **Current Pain**: Manual data gathering from multiple dashboards before restaurant meetings
- **Solution**: Automated AI-powered briefings with actionable insights
- **Impact**: Save 30min-3hrs per restaurant analysis while improving insight quality

## Quick Start

### 1. Prerequisites

#### Claude Code Installation
This project requires Claude Code for AI-powered analysis. Choose one of these authentication methods:

**Option 1: Claude Pro/Max Subscription (Recommended)**
- Subscribe to Claude Pro ($20/month) or Max ($100-200/month) at [claude.ai/upgrade](https://claude.ai/upgrade)

**Option 2: Anthropic API Key (Pay-per-use)**
- Create account at [console.anthropic.com](https://console.anthropic.com)
- Generate API key in console
- Pay-per-token usage model

#### Claude Code Setup
```bash
# System Requirements: macOS 10.15+, Ubuntu 20.04+, or Windows via WSL
# Install Node.js 18+ from nodejs.org

# Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# Navigate to project directory and start Claude Code
cd /path/to/swiggy-dineout-challenge
claude

# First-time authentication:
# - Select authentication method (Console API or Pro/Max subscription)
# - Follow browser prompts to connect your account
# - If switching from API to subscription, run: /login
```

#### Project Dependencies
```bash
# Install dependencies
uv sync

# Initialize database with sample data
uv run tools/utils/init_database.py

# Verify setup
sqlite3 swiggy_dineout.db ".tables"
```

### 2. Generate Mode - Sales Intelligence Briefings

Generate comprehensive performance analysis and improvement recommendations:

```bash
# Generate briefing for restaurant R001
python main.py generate R001
```

### 3. Evaluate Mode - Quality Assessment

Evaluate existing session results against PRD criteria and scoring rubrics:

```bash
# Evaluate a specific session's output quality
python main.py evaluate --session-id acad9e9a
```

## File Organization

```
├── main.py                 # Dual-mode entry point
├── prompts/               # System prompts by category
│   ├── orchestration.md   # Multi-agent coordination
│   ├── analysis-categories.md  # Specialist analyst roles
│   ├── data-sources.md    # Available data tables
│   ├── artifacts-protocol.md   # Output standardization
│   ├── dashboard-generator.md  # HTML dashboard creation
│   ├── instructions.md    # General system instructions
│   ├── output-format.md   # Report formatting guidelines
│   ├── tools-build.md     # Tool construction prompts
│   ├── tools.md          # Available tool definitions
│   └── evaluation/       # Assessment prompts
│       └── evaluate-solution.md
├── tools/                # Utilities and evaluation
│   ├── utils/           # Session management, DB operations
│   │   ├── get_tools.py
│   │   ├── init_database.py
│   │   └── initialize_session.py
│   └── evaluation/      # Quality assessment tools
│       ├── get_trends.py
│       ├── initialize_db.py
│       └── save_score.py
├── docs/                # Technical documentation
│   ├── data-requirements-and-generation.md
│   ├── problem-exploration.md
│   ├── problem-statement.md
│   ├── restaurant-performance-agent-prd.md
│   ├── system-architecture.md
│   ├── images/          # Architecture diagrams
│   └── external/        # External documentation
├── artifacts/           # Generated session outputs
├── logs/               # System execution logs
└── pyproject.toml      # UV package management
```

