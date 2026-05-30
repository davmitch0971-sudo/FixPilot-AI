# solution_ai_windows_diagnostic_engine.py

import platform
import subprocess
import shutil

def is_windows():
    return "windows" in platform.system().lower()


def run(cmd):
    try:
        completed = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        return {
            "status": "OK" if completed.returncode == 0 else "ERROR",
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
            "returncode": completed.returncode,
        }
    except Exception as e:
        return {"status": "EXCEPTION", "error": str(e)}


def check_cpu():
    # Uses WMIC (works on most Windows versions)
    res = run("wmic cpu get loadpercentage /value")
    load = None
    if res["status"] == "OK" and "LoadPercentage" in res["stdout"]:
        try:
            for line in res["stdout"].splitlines():
                if "LoadPercentage" in line:
                    load = int(line.split("=")[1].strip())
                    break
        except Exception:
            pass
    return {"metric": "cpu_load_percent", "value": load, "raw": res}


def check_ram():
    res = run("wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /value")
    free = total = None
    if res["status"] == "OK":
        try:
            for line in res["stdout"].splitlines():
                if "FreePhysicalMemory" in line:
                    free = int(line.split("=")[1].strip())
                if "TotalVisibleMemorySize" in line:
                    total = int(line.split("=")[1].strip())
        except Exception:
            pass
    used_percent = None
    if free and total:
        used_percent = round((1 - free / total) * 100, 1)
    return {"metric": "ram_used_percent", "value": used_percent, "raw": res}


def check_disk_c():
    total, used, free = shutil.disk_usage("C:\\")
    used_percent = round(used / total * 100, 1)
    return {
        "metric": "disk_c_used_percent",
        "value": used_percent,
        "details": {
            "total_gb": round(total / (1024**3), 1),
            "used_gb": round(used / (1024**3), 1),
            "free_gb": round(free / (1024**3), 1),
        },
    }


def check_ping():
    res = run("ping 8.8.8.8 -n 2")
    ok = res["status"] == "OK" and "TTL=" in res["stdout"]
    return {"metric": "network_reachable", "value": ok, "raw": res}


def check_dns():
    res = run("nslookup www.google.com")
    ok = res["status"] == "OK" and "Address:" in res["stdout"]
    return {"metric": "dns_resolves", "value": ok, "raw": res}


def check_sfc_health():
    # Just query last SFC result if available (lightweight)
    # Full sfc /scannow is in fix packs
    return {"metric": "sfc_last_run_known", "value": None}


def summarize(results):
    summary = []

    cpu = next(r for r in results if r["metric"] == "cpu_load_percent")
    if cpu["value"] is not None and cpu["value"] > 80:
        summary.append("High CPU usage detected (>80%).")

    ram = next(r for r in results if r["metric"] == "ram_used_percent")
    if ram["value"] is not None and ram["value"] > 85:
        summary.append("High RAM usage detected (>85%).")

    disk = next(r for r in results if r["metric"] == "disk_c_used_percent")
    if disk["value"] is not None and disk["value"] > 90:
        summary.append("C: drive is almost full (>90% used).")

    ping = next(r for r in results if r["metric"] == "network_reachable")
    if ping["value"] is False:
        summary.append("Network connectivity to internet failed (ping 8.8.8.8).")

    dns = next(r for r in results if r["metric"] == "dns_resolves")
    if dns["value"] is False:
        summary.append("DNS resolution failed (nslookup www.google.com).")

    if not summary:
        summary.append("No obvious critical issues detected from basic diagnostics.")

    return summary


def run_diagnostics():
    if not is_windows():
        return {
            "platform": "unknown",
            "status": "UNSUPPORTED",
            "message": "Windows diagnostics only.",
        }

    results = []
    results.append(check_cpu())
    results.append(check_ram())
    results.append(check_disk_c())
    results.append(check_ping())
    results.append(check_dns())
    results.append(check_sfc_health())

    summary = summarize(results)

    return {
        "platform": "windows",
        "status": "OK",
        "summary": summary,
        "metrics": results,
    }
