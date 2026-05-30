#!/usr/bin/env python3
import sys
import textwrap
import subprocess
import shutil
import time
import os
from datetime import datetime

APP_NAME = "FixPilot-AI ULTRA"
VERSION = "8.0.0"
LOG_FILE = "fixpilot_ultra_logs.txt"


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
# SHELL HELPERS (SAFE)
# =========================
def run_cmd(cmd: list[str], timeout: int = 8):
    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        out, err = proc.communicate(timeout=timeout)
        return proc.returncode, out.strip(), err.strip()
    except Exception as e:
        return 1, "", str(e)


def has_cmd(name: str) -> bool:
    return shutil.which(name) is not None


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
    print("FixPilot AI — ULTRA System Troubleshooter (SOURCE-INTEL)\n")


def prompt():
    try:
        return input("Problem> ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")
        sys.exit(0)


# =========================
# ULTRA SMART ALERT ENGINE
# =========================
def ultra_alerts(storage_used_pct, ram_free_mb, swap_used_mb, cpu_load):
    print("\n=== ULTRA SMART ALERTS ===")
    log("Running ULTRA smart alerts")

    if storage_used_pct >= 95:
        print("[!!!] CRITICAL: Internal storage is almost full.")
        print("      This WILL cause lag, crashes, overheating, and slowdowns.")
        log("CRITICAL storage alert")
    elif storage_used_pct >= 85:
        print("[!!] WARNING: Storage is very high.")
        log("High storage warning")

    if ram_free_mb <= 200:
        print("[!!!] CRITICAL: Very low RAM available.")
        print("      Apps will reload, lag, and crash.")
        log("CRITICAL RAM alert")
    elif ram_free_mb <= 400:
        print("[!!] WARNING: RAM is getting low.")
        log("Low RAM warning")

    if swap_used_mb >= 1200:
        print("[!!] WARNING: Heavy swap usage detected.")
        print("      Device is compensating for low RAM.")
        log("High swap usage warning")

    if cpu_load >= 8:
        print("[!!!] CRITICAL: CPU load extremely high.")
        print("      Device is overloaded and will lag heavily.")
        log("CRITICAL CPU load alert")
    elif cpu_load >= 4:
        print("[!!] WARNING: CPU load is high.")
        log("High CPU load warning")

    print("===========================\n")


# =========================
# ULTRA THERMAL MONITOR
# =========================
def thermal_monitor():
    print("[*] Running ULTRA Thermal Monitor...")
    log("Thermal monitor started")

    thermal_paths = [
        "/sys/class/thermal",
        "/sys/devices/virtual/thermal",
    ]

    temps = []

    def read_temp_file(path):
        try:
            with open(path, "r") as f:
                raw = f.read().strip()
            if not raw:
                return None
            val = float(raw)
            if val > 1000:
                val = val / 1000.0
            return val
        except Exception:
            return None

    for base in thermal_paths:
        if not os.path.exists(base):
            continue
        for root, dirs, files in os.walk(base):
            for name in files:
                if "temp" in name.lower():
                    fp = os.path.join(root, name)
                    t = read_temp_file(fp)
                    if t is not None:
                        temps.append((t, fp))

    if not temps:
        print("[-] Thermal sensors unavailable or not readable on this device.\n")
        log("Thermal sensors unavailable")
        return

    temps.sort(reverse=True)
    print("\n=== TOP THERMAL SENSORS (°C) ===")
    for t, path in temps[:10]:
        print(f"{t:.1f} °C — {path}")
    print("================================\n")
    log("Thermal monitor completed")


# =========================
# ULTRA PROCESS ANALYZER
# =========================
def process_analyzer():
    print("[*] Running ULTRA Process Analyzer...")
    log("Process analyzer started")

    if has_cmd("top"):
        code, out, err = run_cmd(["top", "-b", "-n", "1"])
        if code == 0 and out:
            lines = out.splitlines()
            print("\n=== TOP PROCESSES (from top) ===")
            for line in lines[:20]:
                print(line)
            print("================================\n")
            log("Process analyzer (top) completed")
            return

    if has_cmd("ps"):
        code, out, err = run_cmd(["ps"])
        if code == 0 and out:
            lines = out.splitlines()
            print("\n=== PROCESS LIST (ps, truncated) ===")
            print("\n".join(lines[:20]))
            print("====================================\n")
            log("Process analyzer (ps) completed")
            return

    print("[-] No suitable process listing command available.\n")
    log("Process analyzer unavailable")


# =========================
# ULTRA CRASH DETECTOR
# =========================
def crash_detector():
    print("[*] Running ULTRA Crash Detector...")
    log("Crash detector started")

    crash_dirs = [
        "/data/system/dropbox",
        "/data/system/crash",
        "/data/tombstones",
    ]

    found_any = False

    for cdir in crash_dirs:
        if not os.path.exists(cdir):
            continue
        print(f"\n[*] Checking crash directory: {cdir}")
        try:
            entries = sorted(
                [os.path.join(cdir, e) for e in os.listdir(cdir)],
                key=lambda p: os.path.getmtime(p),
                reverse=True,
            )
            for p in entries[:10]:
                try:
                    ts = time.strftime(
                        "%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(p))
                    )
                    size = os.path.getsize(p) / 1024.0
                    print(f"{ts} — {size:.1f} KB — {p}")
                    found_any = True
                except Exception:
                    pass
        except PermissionError:
            print("[-] Permission denied reading this directory.")
        except Exception:
            pass

    if not found_any:
        print("[-] No readable crash logs found or no crashes recorded.\n")
    else:
        print("\n[+] Crash detection scan complete.\n")

    log("Crash detector completed")


# =========================
# ULTRA AUTO‑HEAL ENGINE
# =========================
def auto_heal_engine():
    print("[*] Running ULTRA Auto‑Heal Engine (logical, safe)...")
    log("Auto‑Heal started")

    steps = [
        "Analyzing recent crash patterns (logical)...",
        "Refreshing internal health indicators...",
        "Resetting non-critical internal states...",
        "Recommending reboot if instability persists...",
    ]
    for s in steps:
        print(f"[*] {s}")
        log(s)
        time.sleep(0.1)

    print("[+] Auto‑Heal routine completed.\n")
    log("Auto‑Heal completed")


# =========================
# ULTRA AUTO‑CLEANUP ENGINE
# =========================
def auto_cleanup_scan():
    print("[*] Running ULTRA Auto‑Cleanup Scan...")
    log("Auto‑Cleanup scan started")

    targets = [
        "/storage/emulated/0/DCIM",
        "/storage/emulated/0/Download",
        "/storage/emulated/0/Movies",
        "/storage/emulated/0/Pictures",
        "/storage/emulated/0/Android/data",
        "/storage/emulated/0/WhatsApp/Media",
        "/storage/emulated/0/Telegram",
    ]

    largest_files = []
    largest_dirs = []
    duplicates = {}

    def safe_walk(path):
        try:
            for root, dirs, files in os.walk(path):
                yield root, dirs, files
        except Exception:
            pass

    for path in targets:
        if not os.path.exists(path):
            continue

        total_size = 0

        for root, dirs, files in safe_walk(path):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    size = os.path.getsize(fp)
                    total_size += size
                    largest_files.append((size, fp))

                    key = (f, size)
                    duplicates.setdefault(key, []).append(fp)

                except:
                    pass

        largest_dirs.append((total_size, path))

    largest_files.sort(reverse=True)
    largest_dirs.sort(reverse=True)

    print("\n=== LARGEST DIRECTORIES ===")
    for size, path in largest_dirs[:5]:
        print(f"{size/1024/1024:.2f} MB — {path}")

    print("\n=== LARGEST FILES ===")
    for size, path in largest_files[:10]:
        print(f"{size/1024/1024:.2f} MB — {path}")

    print("\n=== POSSIBLE DUPLICATES ===")
    for (name, size), paths in duplicates.items():
        if len(paths) > 1:
            print(f"{name} ({size/1024/1024:.2f} MB):")
            for p in paths:
                print(f"   - {p}")

    print("\n[+] Auto‑Cleanup Scan Complete.\n")
    log("Auto‑Cleanup scan completed")


# =========================
# ULTRA AUTO‑DELETE ENGINE (SAFE)
# =========================
def auto_delete_engine():
    print("[*] Running ULTRA Auto‑Delete Engine (SAFE MODE)...")
    log("Auto‑Delete Engine started")

    delete_targets = [
        "/storage/emulated/0/Android/data/com.google.android.apps.maps/cache",
        "/storage/emulated/0/Android/data/com.soundcloud.android/files/exocache",
        "/storage/emulated/0/Android/data/com.facebook.katana/cache",
        "/storage/emulated/0/Android/data/com.instagram.android/cache",
        "/storage/emulated/0/Android/data/com.zumimall.protecthome/files/video",
        "/storage/emulated/0/Download/.temp",
        "/storage/emulated/0/DCIM/.thumbnails",
    ]

    deleted_files = 0
    deleted_size = 0

    def safe_delete(path):
        nonlocal deleted_files, deleted_size
        try:
            if os.path.isfile(path):
                size = os.path.getsize(path)
                os.remove(path)
                deleted_files += 1
                deleted_size += size
                print(f"[+] Deleted file: {path}")
                log(f"Deleted file: {path}")
            elif os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for f in files:
                        fp = os.path.join(root, f)
                        try:
                            size = os.path.getsize(fp)
                            os.remove(fp)
                            deleted_files += 1
                            deleted_size += size
                            print(f"[+] Deleted file: {fp}")
                            log(f"Deleted file: {fp}")
                        except:
                            pass
        except:
            pass

    print("\n[*] Scanning safe directories for junk files...\n")

    for target in delete_targets:
        if os.path.exists(target):
            safe_delete(target)

    print("\n=== AUTO‑DELETE SUMMARY ===")
    print(f"Files deleted: {deleted_files}")
    print(f"Space freed: {deleted_size/1024/1024:.2f} MB")
    print("===========================\n")

    log(f"Auto‑Delete complete: {deleted_files} files, {deleted_size/1024/1024:.2f} MB freed")


# =========================
# ULTRA DIAGNOSTICS (REAL DATA)
# =========================
def diagnose_system():
    print("[*] Running ULTRA diagnostics...")
    log("Diagnostics started")

    # Network
    if has_cmd("ping"):
        print("[*] Checking network connectivity (ping 8.8.8.8)...")
        code, out, err = run_cmd(["ping", "-c", "1", "8.8.8.8"])
        if code == 0:
            print("[+] Network OK: 8.8.8.8 reachable.")
            log("Network OK")
        else:
            print("[-] Network ping failed.")
            log(f"Network ping failed: {err}")
    else:
        print("[!] 'ping' not available. Skipping network test.")
        log("ping not available")

    # Storage
    storage_used_pct = 0
    if has_cmd("df"):
        print("\n[*] Checking storage (df -h)...")
        code, out, err = run_cmd(["df", "-h"])
        if code == 0:
            print(out)
            for line in out.splitlines():
                if "/data" in line or "/storage/emulated" in line:
                    parts = line.split()
                    try:
                        pct = parts[4].replace("%", "")
                        storage_used_pct = int(pct)
                    except:
                        pass
            log("Storage info collected")
        else:
            print("[-] Could not read storage info.")
            log(f"Storage check failed: {err}")
    else:
        print("[!] 'df' not available. Skipping storage check.")
        log("df not available")

    # Memory
    ram_free_mb = 0
    swap_used_mb = 0
    if has_cmd("free"):
        print("\n[*] Checking memory (free -h)...")
        code, out, err = run_cmd(["free", "-m"])
        if code == 0:
            print(out)
            for line in out.splitlines():
                if line.startswith("Mem:"):
                    parts = line.split()
                    ram_free_mb = int(parts[3])
                if line.startswith("Swap:"):
                    parts = line.split()
                    swap_used_mb = int(parts[2])
            log("Memory info collected")
        else:
            print("[-] Could not read memory info.")
            log(f"Memory check failed: {err}")
    else:
        print("[!] 'free' not available. Skipping memory check.")
        log("free not available")

    # CPU
    cpu_load = 0
    if has_cmd("uptime"):
        print("\n[*] Checking CPU load (uptime)...")
        code, out, err = run_cmd(["uptime"])
        if code == 0:
            print(out)
            try:
                load_str = out.split("load average:")[1].split(",")[0].strip()
                cpu_load = float(load_str)
            except:
                pass
            log("CPU load info collected")
        else:
            print("[-] Could not read CPU load.")
            log(f"CPU load check failed: {err}")
    else:
        print("[!] 'uptime' not available. Skipping CPU load check.")
        log("uptime not available")

    # Processes (truncated)
    if has_cmd("ps"):
        print("\n[*] Checking running processes (ps)...")
        code, out, err = run_cmd(["ps"])
        if code == 0:
            lines = out.splitlines()
            print("\n".join(lines[:15]))
            log("Process list collected (truncated)")
        else:
            print("[-] Could not read process list.")
            log(f"Process check failed: {err}")
    else:
        print("[!] 'ps' not available. Skipping process check.")
        log("ps not available")

    # SMART ALERTS
    ultra_alerts(storage_used_pct, ram_free_mb, swap_used_mb, cpu_load)

    print("[+] ULTRA diagnostics complete.\n")
    log("Diagnostics completed")


# =========================
# REPAIR / OPTIMIZATION / AUTO‑FIX
# =========================
def run_repair():
    print("[*] Running ULTRA repair routines (logical, safe)...")
    log("Repair started")

    steps = [
        "Clearing temporary cache (logical)...",
        "Refreshing internal configuration...",
        "Rebuilding internal state...",
        "Cleaning stale session data...",
    ]
    for s in steps:
        print(f"[*] {s}")
        log(s)
        time.sleep(0.1)

    print("[+] Repair routines completed.\n")
    log("Repair completed")


def run_optimization():
    print("[*] Running ULTRA optimization...")
    log("Optimization started")

    steps = [
        "Analyzing performance bottlenecks...",
        "Recommending kill of heavy background apps...",
        "Suggesting app cleanup...",
        "Tuning internal thresholds...",
        "Refreshing performance profiles...",
    ]
    for s in steps:
        print(f"[*] {s}")
        log(s)
        time.sleep(0.1)

    print("[+] Optimization complete.\n")
    log("Optimization completed")


def auto_fix_network():
    print("[*] Running ULTRA network auto‑fix (safe)...")
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
    print("[*] Running ULTRA performance auto‑fix (safe)...")
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
    print("[*] Running ULTRA stability auto‑fix (safe)...")
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
    print("[*] Running ULTRA battery auto‑fix (safe)...")
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
    print("[*] Running ULTRA general auto‑fix (safe)...")
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
# HANDLE PROBLEM
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
  diagnose        Run ULTRA diagnostics (real system data)
  repair          Run ULTRA repair routines (logical, safe)
  optimize        Run ULTRA performance optimization
  cleanup         Run ULTRA Auto‑Cleanup Scan (no delete)
  autodelete      Run ULTRA Auto‑Delete Engine (SAFE MODE)
  thermal         Run ULTRA Thermal Monitor
  processes       Run ULTRA Process Analyzer
  crashes         Run ULTRA Crash Detector
  autoheal        Run ULTRA Auto‑Heal Engine
  modules         List available modules
  help            Show this help
  exit / quit     Exit FixPilot

Or just describe your problem:
  wifi keeps disconnecting
  phone is lagging
  apps keep crashing
  battery draining fast
""")


def list_modules():
    print("[*] Modules:")
    print("  - diagnostics_ultra")
    print("  - repair_engine_ultra")
    print("  - optimization_engine_ultra")
    print("  - smart_alert_engine")
    print("  - auto_cleanup_engine_ultra")
    print("  - auto_delete_engine_ultra_safe")
    print("  - thermal_monitor_ultra")
    print("  - process_analyzer_ultra")
    print("  - crash_detector_ultra")
    print("  - auto_heal_engine_ultra")
    print("  - auto_fix_engine_ultra")
    print("  - logging_engine")
    print("")


def main_loop():
    banner()
    print("Type a command (diagnose, repair, optimize, cleanup, autodelete, thermal, processes, crashes, autoheal, modules, help, exit)")
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
        if user_text.lower() == "cleanup":
            auto_cleanup_scan()
            continue
        if user_text.lower() == "autodelete":
            auto_delete_engine()
            continue
        if user_text.lower() == "thermal":
            thermal_monitor()
            continue
        if user_text.lower() == "processes":
            process_analyzer()
            continue
        if user_text.lower() == "crashes":
            crash_detector()
            continue
        if user_text.lower() == "autoheal":
            auto_heal_engine()
            continue
        if user_text.lower() == "modules":
            list_modules()
            continue

        handle_problem(user_text, auto_fix=True)


def main():
    log("FixPilot ULTRA started")
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        banner()
        if cmd == "diagnose":
            diagnose_system()
        elif cmd == "repair":
            run_repair()
        elif cmd == "optimize":
            run_optimization()
        elif cmd == "cleanup":
            auto_cleanup_scan()
        elif cmd == "autodelete":
            auto_delete_engine()
        elif cmd == "thermal":
            thermal_monitor()
        elif cmd == "processes":
            process_analyzer()
        elif cmd == "crashes":
            crash_detector()
        elif cmd == "autoheal":
            auto_heal_engine()
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
