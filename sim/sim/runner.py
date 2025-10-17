import json, os, datetime

# Default paths (you can change these or pass as CLI args later)
DEFAULT_CONFIG_PATH = "config/model.defaults.json"
DEFAULT_INPUTS_PATH = "config/inputs.sample.json"
DEFAULT_OUTPUTS_DIR = "outputs/_wire_test"

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def run_simulation():
    # Load configuration and inputs
    config = load_json(DEFAULT_CONFIG_PATH)
    inputs = load_json(DEFAULT_INPUTS_PATH)

    # Sim context summary
    print("Loaded config version:", config.get("version"))
    print("Loaded game:", inputs.get("game"))
    print("Umpire bias:", inputs["context"]["umpire"])
    print("Weather:", inputs["context"]["weather"])

    # Basic mock output (we’ll later replace this with model logic)
    result = {
        "game": inputs["game"],
        "timestamp": datetime.datetime.now().isoformat(),
        "simulated": True,
        "total_runs_pred": 7.6,
        "home_win_prob": 0.57,
        "away_win_prob": 0.43,
        "stabilizer_used": config["stabilizer"]["enabled"]
    }

    # Save results
    save_path = os.path.join(DEFAULT_OUTPUTS_DIR, "full_game_edges.json")
    save_json(result, save_path)
    print(f"✅ Simulation complete. Output saved to {save_path}")

if __name__ == "__main__":
    run_simulation()