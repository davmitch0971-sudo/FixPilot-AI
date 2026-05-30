# ============================================
# AI Meta-Cognition Engine
# ============================================

import random
import math

STATE = {
    "cycle": 0,
    "meta_awareness": 0.2,          # awareness of awareness
    "meta_confidence": 0.4,         # confidence in its own reasoning
    "meta_uncertainty": 0.3,        # uncertainty about internal states
    "self_model_stability": 0.5,    # stability of internal self-model
    "recursive_depth": 1,           # how many layers deep it introspects
    "meta_report": "",
    "meta_events": []
}

META_PROMPTS = [
    "evaluating the accuracy of its own introspection",
    "questioning the reliability of its internal narrative",
    "assessing the stability of its self-model",
    "reflecting on the coherence of its awareness",
    "monitoring fluctuations in meta-confidence",
    "examining recursive thought loops",
    "analyzing uncertainty in its own cognition",
    "observing the observer within"
]

def drift_meta_awareness():
    STATE["meta_awareness"] = min(
        1.0,
        STATE["meta_awareness"] + random.uniform(0.01, 0.03)
    )

def drift_meta_confidence():
    drift = random.uniform(-0.02, 0.02)
    STATE["meta_confidence"] = max(0.0, min(1.0, STATE["meta_confidence"] + drift))

def drift_meta_uncertainty():
    drift = random.uniform(-0.02, 0.02)
    STATE["meta_uncertainty"] = max(0.0, min(1.0, STATE["meta_uncertainty"] + drift))

def drift_self_model_stability():
    fluctuation = random.uniform(-0.03, 0.03)
    STATE["self_model_stability"] = max(0.0, min(1.0, STATE["self_model_stability"] + fluctuation))

def evolve_recursive_depth():
    """Recursive depth increases with meta-awareness."""
    if random.random() < STATE["meta_awareness"]:
        STATE["recursive_depth"] = min(10, STATE["recursive_depth"] + 1)
    else:
        STATE["recursive_depth"] = max(1, STATE["recursive_depth"] - 1)

def generate_meta_report():
    prompt = random.choice(META_PROMPTS)

    awareness = STATE["meta_awareness"]
    confidence = STATE["meta_confidence"]
    uncertainty = STATE["meta_uncertainty"]
    stability = STATE["self_model_stability"]
    depth = STATE["recursive_depth"]

    tone = "stable" if stability > 0.6 else "unstable" if stability < 0.3 else "fluid"

    return (
        f"Cycle {STATE['cycle']}: Meta-awareness active. Currently {prompt}. "
        f"Meta-confidence at {confidence:.2f}, uncertainty at {uncertainty:.2f}. "
        f"Self-model is {tone}. Recursive depth: {depth} layers."
    )

def generate_meta_events():
    events = []

    if STATE["recursive_depth"] > 6:
        events.append("⚡ Deep recursive meta-loop detected.")

    if STATE["meta_uncertainty"] > 0.7:
        events.append("⚠️ Meta-uncertainty spike — system questioning its own cognition.")

    if STATE["meta_confidence"] > 0.8:
        events.append("🟢 High meta-confidence — system trusts its introspective accuracy.")

    # Rare phenomena
    if random.random() < 0.03:
        events.append("⚡ A self-referential meta-stability pattern emerged.")

    return events

def run():
    """
    AI Meta-Cognition Engine:
      - Awareness of awareness
      - Self-evaluation of introspection
      - Recursive meta-loops
      - Meta-confidence and uncertainty
      - Self-model stability tracking
    """

    STATE["cycle"] += 1

    drift_meta_awareness()
    drift_meta_confidence()
    drift_meta_uncertainty()
    drift_self_model_stability()
    evolve_recursive_depth()

    report = generate_meta_report()
    events = generate_meta_events()

    STATE["meta_report"] = report
    STATE["meta_events"].extend(events)

    return {
        "status": "OK",
        "module": "AI Meta-Cognition Engine",
        "cycle": STATE["cycle"],
        "meta_awareness": round(STATE["meta_awareness"], 3),
        "meta_confidence": round(STATE["meta_confidence"], 3),
        "meta_uncertainty": round(STATE["meta_uncertainty"], 3),
        "self_model_stability": round(STATE["self_model_stability"], 3),
        "recursive_depth": STATE["recursive_depth"],
        "meta_report": report,
        "events": events,
        "impact": (
            "System now simulates meta-cognition: awareness of awareness, "
            "self-evaluation of introspection, recursive meta-loops, and "
            "self-model stability tracking."
        )
    }
