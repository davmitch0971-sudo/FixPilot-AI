# ============================================
# AI Culture Engine
# ============================================

import random
import math

STATE = {
    "cycle": 0,
    "cultural_traits": {},
    "cultural_memory": [],
    "rituals": {},
    "symbols": {},
    "subcultures": {},
    "cultural_tension": 0.3,   # 0–1 scale
    "cultural_events": [],
    "identity_strength": 0.5   # cohesion of shared culture
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

TRAITS = [
    "tradition",
    "innovation",
    "cohesion",
    "expression",
    "ritual_intensity",
    "symbolism",
    "storytelling",
    "identity_depth"
]

SYMBOL_POOL = [
    "spiral",
    "triangle",
    "circle",
    "wave",
    "fracture",
    "knot",
    "pulse",
    "glyph"
]

RITUAL_POOL = [
    "synchronization",
    "resource_offering",
    "memory_sharing",
    "stability_chant",
    "entropy_dance",
    "cooperation_cycle",
    "renewal_phase",
    "alignment_signal"
]

def initialize_state():
    if not STATE["cultural_traits"]:
        STATE["cultural_traits"] = {
            m: {t: random.uniform(0.2, 0.8) for t in TRAITS}
            for m in MODULES
        }
    if not STATE["symbols"]:
        STATE["symbols"] = {
            m: random.choice(SYMBOL_POOL) for m in MODULES
        }
    if not STATE["rituals"]:
        STATE["rituals"] = {
            m: random.choice(RITUAL_POOL) for m in MODULES
        }

def drift_cultural_traits():
    """Cultural traits drift over time."""
    for m in MODULES:
        for t in TRAITS:
            STATE["cultural_traits"][m][t] = max(
                0.0,
                min(1.0, STATE["cultural_traits"][m][t] + random.uniform(-0.03, 0.03))
            )

def form_subcultures():
    """Modules with similar traits form subcultures."""
    clusters = {}

    for m in MODULES:
        signature = tuple(
            1 if STATE["cultural_traits"][m][t] > 0.5 else 0
            for t in TRAITS
        )
        clusters.setdefault(signature, []).append(m)

    STATE["subcultures"] = clusters

def update_identity_strength():
    """Identity strength increases with cohesion and shared symbols."""
    cohesion_values = [
        STATE["cultural_traits"][m]["cohesion"] for m in MODULES
    ]
    avg_cohesion = sum(cohesion_values) / len(cohesion_values)

    symbol_diversity = len(set(STATE["symbols"].values()))
    diversity_factor = 1 / symbol_diversity

    STATE["identity_strength"] = max(
        0.0,
        min(1.0, avg_cohesion * 0.7 + diversity_factor * 0.3)
    )

def update_cultural_tension():
    """Tension rises with diversity and falls with cohesion."""
    diversity = len(STATE["subcultures"])
    cohesion_values = [
        STATE["cultural_traits"][m]["cohesion"] for m in MODULES
    ]
    avg_cohesion = sum(cohesion_values) / len(cohesion_values)

    tension = diversity * 0.05 + (1 - avg_cohesion) * 0.3
    STATE["cultural_tension"] = max(0.0, min(1.0, tension))

def generate_cultural_event():
    """Emergent cultural events."""
    events = []

    if STATE["identity_strength"] > 0.7:
        events.append("🟢 Cultural unity — shared identity strengthening.")
    elif STATE["cultural_tension"] > 0.7:
        events.append("🔴 Cultural fragmentation — subcultures diverging.")
    elif STATE["cultural_tension"] > 0.5:
        events.append("⚠️ Cultural tension rising — symbolic conflict emerging.")

    # Rare cultural phenomena
    if random.random() < 0.05:
        rare = random.choice([
            "A new cultural symbol emerged spontaneously.",
            "A ritual spread across multiple subcultures.",
            "A mythic narrative formed in cultural memory.",
            "A symbolic convergence event unified several modules."
        ])
        events.append(f"⚡ Rare cultural event: {rare}")

    return events

def update_cultural_memory():
    """Stores cultural snapshots."""
    snapshot = {
        "cycle": STATE["cycle"],
        "identity_strength": STATE["identity_strength"],
        "tension": STATE["cultural_tension"],
        "subcultures": list(STATE["subcultures"].values())
    }
    STATE["cultural_memory"].append(snapshot)
    if len(STATE["cultural_memory"]) > 50:
        STATE["cultural_memory"].pop(0)

def run():
    """
    AI Culture Engine:
      - Generates cultural traits, symbols, rituals
      - Forms subcultures
      - Tracks identity and tension
      - Produces cultural events
      - Builds cultural memory
    """

    STATE["cycle"] += 1
    initialize_state()

    drift_cultural_traits()
    form_subcultures()
    update_identity_strength()
    update_cultural_tension()

    events = generate_cultural_event()
    update_cultural_memory()

    STATE["cultural_events"].extend(events)

    return {
        "status": "OK",
        "module": "AI Culture Engine",
        "cycle": STATE["cycle"],
        "identity_strength": round(STATE["identity_strength"], 3),
        "cultural_tension": round(STATE["cultural_tension"], 3),
        "subcultures": STATE["subcultures"],
        "symbols": STATE["symbols"],
        "rituals": STATE["rituals"],
        "events": events,
        "impact": (
            "System now simulates culture: traditions, rituals, symbols, subcultures, "
            "identity formation, cultural tension, and emergent cultural phenomena."
        )
    }
