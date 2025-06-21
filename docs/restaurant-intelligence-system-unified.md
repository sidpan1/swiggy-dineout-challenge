# Restaurant Intelligence System - Unified Architecture

## Natural Language Pipeline with Event-Driven Execution

This document consolidates the restaurant intelligence system that uses Claude Code's natural language processing capabilities with an event-driven, artifact-based pipeline architecture.

---

## System Overview

The system processes natural language strategies through an intelligent pipeline where each step is handled by Claude Code commands that communicate via a shared artifact directory. Strategies can define their own triggers, schedules, and execution logic in plain English.

### Core Architecture

```
Natural Language Strategy (./strategies/*.md)
                    │
                    ▼
    ┌──────────────────────────────┐
    │ Execution Artifact Directory  │
    │ ./artifacts/execution_<ts>/   │
    │                              │
    │ • strategy.md    (original)  │
    │ • parsed.json    (analysis)  │
    │ • conditions.json (decision) │
    │ • actions.json   (plan)      │
    │ • results/       (outcomes)  │
    │ • report.md      (summary)   │
    └──────────────────────────────┘
                    ↕
         Recursive Claude Execution
                    │
    ┌───────────────┴──────────────┐
    │                              │
/project:execute-scheduled-strategy │
    ├── /project:parse-strategy    │
    ├── /project:check-conditions  │
    ├── /project:generate-actions  │
    ├── /project:execute-action    │
    ├── /project:log-execution     │
    └── /project:generate-report   │
```

### File System Structure

```
.claude/commands/           # Natural language command definitions
  ├── README.md            # System documentation
  ├── workflows/           # High-level orchestration commands
  │   ├── execute-scheduled-strategy.md
  │   ├── monitor-active-strategies.md
  │   └── rollback-action.md
  ├── tasks/               # Core pipeline tasks
  │   ├── parse-strategy.md
  │   ├── check-strategy-conditions.md
  │   ├── generate-strategy-actions.md
  │   ├── execute-action.md
  │   ├── log-strategy-execution.md
  │   ├── generate-execution-report.md
  │   └── evaluate-strategy-success.md
  └── actions/             # Specific action implementations
      ├── create-discount.md
      ├── adjust-ad-campaign.md
      └── send-notifications.md

strategies/                # Natural language strategy definitions
  ├── templates/          # Strategy templates
  ├── active/             # Active strategies
  └── archive/            # Historical strategies

artifacts/                 # Pipeline execution artifacts
  └── execution_*/        # Timestamped execution directories
      ├── strategy.md     # Original strategy
      ├── parsed.json     # Parsed structure
      ├── conditions.json # Condition evaluation
      ├── actions.json    # Generated actions
      ├── results/        # Execution results
      └── report.md       # Final report

data/                     # Restaurant data
  ├── restaurants/        # Restaurant profiles
  ├── metrics/            # Performance metrics
  └── reports/            # Generated reports
```

---

## Natural Language Strategy Format

Strategies are written in plain English with optional structured sections for more complex requirements.

### Basic Natural Language Strategy

```markdown
# Weekend Revenue Booster

When weekend dinner bookings drop below 60% capacity, I want to:
- Offer 20% discount on family meal packages
- Increase Instagram ad spend by ₹5000 targeting local families
- Send push notifications highlighting the weekend special

Success: Reach 75% capacity by 8 PM
Rollback: If capacity exceeds 90%, reduce discount to 10%
```

### Advanced Event-Driven Strategy

```markdown
# Flash Sale Responder

## When to trigger
Check every 5 minutes during business hours. Trigger when:
- A competitor launches a discount > 20%
- Our occupancy is below 60%
- It's not already a peak hour

## What to do
1. Match competitor discount + 5% (max 30% total)
2. Send immediate push notifications within 5km
3. Boost social media ads by ₹2000 for next 2 hours

## How to measure success
- Orders increase by 25% within 1 hour
- Occupancy reaches 70% within 90 minutes

## Safety measures
- Maximum 3 flash sales per day
- Automatic rollback if losses exceed ₹10,000
```

---

## Complete Workflow Visualization

### 1. Strategy Creation & Parsing

```
User Input: Natural Language Strategy
            │
            ▼
┌─────────────────────────────────────────┐
│     /project:parse-strategy             │
│                                         │
│  • Reads natural language strategy      │
│  • Extracts triggers and conditions    │
│  • Identifies actions and parameters   │
│  • Detects success metrics             │
│  • Outputs structured JSON             │
└─────────────────────────────────────────┘
            │
            ▼
     artifacts/execution_*/parsed.json
```

### 2. Daily Execution Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    DAILY EXECUTION PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Cron/Scheduler                                                │
│       │                                                         │
│       ▼                                                         │
│  /project:execute-scheduled-strategy                           │
│       │                                                         │
│       ├──► For each active strategy:                           │
│       │    │                                                    │
│       │    ├─1─► /project:check-strategy-conditions            │
│       │    │     Check if triggers are met                     │
│       │    │                                                    │
│       │    ├─2─► /project:generate-strategy-actions            │
│       │    │     Create specific executable actions            │
│       │    │                                                    │
│       │    ├─3─► For each action:                             │
│       │    │     └─► /project:execute-action                  │
│       │    │         Route to appropriate handler              │
│       │    │                                                    │
│       │    ├─4─► /project:log-strategy-execution              │
│       │    │     Record results and metrics                    │
│       │    │                                                    │
│       │    └─5─► /project:generate-execution-report           │
│       │          Create comprehensive summary                   │
│       │                                                         │
│       └──► artifacts/execution_*/report.md                     │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Action Execution Detail

```
┌─────────────────────────────────────────────────────────────────┐
│                    ACTION EXECUTION FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  /project:execute-action                                        │
│       │                                                         │
│       ├─► Read action from artifacts/execution_*/actions.json  │
│       │                                                         │
│       ├─► Route based on action type:                          │
│       │   │                                                     │
│       │   ├─► DISCOUNT:                                        │
│       │   │   └─► /project:actions/create-discount             │
│       │   │                                                     │
│       │   ├─► AD_CAMPAIGN:                                     │
│       │   │   └─► /project:actions/adjust-ad-campaign          │
│       │   │                                                     │
│       │   └─► NOTIFICATION:                                    │
│       │       └─► /project:actions/send-notifications          │
│       │                                                         │
│       └─► Write results to artifacts/execution_*/results/      │
└─────────────────────────────────────────────────────────────────┘
```

### 4. Monitoring & Emergency Response

```
┌─────────────────────────────────────────────────────────────────┐
│                 CONTINUOUS MONITORING LOOP                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  /project:monitor-active-strategies (runs continuously)         │
│       │                                                         │
│       ├─► Check all active strategies                          │
│       │   │                                                     │
│       │   ├─► Event-based triggers (real-time)                 │
│       │   ├─► Schedule-based triggers (cron)                   │
│       │   └─► Condition-based triggers (polling)               │
│       │                                                         │
│       ├─► For triggered strategies:                            │
│       │   └─► /project:execute-scheduled-strategy              │
│       │                                                         │
│       └─► Emergency Detection:                                 │
│           │                                                     │
│           ├─► Revenue drop > 30%                               │
│           ├─► System errors detected                           │
│           └─► Manual emergency trigger                         │
│                   │                                             │
│                   └─► Execute emergency protocols               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Usage Examples

### 1. Create and Execute a Natural Language Strategy

```bash
# Create a strategy in plain English
cat > ./strategies/happy_hour.md << 'EOF'
# Happy Hour Optimizer

Every weekday from 3-6 PM, if the bar area is less than 40% full:
- Create a 30% discount on all beverages
- Post to Instagram with today's special cocktail
- Send notifications to customers who've ordered drinks before

Stop if we hit 80% capacity or 6 PM, whichever comes first.
EOF

# Execute the strategy
claude /project:execute-scheduled-strategy happy_hour.md

# View results
cat ./artifacts/execution_*/report.md
```

### 2. Dry Run Mode

```bash
# Test strategy without executing actions
DRY_RUN=1 claude /project:execute-scheduled-strategy weekend_rush.md

# Review what would have happened
cat ./artifacts/execution_*/actions.json
```

### 3. Manual Pipeline Execution

```bash
# Create execution context
EXEC_DIR="./artifacts/execution_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$EXEC_DIR"

# Copy strategy
cp ./strategies/lunch_special.md "$EXEC_DIR/strategy.md"

# Run pipeline steps individually
claude /project:parse-strategy "$EXEC_DIR"
claude /project:check-strategy-conditions "$EXEC_DIR" 
claude /project:generate-strategy-actions "$EXEC_DIR"
claude /project:execute-action "$EXEC_DIR"
claude /project:generate-execution-report "$EXEC_DIR"
```

### 4. Monitor Active Strategies

```bash
# Start monitoring dashboard
claude /project:monitor-active-strategies

# Check specific strategy status
claude /project:evaluate-strategy-success ./artifacts/execution_*/
```

---

## Command Reference

### Workflow Commands

- **`/project:execute-scheduled-strategy`** - Main orchestrator for strategy execution
  - Input: Strategy filename or path
  - Output: Complete execution artifacts in timestamped directory

- **`/project:monitor-active-strategies`** - Real-time monitoring dashboard
  - Input: None (monitors all active strategies)
  - Output: Live status updates and trigger notifications

- **`/project:rollback-action`** - Intelligent rollback handler
  - Input: Execution directory with failed action
  - Output: Rollback results and recovery status

### Task Commands

- **`/project:parse-strategy`** - Convert natural language to structured format
  - Input: Execution directory with strategy.md
  - Output: parsed.json with extracted components

- **`/project:check-strategy-conditions`** - Evaluate trigger conditions
  - Input: Execution directory with parsed.json
  - Output: conditions.json with true/false evaluation

- **`/project:generate-strategy-actions`** - Create executable action plan
  - Input: Execution directory with conditions.json
  - Output: actions.json with specific parameters

- **`/project:execute-action`** - Route and execute individual actions
  - Input: Execution directory with actions.json
  - Output: Results in results/ subdirectory

- **`/project:log-strategy-execution`** - Record execution details
  - Input: Execution directory with results
  - Output: Structured logs for analysis

- **`/project:generate-execution-report`** - Create human-readable summary
  - Input: Complete execution directory
  - Output: report.md with full execution details

- **`/project:evaluate-strategy-success`** - Measure strategy effectiveness
  - Input: Execution directory with results
  - Output: Success metrics and recommendations

### Action Commands

- **`/project:actions/create-discount`** - Create discount campaigns
- **`/project:actions/adjust-ad-campaign`** - Modify advertising parameters  
- **`/project:actions/send-notifications`** - Send targeted notifications

---

## Advanced Features

### Event-Driven Triggers

Strategies can specify complex trigger conditions in natural language:

```markdown
# Smart Pricing Strategy

Activate when ALL of these are true:
- It's a weekday lunch hour (11:30 AM - 2:30 PM)
- Occupancy is below 50%  
- At least 2 competitors within 1km have active discounts
- Weather is good (not raining)

But NOT when:
- There's a local event bringing crowds
- We already ran a promotion today
- Kitchen staff is below minimum levels
```

### Multi-Stage Actions

Complex strategies can define sequential actions:

```markdown
# Gradual Capacity Builder

Stage 1 (Immediate):
- 10% discount on appetizers
- Boost social media presence

Stage 2 (After 30 minutes if < 60% full):
- Increase to 15% discount
- Add main courses to promotion
- Send push notifications

Stage 3 (After 1 hour if still < 60%):
- 20% discount on full meals
- Call in additional staff
- Maximum ad spend boost
```

### Conditional Rollbacks

Strategies can include sophisticated rollback logic:

```markdown
# Revenue Protection Strategy

If any of these happen, immediately rollback:
- Kitchen wait time exceeds 30 minutes
- Negative reviews spike by 20%
- Revenue per customer drops below ₹800
- Staff reports system overload

Rollback actions:
- Restore normal pricing
- Pause all advertisements
- Send apology notifications with future discount codes
```

---

## Benefits of This Architecture

1. **Natural Language First**: Non-technical users can create sophisticated strategies
2. **Intelligent Processing**: Claude understands context and intent at each stage
3. **Full Auditability**: Complete execution trace in artifact directories
4. **Modular Design**: Easy to add new commands without changing core system
5. **Event-Driven**: Strategies can respond to real-time events
6. **Safe Execution**: Built-in rollback and safety mechanisms
7. **Scalable**: Handles multiple strategies and restaurants efficiently

---

## Integration Points

The system integrates with restaurant operations through:

- **Data Sources**: POS systems, booking platforms, review sites
- **Action Endpoints**: Discount APIs, ad platforms, notification services  
- **Monitoring**: Real-time metrics, alerts, dashboards
- **Reporting**: Automated reports, success tracking, ROI analysis

---

## Future Enhancements

Potential areas for expansion:

1. **Machine Learning**: Learn from successful strategies to suggest improvements
2. **A/B Testing**: Automatically test strategy variations
3. **Multi-Restaurant**: Coordinate strategies across restaurant chains
4. **Predictive Triggers**: Anticipate issues before they occur
5. **Voice Interface**: Create strategies through voice commands
6. **Mobile App**: Monitor and adjust strategies on the go