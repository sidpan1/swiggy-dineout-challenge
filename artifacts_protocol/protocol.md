# Artifact Management Protocol

## Overview
This protocol defines how Claude workflows manage and share artifacts within a single session to enable seamless context sharing and independent workflow execution.

## Core Principles
- **Single Session**: All sub-workflows share one session directory
- **File-Based**: Artifacts are stored as markdown and JSON files
- **Claude-Managed**: All operations performed via Claude's file tools
- **Context Continuity**: Workflows can build upon previous workflow outputs

## Directory Structure

### Session Directory
```
/artifacts/{session_id}/
├── session_context.json          # Session metadata and configuration
├── workflow_execution.json       # Workflow completion status log
├── error_log.json               # Error and warning tracking
├── restaurant_data.json       # Raw restaurant performance data
├── peer_benchmarks.json       # Peer comparison data
├── ads_data.json             # Advertising campaign data
├── performance_trends.json    # Trend analysis results
├── ad_evaluation.json        # Ad campaign effectiveness analysis
├── peer_insights.json        # Peer benchmarking insights
├── anomalies.json            # Anomaly detection results
├── recommendations.json       # Generated recommendations (detailed)
├── restaurant_report.md       # Restaurant report for sales team
```

## File Naming Conventions

### Data Artifacts (JSON)
- `restaurant_data.json` - Raw restaurant metrics and information
- `peer_benchmarks.json` - Peer comparison baseline data
- `ads_data.json` - Advertising campaign performance data

### Analysis Artifacts (JSON)
- `performance_trends.json` - Trend analysis results
- `ad_evaluation.json` - Ad campaign effectiveness assessment
- `peer_insights.json` - Peer benchmarking analysis
- `anomalies.json` - Anomaly detection findings

### Context Artifacts (JSON)
- `session_context.json` - Session metadata and workflow configuration
- `workflow_execution.json` - Workflow completion status and timing
- `error_log.json` - Error tracking and resolution status

### Output Artifacts (Mixed)
- `recommendations.json` - Structured recommendations data (detailed)
- `restaurant_report.md` - Restaurant report for sales team
