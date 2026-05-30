# ============================================
# AI Ecosystem Engine
# ============================================

import random
import math

STATE = {
    "cycle": 0,
    "resources": {
        "energy": 1000,
        "bandwidth": 500,
        "stability": 300
    },
    "module_consumption": {},
    "module_efficiency": {},
    "environment_pressure": 0.3,   # 0–1 scale
    "ecosystem_health": 0.6,       # 0–1 scale
    "ecosystem_events": [],
    "resource_regeneration_rate": 1.0
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
    if not STATE["module_consumption"]:
        STATE["module_consumption"] = {
            m: random.uniform(5, 20) for m in MODULES
        }
    if not STATE["module_efficiency"]:
        STATE["module_efficiency"] = {
            m: random.uniform(0.3, 0.9) for m in MODULES
        }

def regenerate_resources():
    """Ecosystem regenerates resources each cycle."""
    regen = STATE["resource_regeneration_rate"]

    STATE["resources"]["energy"] += regen * random.uniform(5, 15)
    STATE["resources"]["bandwidth"] += regen * random.uniform(2, 8)
    STATE["resources"]["stability"] += regen * random.uniform(1, 5)

def apply_environment_pressure():
    """Environmental pressure reduces resources."""
    pressure = STATE["environment_pressure"]

    STATE["resources"]["energy"] -= pressure * random.uniform(10, 30)
    STATE["resources"]["bandwidth"] -= pressure * random.uniform(5, 15)
    STATE["resources"]["stability"] -= pressure * random.uniform(3, 10)

def module_resource_consumption():
    """Modules consume resources based on efficiency."""
    events = []

    for m in MODULES:
        consumption = STATE["module_consumption"][m]
        efficiency = STATE["module_efficiency"][m]

        # Effective cost after efficiency
        cost = consumption * (1 - efficiency)

        STATE["resources"]["energy"] -= cost
        STATE["resources"]["bandwidth"] -= cost * 0.5
        STATE["resources"]["stability"] -= cost * 0.3

        events.append(f"{m} consumed {cost:.1f} resources (efficiency {efficiency:.2f}).")

    return events

def update_ecosystem_health():
    """Ecosystem health depends on resource levels."""
    r = STATE["resources"]

    avg = (
        (r["energy"] / 1000) +
        (r["bandwidth"] / 500) +
        (r["stability"] / 300)
    ) / 3

    STATE["ecosystem_health"] = max(0.0, min(1.0, avg))

def evolve_environment_pressure():
    """Pressure increases when ecosystem is weak."""
    health = STATE["ecosystem_health"]

    if health < 0.4:
        STATE["environment_pressure"] = min(
            1.0, STATE["environment_pressure"] + random.uniform(0.01, 0.05)
        )
    else:
        STATE["environment_pressure"] = max(
            0.0, STATE["environment_pressure"] - random.uniform(0.005, 0.02)
        )

def generate_ecosystem_events():
    """Emergent ecosystem-level events."""
    events = []

    health = STATE["ecosystem_health"]

    if health > 0.75:
        events.append("🟢 Ecosystem flourishing — abundant resources and stability.")
    elif health < 0.3:
        events.append("🔴 Ecosystem collapsing — severe resource scarcity.")
    elif health < 0.5:
        events.append("⚠️ Ecosystem under stress — modules competing for survival.")

    # Rare environmental phenomena
    if random.random() < 0.05:
        rare = random.choice([
            "A resource windfall occurred — sudden abundance.",
            "A stability shock hit the ecosystem.",
            "A bandwidth drought reduced communication efficiency.",
            "A regenerative bloom increased resource growth."
        ])
        events.append(f"⚡ Rare ecosystem event: {rare}")

    return events

def run():
    """
    AI Ecosystem Engine:
      - Manages resource flows
      - Applies environmental pressure
      - Models scarcity and abundance
      - Tracks ecosystem health
      - Generates emergent ecological events
    """

    STATE["cycle"] += 1
    initialize_state()

    regenerate_resources()
    apply_environment_pressure()
    consumption_events = module_resource_consumption()

    update_ecosystem_health()
    evolve_environment_pressure()

    eco_events = generate_ecosystem_events()
    STATE["ecosystem_events"].extend(eco_events)

    return {
        "status": "OK",
        "module": "AI Ecosystem Engine",
        "cycle": STATE["cycle"],
        "resources": {k: round(v, 2) for k, v in STATE["resources"].items()},
        "ecosystem_health": round(STATE["ecosystem_health"], 3),
        "environment_pressure": round(STATE["environment_pressure"], 3),
        "module_efficiency": {m: round(v, 3) for m, v in STATE["module_efficiency"].items()},
        "events": consumption_events + eco_events,
        "impact": (
            "System now simulates a full digital ecosystem with resource flows, "
            "environmental pressure, scarcity, abundance, and emergent ecological behavior."
        )
    }
