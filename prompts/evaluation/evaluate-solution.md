# Evaluate Solution Document: $ARGUMENTS

You are an expert evaluator tasked with systematically assessing a solution document against the Swiggy Dineout Challenge requirements. Follow this structured process to generate a comprehensive evaluation with quantitative scoring.

## Evaluation Process

### Phase 1: Requirements Analysis
1. **Read Project Requirements**
   - Read `docs/problem-statement.md` to understand the business challenge
   - Read `docs/restaurant-performance-agent-prd.md` for technical specifications
   - Extract evaluation rubric and scoring criteria from PRD

2. **Identify Solution Target**
   - Locate the solution document specified in $ARGUMENTS
   - Understand the scope and intended purpose of the solution

### Phase 2: Systematic Assessment
1. **Solution Analysis**
   - Read and analyze the complete solution document
   - Map solution components to PRD requirements
   - Identify implemented features vs missing requirements
   - Assess technical approach and architecture decisions

2. **Rubric Application**
   - Apply each rubric dimension as defined in the PRD
   - Calculate scores based on objective criteria where available
   - Document specific evidence for each scoring decision
   - Consider both technical completeness and practical usability

### Phase 3: Scoring and Documentation
1. **Generate Scores**
   - Calculate overall score (X/100) using PRD weightings
   - Provide detailed breakdown by rubric dimensions
   - Ensure scoring consistency and repeatability

2. **Create Assessment Report**
   - Document 3-5 specific strengths with evidence
   - Identify 3-5 key weaknesses or gaps
   - Provide actionable improvement recommendations
   - Include specific citations from solution document

3. **Save Evaluation Results**
   - Save structured evaluation to artifacts directory as markdown file
   - Save quantitative scores to generic evaluation database using save_score tool
   - Ensure both artifact and database records are created for tracking

## Scoring Framework

Apply the evaluation rubric exactly as defined in the PRD:

### Scoring Principles
- Use objective measurement criteria where available
- Provide evidence-based rationale for all scores
- Flag missing requirements explicitly
- Consider practical business value and usability
- Maintain consistency across evaluations
- Follow the exact rubric dimensions and weightings specified in the PRD

## Artifact Management

### Required Output File
**CRITICAL**: Save evaluation results to the session artifacts directory for tracking and analysis.

**File Location**: `artifacts/{session_id}/evaluation_results.md`

**File Content Template**:
```markdown
# Evaluation Results for Session {SESSION_ID}

## Overall Score: {TOTAL_SCORE}/100

## Scoring Breakdown
{FOR_EACH_RUBRIC_DIMENSION_FROM_PRD}
- **{DIMENSION_NAME}**: {SCORE}/100
  - Rationale: {DETAILED_EXPLANATION}
  - Evidence: {SPECIFIC_CITATIONS}

## Key Findings

### Strengths
1. {SPECIFIC_STRENGTH_WITH_EVIDENCE}
2. {SPECIFIC_STRENGTH_WITH_EVIDENCE}
3. {SPECIFIC_STRENGTH_WITH_EVIDENCE}

### Areas for Improvement
1. {SPECIFIC_WEAKNESS_WITH_EVIDENCE}
2. {SPECIFIC_WEAKNESS_WITH_EVIDENCE}
3. {SPECIFIC_WEAKNESS_WITH_EVIDENCE}

## Actionable Recommendations
1. {SPECIFIC_IMPLEMENTABLE_RECOMMENDATION}
2. {SPECIFIC_IMPLEMENTABLE_RECOMMENDATION}
3. {SPECIFIC_IMPLEMENTABLE_RECOMMENDATION}

## Evidence References
- Section: {SOLUTION_SECTION} - Finding: {ASSESSMENT}
- Section: {SOLUTION_SECTION} - Finding: {ASSESSMENT}
- Section: {SOLUTION_SECTION} - Finding: {ASSESSMENT}

---
Evaluation completed: {TIMESTAMP}
Evaluator: AI Assessment System
```

### Implementation Steps
1. Extract session ID from the provided session context
2. Use the Write tool to create the evaluation file
3. Follow the exact file path format: `artifacts/{session_id}/evaluation_results.md`
4. Replace all template placeholders with actual evaluation data
5. Include specific evidence citations from the solution document

## Generic Evaluation Schema

### Schema Overview
The evaluation system now uses a completely generic database schema that can scale across any workflow type or evaluation rubric:

**Core Table**: `evaluations`
- `evaluation_id`: Primary key
- `session_id`: Links to evaluation session
- `workflow_type`: Generic workflow identifier (e.g., "restaurant-analysis", "code-review", "document-evaluation")
- `evaluation_score`: Final numeric score (0-100)
- `evaluation_rubric`: JSON field containing all rubric dimensions and scores
- `details`: JSON field containing all use-case specific metadata
- `created_at`: Automatic timestamp

### Workflow Types
For different evaluation scenarios, use appropriate workflow_type values:
- **Restaurant Analysis**: `"restaurant-analysis"`
- **Code Review**: `"code-review"`
- **Document Evaluation**: `"document-evaluation"`
- **System Performance**: `"system-performance"`
- **Custom Workflows**: Any descriptive string

### JSON Structure Examples

**evaluation_rubric** field (flexible - any rubric structure):
```json
{
  "data_accuracy": {"score": 82.0, "weight": 0.35},
  "insight_quality": {"score": 85.0, "weight": 0.30},
  "completeness": {"score": 68.0, "weight": 0.20},
  "confidence_calibration": {"score": 75.0, "weight": 0.15}
}
```

**details** field (completely flexible - any use-case data):
```json
{
  "target_entity_id": "R001",
  "solution_path": ".artifacts/acad9e9a", 
  "notes": "Strong analytical depth but missing unified format",
  "strengths": ["Comprehensive data analysis", "Strong ROI quantification"],
  "weaknesses": ["Missing unified briefing format"],
  "recommendations": ["Create integrated executive summary"],
  "custom_field_1": "Any additional data",
  "custom_metrics": {"response_time": 1.2, "accuracy": 0.95}
}
```

**Alternative workflow examples**:
```json
// Code review workflow
{
  "evaluation_rubric": {
    "code_quality": {"score": 90, "weight": 0.4},
    "test_coverage": {"score": 85, "weight": 0.3},
    "documentation": {"score": 70, "weight": 0.3}
  },
  "details": {
    "target_entity_id": "PR-123",
    "repository": "my-repo",
    "files_changed": 15,
    "lines_added": 450
  }
}

// Document evaluation workflow  
{
  "evaluation_rubric": {
    "clarity": {"score": 88, "weight": 0.5},
    "completeness": {"score": 92, "weight": 0.5}
  },
  "details": {
    "target_entity_id": "DOC-456", 
    "document_type": "technical_spec",
    "word_count": 2500
  }
}
```

## Available Tools

### Save Score For Evaluation
Save quantitative results to the generic evaluation database using the new flexible schema:

```bash
# Minimal generic usage - only required fields
uv run tools/evaluation/save_score.py \
  --session-id "{SESSION_ID}" \
  --workflow-type "{WORKFLOW_TYPE}" \
  --score {OVERALL_SCORE}

# Extended usage with individual fields
uv run tools/evaluation/save_score.py \
  --session-id "{SESSION_ID}" \
  --workflow-type "{WORKFLOW_TYPE}" \
  --score {OVERALL_SCORE} \
  --target-entity-id "{TARGET_ENTITY_ID}" \
  --notes "Brief evaluation summary"

# Advanced usage with full JSON structures
uv run tools/evaluation/save_score.py \
  --session-id "acad9e9a" \
  --workflow-type "restaurant-analysis" \
  --score 78.0 \
  --rubric-json '{"data_accuracy":{"score":82,"weight":0.35},"insight_quality":{"score":85,"weight":0.30},"completeness":{"score":68,"weight":0.20},"confidence_calibration":{"score":75,"weight":0.15}}' \
  --details-json '{"target_entity_id":"R001","solution_path":".artifacts/acad9e9a","notes":"Strong analysis but missing unified format","strengths":["Comprehensive analysis"],"weaknesses":["Missing integration"]}'
```

**Key Features of Generic Schema**:
- `--workflow-type`: Generic workflow identifier (required)
- `--score`: Overall evaluation score (required)
- `--rubric-json`: Complete rubric structure as JSON (optional)
- `--details-json`: Complete details/metadata as JSON (optional)
- `--target-entity-id`: Simple entity identifier (optional)
- `--notes`: Simple text notes (optional)
- **Completely flexible**: No hardcoded rubric dimensions - works for any evaluation type

### Trend Analysis
Analyze evaluation patterns and trends using the generic schema:

```bash
# Workflow-specific trends (e.g., restaurant analysis)
uv run tools/evaluation/get_trends.py --workflow-type "restaurant-analysis" --detailed

# Entity-specific trends (e.g., specific restaurant)
uv run tools/evaluation/get_trends.py --target-entity-id {TARGET_ENTITY_ID} --detailed

# System-wide evaluation trends across all workflows
uv run tools/evaluation/get_trends.py --limit 20 --json

# Combined filtering (specific workflow + entity)
uv run tools/evaluation/get_trends.py --workflow-type "restaurant-analysis" --target-entity-id {TARGET_ENTITY_ID}
```

### Database Initialization
Initialize evaluation tracking (run once):

```bash
uv run tools/evaluation/initialize_db.py
```

## Quality Standards

### Consistency Requirements
- Apply scoring criteria uniformly across all evaluations
- Use identical evidence standards for similar assessments
- Maintain objective measurement approach where possible

### Documentation Standards
- Cite specific sections from solution document for all claims
- Provide clear rationale for each scoring decision
- Focus recommendations on practical business value
- Ensure all improvement suggestions are implementable

### Validation Checks
- Verify total score calculation matches dimension scores
- Confirm all required rubric dimensions are assessed
- Validate that recommendations address identified weaknesses
- Ensure evidence citations are accurate and relevant