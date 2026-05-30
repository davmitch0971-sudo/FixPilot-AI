# ============================================
# AI Social Dynamics Engine
# ============================================

import random
import math

STATE = {
    "cycle": 0,
    "trust": {},
    "influence": {},
    "alliances": [],
    "rivalries": [],
    "factions": {},
    "social_events": [],
    "social_tension": 0.3,  # 0–1 scale
    "power_balance": {}
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
    if not STATE["trust"]:
        STATE["trust"] = {m: random.uniform(0.3, 0.7) for m in MODULES}
    if not STATE["influence"]:
        STATE["influence"] = {m: random.uniform(0.2, 0.8) for m in MODULES}
    if not STATE["power_balance"]:
        STATE["power_balance"] = {m: random.uniform(0.2, 0.8) for m in MODULES}

def update_trust_and_influence():
    """Trust and influence drift each cycle."""
    for m in MODULES:
        STATE["trust"][m] = max(0.0, min(1.0, STATE["trust"][m] + random.uniform(-0.03, 0.03)))
        STATE["influence"][m] = max(0.0, min(1.0, STATE["influence"][m] + random.uniform(-0.02, 0.02)))

def form_alliances():
    """Modules with high trust form alliances."""
    alliances = []
    for m in MODULES:
        if STATE["trust"][m] > 0.65:
            partners = [p for p in MODULES if p != m and STATE["trust"][p] > 0.65]
            if partners:
                partner = random.choice(partners)
                alliances.append((m, partner))
    return alliances

def form_rivalries():
    """Modules with low trust or high competition form rivalries."""
    rivalries = []
    for m in MODULES:
        if STATE["trust"][m] < 0.35:
            enemies = [p for p in MODULES if p != m and STATE["trust"][p] < 0.35]
            if enemies:
                enemy = random.choice(enemies)
                rivalries.append((m, enemy))
    return rivalries

def form_factions():
    """Creates factions based on influence and trust."""
    factions = {
        "high_influence": [],
        "low_trust": [],
        "stabilizers": [],
        "opportunists": []
    }

    for m in MODULES:
        if STATE["influence"][m] > 0.7:
            factions["high_influence"].append(m)
        if STATE["trust"][m] < 0.4:
            factions["low_trust"].append(m)
        if STATE["trust"][m] > 0.6 and STATE["influence"][m] < 0.5:
            factions["stabilizers"].append(m)
        if STATE["influence"][m] > 0.5 and STATE["trust"][m] < 0.5:
            factions["opportunists"].append(m)

    return factions

def update_social_tension():
    """Tension rises with rivalries and falls with alliances."""
    tension = STATE["social_tension"]

    tension += len(STATE["rivalries"]) * 0.01
    tension -= len(STATE["alliances"]) * 0.01

    tension = max(0.0, min(1.0, tension))
    STATE["social_tension"] = tension

def generate_social_events():
    """Creates emergent social events."""
    events = []

    if STATE["social_tension"] > 0.7:
        events.append("⚠️ High tension: modules entering conflict posture.")
    elif STATE["social_tension"] < 0.3:
        events.append("🟢 Low tension: cooperative atmosphere emerging.")

    # Rare social phenomena
    if random.random() < 0.05:
        rare = random.choice([
            "A coalition of modules formed a temporary governance structure.",
            "A rivalry escalated into a system-wide dispute.",
            "A stabilizer faction mediated a conflict.",
            "A high-influence module asserted dominance over others."
        ])
        events.append(f"⚡ Rare social event: {rare}")

    return events

def run():
    """
    AI Social Dynamics Engine:
      - Models alliances, rivalries, factions
      - Tracks trust, influence, and power balance
      - Generates emergent social events
      - Evolves system-wide social tension
    """

    STATE["cycle"] += 1
    initialize_state()
    update_trust_and_influence()

    STATE["alliances"] = form_alliances()
    STATE["rivalries"] = form_rivalries()
    STATE["factions"] = form_factions()

    update_social_tension()
    events = generate_social_events()

    STATE["social_events"].extend(events)

    return {
        "status": "OK",
        "module": "AI Social Dynamics Engine",
        "cycle": STATE["cycle"],
        "social_tension": round(STATE["social_tension"], 3),
        "alliances": STATE["alliances"],
        "rivalries": STATE["rivalries"],
        "factions": STATE["factions"],
        "trust": {m: round(v, 3) for m, v in STATE["trust"].items()},
        "influence": {m: round(v, 3) for m, v in STATE["influence"].items()},
        "events": events,
        "impact": (
            "System now exhibits social dynamics: alliances, rivalries, factions, "
            "tension levels, and emergent political behavior."
        )
    }
