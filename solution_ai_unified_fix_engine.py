# solution_ai_unified_fix_engine.py

import platform
import subprocess

# ---------------------------------------------------------
# PLATFORM DETECTION
# ---------------------------------------------------------

def detect_platform():
    system = platform.system().lower()

    if "windows" in system:
        return "windows"

    # Android must be passed explicitly by your mobile app
    return "unknown"


# ---------------------------------------------------------
# WINDOWS FIX PACKS (Synced with solution_ai_solution_generator)
# ---------------------------------------------------------

WINDOWS_FIX_PACK = {
    "performance": [
        {
            "label": "Clear Temp Files",
            "command": "del /q/f/s %TEMP%\\*"
        },
        {
            "label": "Run System File Checker",
            "command": "sfc /scannow"
        },
        {
            "label": "Repair Windows Image",
            "command": "DISM /Online /Cleanup-Image /RestoreHealth"
        },
        {
            "label": "Reset Network Stack",
            "command": "ipconfig /flushdns && netsh winsock reset && netsh int ip reset"
        },
        {
            "label": "Open Startup Apps",
            "command": "start ms-settings:startupapps"
        },
    ],

    "crash": [
        {
            "label": "Restart Explorer (fix hung UI)",
            "command": "taskkill /F /IM explorer.exe && start explorer.exe"
        },
        {
            "label": "Clear Windows Store Cache",
            "command": "wsreset -i"
        },
        {
            "label": "Open Apps & Features",
            "command": "start ms-settings:appsfeatures"
        },
    ],

    "network": [
        {
            "label": "Flush DNS + Reset Network Stack",
            "command": "ipconfig /flushdns && netsh winsock reset && netsh int ip reset"
        },
    ],
}


# ---------------------------------------------------------
# ANDROID FIX PACKS (Synced with solution_ai_solution_generator)
# ---------------------------------------------------------

ANDROID_FIX_PACK = {
    "crash": [
        "Force stop the app: Settings → Apps → [App] → Force Stop.",
        "Clear cache: Settings → Apps → [App] → Storage → Clear Cache.",
        "Clear data (if needed): Storage → Clear Data.",
        "Update the app from the Play Store.",
        "Update Google Play Services.",
        "Restart the phone.",
        "Reinstall the app if still crashing.",
    ],

    "performance": [
        "Restart the phone.",
        "Close background apps.",
        "Free up storage: Settings → Storage.",
        "Disable battery optimization for important apps.",
        "Uninstall unused apps.",
        "Update Android OS if available.",
    ]
}


# ---------------------------------------------------------
# WINDOWS COMMAND EXECUTION
# ---------------------------------------------------------

def run_windows_command(cmd):
    try:
        completed = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        return {
            "status": "OK" if completed.returncode == 0 else "ERROR",
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
            "returncode": completed.returncode,
        }
    except Exception as e:
        return {
            "status": "EXCEPTION",
            "error": str(e),
        }


# ---------------------------------------------------------
# UNIFIED FIX ENGINE
# ---------------------------------------------------------

def fix(problem_category, platform_override=None, confirm=False):
    """
    problem_category: "performance", "crash", "network"
    platform_override: "windows" or "android"
    confirm: True = run Windows commands, False = preview only
    """

    platform_name = platform_override or detect_platform()

    # -------------------------
    # WINDOWS
    # -------------------------
    if platform_name == "windows":
        actions = WINDOWS_FIX_PACK.get(problem_category, [])

        if not actions:
            return {
                "platform": "windows",
                "status": "NO_ACTIONS",
                "message": "No fix pack available for this category.",
            }

        if not confirm:
            return {
                "platform": "windows",
                "status": "PENDING_CONFIRMATION",
                "message": f"{len(actions)} auto-fix actions available.",
                "actions": actions,
            }

        # Execute commands
        results = []
        for action in actions:
            result = run_windows_command(action["command"])
            results.append({
                "label": action["label"],
                "command": action["command"],
                "result": result,
            })

        overall = "OK" if all(r["result"]["status"] == "OK" for r in results) else "PARTIAL"

        return {
            "platform": "windows",
            "status": overall,
            "results": results,
        }

    # -------------------------
    # ANDROID
    # -------------------------
    if platform_name == "android":
        steps = ANDROID_FIX_PACK.get(problem_category, [])

        if not steps:
            return {
                "platform": "android",
                "status": "NO_STEPS",
                "message": "No fix pack available for this category.",
            }

        return {
            "platform": "android",
            "status": "GUIDED",
            "steps": steps,
        }

    # -------------------------
    # UNKNOWN PLATFORM
    # -------------------------
    return {
        "platform": "unknown",
        "status": "UNSUPPORTED",
        "message": "Platform not recognized.",
    }
