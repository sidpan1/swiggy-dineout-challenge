# Generate Restaurant Insights

## Description
Master workflow that generates comprehensive restaurant performance insights for Sales Executives and Account Managers. This workflow orchestrates multiple sub-workflows by invoking Claude recursively to provide actionable insights for restaurant partner management.

## Inputs
Natural language prompt containing restaurant identifier:
- "Generate comprehensive insights for restaurant R001"
- "Analyze Spice Garden restaurant performance" 
- "Create performance report for restaurant R002"

## Workflow Steps

### 1. Install Dependencies
Ensure all required Python dependencies are available:
```bash
uv sync
```

This command:
- Installs all dependencies from `pyproject.toml` including numpy, pandas, scipy
- Sets up the virtual environment for consistent execution
- Ensures reproducible dependency versions across environments

### 2. Initialize Restaurant Analysis Context

Parse the user request to extract restaurant ID and create analysis session:
```bash
uv run python tools/initialize_session.py {restaurant_id} --artifacts-dir artifacts
```

This script automatically:
- Generates unique 8-character session ID
- Creates artifact directory structure: `/artifacts/{session_id}/`
- Creates `session_context.json` with restaurant and workflow metadata
- Initializes `workflow_execution.json` for tracking sub-workflow completion  
- Creates `error_log.json` for error tracking and resolution status
- Sets up shared artifact directory structure per protocol

The script outputs the session ID for use in subsequent workflow steps.

### 3. Collect Restaurant Data
Execute deterministic data collection using Python script:
```bash
uv run python tools/collect_restaurant_data.py {restaurant_id} {session_id} --artifacts-dir artifacts --output-format summary
```

This script automatically:
- Queries all required database tables (restaurant_master, restaurant_metrics, ads_data, peer_benchmarks, discount_history)
- Calculates performance summaries and validates data quality
- Creates artifacts per protocol: `restaurant_data.json`, `peer_benchmarks.json`, `ads_data.json`
- Updates `workflow_execution.json` with completion status
- Handles errors gracefully with structured error responses

### 4. Analyze Performance Trends  
Execute deterministic performance analysis using Python script:
```bash
uv run python tools/analyze_performance_trends.py {session_id} --artifacts-dir artifacts
```

This script automatically:
- Calculates booking, revenue, and rating trends with growth rates
- Identifies day-of-week performance patterns and anomalies  
- Performs statistical analysis (volatility, consistency scores)
- Compares performance against peer benchmarks
- Saves results to `/artifacts/{session_id}/performance_trends.json`

### 5. Evaluate Ad Campaign Effectiveness
Invoke Claude to assess advertising performance using shared artifacts:
```bash
claude -p "/evaluate-ad-campaigns SESSION_ID={session_id} Evaluate ad campaign effectiveness, analyze ROI, and compare against benchmarks for the restaurant." --output-format json --dangerously-skip-permissions
```

### 6. Generate Peer Benchmarking Insights
Invoke Claude to perform competitive analysis using shared artifacts:
```bash
claude -p "/generate-peer-insights SESSION_ID={session_id} Compare restaurant performance against peer benchmarks and identify over/underperforming areas." --output-format json --dangerously-skip-permissions
```

### 7. Detect Performance Anomalies
Execute deterministic anomaly detection using Python script:
```bash
uv run python tools/detect_anomalies.py {session_id} --artifacts-dir artifacts
```

This script automatically:
- Performs statistical anomaly detection using Z-scores and pattern analysis
- Identifies operational anomalies (cancellation spikes, rating drops, spend patterns)
- Detects trend-based anomalies (negative growth, high volatility)
- Analyzes competitive positioning vs peer benchmarks
- Categorizes anomalies by severity (critical/high/medium/low) with risk assessment
- Saves results to `/artifacts/{session_id}/anomalies.json`

### 8. Create Actionable Recommendations
Invoke Claude to generate improvement suggestions using all shared artifacts:
```bash
claude -p "/generate-recommendations SESSION_ID={session_id} Generate data-backed actionable recommendations combining performance analysis, ad effectiveness, peer comparisons, and anomaly findings." --output-format json --dangerously-skip-permissions
```

### 9. Generate Final Report
Invoke Claude to compile comprehensive report using all shared artifacts:
```bash
claude -p "/generate-restaurant-report SESSION_ID={session_id} Create comprehensive markdown report combining all insights and recommendations for Sales Executive review." --output-format json --dangerously-skip-permissions
```

### 10. Complete Session and Archive
Complete the analysis session and prepare for archival:
- Mark session as completed in `workflow_execution.json`
- Validate all required artifacts were generated successfully per protocol
- Update `session_context.json` with completion status and session summary
- Log any errors or warnings in `error_log.json`
- Archive session directory if configured for long-term storage

## Artifacts Generated
After all sub-workflows complete, the following artifacts are available in `/artifacts/{session_id}/`:

### Core Data Files
- `restaurant_data.json` - Complete restaurant performance data and metrics
- `peer_benchmarks.json` - Peer comparison baseline data  
- `ads_data.json` - Advertising campaign performance data

### Analysis Files
- `performance_trends.json` - Trend analysis results and patterns
- `ad_evaluation.json` - Ad campaign effectiveness assessment
- `peer_insights.json` - Peer benchmarking analysis
- `anomalies.json` - Anomaly detection findings with severity classification
- `recommendations.json` - Data-backed actionable recommendations

### Reports
- `restaurant_report.md` - Comprehensive markdown report for Sales Executive review

### Session Management
- `workflow_execution.json` - Workflow completion status and timing
- `session_context.json` - Session metadata and configuration
- `error_log.json` - Error tracking and resolution status

## Error Handling

### Invalid Restaurant ID
If restaurant cannot be found:
- List available restaurants with IDs and names
- Suggest corrections for potential typos
- Ask user to clarify which restaurant to analyze

### Sub-workflow Failures
If any invoked workflow fails:
- Continue with remaining analyses where possible
- Document failed components in final report
- Provide partial insights based on successful analyses
- Include error details and suggested remediation

### Data Quality Issues
If data is incomplete or inconsistent:
- Proceed with available data and note limitations
- Identify specific missing data sources
- Provide recommendations despite data gaps
- Suggest data collection improvements

## Success Criteria
- All sub-workflows execute successfully and return results
- Comprehensive analysis completed within 2 minutes
- Final report contains actionable insights and recommendations
- Analysis execution properly logged for audit trail
- Results formatted for immediate Sales Executive use

## Example Execution Flow

**User Input**: "Generate comprehensive insights for restaurant R001"

**Workflow Execution**:
1. Install dependencies → `uv sync` for reproducible environment
2. Parse request → Extract restaurant_id = "R001" and initialize analysis context for R001 (Spice Garden)
3. Execute data collection → Collect metrics, ads, benchmarks using Python script
4. Execute trend analysis → Identify 15% booking increase trend using Python script
5. Invoke ad evaluation → ROI 2.1x vs peer average 2.8x
6. Invoke peer insights → Performing below average in conversion rate
7. Execute anomaly detection → Rating spike detected last week using Python script
8. Invoke recommendations → Suggest ad spend increase of ₹2000
9. Invoke report generation → Create formatted markdown report
10. Complete session → Archive analysis results

**Final Output**: Complete restaurant performance report with executive summary and 4 prioritized recommendations