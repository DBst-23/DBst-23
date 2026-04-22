from modules.liveflow_middle_band_engine import evaluate_middle_band


def process_liveflow_signal(entry_line, updated_line, current_score, pace_factor, signal):
    middle = evaluate_middle_band(entry_line, updated_line, current_score, pace_factor)

    if middle["middle_active"]:
        signal["middle_band"] = middle

    return signal
