# Charlotte Bridge Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Charlotte Control Console                    │
│                      (Bridge Command Hub)                        │
└─────────────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
          ┌─────────▼─────────┐     ┌────────▼────────┐
          │  Web Console      │     │  CLI Console    │
          │  (HTML/JS)        │     │  (Python)       │
          └─────────┬─────────┘     └────────┬────────┘
                    │                        │
                    └────────────┬───────────┘
                                 │
                    ┌────────────▼────────────┐
                    │  Command Display        │
                    │  /charlotte [action]    │
                    └────────────┬────────────┘
                                 │
                                 │ User posts command
                                 │ as GitHub comment
                                 │
                    ┌────────────▼─────────────┐
                    │  GitHub Issue Comment    │
                    │  or Workflow Dispatch    │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │  Charlotte Bridge        │
                    │  GitHub Actions          │
                    │  Workflow                │
                    └────────────┬─────────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
    ┌───────────▼──────┐  ┌──────▼──────┐  ┌─────▼────────┐
    │  Data Pulls      │  │ Simulations │  │  Utilities   │
    │  (NBA/MLB/NFL)   │  │  (MLB EV)   │  │ (Batch/Help) │
    └───────────┬──────┘  └──────┬──────┘  └─────┬────────┘
                │                │                │
                └────────────────┼────────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │   Git Commit & Push      │
                    │   Auto-versioned files   │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │  Data Directories        │
                    │  - data/raw/nba/         │
                    │  - data/raw/mlb/         │
                    │  - data/raw/nfl/         │
                    │  - data/models/mlb/sims/ │
                    │  - data/batches/         │
                    └──────────────────────────┘
```

## Command Flow

### Data Pull Flow
```
User clicks "Pull NBA Data" in console
    │
    ▼
Command displayed: /charlotte nba pull
    │
    ▼
User posts comment on GitHub issue
    │
    ▼
GitHub Actions workflow triggered
    │
    ▼
Charlotte bridge "NBA pull" step executes
    │
    ├─► Create data/raw/nba/games_YYYY-MM-DD.json
    │
    ├─► Build data index (freshness map)
    │
    ├─► Validate JSON files
    │
    ├─► Git commit with message
    │
    └─► Push to repository
```

### Simulation Flow
```
User clicks "Run MLB Pregame Simulation"
    │
    ▼
Command displayed: /charlotte mlb sim pregame
    │
    ▼
User posts comment on GitHub issue
    │
    ▼
GitHub Actions workflow triggered
    │
    ▼
Charlotte bridge checks for simulate_ev_edges.py
    │
    ├─► If exists: Run Python simulation script
    │            with data/batches/pregame_sim_config.json
    │
    └─► If not exists: Create stub result JSON
    │
    ▼
Save results to data/models/mlb/sims/sim_YYYY-MM-DD_HHMMSS.json
    │
    ▼
Git commit and push results
```

## Trigger Mechanisms

```
┌────────────────────────────────────────────────┐
│           Charlotte Bridge Triggers            │
└────────────────────────────────────────────────┘

1. Issue Comments
   ─────────────────
   When: Comment contains "/charlotte"
   Who: Only @DBst-23
   What: Executes specific command in comment
   
   Example:
   User posts: "/charlotte nba pull"
   → NBA pull step runs

2. Workflow Dispatch
   ──────────────────
   When: Manual trigger in GitHub Actions UI
   Who: Repository collaborators
   What: Runs all enabled steps
   
   Example:
   User clicks "Run workflow" button
   → All commands execute

3. Scheduled Runs
   ───────────────
   When: Cron schedule (every 12 hours)
   Who: Automated
   What: Routine maintenance and data pulls
   
   Example:
   00:00 UTC and 12:00 UTC daily
   → Automatic data refresh
```

## Component Details

### Web Console (charlotte_console.html)
```
Features:
├── Visual Dashboard
│   ├── Status Panel (workflow, repo, timestamp)
│   ├── Command Buttons (organized by category)
│   ├── Command Log (execution history)
│   └── Reference Documentation
│
├── Styling
│   ├── Gradient backgrounds
│   ├── Responsive grid layout
│   ├── Hover effects and transitions
│   └── Color-coded command categories
│
└── JavaScript
    ├── Command execution handlers
    ├── Real-time timestamp updates
    ├── Console logging
    └── User feedback (alerts)
```

### CLI Console (charlotte_console.py)
```
Features:
├── Interactive Menu
│   ├── Command selection by number
│   ├── Category grouping
│   └── Exit option
│
├── Non-Interactive Modes
│   ├── list - Show all commands
│   ├── status - Show system status
│   └── <command> - Execute specific command
│
├── Status Display
│   ├── Data directory file counts
│   ├── Latest file timestamps
│   └── Git repository context
│
└── Color Coding
    ├── Headers - Cyan
    ├── Success - Green
    ├── Info - Yellow
    └── Errors - Red
```

### Charlotte Bridge Workflow (.github/workflows/charlotte_bridge.yml)
```
Structure:
├── Triggers
│   ├── workflow_dispatch
│   ├── issue_comment (with /charlotte)
│   └── schedule (cron)
│
├── Data Pull Jobs
│   ├── NBA pull → data/raw/nba/
│   ├── MLB pull → data/raw/mlb/
│   └── NFL pull → data/raw/nfl/
│
├── Processing Jobs
│   ├── Data index building
│   ├── MLB pregame simulation
│   └── Batch configuration generation
│
├── Utility Jobs
│   ├── Help display
│   └── Release tagging
│
└── Maintenance Jobs
    ├── JSON validation
    ├── Heartbeat logging
    └── Auto-cleanup
```

## Data Flow

```
External Sources (Future Integration)
        │
        ▼
Charlotte Bridge Workflow
        │
        ├─► Raw Data Storage
        │   └── data/raw/{sport}/
        │       ├── games_*.json
        │       └── schedule_*.json
        │
        ├─► Batch Configs
        │   └── data/batches/
        │       └── pregame_sim_config.json
        │
        ├─► Model Outputs
        │   └── data/models/{sport}/sims/
        │       └── sim_*.json
        │
        └─► System Logs
            └── data/data/logs/
                ├── run_*.log
                └── heartbeat.json
```

## Workflow Permissions

```yaml
permissions:
  contents: write        # Commit and push data
  pull-requests: write   # PR operations
  issues: write          # Respond to commands
```

## Concurrency Control

```yaml
concurrency:
  group: charlotte-bridge
  cancel-in-progress: false
```

This ensures:
- Only one bridge run at a time
- Runs complete fully before next starts
- No data race conditions
- Orderly execution

## Future Enhancements

Possible additions to the Charlotte Control Console:

1. **Real-Time Integration**
   - Direct GitHub API calls
   - OAuth authentication
   - Live workflow status monitoring
   - Real-time log streaming

2. **Data Visualization**
   - Charts showing data freshness
   - Workflow run history graphs
   - Success/failure metrics

3. **Advanced Features**
   - Batch command queuing
   - Scheduled command execution
   - Notification system
   - Custom command builder

4. **Mobile Support**
   - Progressive Web App (PWA)
   - Mobile-optimized layout
   - Push notifications

## Security Notes

Current Implementation:
- Console displays commands only
- No direct workflow execution from console
- Requires GitHub authentication for actual execution
- Limited to repository collaborators

Production Considerations:
- Implement OAuth for GitHub API
- Add rate limiting
- Log all command executions
- Implement audit trail

---

This architecture provides a robust, maintainable system for automated sports data operations through an intuitive command hub interface.
