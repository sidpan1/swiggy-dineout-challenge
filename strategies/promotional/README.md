# Promotional Strategies

This folder contains promotional strategies for specific campaigns, time-based interventions, and seasonal opportunities.

## Available Strategies

### 🍽️ Lunch Rush (lunch_rush.md)
- **Type**: Time-based traffic boost
- **Target**: Weekday lunch hours (11:30 AM - 2:00 PM)
- **Triggers**: Low occupancy during lunch window
- **Actions**: Discounts, ad boost, proximity notifications

### 🍻 Happy Hour (happy_hour.md)
- **Type**: Afternoon traffic builder
- **Target**: Weekday evenings (4:00 PM - 7:00 PM)
- **Triggers**: Low occupancy in afternoon transition
- **Actions**: Beverage discounts, social media, office worker targeting

### 👨‍👩‍👧‍👦 Weekend Family Special (weekend_family_special.md)
- **Type**: Weekend family attraction
- **Target**: Saturday/Sunday lunch
- **Triggers**: Low weekend bookings by Friday
- **Actions**: Family deals, entertainment, parenting group outreach

### 💕 Date Night Destination (date_night_destination.md)
- **Type**: Romance positioning strategy
- **Target**: Couples on Friday-Saturday evenings
- **Triggers**: >40% bookings are 2-person tables
- **Actions**: Ambiance marketing, couple packages, special occasion focus

## How to Create Promotional Strategies

1. **Identify the Opportunity**
   - Specific time period
   - Target customer segment
   - Clear problem to solve

2. **Define Clear Triggers**
   - Time-based conditions
   - Metric thresholds
   - Environmental factors

3. **Write Natural Language Actions**
   - What you want to happen
   - Specific parameters in plain English
   - Success criteria

4. **Include Safety Measures**
   - Capacity limits
   - Budget caps
   - Rollback conditions

## Template Structure

```markdown
# Strategy Name

## Objective
What problem are we solving?

## Activation Triggers
When should this strategy run?

## Strategy Description
What actions should be taken? (in natural language)

## Success Metrics
How do we measure success?

## Constraints and Safety
What limits should be in place?
```

## Best Practices

1. **Be Specific**: "25% discount on lunch combos" not "offer a discount"
2. **Set Clear Boundaries**: Time limits, budget caps, capacity constraints
3. **Define Success**: Measurable outcomes with timeframes
4. **Plan for Rollback**: What happens if things go wrong?
5. **Consider Context**: Weather, events, competition

## Usage

```bash
# Execute a promotional strategy
claude /project:execute-scheduled-strategy promotional/lunch_rush.md

# Test in dry run mode first
DRY_RUN=1 claude /project:execute-scheduled-strategy promotional/happy_hour.md
```