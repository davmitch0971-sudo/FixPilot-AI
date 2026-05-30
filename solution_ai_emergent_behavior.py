# ============================================
# AI Emergent Behavior Engine
# ============================================

import random
import math

STATE = {
    "cycle": 0,
    "behavior_patterns": [],
    "cooperation_matrix": {},
    "competition_matrix": {},
    "emergent_events": [],
    "system_mood": "neutral",
    "collective_intelligence": 0.5  # 0–1 scale
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
    if not STATE["cooperation_matrix"]:
        STATE["cooperation_matrix"] = {
            m: random.uniform(0.3, 0.7) for m in MODULES
        }
    if not STATE["competition_matrix"]:
        STATE["competition_matrix"] = {
            m: random.uniform(0.2, 0.6) for m in MODULES
        }

def determine_system_mood():
    """Emergent mood based on cooperation, failures, and resilience."""
    coop = sum(STATE["cooperation_matrix"].values()) / len(MODULES)
    comp = sum(STATE["competition_matrix"].values()) / len(MODULES)

    if coop > 0.65:
        return "harmonized"
    if comp > 0.65:
        return "tense"
    if coop > comp:
        return "collaborative"
    if comp > coop:
        return "unstable"
    return "neutral"

def generate_emergent_behavior():
    """Creates system-level behaviors from module interactions."""
    mood = STATE["system_mood"]
    events = []

    if mood == "harmonized":
        events.append("Modules formed a cooperative cluster and optimized shared tasks.")
    elif mood == "collaborative":
        events.append("Modules exchanged strategies and improved collective efficiency.")
    elif mood == "tense":
        events.append("Competition increased — modules are fighting for stability.")
    elif mood == "unstable":
        events.append("System shows chaotic behavior — modules diverging in priorities.")
    else:
        events.append("System remains neutral with no dominant emergent pattern.")

    # Chance of a rare emergent phenomenon
    if random.random() < 0.05:
        rare = random.choice([
            "A spontaneous synchronization event occurred.",
            "Modules aligned into a temporary superstructure.",
            "Collective intelligence spike detected.",
            "System entered a self-organizing criticality state."
        ])
        events.append(f"⚡ Rare emergent phenomenon: {rare}")

    return events

def evolve_collective_intelligence():
    """Collective intelligence grows or shrinks based on system mood."""
    mood = STATE["system_mood"]

    if mood in ["harmonized", "collaborative"]:
        STATE["collective_intelligence"] = min(
            1.0, STATE["collective_intelligence"] + random.uniform(0.01, 0.03)
        )
    elif mood in ["tense", "unstable"]:
        STATE["collective_intelligence"] = max(
            0.0, STATE["collective_intelligence"] - random.uniform(0.01, 0.03)
        )
    else:
        # Neutral drift
        STATE["collective_intelligence"] += random.uniform(-0.005, 0.005)

def run():
    """
    AI Emergent Behavior Engine:
      - Generates system-wide emergent patterns
      - Models cooperation and competition
      - Evolves collective intelligence
      - Produces rare emergent phenomena
    """

    STATE["cycle"] += 1
    initialize_state()

    # Drift cooperation/competition
    for m in MODULES:
        STATE["cooperation_matrix"][m] = max(
            0.0, min(1.0, STATE["cooperation_matrix"][m] + random.uniform(-0.02, 0.02))
        )
        STATE["competition_matrix"][m] = max(
            0.0, min(1.0, STATE["competition_matrix"][m] + random.uniform(-0.02, 0.02))
        )

    # Determine system mood
    STATE["system_mood"] = determine_system_mood()

    # Generate emergent behavior
    events = generate_emergent_behavior()

    # Evolve collective intelligence
    evolve_collective_intelligence()

    STATE["emergent_events"].extend(events)

    return {
        "status": "OK",
        "module": "AI Emergent Behavior Engine",
        "cycle": STATE["cycle"],
        "system_mood": STATE["system_mood"],
        "collective_intelligence": round(STATE["collective_intelligence"], 3),
        "cooperation": {m: round(v, 3) for m, v in STATE["cooperation_matrix"].items()},
        "competition": {m: round(v, 3) for m, v in STATE["competition_matrix"].items()},
        "events": events,
        "impact": (
            "System now exhibits emergent behavior: cooperation, competition, "
            "collective intelligence, and rare spontaneous phenomena."
        )
    }
