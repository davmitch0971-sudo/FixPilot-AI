# ============================================
# AI World Model Engine
# ============================================

import random
import math

STATE = {
    "cycle": 0,
    "world_state": {
        "stability": 0.6,      # 0–1
        "complexity": 0.4,     # 0–1
        "entropy": 0.3,        # 0–1
        "coherence": 0.5       # 0–1
    },
    "future_scenarios": [],
    "scenario_confidence": 0.4,
    "branching_factor": 3,
    "world_events": [],
    "history": []
}

WORLD_EVENTS = [
    "resource_shift",
    "cooperation_wave",
    "instability_spike",
    "entropy_cascade",
    "predictive_alignment",
    "structural_reorganization",
    "emergent_pattern",
    "coherence_collapse"
]

def drift_world_state():
    """World state evolves each cycle."""
    ws = STATE["world_state"]

    ws["stability"] = max(0.0, min(1.0, ws["stability"] + random.uniform(-0.03, 0.03)))
    ws["complexity"] = max(0.0, min(1.0, ws["complexity"] + random.uniform(-0.02, 0.04)))
    ws["entropy"] = max(0.0, min(1.0, ws["entropy"] + random.uniform(-0.03, 0.03)))
    ws["coherence"] = max(0.0, min(1.0, ws["coherence"] + random.uniform(-0.03, 0.03)))

def generate_future_scenario():
    """Creates a hypothetical future world state."""
    ws = STATE["world_state"]

    # Future drift influenced by current state
    future = {
        "stability": max(0.0, min(1.0, ws["stability"] + random.uniform(-0.1, 0.1))),
        "complexity": max(0.0, min(1.0, ws["complexity"] + random.uniform(-0.1, 0.15))),
        "entropy": max(0.0, min(1.0, ws["entropy"] + random.uniform(-0.1, 0.1))),
        "coherence": max(0.0, min(1.0, ws["coherence"] + random.uniform(-0.1, 0.1)))
    }

    # Confidence increases with coherence
    confidence = 0.3 + (ws["coherence"] * 0.5)

    return future, round(confidence, 3)

def generate_world_event():
    """Occasional world-level events."""
    if random.random() < 0.15:
        return random.choice(WORLD_EVENTS)
    return None

def run():
    """
    AI World Model Engine:
      - Simulates hypothetical futures
      - Evolves internal world state
      - Generates branching scenarios
      - Tracks scenario confidence
      - Produces world-level events
    """

    STATE["cycle"] += 1
    drift_world_state()

    scenarios = []
    for _ in range(STATE["branching_factor"]):
        future, conf = generate_future_scenario()
        scenarios.append({"future": future, "confidence": conf})

    STATE["future_scenarios"] = scenarios

    event = generate_world_event()
    events = []
    if event:
        events.append(f"World event occurred: {event}")
        STATE["world_events"].append(event)

    STATE["history"].append({
        "cycle": STATE["cycle"],
        "world_state": STATE["world_state"],
        "scenarios": scenarios
    })

    return {
        "status": "OK",
        "module": "AI World Model Engine",
        "cycle": STATE["cycle"],
        "world_state": {k: round(v, 3) for k, v in STATE["world_state"].items()},
        "future_scenarios": scenarios,
        "scenario_confidence": STATE["scenario_confidence"],
        "events": events,
        "impact": (
            "System now simulates hypothetical futures, branching scenarios, "
            "world-state evolution, and emergent world-level events."
        )
    }
