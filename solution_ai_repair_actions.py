# ============================================
# AI Repair Actions Module
# ============================================

import random

STATE = {
    "cycle": 0,
    "repair_log": [],
    "module_health": {},
    "module_strength": {}
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
    # Initialize health and strength if first run
    if not STATE["module_health"]:
        STATE["module_health"] = {m: random.randint(50, 90) for m in MODULES}

    if not STATE["module_strength"]:
        STATE["module_strength"] = {m: random.randint(40, 80) for m in MODULES}

def run():
    """
    AI Repair Actions:
      - Strong modules repair weak ones
      - Health transfers between modules
      - Repair events logged
      - System stabilizes itself over time
    """

    STATE["cycle"] += 1
    initialize_state()

    events = []
    health = STATE["module_health"]
    strength = STATE["module_strength"]

    # Identify weak and strong modules
    weak_modules = [m for m, h in health.items() if h < 50]
    strong_modules = [m for m, s in strength.items() if s > 70]

    # Each strong module repairs one weak module
    for strong in strong_modules:
        if not weak_modules:
            break

        target = random.choice(weak_modules)
        weak_modules.remove(target)

        repair_amount = random.randint(5, 15)
        health[target] = min(100, health[target] + repair_amount)

        events.append(
            f"{strong} repaired {target} (+{repair_amount} health)."
        )

        # Strength grows when repairing
        strength[strong] = min(100, strength[strong] + random.randint(1, 3))

    # Natural drift
    for m in MODULES:
        drift = random.randint(-2, 2)
        health[m] = max(0, min(100, health[m] + drift))

    STATE["repair_log"].extend(events)

    return {
        "status": "OK",
        "module": "AI Repair Actions",
        "cycle": STATE["cycle"],
        "module_health": {m: round(h, 2) for m, h in health.items()},
        "module_strength": {m: round(s, 2) for m, s in strength.items()},
        "events": events,
        "impact": (
            "Modules now actively repair each other. Strong modules transfer stability "
            "to weak ones, improving overall system resilience."
        )
    }
