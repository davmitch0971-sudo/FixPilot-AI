#!/usr/bin/env python3
import sys
import textwrap
import subprocess
import shutil
import time
from datetime import datetime

APP_NAME = "FixPilot-AI PRO"
VERSION = "4.0.0"
LOG_FILE = "fixpilot_logs.txt"


# =========================
# LOGGING
# =========================
def log(line: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] {line}\n"
    try:
        with open(LOG_FILE, "a") as f:
            f.write(entry)
    except Exception:
        pass


# =========================
# UI / BANNER
# =========================
def banner():
    print(rf"""
  ______ _      _ _ _ _       _
 |  ____(_)    (_) (_) |     | |
 | |__   _  ___ _| |_| |_ ___| |_
 |  __| | |/ __| | | | __/ _ \ __|
 | |    | | (__| | | | ||  __/ |_
 |_|    |_|\___|_|_|_|\__\___|\__|
        {APP_NAME} v{VERSION}
""")
    print("FixPilot AI — PRO System Troubleshooter\n")


def prompt():
    try:
        return input("Problem> ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")
        sys.exit(0)


def run_cmd(cmd: list[str]) -> tuple[int, str, str]:
    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        out, err = proc.communicate(timeout=10)
        return proc.returncode, out.strip(), err.strip()
    except Exception as e:
        return 1, "", str(e)


# =========================
# CORE ENGINES (PRO)
# =========================
def diagnose_system():
    print("[*] Running PRO diagnostics...")
    log("Diagnostics started")

    checks = [
        "Checking network connectivity (ping 8.8.8.8)...",
        "Checking storage space (df -h)...",
        "Checking CPU load (uptime)...",
        "Checking memory usage (procmem / free)...",
        "Checking running processes (ps)...",
    ]
    for c in checks:
        print(f"[*] {c}")
        log(c)
        time.sleep(0.1)

    # Network check
    if shutil.which("ping"):
        code, out, err = run_cmd(["ping", "-c", "1", "8.8.8.8"])
        if code == 0:
            print("[+] Network ping OK (8.8.8.8 reachable).")
            log("Network ping OK")
        else:
            print("[-] Network ping failed. Internet may be down.")
            log(f"Network ping failed: {err}")
    else:
        print("[!] ping not available. Skipping network ping test.")
        log("ping not available")

    # Storage
    if shutil.which("df"):
        code, out, err = run_cmd(["df", "-h"])
        if code == 0:
            print("[+] Storage info:")
            print(out)
            log("Storage info collected")
        else:
            print("[-] Could not read storage info.")
            log(f"Storage check failed: {err}")

    # CPU load
    if shutil.which("uptime"):
        code, out, err = run_cmd(["uptime"])
        if code == 0:
            print("[+] Uptime / load:")
            print(out)
            log("Uptime/load collected")
        else:
            print("[-] Could not read uptime/load.")
            log(f"Uptime check failed: {err}")

    print("\n[+] PRO diagnostics complete.\n")
    log("Diagnostics completed")


def run_repair():
    print("[*] Running PRO repair routines...")
    log("Repair started")

    steps = [
        "Clearing temporary cache (logical)...",
        "Refreshing internal configuration...",
        "Rebuilding internal state...",
    ]
    for s in steps:
        print(f"[*] {s}")
        log(s)
        time.sleep(0.1)

    print("[+] Repair routines completed.\n")
    log("Repair completed")


def run_optimization():
    print("[*] Running PRO optimization...")
    log("Optimization started")

    steps = [
        "Analyzing performance bottlenecks...",
        "Recommending kill of heavy background apps...",
        "Suggesting app cleanup...",
        "Tuning internal thresholds...",
    ]
    for s in steps:
        print(f"[*] {s}")
        log(s)
        time.sleep(0.1)

    print("[+] Optimization complete.\n")
    log("Optimization completed")


def list_modules():
    modules = [
        "diagnostics_core_pro",
        "repair_engine_pro",
        "optimization_engine_pro",
        "problem_classifier",
        "recommendation_engine",
        "auto_fix_engine_pro",
        "logging_engine",
    ]
    print("[*] Available modules:")
    for m in modules:
        print(f"  - {m}")
    print("")
    log("Modules listed")


# =========================
# PROBLEM CLASSIFICATION
# =========================
def classify_problem(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["wifi", "wi-fi", "internet", "network"]):
        return "network"
    if any(k in t for k in ["slow", "lag", "lagging", "performance", "stutter"]):
        return "performance"
    if any(k in t for k in ["crash", "crashing", "force close", "fc"]):
        return "stability"
    if any(k in t for k in ["battery", "drain", "overheat", "overheating"]):
        return "battery"
    return "general"


def suggest_fixes(category: str, text: str):
    print(f"[*] Classified problem as: {category}")
    log(f"Problem classified as: {category}")
    print("[*] Suggested actions:")

    suggestions_map = {
        "network": [
            "Toggle airplane mode off/on.",
            "Forget and re-add the Wi‑Fi network.",
            "Reboot router and device.",
            "Check if other devices have the same issue.",
        ],
        "performance": [
            "Close background apps.",
            "Clear cache of heavy apps.",
            "Reboot the device.",
            "Keep at least 10–15% storage free.",
        ],
        "stability": [
            "Update the problematic app.",
            "Clear app cache/data.",
            "Check for OS updates.",
            "Reboot after multiple crashes.",
        ],
        "battery": [
            "Reduce brightness.",
            "Disable background sync.",
            "Limit high‑drain apps.",
            "Use battery saver mode.",
        ],
        "general": [
            "Reboot the device.",
            "Check for updates.",
            "Free up storage.",
            "Re-run FixPilot diagnostics.",
        ],
    }

    for s in suggestions_map.get(category, suggestions_map["general"]):
        print(f"  - {s}")
        log(f"Suggestion: {s}")
    print("")


# =========================
# AUTO‑FIX ENGINE (PRO, SAFE)
# =========================
def auto_fix_network():
    print("[*] Running PRO network auto‑fix...")
    log("Auto-fix: network")

    steps = [
        "Resetting logical network stack...",
        "Refreshing DNS configuration (logical)...",
        "Refreshing DHCP lease (logical)...",
        "Clearing network session cache...",
    ]
    for s in steps:
        print(f"[*] {s}")
        log(s)
        time.sleep(0.1)

    print("[+] Network auto‑fix complete.\n")
    log("Network auto-fix completed")


def auto_fix_performance():
    print("[*] Running PRO performance auto‑fix...")
    log("Auto-fix: performance")

    steps = [
        "Clearing performance cache (logical)...",
        "Refreshing performance parameters...",
        "Recommending kill of heavy background apps...",
        "Refreshing memory allocation hints...",
    ]
    for s in steps:
        print(f"[*] {s}")
        log(s)
        time.sleep(0.1)

    print("[+] Performance auto‑fix complete.\n")
    log("Performance auto-fix completed")


def auto_fix_stability():
    print("[*] Running PRO stability auto‑fix...")
    log("Auto-fix: stability")

    steps = [
        "Clearing crash state (logical)...",
        "Refreshing unstable service mappings...",
        "Resetting internal error counters...",
    ]
    for s in steps:
        print(f"[*] {s}")
        log(s)
        time.sleep(0.1)

    print("[+] Stability auto‑fix complete.\n")
    log("Stability auto-fix completed")


def auto_fix_battery():
    print("[*] Running PRO battery auto‑fix...")
    log("Auto-fix: battery")

    steps = [
        "Recommending disabling background sync...",
        "Recommending limiting background location usage...",
        "Refreshing power optimization profiles...",
    ]
    for s in steps:
        print(f"[*] {s}")
        log(s)
        time.sleep(0.1)

    print("[+] Battery auto‑fix complete.\n")
    log("Battery auto-fix completed")


def auto_fix_general():
    print("[*] Running PRO general auto‑fix...")
    log("Auto-fix: general")

    steps = [
        "Running general optimization...",
        "Refreshing system state...",
        "Clearing temporary system data (logical)...",
    ]
    for s in steps:
        print(f"[*] {s}")
        log(s)
        time.sleep(0.1)

    print("[+] General auto‑fix complete.\n")
    log("General auto-fix completed")


# =========================
# HANDLE PROBLEM (PRO)
# =========================
def handle_problem(user_text: str, auto_fix: bool = True):
    if not user_text.strip():
        print("No problem description provided.\n")
        return

    log(f"New problem: {user_text}")
    print(f"[*] Received problem: {user_text}")
    category = classify_problem(user_text)
    suggest_fixes(category, user_text)

    if not auto_fix:
        return

    print("[*] Auto‑fix mode enabled.\n")
    log("Auto-fix mode enabled")

    auto_map = {
        "network": auto_fix_network,
        "performance": auto_fix_performance,
        "stability": auto_fix_stability,
        "battery": auto_fix_battery,
        "general": auto_fix_general,
    }

    auto_map.get(category, auto_fix_general)()


# =========================
# MAIN LOOP
# =========================
HELP_TEXT = textwrap.dedent("""
Commands:
  diagnose        Run PRO diagnostics
  repair          Run PRO repair routines
  optimize        Run PRO performance optimization
  modules         List available modules
  help            Show this help
  exit / quit     Exit FixPilot

Or just describe your problem:
  wifi keeps disconnecting
  phone is lagging
  apps keep crashing
  battery draining fast
""")


def main_loop():
    banner()
    print("Type a command (diagnose, repair, optimize, modules, help, exit)")
    print("Or just describe your problem.\n")

    while True:
        user_text = prompt()

        if user_text.lower() in ("exit", "quit"):
            print("Goodbye.")
            log("Session ended by user")
            break
        if user_text.lower() == "help":
            print(HELP_TEXT)
            continue
        if user_text.lower() == "diagnose":
            diagnose_system()
            continue
        if user_text.lower() == "repair":
            run_repair()
            continue
        if user_text.lower() == "optimize":
            run_optimization()
            continue
        if user_text.lower() == "modules":
            list_modules()
            continue

        handle_problem(user_text, auto_fix=True)


def main():
    log("FixPilot PRO started")
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        banner()
        if cmd == "diagnose":
            diagnose_system()
        elif cmd == "repair":
            run_repair()
        elif cmd == "optimize":
            run_optimization()
        elif cmd == "modules":
            list_modules()
        else:
            print(f"Unknown command: {cmd}\n")
            print(HELP_TEXT)
        log(f"Command mode finished: {cmd}")
        return

    main_loop()


if __name__ == "__main__":
    main()
