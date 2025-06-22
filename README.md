s# Swiggy Dineout Restaurant Intelligence Workflows

## Overview

This directory contains natural language hierarchical workflows for the Swiggy Dineout restaurant intelligence system. These workflows automate the generation of comprehensive restaurant performance insights for Sales Executives and Account Managers.

## Main Workflow

The primary workflow that generates complete restaurant insights:

### `/generate-restaurant-insights`
**Input**: Natural language prompt with restaurant ID  
**Output**: Comprehensive restaurant performance report with session-based artifacts  
**Description**: Master workflow that orchestrates complete restaurant analysis using a hybrid approach of deterministic Python scripts and Claude sub-workflows. Generates comprehensive insights including performance trends, ad campaign effectiveness, peer benchmarking, and actionable recommendations with full session management and error handling.

**Key Features**:
- **Session Management**: Unique 8-character session IDs with structured artifact directories
- **Hybrid Execution**: Combines deterministic Python scripts with Claude sub-workflows
- **Error Handling**: Graceful handling of data issues and sub-workflow failures
- **Artifact Protocol**: Structured JSON outputs for each analysis component
- **Reproducible Environment**: Uses `uv` for consistent dependency management

**Usage Examples**:
```bash
claude "/generate-restaurant-insights Generate comprehensive performance insights for restaurant R001"

claude "/generate-restaurant-insights Analyze restaurant R002 performance for the last 30 days"

claude "/generate-restaurant-insights Create a complete analysis report for Spice Garden restaurant (R001)"
```

**Execution Flow**:
1. Initialize session with unique ID and artifact structure
2. Install dependencies using `uv sync`
3. Execute data collection via Python script
4. Analyze performance trends via Python script
5. Evaluate ad campaigns via Claude sub-workflow
6. Generate peer insights via Claude sub-workflow
7. Detect anomalies via Python script
8. Create recommendations via Claude sub-workflow
9. Generate final report via Claude sub-workflow
10. Complete session and archive results

## Workflow Categories

### 🔍 Analysis Workflows (`analysis/`)
Core analytical workflows that examine different aspects of restaurant performance:

- `claude -p "/analyze-performance-trends Analyze 30-day performance trends for restaurant R001"`
- `claude -p "/evaluate-ad-campaigns Evaluate ad campaign effectiveness for restaurant R001"`
- `claude -p "/generate-peer-insights Compare restaurant R001 with similar restaurants in the area"`
- `claude -p "/detect-anomalies Identify unusual patterns in restaurant R001 performance"`

### 📊 Data Collection Workflows (`tasks/`)
Workflows that gather and validate data from various sources:

- `claude -p "/collect-restaurant-data Collect all performance data for restaurant R001"`

### 🎯 Action Generation Workflows (`actions/`)
Workflows that generate specific actionable recommendations:

- `claude -p "/generate-recommendations Generate improvement recommendations for restaurant R001"`

### 📋 Reporting Workflows (`workflows/`)
Workflows that create formatted outputs for different audiences:

- `claude -p "/generate-restaurant-insights Generate comprehensive insights for restaurant R001"` **(Master Workflow)**
- `claude -p "/generate-restaurant-report Create a detailed report for restaurant R001"`

## Workflow Hierarchy

The master workflow uses a hybrid execution pattern combining Python scripts and Claude sub-workflows:

```
generate-restaurant-insights (Master Workflow)
├── initialize_session.py (Session Setup - Python Script)
├── uv sync (Dependency Management)
├── collect_restaurant_data.py (Data Collection - Python Script)
├── analyze_performance_trends.py (Performance Analysis - Python Script)
├── evaluate-ad-campaigns (Marketing Analysis - Claude Sub-workflow)
├── generate-peer-insights (Competitive Analysis - Claude Sub-workflow)
├── detect_anomalies.py (Risk Detection - Python Script)
├── generate-recommendations (Action Planning - Claude Sub-workflow)
├── generate-restaurant-report (Output Generation - Claude Sub-workflow)
└── session completion (Archive Results)
```

### Execution Patterns

#### Python Script Execution
Deterministic data processing and analysis:
```bash
uv run python tools/script_name.py {restaurant_id} {session_id} --artifacts-dir artifacts
```

#### Claude Sub-workflow Execution
Natural language processing and insight generation:
```bash
claude -p "/workflow-name SESSION_ID={session_id} Natural language prompt with context" --output-format json --dangerously-skip-permissions
```

#### Session-Based Artifact Sharing
All workflows share data through structured artifact directories:
```
/artifacts/{session_id}/
├── restaurant_data.json
├── performance_trends.json
├── ad_evaluation.json
├── peer_insights.json
├── anomalies.json
├── recommendations.json
├── restaurant_report.md
├── workflow_execution.json
├── session_context.json
└── error_log.json
```

## Natural Language Input Examples

### Basic Analysis Requests
- "Analyze restaurant R001 performance"
- "Generate insights for Spice Garden restaurant"
- "Create performance report for restaurant R002"

### Specific Analysis Requests  
- "Focus on ad campaign performance for restaurant R001"
- "Compare restaurant R001 with peer restaurants"
- "Identify performance anomalies for restaurant R003"

### Time-Based Analysis
- "Analyze restaurant R001 performance over the last 30 days"
- "Generate weekly performance summary for restaurant R002"
- "Compare this month vs last month for restaurant R001"

### Output Format Requests
- "Create a summary report for restaurant R001"
- "Generate detailed analysis for restaurant R002"
- "Provide executive summary for restaurant R003"

## Workflow Responses

Each workflow understands context and responds intelligently:

- **Restaurant Identification**: Automatically extracts restaurant ID from natural language
- **Context Awareness**: Understands related requests and maintains context
- **Error Handling**: Provides helpful suggestions when information is unclear
- **Intelligent Defaults**: Uses sensible defaults when specific parameters aren't mentioned

## Example Workflow Execution

**User Input**: "Generate comprehensive insights for restaurant R001"

**Detailed Workflow Response**:
1. **Parse Request**: Extract restaurant_id = "R001" and create analysis context
2. **Install Dependencies**: Execute `uv sync` to ensure reproducible Python environment
3. **Initialize Session**: Generate unique session ID (e.g., "a1b2c3d4") and create artifact structure
4. **Collect Data**: Run `collect_restaurant_data.py` to gather all restaurant metrics, ads data, and peer benchmarks
5. **Analyze Trends**: Execute `analyze_performance_trends.py` to identify booking/revenue patterns and growth rates
6. **Evaluate Campaigns**: Invoke Claude sub-workflow for ad campaign ROI analysis using shared artifacts
7. **Generate Peer Insights**: Invoke Claude sub-workflow for competitive positioning analysis
8. **Detect Anomalies**: Run `detect_anomalies.py` for statistical anomaly detection and risk assessment
9. **Create Recommendations**: Invoke Claude sub-workflow to generate data-backed actionable suggestions
10. **Generate Report**: Invoke Claude sub-workflow to compile comprehensive markdown report
11. **Complete Session**: Archive results and update workflow execution status

## Error Handling

All workflows handle ambiguous or incomplete requests gracefully:

- **Missing Restaurant ID**: "Which restaurant would you like me to analyze?"
- **Invalid Restaurant ID**: "I couldn't find restaurant R999. Available restaurants are: R001, R002, R003..."
- **Incomplete Data**: "Analysis completed with available data. Missing: recent ad campaign data"

## Performance Targets

- **Complete Analysis**: < 120 seconds per restaurant (with full session management)
- **Data Collection**: < 15 seconds per restaurant (Python script)
- **Trend Analysis**: < 20 seconds per restaurant (Python script)
- **Anomaly Detection**: < 10 seconds per restaurant (Python script)
- **Claude Sub-workflows**: < 30 seconds each (ad evaluation, peer insights, recommendations, reporting)

## Dependencies

### Core Dependencies
- SQLite database with restaurant data (`swiggy_dineout.db`)
- Python environment managed by `uv` with `pyproject.toml`
- Mock data generation utilities (`init_database.py`)

### Python Packages (via uv)
- `numpy`, `pandas`, `scipy` for statistical analysis
- `sqlite3` for database operations
- `json` for artifact management
- `argparse` for script parameter handling

### Required Tools
- `tools/initialize_session.py` - Session initialization and artifact structure setup
- `tools/collect_restaurant_data.py` - Database querying and data collection
- `tools/analyze_performance_trends.py` - Statistical trend analysis
- `tools/detect_anomalies.py` - Anomaly detection and risk assessment

### Claude Sub-workflows
- `/evaluate-ad-campaigns` - Marketing analysis workflow
- `/generate-peer-insights` - Competitive analysis workflow
- `/generate-recommendations` - Action planning workflow
- `/generate-restaurant-report` - Report generation workflow

## Available Workflows

### Implemented Workflows
✅ **Master Workflow**: `/generate-restaurant-insights`  
✅ **Data Collection**: `/collect-restaurant-data`  
✅ **Performance Analysis**: `/analyze-performance-trends`  
✅ **Marketing Analysis**: `/evaluate-ad-campaigns`  
✅ **Competitive Analysis**: `/generate-peer-insights`  
✅ **Anomaly Detection**: `/detect-anomalies`  
✅ **Recommendations**: `/generate-recommendations`  
✅ **Report Generation**: `/generate-restaurant-report`  

## Getting Started

1. **Initialize Database**: `python init_database.py`
2. **Run Master Workflow**: `claude -p "/generate-restaurant-insights Generate comprehensive insights for restaurant R001"`
3. **Review Generated Report**: Complete analysis with actionable recommendations

## Complete Example Workflow Execution

```bash
# Execute the master workflow with natural language prompt
claude "/generate-restaurant-insights Generate comprehensive performance insights for restaurant R001"

# The workflow will automatically execute the following steps:

# 1. Dependency Management  
# → uv sync
# → Installs numpy, pandas, scipy from pyproject.toml

# 2. Session Initialization
# → uv run python tools/initialize_session.py R001 --artifacts-dir artifacts
# → Creates session ID: a1b2c3d4
# → Sets up /artifacts/a1b2c3d4/ directory structure

# 3. Data Collection (Python Script)
# → uv run python tools/collect_restaurant_data.py R001 a1b2c3d4 --artifacts-dir artifacts
# → Queries database and creates restaurant_data.json, peer_benchmarks.json, ads_data.json

# 4. Performance Analysis (Python Script)  
# → uv run python tools/analyze_performance_trends.py a1b2c3d4 --artifacts-dir artifacts
# → Statistical analysis and creates performance_trends.json

# 5. Ad Campaign Evaluation (Claude Sub-workflow)
# → claude -p "/evaluate-ad-campaigns SESSION_ID=a1b2c3d4 Evaluate ad campaign effectiveness..."
# → Creates ad_evaluation.json

# 6. Peer Benchmarking (Claude Sub-workflow)
# → claude -p "/generate-peer-insights SESSION_ID=a1b2c3d4 Compare restaurant performance..."
# → Creates peer_insights.json

# 7. Anomaly Detection (Python Script)
# → uv run python tools/detect_anomalies.py a1b2c3d4 --artifacts-dir artifacts  
# → Statistical anomaly detection and creates anomalies.json

# 8. Recommendations (Claude Sub-workflow)
# → claude -p "/generate-recommendations SESSION_ID=a1b2c3d4 Generate data-backed recommendations..."
# → Creates recommendations.json

# 9. Final Report (Claude Sub-workflow)
# → claude -p "/generate-restaurant-report SESSION_ID=a1b2c3d4 Create comprehensive markdown report..."
# → Creates restaurant_report.md

# 10. Session Completion
# → Updates workflow_execution.json with completion status
# → Archives session results for audit trail
```

## Expected Output

The system generates a comprehensive restaurant performance report including:

### Executive Summary
- Key performance metrics vs peers
- Top 3 critical insights
- Priority recommendations with timelines
- Overall assessment and trajectory

### Detailed Analysis
- 30-day performance trends
- Ad campaign ROI analysis
- Competitive positioning insights
- Anomaly detection results

### Action Plan
- Prioritized recommendations by impact/effort
- Specific implementation guidance
- Expected outcomes and timelines
- Success metrics for monitoring