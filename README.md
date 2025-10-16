# DBst-23 Sports Data Platform

Automated sports data operations and analytics platform.

## 🎮 Charlotte Control Console

**Bridge Command Hub** - Your centralized interface for automated operations.

The Charlotte Control Console provides an easy-to-use interface for triggering data pulls, simulations, and other automated operations across NBA, MLB, and NFL datasets.

### Quick Start

**Web Console:**
Open `charlotte_console.html` in your browser for a beautiful, interactive dashboard.

**CLI Console:**
```bash
# Interactive mode
python3 charlotte_console.py

# List available commands
python3 charlotte_console.py list

# Check system status
python3 charlotte_console.py status

# Execute specific command
python3 charlotte_console.py nba_pull
```

### Available Commands

- `/charlotte nba pull` - Fetch NBA game data
- `/charlotte mlb pull` - Fetch MLB game data and schedules  
- `/charlotte nfl pull` - Fetch NFL game data
- `/charlotte mlb sim pregame` - Run MLB pregame simulation
- `/charlotte batch starter` - Generate batch configuration
- `/charlotte help` - Show all commands
- `/charlotte release` - Create release tag

📚 See [CHARLOTTE_CONSOLE_README.md](CHARLOTTE_CONSOLE_README.md) for complete documentation.

## Automated Workflows

The Charlotte bridge workflow runs on:
- Issue comments containing `/charlotte` commands
- Manual workflow dispatch
- Scheduled runs every 12 hours

View workflow runs: [Charlotte Bridge Actions](https://github.com/DBst-23/DBst-23/actions/workflows/charlotte_bridge.yml)

---

<!---
DBst-23/DBst-23 is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->
