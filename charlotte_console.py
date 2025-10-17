#!/usr/bin/env python3
"""
Charlotte Control Console - CLI Interface
Bridge Command Hub for automated sports data operations

This script provides a command-line interface to interact with the Charlotte
bridge workflow system.
"""

import sys
import os
import json
import subprocess
from datetime import datetime
from typing import Optional

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CharlotteConsole:
    """Charlotte Control Console - Bridge Command Hub"""
    
    COMMANDS = {
        'nba_pull': {
            'cmd': '/charlotte nba pull',
            'desc': 'Pull latest NBA game data',
            'category': 'Data Pull'
        },
        'mlb_pull': {
            'cmd': '/charlotte mlb pull',
            'desc': 'Pull latest MLB game data and schedules',
            'category': 'Data Pull'
        },
        'nfl_pull': {
            'cmd': '/charlotte nfl pull',
            'desc': 'Pull latest NFL game data',
            'category': 'Data Pull'
        },
        'mlb_sim': {
            'cmd': '/charlotte mlb sim pregame',
            'desc': 'Run MLB pregame simulation with EV edge detection',
            'category': 'Simulation'
        },
        'batch': {
            'cmd': '/charlotte batch starter',
            'desc': 'Generate pregame simulation configuration',
            'category': 'Batch Operations'
        },
        'help': {
            'cmd': '/charlotte help',
            'desc': 'Display all available Charlotte commands',
            'category': 'Utilities'
        },
        'release': {
            'cmd': '/charlotte release',
            'desc': 'Create a stable release tag with timestamp',
            'category': 'Utilities'
        }
    }
    
    def __init__(self):
        self.repo_path = os.path.dirname(os.path.abspath(__file__))
        
    def print_header(self):
        """Print the console header"""
        print(f"\n{Colors.CYAN}{'=' * 70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}🎮 Charlotte Control Console{Colors.ENDC}")
        print(f"{Colors.CYAN}Bridge Command Hub - Automated Sports Data Operations{Colors.ENDC}")
        print(f"{Colors.CYAN}{'=' * 70}{Colors.ENDC}\n")
        
    def print_status(self):
        """Print system status"""
        print(f"{Colors.BOLD}📡 System Status:{Colors.ENDC}")
        print(f"  Workflow: {Colors.GREEN}Charlotte Bridge Active{Colors.ENDC}")
        print(f"  Repository: {Colors.CYAN}DBst-23/DBst-23{Colors.ENDC}")
        print(f"  Time: {Colors.YELLOW}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
        print()
        
    def print_menu(self):
        """Print the interactive menu"""
        print(f"{Colors.BOLD}📋 Available Commands:{Colors.ENDC}\n")
        
        # Group commands by category
        categories = {}
        for key, cmd_info in self.COMMANDS.items():
            cat = cmd_info['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((key, cmd_info))
        
        i = 1
        for category, commands in categories.items():
            print(f"{Colors.BOLD}{Colors.BLUE}{category}:{Colors.ENDC}")
            for key, cmd_info in commands:
                print(f"  {Colors.GREEN}{i}.{Colors.ENDC} {cmd_info['desc']}")
                print(f"     {Colors.YELLOW}{cmd_info['cmd']}{Colors.ENDC}")
                i += 1
            print()
        
        print(f"{Colors.BOLD}{Colors.RED}0. Exit Console{Colors.ENDC}\n")
        
    def execute_command(self, command_key: str):
        """Execute a Charlotte command"""
        if command_key not in self.COMMANDS:
            print(f"{Colors.RED}Error: Unknown command key '{command_key}'{Colors.ENDC}")
            return
        
        cmd_info = self.COMMANDS[command_key]
        command = cmd_info['cmd']
        
        print(f"\n{Colors.CYAN}{'─' * 70}{Colors.ENDC}")
        print(f"{Colors.BOLD}Executing:{Colors.ENDC} {Colors.YELLOW}{command}{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─' * 70}{Colors.ENDC}\n")
        
        # Show information about how the command would be executed
        print(f"{Colors.BOLD}Command Details:{Colors.ENDC}")
        print(f"  Description: {cmd_info['desc']}")
        print(f"  Category: {cmd_info['category']}")
        print(f"  Full Command: {command}")
        print()
        
        print(f"{Colors.YELLOW}ℹ️  To execute this command:{Colors.ENDC}")
        print(f"  1. Post '{command}' as a comment on a GitHub issue")
        print(f"  2. Manually trigger the workflow in GitHub Actions")
        print(f"  3. Use GitHub API with proper authentication")
        print()
        
        # Check if we're in a git repo and show some context
        self.show_git_context()
        
        print(f"{Colors.GREEN}✅ Command prepared successfully{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─' * 70}{Colors.ENDC}\n")
        
    def show_git_context(self):
        """Show git repository context"""
        try:
            # Get current branch
            branch = subprocess.check_output(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                cwd=self.repo_path,
                stderr=subprocess.DEVNULL
            ).decode().strip()
            
            # Get latest commit
            commit = subprocess.check_output(
                ['git', 'log', '-1', '--format=%h - %s'],
                cwd=self.repo_path,
                stderr=subprocess.DEVNULL
            ).decode().strip()
            
            print(f"{Colors.BOLD}Git Context:{Colors.ENDC}")
            print(f"  Branch: {Colors.CYAN}{branch}{Colors.ENDC}")
            print(f"  Latest: {Colors.CYAN}{commit}{Colors.ENDC}")
            print()
        except Exception:
            pass
    
    def show_data_status(self):
        """Show status of data directories"""
        print(f"\n{Colors.BOLD}📊 Data Status:{Colors.ENDC}\n")
        
        data_dirs = {
            'NBA': 'data/raw/nba',
            'MLB': 'data/raw/mlb',
            'NFL': 'data/raw/nfl',
            'Batches': 'data/batches',
            'MLB Sims': 'data/models/mlb/sims'
        }
        
        for name, path in data_dirs.items():
            full_path = os.path.join(self.repo_path, path)
            if os.path.exists(full_path):
                files = [f for f in os.listdir(full_path) if f.endswith('.json')]
                count = len(files)
                status = f"{Colors.GREEN}✓{Colors.ENDC} {count} files"
                
                # Get latest file timestamp if available
                if files:
                    latest = max([os.path.join(full_path, f) for f in files], 
                               key=os.path.getmtime)
                    mtime = datetime.fromtimestamp(os.path.getmtime(latest))
                    status += f" (latest: {Colors.YELLOW}{mtime.strftime('%Y-%m-%d %H:%M')}{Colors.ENDC})"
            else:
                status = f"{Colors.RED}✗{Colors.ENDC} Not found"
            
            print(f"  {name:12} {status}")
        print()
    
    def run_interactive(self):
        """Run the interactive console"""
        self.print_header()
        self.print_status()
        
        while True:
            self.print_menu()
            
            try:
                choice = input(f"{Colors.BOLD}Select command (0-{len(self.COMMANDS)}): {Colors.ENDC}").strip()
                
                if choice == '0':
                    print(f"\n{Colors.CYAN}Goodbye! 👋{Colors.ENDC}\n")
                    break
                
                try:
                    idx = int(choice)
                    if 1 <= idx <= len(self.COMMANDS):
                        command_key = list(self.COMMANDS.keys())[idx - 1]
                        self.execute_command(command_key)
                        
                        # Ask if user wants to continue
                        cont = input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
                    else:
                        print(f"{Colors.RED}Invalid choice. Please select 0-{len(self.COMMANDS)}{Colors.ENDC}\n")
                except ValueError:
                    print(f"{Colors.RED}Invalid input. Please enter a number.{Colors.ENDC}\n")
                    
            except KeyboardInterrupt:
                print(f"\n\n{Colors.CYAN}Goodbye! 👋{Colors.ENDC}\n")
                break
            except EOFError:
                print(f"\n{Colors.CYAN}Goodbye! 👋{Colors.ENDC}\n")
                break
    
    def run_command(self, command_name: str):
        """Run a specific command by name"""
        self.print_header()
        
        # Try to find the command
        for key, cmd_info in self.COMMANDS.items():
            if key == command_name or cmd_info['cmd'] == command_name:
                self.execute_command(key)
                return
        
        print(f"{Colors.RED}Error: Command '{command_name}' not found{Colors.ENDC}\n")
        print(f"{Colors.YELLOW}Available commands:{Colors.ENDC}")
        for key, cmd_info in self.COMMANDS.items():
            print(f"  {key:15} - {cmd_info['desc']}")
        print()


def main():
    """Main entry point"""
    console = CharlotteConsole()
    
    if len(sys.argv) > 1:
        # Non-interactive mode - run specific command
        if sys.argv[1] == 'status':
            console.print_header()
            console.print_status()
            console.show_data_status()
        elif sys.argv[1] == 'list':
            console.print_header()
            print(f"{Colors.BOLD}Available Commands:{Colors.ENDC}\n")
            for key, cmd_info in console.COMMANDS.items():
                print(f"  {key:15} - {cmd_info['desc']}")
                print(f"  {'':15}   {Colors.YELLOW}{cmd_info['cmd']}{Colors.ENDC}")
            print()
        else:
            console.run_command(sys.argv[1])
    else:
        # Interactive mode
        console.run_interactive()


if __name__ == '__main__':
    main()

# ---- quick one-click MLB sim launcher ---------------------------------------
import os, sys, subprocess

def run_mil_at_lad_verify():
    cfg = os.path.join("config", "inputs.sample.json")         # you already edited this
    out = os.path.join("outputs", "verify_MIL_at_LAD")         # results folder
    cmd = [
        sys.executable, os.path.join("sim", "run_sims.py"),
        "--game", "MIL@LAD",
        "--sport", "mlb",
        "--mode", "V001_FULL_GAME_EDGES",
        "--inputs_file", cfg,
        "--freeze_feeds", "true",
        "--sims", "25000",
        "--outputs_dir", out,
        "--explain_inputs",
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    run_mil_at_lad_verify()