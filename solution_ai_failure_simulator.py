# ============================================
# AI Failure Simulator Module
# ============================================

import random
import time

STATE = {
    "cycle": 0,
    "failure_events": [],
    "module_health": {},
    "catastrophic_mode": False,
    "catastrophic_timer": 0
}

MODULES = [
    "broken_build_pipelines",
    "api_latency",
    "memory_leaks",
    "api_rate_limiting",
    "saas_churn",
    "security_vulnerabilities",
    "cloud_costs",
    "data_privacy",
    "database_migration",
    "slow_database_queries"
]

def initialize_state():
    if not STATE["module_health"]:
        STATE["module_health"] = {m: random.randint(60, 100) for m in MODULES}

def trigger_catastrophic_failure():
    """Triggers a major system-wide failure event."""
    STATE["catastrophic_mode"] = True
    STATE["catastrophic_timer"] = random.randint(3, 7)

    return "⚠️ CATASTROPHIC FAILURE TRIGGERED — system entering emergency mode."

def apply_catastrophic_damage():
    """Applies heavy damage to all modules during catastrophic mode."""
    events = []
    for m in MODULES:
        dmg = random.randint(10, 25)
        STATE["module_health"][m] = max(0, STATE["module_health"][m] - dmg)
        events.append(f"{m} suffered catastrophic damage (-{dmg}).")
    return events

def run():
    """
    AI Failure Simulator:
      - Random catastrophic failures
      - Cascading damage
      - Emergency mode
      - Recovery after timer expires
    """

    STATE["cycle"] += 1
    initialize_state()

    events = []
    health = STATE["module_health"]

    # 1. Random chance to trigger catastrophic failure
    if not STATE["catastrophic_mode"]:
        if random.random() < 0.10:  # 10% chance per cycle
            events.append(trigger_catastrophic_failure())

    # 2. If in catastrophic mode, apply heavy damage
    if STATE["catastrophic_mode"]:
        events.extend(apply_catastrophic_damage())
        STATE["catastrophic_timer"] -= 1

        if STATE["catastrophic_timer"] <= 0:
            STATE["catastrophic_mode"] = False
            events.append("🟢 System recovered from catastrophic failure.")

    # 3. Normal drift (small damage or healing)
    for m in MODULES:
        drift = random.randint(-3, 3)
        health[m] = max(0, min(100, health[m] + drift))

    STATE["failure_events"].extend(events)

    return {
        "status": "OK" if not STATE["catastrophic_mode"] else "CRITICAL",
        "module": "AI Failure Simulator",
        "cycle": STATE["cycle"],
        "catastrophic_mode": STATE["catastrophic_mode"],
        "module_health": {m: round(h, 2) for m, h in health.items()},
        "events": events,
        "impact": (
            "Simulates catastrophic failures, cascading damage, and emergency recovery. "
            "System now behaves like a real distributed environment under stress."
        )
    }
