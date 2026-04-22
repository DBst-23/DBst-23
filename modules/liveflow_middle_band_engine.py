def evaluate_middle_band(entry_line, updated_line, current_score, pace_factor):
    """
    Detects when a second entry creates a profitable scoring band window.
    """

    band_width = abs(updated_line - entry_line)

    if band_width >= 2.5:
        return {
            "middle_active": True,
            "band_range": (entry_line, updated_line),
            "band_width": band_width,
            "classification": "MIDDLE_CAPTURE_WINDOW"
        }

    return {
        "middle_active": False
    }
