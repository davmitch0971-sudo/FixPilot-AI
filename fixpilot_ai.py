# =========================================================
# FixPilot AI — One‑File Troubleshooting Engine
# =========================================================

import platform
import subprocess
import shutil

# =========================================================
# LOGGING
# =========================================================

def log(session: dict, message: str):
    session.setdefault("logs", []).append(message)


# =========================================================
# MEMORY + LEARNING
# =========================================================

CASES = []
HISTORY = []

def store_case(problem, diagnosis, solution, autofix):
    CASES.append({
        "problem": problem,
        "diagnosis": diagnosis,
        "solution": solution,
        "autofix": autofix,
    })
    if len(CASES) > 1000:
        CASES.pop(0)

def recent_cases(n=5):
    return CASES[-n:]

def update_learning(problem, diagnosis, solution, autofix):
    HISTORY.append({
        "problem": problem,
        "diagnosis": diagnosis,
        "solution": solution,
        "autofix": autofix,
    })


# =========================================================
# PERSONALITY / RESPONSE FORMATTER
# =========================================================

def format_response(problem, diagnosis, solution, autofix):
    lines = []
    lines.append("FixPilot AI Analysis:\n")
    lines.append(f"Category: {problem['category']}")
    lines.append(f"Likely cause: {diagnosis['root_cause']} (confidence {diagnosis['confidence']:.2f})\n")

    lines.append("Recommended steps:")
    for i, step in enumerate(solution["steps"], 1):
        lines.append(f"{i}. {step}")

    if autofix:
        lines.append(f"\nAuto‑fix status: {autofix['status']}")

    return "\n".join(lines)


# =========================================================
# PROBLEM CLASSIFIER
# =========================================================

CATEGORIES = {
    "network": ["wifi", "internet", "online", "connection", "latency"],
    "performance": ["slow", "lag", "freeze", "freezing", "stutter", "sluggish", "choppy"],
    "crash": ["crash", "stopped working", "not responding", "closed", "won't open", "wont open", "force close"],
    "boot": ["won't start", "wont start", "boot", "black screen", "no display"],
}

def classify(raw_text: str):
    text = raw_text.lower()

    category = "general"
    for cat, keywords in CATEGORIES.items():
        if any(k in text for k in keywords):
            category = cat
            break

    signals = {
        "mentions_windows": any(w in text for w in ["windows", "pc", "laptop", "desktop"]),
        "mentions_android": any(w in text for w in ["android", "phone", "tablet"]),
        "mentions_ios": any(w in text for w in ["iphone", "ios", "ipad"]),
    }

    return {
        "raw_text": raw_text,
        "category": category,
        "signals": signals,
    }


# =========================================================
# DIAGNOSIS ENGINE
# =========================================================

def diagnose(problem: dict):
    category = problem["category"]
    signals = problem.get("signals", {})

    if category == "performance":
        return {
            "root_cause": "High CPU/RAM usage or low disk space.",
            "confidence": 0.75,
            "checks": ["CPU", "RAM", "Disk", "Startup apps"],
        }

    if category == "crash":
        if signals.get("mentions_android"):
            root = "Corrupted app cache/data or outdated Play Services."
        else:
            root = "Application instability or corrupted program files."
        return {
            "root_cause": root,
            "confidence": 0.7,
            "checks": ["App version", "System updates"],
        }

    if category == "network":
        return {
            "root_cause": "Network stack corruption or DNS issues.",
            "confidence": 0.7,
            "checks": ["DNS", "Router", "Wi‑Fi"],
        }

    if category == "boot":
        return {
            "root_cause": "Startup corruption or driver initialization failure.",
            "confidence": 0.65,
            "checks": ["Startup Repair", "Safe Mode"],
        }

    return {
        "root_cause": "General issue — needs more details.",
        "confidence": 0.5,
        "checks": ["Ask user for more info"],
    }


# =========================================================
# SOLUTION GENERATOR
# =========================================================

def generate_solution(problem: dict, diagnosis: dict):
    category = problem["category"]
    signals = problem.get("signals", {})

    is_windows = signals.get("mentions_windows")
    is_android = signals.get("mentions_android")

    steps = []
    auto_actions = []

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

    # WINDOWS NETWORK
    elif category == "network" and is_windows:
        steps = [
            "Restart router and modem.",
            "Toggle Wi‑Fi off and on.",
            "Forget and reconnect to Wi‑Fi.",
        ]
        auto_actions = [
            {"os": "windows", "label": "Reset Network Stack", "command": "ipconfig /flushdns && netsh winsock reset && netsh int ip reset"},
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

    # ANDROID PERFORMANCE
    elif category == "performance" and is_android:
        steps = [
            "Restart the phone.",
            "Close background apps.",
            "Free up storage.",
            "Disable battery optimization.",
        ]

    else:
        steps = ["Restart the device.", "Check for updates."]

    return {
        "steps": steps,
        "auto_actions": auto_actions,
    }


# =========================================================
# AUTO-FIX ENGINE
# =========================================================

def get_os():
    system = platform.system().lower()
    if "windows" in system:
        return "windows"
    return "unknown"

def run_command(cmd):
    try:
        completed = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=120
        )
        return {
            "status": "OK" if completed.returncode == 0 else "ERROR",
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
    except Exception as e:
        return {"status": "EXCEPTION", "error": str(e)}

def apply_autofix(solution: dict, confirm: bool = False):
    os_name = get_os()
    actions = [a for a in solution["auto_actions"] if a["os"] == os_name]

    if not actions:
        return {"status": "NO_ACTIONS"}

    if not confirm:
        return {"status": "PENDING_CONFIRMATION", "actions": actions}

    results = []
    for action in actions:
        results.append({
            "label": action["label"],
            "command": action["command"],
            "result": run_command(action["command"]),
        })

    return {"status": "OK", "results": results}


# =========================================================
# UNIFIED FIX ENGINE
# =========================================================

WINDOWS_FIX_PACK = {
    "performance": [
        {"label": "Clear Temp Files", "command": "del /q/f/s %TEMP%\\*"},
        {"label": "Run SFC", "command": "sfc /scannow"},
        {"label": "Repair Windows Image", "command": "DISM /Online /Cleanup-Image /RestoreHealth"},
        {"label": "Reset Network Stack", "command": "ipconfig /flushdns && netsh winsock reset && netsh int ip reset"},
    ],
    "crash": [
        {"label": "Restart Explorer", "command": "taskkill /F /IM explorer.exe && start explorer.exe"},
        {"label": "Clear Windows Store Cache", "command": "wsreset -i"},
    ],
    "network": [
        {"label": "Reset Network Stack", "command": "ipconfig /flushdns && netsh winsock reset && netsh int ip reset"},
    ],
}

ANDROID_FIX_PACK = {
    "crash": [
        "Force stop the app.",
        "Clear cache.",
        "Clear data.",
        "Update the app.",
        "Restart the phone.",
    ],
    "performance": [
        "Restart the phone.",
        "Close background apps.",
        "Free up storage.",
        "Disable battery optimization.",
    ]
}

def unified_fix(problem_category, platform_override=None, confirm=False):
    platform_name = platform_override or get_os()

    if platform_name == "windows":
        actions = WINDOWS_FIX_PACK.get(problem_category, [])
        if not confirm:
            return {"status": "PENDING_CONFIRMATION", "actions": actions}

        results = []
        for action in actions:
            results.append({
                "label": action["label"],
                "command": action["command"],
                "result": run_command(action["command"]),
            })
        return {"status": "OK", "results": results}

    if platform_name == "android":
        return {"status": "GUIDED", "steps": ANDROID_FIX_PACK.get(problem_category, [])}

    return {"status": "UNSUPPORTED"}


# =========================================================
# WINDOWS DIAGNOSTIC ENGINE
# =========================================================

def run_diag_cmd(cmd):
    try:
        completed = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=60
        )
        return {
            "status": "OK" if completed.returncode == 0 else "ERROR",
            "stdout": completed.stdout.strip(),
        }
    except Exception as e:
        return {"status": "EXCEPTION", "error": str(e)}

def check_cpu():
    res = run_diag_cmd("wmic cpu get loadpercentage /value")
    load = None
    if "LoadPercentage" in res.get("stdout", ""):
        try:
            load = int(res["stdout"].split("=")[1].strip())
        except:
            pass
    return {"metric": "cpu", "value": load}

def check_ram():
    res = run_diag_cmd("wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /value")
    free = total = None
    for line in res.get("stdout", "").splitlines():
        if "FreePhysicalMemory" in line:
            free = int(line.split("=")[1])
        if "TotalVisibleMemorySize" in line:
            total = int(line.split("=")[1])
    used = None
    if free and total:
        used = round((1 - free / total) * 100, 1)
    return {"metric": "ram", "value": used}

def check_disk():
    total, used, free = shutil.disk_usage("C:\\")
    used_percent = round(used / total * 100, 1)
    return {"metric": "disk", "value": used_percent}

def check_ping():
    res = run_diag_cmd("ping 8.8.8.8 -n 2")
    ok = "TTL=" in res.get("stdout", "")
    return {"metric": "ping", "value": ok}

def check_dns():
    res = run_diag_cmd("nslookup www.google.com")
    ok = "Address:" in res.get("stdout", "")
    return {"metric": "dns", "value": ok}

def run_diagnostics():
    results = [
        check_cpu(),
        check_ram(),
        check_disk(),
        check_ping(),
        check_dns(),
    ]

    summary = []

    if results[0]["value"] and results[0]["value"] > 80:
        summary.append("High CPU usage detected.")
    if results[1]["value"] and results[1]["value"] > 85:
        summary.append("High RAM usage detected.")
    if results[2]["value"] and results[2]["value"] > 90:
        summary.append("Disk almost full.")
    if not results[3]["value"]:
        summary.append("Ping test failed.")
    if not results[4]["value"]:
        summary.append("DNS resolution failed.")

    if not summary:
        summary.append("No major issues detected.")

    return {"summary": summary, "metrics": results}


# =========================================================
# AUTO‑SELECT FIX PACK
# =========================================================

def auto_select_fix_pack(diag):
    text = " ".join(diag["summary"]).lower()
    if "cpu" in text or "ram" in text or "disk" in text:
        return "performance"
    if "ping" in text or "dns" in text:
        return "network"
    return "performance"


# =========================================================
# MAIN LOOP
# =========================================================

def main():
    print("FixPilot AI — System Troubleshooter\n")

    while True:
        user_text = input("Problem> ").strip()
        if user_text.lower() in ("exit", "quit"):
            break

        result = handle_problem(user_text, auto_fix=True, auto_fix_confirm=False)

        print("\n--- FixPilot AI Report ---")
        print(result["response_text"])

        # Classic auto‑fix
        if result["autofix"] and result["autofix"]["status"] == "PENDING_CONFIRMATION":
            actions = result["autofix"]["actions"]
            print("\nAuto‑fix actions available:")
            for i, a in enumerate(actions, 1):
                print(f"{i}. {a['label']} -> {a['command']}")
            if input("Run them? (yes/no) ").lower() == "yes":
                result = handle_problem(user_text, auto_fix=True, auto_fix_confirm=True)
                print("\nAuto‑fix complete.")

        # Diagnostics
        if input("\nRun Windows diagnostics? (yes/no) ").lower() == "yes":
            diag = run_diagnostics()
            print("\nDiagnostics Summary:")
            for line in diag["summary"]:
                print("-", line)

            fix_pack = auto_select_fix_pack(diag)
            print(f"\nFixPilot AI recommends: {fix_pack.upper()} fix pack")

            uf = unified_fix(fix_pack, platform_override="windows", confirm=False)
            print("\nActions:")
            for a in uf["actions"]:
                print("-", a["label"])

            if input("Run recommended fix pack? (yes/no) ").lower() == "yes":
                uf = unified_fix(fix_pack, platform_override="windows", confirm=True)
                print("\nFix pack executed.")

        print("\n-----------------------------\n")


if __name__ == "__main__":
    main()
