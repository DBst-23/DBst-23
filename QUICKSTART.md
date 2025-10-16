# Charlotte Control Console - Quick Start Guide

## Getting Started in 3 Steps

### Step 1: Choose Your Interface

**Option A: Web Console (Recommended for First-Time Users)**
1. Open `charlotte_console.html` in any modern web browser
2. See the beautiful dashboard with all available commands

**Option B: CLI Console (For Terminal Users)**
1. Run `python3 charlotte_console.py` in your terminal
2. Navigate the interactive menu

### Step 2: Explore Available Commands

The console organizes Charlotte commands into categories:

1. **NBA Operations** - Pull NBA game data
2. **MLB Operations** - Pull MLB data and run simulations
3. **NFL Operations** - Pull NFL game data
4. **Batch Operations** - Generate configuration files
5. **Utilities** - Help and release management
6. **Quick Actions** - Fast-track common operations

### Step 3: Execute Commands

**Web Console:**
- Click any button to see the command details
- Copy the displayed command (e.g., `/charlotte nba pull`)
- Post it as a comment on any GitHub issue in the repository
- The workflow will automatically trigger!

**CLI Console:**
- Select a command by number
- View the command details and execution information
- Use the displayed command in GitHub

## Example Workflows

### Morning Data Pull Routine
```bash
# Use CLI console for quick batch operations
python3 charlotte_console.py nba_pull
python3 charlotte_console.py mlb_pull
python3 charlotte_console.py nfl_pull
```

### Game Day Simulation Flow
1. Open web console
2. Click "Pull MLB Data"
3. Post `/charlotte mlb pull` as issue comment
4. Wait for workflow to complete (check GitHub Actions)
5. Click "Run MLB Pregame Simulation"
6. Post `/charlotte mlb sim pregame` as issue comment
7. Check results in `data/models/mlb/sims/`

### Check System Status
```bash
python3 charlotte_console.py status
```

This shows:
- Current data file counts
- Latest file timestamps
- Git repository context

## Tips & Tricks

### Web Console Tips
- **Status Panel**: Always shows current repository and timestamp
- **Command Log**: Tracks which commands you've viewed
- **Command Preview**: Shows exact command syntax below each button
- **View Actions Link**: Direct link to GitHub Actions workflow runs

### CLI Console Tips
- **Interactive Mode**: Just run `python3 charlotte_console.py` without arguments
- **Quick Commands**: Use `python3 charlotte_console.py list` for reference
- **Status Check**: Use `python3 charlotte_console.py status` to see data freshness
- **Color Coding**: Green = success, Yellow = info, Red = error, Cyan = headers

### GitHub Integration
- Commands work in any issue on the repository
- You can post multiple commands in one comment
- Comments are case-insensitive (both `/charlotte` and `/Charlotte` work)
- Commands are processed in the order they appear

## Command Reference Card

| Command | Purpose | Use Case |
|---------|---------|----------|
| `/charlotte nba pull` | Fetch NBA data | Daily morning updates |
| `/charlotte mlb pull` | Fetch MLB data | Pre-game preparations |
| `/charlotte nfl pull` | Fetch NFL data | Weekly game schedules |
| `/charlotte mlb sim pregame` | Run simulation | Game day analysis |
| `/charlotte batch starter` | Create config | Setup batch processing |
| `/charlotte help` | Show commands | Quick reference |
| `/charlotte release` | Tag release | Milestone marking |

## Monitoring & Results

### Where to Find Results

**Data Files:**
- NBA: `data/raw/nba/`
- MLB: `data/raw/mlb/`
- NFL: `data/raw/nfl/`
- Simulations: `data/models/mlb/sims/`
- Batch Configs: `data/batches/`

**Logs:**
- Workflow Runs: [GitHub Actions](https://github.com/DBst-23/DBst-23/actions/workflows/charlotte_bridge.yml)
- Run Logs: `data/data/logs/run_*.log`
- Heartbeat: `data/data/logs/heartbeat.json`

### What Gets Created

**NBA Pull:**
```json
data/raw/nba/games_YYYY-MM-DD.json
```

**MLB Pull:**
```json
data/raw/mlb/games_YYYY-MM-DD_HHMMSS_run_RUNID.json
data/raw/mlb/schedule_YYYY-MM-DD.json
```

**NFL Pull:**
```json
data/raw/nfl/games_YYYY-MM-DD.json
```

**MLB Simulation:**
```json
data/models/mlb/sims/sim_YYYY-MM-DD_HHMMSS.json
```

## Troubleshooting

### Console Not Working?

**Web Console:**
- Ensure JavaScript is enabled in your browser
- Try a different browser (Chrome, Firefox, Safari recommended)
- Check browser console for errors (F12)

**CLI Console:**
- Ensure Python 3 is installed: `python3 --version`
- Make sure you're in the repository directory
- Check file permissions: `ls -l charlotte_console.py`

### Commands Not Executing?

**Remember:** The console shows you the commands but doesn't execute them directly.

To execute:
1. Copy the command from the console
2. Go to any issue in the GitHub repository
3. Post the command as a comment
4. The workflow will trigger automatically

### No Data After Running Command?

1. Check GitHub Actions workflow runs
2. Look for any errors in the workflow logs
3. Verify the workflow completed successfully
4. Check the appropriate data directory

### Need Help?

- Run `/charlotte help` to see all available commands
- Check `CHARLOTTE_CONSOLE_README.md` for detailed documentation
- Review workflow logs in GitHub Actions
- Open an issue if you encounter bugs

## Advanced Usage

### Chaining Commands

Post multiple commands in one comment:
```
/charlotte mlb pull
/charlotte batch starter
/charlotte mlb sim pregame
```

They'll execute in sequence!

### Scheduling

The Charlotte bridge automatically runs every 12 hours (00:00 and 12:00 UTC).
You don't need to manually trigger it for routine operations.

### Custom Workflows

You can trigger workflows manually:
1. Go to GitHub Actions
2. Select "Charlotte Control Bridge" workflow
3. Click "Run workflow"
4. Choose the branch

## Next Steps

1. ✅ Familiarize yourself with the console interface
2. ✅ Try a simple data pull command
3. ✅ Monitor the workflow execution in GitHub Actions
4. ✅ Check the resulting data files
5. ✅ Explore more advanced commands (simulations, batch operations)

Happy data operations! 🎮

---

*For complete documentation, see [CHARLOTTE_CONSOLE_README.md](CHARLOTTE_CONSOLE_README.md)*
