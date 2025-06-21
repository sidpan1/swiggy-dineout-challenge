# Restaurant Strategy Library

This directory contains natural language strategies for restaurant optimization, organized by strategic approach.

## Folder Structure

### 📊 quadrant-based/
Strategies based on the ARPU-Occupancy classification matrix:

- **premium_star_optimizer.md** - For high ARPU + high occupancy restaurants
- **volume_play_scaling.md** - For high occupancy + low ARPU restaurants  
- **luxury_niche_monetization.md** - For high ARPU + low occupancy restaurants
- **struggling_restaurant_revival.md** - For low ARPU + low occupancy restaurants

### 🔄 lifecycle-management/
Strategies for different stages of restaurant partnership:

- **new_restaurant_accelerator.md** - 90-day launch program for new partners
- **hidden_gem_discovery.md** - Amplification for high-potential but low-visibility restaurants

### 🚨 system-level/
Proactive monitoring and response strategies:

- **anomaly_response_system.md** - Early warning and rapid intervention system
- **competitive_response_protocol.md** - Framework for competitive threats

### 🎯 promotional/
Custom time-based and promotional strategies:

- **lunch_rush.md** - Time-based lunch traffic boost strategy
- **happy_hour.md** - Afternoon traffic building strategy
- **weekend_family_special.md** - Weekend family-focused campaign

## Usage

Each strategy file contains:
1. **Activation Triggers** - When to use this strategy
2. **Strategic Actions** - What to do, written in natural language
3. **Success Metrics** - How to measure effectiveness
4. **Risk Management** - What to watch out for

## Execution

These strategies are designed to work with the natural language pipeline system in `.claude/commands/`. To execute:

```bash
# Execute a strategy
claude /project:execute-scheduled-strategy quadrant-based/premium_star_optimizer.md

# Dry run mode
DRY_RUN=1 claude /project:execute-scheduled-strategy lifecycle-management/new_restaurant_accelerator.md
```

## Adding New Strategies

1. Determine the appropriate category
2. Create a new `.md` file in the relevant folder
3. Follow the natural language format of existing strategies
4. Test with dry run before live execution