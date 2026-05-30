# solution_ai_diagnosis_engine.py

def diagnose(problem: dict):
    category = problem["category"]
    text = problem["raw_text"].lower()
    signals = problem.get("signals", {})

    if category == "performance":
        root = "High CPU/RAM usage, background processes, or low disk space."
        checks = ["CPU usage", "RAM usage", "Disk space", "Startup apps"]
        confidence = 0.75

    elif category == "crash":
        if signals.get("mentions_android"):
            root = "Corrupted app cache/data or outdated Play Services."
        else:
            root = "Application instability or corrupted program files."
        checks = ["App version", "System updates", "Crash logs"]
        confidence = 0.7

    elif category == "network":
        root = "Network stack corruption or DNS issues."
        checks = ["DNS", "Router", "Wi-Fi signal", "Network adapter"]
        confidence = 0.7

    elif category == "boot":
        root = "Startup corruption or driver initialization failure."
        checks = ["Startup Repair", "Safe Mode", "Boot logs"]
        confidence = 0.65

    else:
        root = "General issue — needs more details."
        checks = ["Ask user for more info"]
        confidence = 0.5

    return {
        "root_cause": root,
        "confidence": confidence,
        "checks": checks,
    }
