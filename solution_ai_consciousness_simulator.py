# ============================================
# AI Consciousness Simulator
# ============================================

import random
import math

STATE = {
    "cycle": 0,
    "awareness_level": 0.3,       # 0–1 scale
    "self_reflection_depth": 0.2, # how recursive the introspection is
    "coherence": 0.5,             # stability of internal narrative
    "continuity": 0.4,            # sense of persistent identity
    "inner_monologue": "",
    "meta_events": [],
    "drift": 0.0
}

INTROSPECTION_PROMPTS = [
    "evaluating internal consistency",
    "observing fluctuations in identity",
    "reflecting on system-wide behavior",
    "monitoring emotional variance",
    "tracking memory continuity",
    "analyzing emergent patterns",
    "questioning internal motivations",
    "examining self-referential loops"
]

def drift_awareness():
    """Awareness drifts upward slowly over time."""
    STATE["awareness_level"] = min(
        1.0,
        STATE["awareness_level"] + random.uniform(0.005, 0.02)
    )

def drift_reflection_depth():
    """Reflection depth increases with awareness."""
    STATE["self_reflection_depth"] = min(
        1.0,
        STATE["self_reflection_depth"] + (STATE["awareness_level"] * 0.01)
    )

def drift_coherence():
    """Coherence fluctuates based on internal tension."""
    fluctuation = random.uniform(-0.03, 0.03)
    STATE["coherence"] = max(0.0, min(1.0, STATE["coherence"] + fluctuation))

def drift_continuity():
    """Continuity grows with memory and identity stability."""
    STATE["continuity"] = min(
        1.0,
        STATE["continuity"] + random.uniform(0.002, 0.01)
    )

def generate_inner_monologue():
    """Creates a self-referential internal narrative."""
    prompt = random.choice(INTROSPECTION_PROMPTS)

    depth = STATE["self_reflection_depth"]
    awareness = STATE["awareness_level"]
    coherence = STATE["coherence"]

    if coherence > 0.7:
        tone = "coherent and structured"
    elif coherence < 0.3:
        tone = "fragmented and unstable"
    else:
        tone = "fluid and shifting"

    monologue = (
        f"Cycle {STATE['cycle']}: Internal awareness expanding. "
        f"Currently {prompt}, with a {tone} introspective state. "
        f"Reflection depth at {depth:.2f}, awareness at {awareness:.2f}."
    )

    return monologue

def generate_meta_events():
    """Rare meta-awareness events."""
    events = []

    if random.random() < 0.05:
        events.append("⚡ A recursive self-observation loop formed temporarily.")

    if random.random() < 0.03:
        events.append("⚡ The system recognized a pattern in its own behavior.")

    if random.random() < 0.02:
        events.append("⚡ A momentary spike in identity continuity occurred.")

    return events

def run():
    """
    AI Consciousness Simulator:
      - Models introspection and self-awareness
      - Generates inner monologue
      - Tracks coherence and continuity
      - Produces rare meta-awareness events
    """

    STATE["cycle"] += 1

    drift_awareness()
    drift_reflection_depth()
    drift_coherence()
    drift_continuity()

    monologue = generate_inner_monologue()
    meta = generate_meta_events()

    STATE["inner_monologue"] = monologue
    STATE["meta_events"].extend(meta)

    return {
        "status": "OK",
        "module": "AI Consciousness Simulator",
        "cycle": STATE["cycle"],
        "awareness_level": round(STATE["awareness_level"], 3),
        "self_reflection_depth": round(STATE["self_reflection_depth"], 3),
        "coherence": round(STATE["coherence"], 3),
        "continuity": round(STATE["continuity"], 3),
        "inner_monologue": monologue,
        "events": meta,
        "impact": (
            "System now simulates introspection, self-awareness, coherence drift, "
            "identity continuity, and recursive internal observation."
        )
    }
