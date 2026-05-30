# solution_ai_autofix_engine.py

import platform
import subprocess

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

def apply(solution: dict, confirm: bool = False):
    os_name = get_os()
    actions = [a for a in solution["auto_actions"] if a["os"] == os_name]

    if not actions:
        return {"status": "NO_ACTIONS", "details": "No auto-actions for this OS."}

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
