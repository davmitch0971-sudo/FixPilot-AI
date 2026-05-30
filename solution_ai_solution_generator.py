# solution_ai_solution_generator.py

def generate(problem: dict, diagnosis: dict):
    category = problem["category"]
    signals = problem.get("signals", {})

    is_windows = signals.get("mentions_windows")
    is_android = signals.get("mentions_android")

    steps = []
    auto_actions = []
    risk_level = "low"

    # WINDOWS PERFORMANCE
    if category == "performance" and is_windows:
        steps = [
            "Restart the PC.",
            "Check Task Manager for high CPU/RAM usage.",
            "Disable unnecessary startup apps.",
            "Free up disk space.",
        ]
        auto_actions = [
            {"os": "windows", "label": "Clear Temp Files", "command": "del /q/f/s %TEMP%\\*"},
            {"os": "windows", "label": "Run SFC", "command": "sfc /scannow"},
            {"os": "windows", "label": "Repair Windows Image", "command": "DISM /Online /Cleanup-Image /RestoreHealth"},
        ]

    # WINDOWS CRASH
    elif category == "crash" and is_windows:
        steps = [
            "Restart the PC.",
            "Update the app.",
            "Reinstall the app if needed.",
        ]
        auto_actions = [
            {"os": "windows", "label": "Restart Explorer", "command": "taskkill /F /IM explorer.exe && start explorer.exe"},
            {"os": "windows", "label": "Clear Windows Store Cache", "command": "wsreset -i"},
        ]

    # ANDROID CRASH
    elif category == "crash" and is_android:
        steps = [
            "Force stop the app.",
            "Clear cache.",
            "Clear data if needed.",
            "Update the app.",
            "Restart the phone.",
        ]
        auto_actions = []  # Android cannot run shell commands without root

    # ANDROID PERFORMANCE
    elif category == "performance" and is_android:
        steps = [
            "Restart the phone.",
            "Close background apps.",
            "Free up storage.",
            "Disable battery optimization for important apps.",
        ]
        auto_actions = []

    else:
        steps = ["Restart the device.", "Check for updates."]
        auto_actions = []

    return {
        "steps": steps,
        "auto_actions": auto_actions,
        "risk_level": risk_level,
    }
