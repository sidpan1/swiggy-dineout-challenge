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
   - Save quantitative scores to evaluation database using save_score tool
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

## Available Tools

### Save Score For Evaluation
Save quantitative results to the evaluation database using the rubric dimensions defined in the PRD:

```bash
uv run tools/evaluation/save_score.py \
  --session-id "{SESSION_ID}" \
  --solution-path "path/to/solution.md" \
  --score {OVERALL_SCORE} \
  --restaurant-id "{RESTAURANT_ID}" \
  {ADD_PARAMETERS_FOR_EACH_PRD_RUBRIC_DIMENSION} \
  --notes "Brief evaluation summary"
```

**Note**: Use the exact parameter names that match the rubric dimensions specified in the PRD.

### Trend Analysis
Analyze evaluation patterns and trends:

```bash
# Restaurant-specific trends
uv run tools/evaluation/get_trends.py --restaurant-id {RESTAURANT_ID} --detailed

# System-wide evaluation trends
uv run tools/evaluation/get_trends.py --limit 20 --json
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