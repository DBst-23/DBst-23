from rebounds_patch import dynamic_reb_chances, RebConfig

def simulate_calibration(samples=50):
    cfg = RebConfig()
    base_chance = 0.25
    results = []
    for i in range(samples):
        val = dynamic_reb_chances(
            base_chance,
            poss_per_team=94 + (i % 6),
            long_reb_share=0.38,
            foul_gate_on=(i % 2 == 0),
            cfg=cfg
        )
        results.append(val)
    mean_val = sum(results) / len(results)
    median_val = sorted(results)[len(results)//2]
    print(f"Calibration complete: mean={mean_val:.4f}, median={median_val:.4f}, samples={samples}")

if __name__ == "__main__":
    simulate_calibration() 