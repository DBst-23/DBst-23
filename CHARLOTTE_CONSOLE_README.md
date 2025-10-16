# 🎮 Charlotte Control Console

**Bridge Command Hub** - Centralized interface for automated sports data operations

## Overview

The Charlotte Control Console provides a user-friendly interface to interact with the Charlotte bridge workflow system. It offers both web-based and command-line interfaces for triggering data pulls, simulations, and other automated operations.

## Features

### 🌐 Web Console (`charlotte_console.html`)

A beautiful, interactive web-based dashboard featuring:

- **Visual Command Interface**: Click buttons to execute Charlotte commands
- **Real-time Status Display**: Monitor system status and last update time
- **Command Logging**: Track executed commands with timestamps
- **Quick Actions**: Fast-track common operations
- **Organized Categories**: Commands grouped by function (NBA, MLB, NFL, Batch, Utilities)
- **Command Preview**: See the exact command that will be executed
- **Reference Documentation**: Built-in command reference guide

### 💻 CLI Console (`charlotte_console.py`)

A powerful command-line interface offering:

- **Interactive Menu**: Navigate through available commands
- **Direct Command Execution**: Run specific commands from the terminal
- **Status Monitoring**: View data directory status and git context
- **Color-Coded Output**: Easy-to-read terminal formatting
- **Multiple Modes**: Interactive and non-interactive operation

## Getting Started

### Web Console

1. Open `charlotte_console.html` in your web browser
2. Browse available commands organized by category
3. Click any button to view the command details
4. Use the "View Actions" link to monitor workflow runs in GitHub

### CLI Console

#### Interactive Mode

```bash
python3 charlotte_console.py
```

This launches the interactive menu where you can:
- Select commands by number
- View system status
- Execute Charlotte operations
- Monitor data directories

#### Non-Interactive Mode

**List all commands:**
```bash
python3 charlotte_console.py list
```

**Show system status:**
```bash
python3 charlotte_console.py status
```

**Execute specific command:**
```bash
python3 charlotte_console.py nba_pull
python3 charlotte_console.py mlb_sim
python3 charlotte_console.py batch
```

## Available Commands

### 📊 Data Pull Commands

- **NBA Pull**: `/charlotte nba pull`
  - Fetch latest NBA game data
  - Creates timestamped JSON in `data/raw/nba/`

- **MLB Pull**: `/charlotte mlb pull`
  - Fetch latest MLB game data and schedules
  - Creates timestamped JSON in `data/raw/mlb/`

- **NFL Pull**: `/charlotte nfl pull`
  - Fetch latest NFL game data
  - Creates timestamped JSON in `data/raw/nfl/`

### 🔬 Simulation Commands

- **MLB Pregame Sim**: `/charlotte mlb sim pregame`
  - Run MLB pregame simulation with EV edge detection
  - Results saved to `data/models/mlb/sims/`

### 📦 Batch Operations

- **Batch Starter**: `/charlotte batch starter`
  - Generate pregame simulation configuration
  - Creates `data/batches/pregame_sim_config.json`

### 🔧 Utilities

- **Help**: `/charlotte help`
  - Display all available Charlotte commands in workflow logs

- **Release**: `/charlotte release`
  - Create a stable release tag with timestamp format `vYYYY.MM.DD-HHMM`

## How It Works

The Charlotte Control Console interfaces with the GitHub Actions workflow defined in `.github/workflows/charlotte_bridge.yml`. 

### Execution Methods

1. **Issue Comments**: Post commands as comments on GitHub issues
2. **Workflow Dispatch**: Manually trigger workflows in GitHub Actions UI
3. **GitHub API**: Use authenticated API calls (for advanced integration)

### Automated Features

The Charlotte bridge automatically:
- Builds a data index after pulls (freshness map)
- Validates all JSON files
- Logs heartbeat for maintenance tracking
- Auto-commits results with descriptive messages
- Manages data directories

## Directory Structure

```
data/
├── raw/
│   ├── nba/          # NBA game data
│   ├── mlb/          # MLB game data and schedules
│   ├── nfl/          # NFL game data
│   └── data/
│       └── index.json # Data freshness index
├── batches/          # Batch configuration files
│   └── pregame_sim_config.json
├── models/
│   └── mlb/
│       └── sims/     # MLB simulation results
└── data/
    └── logs/         # Bridge run logs and heartbeat
```

## Workflow Integration

### Triggers

The Charlotte bridge workflow runs on:
- **Manual Dispatch**: Triggered from GitHub Actions UI
- **Issue Comments**: Automatically when comments contain `/charlotte` commands
- **Schedule**: Every 12 hours (00:00, 12:00 UTC)

### Permissions

Required permissions:
- `contents: write` - For committing data
- `pull-requests: write` - For PR operations
- `issues: write` - For responding to commands

### Concurrency

- **Group**: `charlotte-bridge`
- **Cancel in Progress**: `false` (ensures runs complete)

## Example Usage Scenarios

### Scenario 1: Daily Data Pull

```bash
# Morning routine: Pull all league data
python3 charlotte_console.py nba_pull
python3 charlotte_console.py mlb_pull
python3 charlotte_console.py nfl_pull
```

### Scenario 2: Game Day Simulation

```bash
# Pre-game: Pull MLB data and run simulation
python3 charlotte_console.py mlb_pull
# Wait for data pull to complete
python3 charlotte_console.py mlb_sim
```

### Scenario 3: Check System Status

```bash
# View current data state
python3 charlotte_console.py status
```

### Scenario 4: Batch Processing

```bash
# Generate batch config and run simulation
python3 charlotte_console.py batch
python3 charlotte_console.py mlb_sim
```

## Customization

### Adding New Commands

To add a new Charlotte command:

1. **Update the workflow** (`.github/workflows/charlotte_bridge.yml`):
   - Add new job steps with appropriate conditions

2. **Update the CLI console** (`charlotte_console.py`):
   - Add entry to the `COMMANDS` dictionary

3. **Update the web console** (`charlotte_console.html`):
   - Add new button in appropriate card section
   - Add command preview

## Monitoring & Logs

### GitHub Actions Logs

View detailed execution logs at:
- https://github.com/DBst-23/DBst-23/actions/workflows/charlotte_bridge.yml

### Data Logs

- **Run Logs**: `data/data/logs/run_*.log`
- **Heartbeat**: `data/data/logs/heartbeat.json`

### Command Log

The web console maintains a real-time command log showing:
- Timestamp of execution
- Command name
- Status indicator

## Security Notes

⚠️ **Important**: The console displays command information but does not directly execute workflow runs. To actually trigger workflows, you need:

- GitHub repository access
- Appropriate permissions
- GitHub API token (for programmatic access)

The current implementation is a command reference and preparation tool. For production use with API integration, implement proper authentication and error handling.

## Troubleshooting

### Command Not Executing

**Issue**: Clicking buttons shows info but doesn't run workflow

**Solution**: This is expected behavior. To execute:
1. Copy the displayed command (e.g., `/charlotte nba pull`)
2. Post as a comment on any issue in the repository
3. The workflow will trigger automatically

### Data Not Updating

**Issue**: Data directories show old timestamps

**Solution**: 
1. Check GitHub Actions workflow runs
2. Ensure workflows completed successfully
3. Verify git commits were pushed

### CLI Colors Not Showing

**Issue**: Terminal shows escape codes instead of colors

**Solution**: Ensure your terminal supports ANSI colors. Most modern terminals do by default.

## Contributing

To enhance the Charlotte Control Console:

1. Add new command categories for different sports or operations
2. Implement GitHub API integration for direct execution
3. Add real-time workflow status monitoring
4. Create notification system for completed runs
5. Implement data visualization for pulled data

## License

This console is part of the DBst-23/DBst-23 repository and follows the same license.

## Support

For issues or questions:
- Open an issue in the GitHub repository
- Check workflow logs for execution details
- Review the Charlotte bridge workflow configuration

---

**Built with ❤️ for automated sports data operations**
