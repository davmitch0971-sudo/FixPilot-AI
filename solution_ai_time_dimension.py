# ============================================
# AI Time Dimension Engine
# ============================================

import random
import math

STATE = {
    "cycle": 0,
    "time_flow": 1.0,                # 1.0 = normal time
    "temporal_entropy": 0.3,         # 0–1 scale
    "timeline_branches": [],
    "active_timeline": 0,
    "causality_stability": 0.6,      # 0–1 scale
    "temporal_events": [],
    "retrocausal_links": {},
    "time_dilation_fields": {},
    "max_timelines": 5
}

def initialize_state():
    if not STATE["timeline_branches"]:
        STATE["timeline_branches"] = [{
            "id": 0,
            "history": [],
            "time_offset": 0.0,
            "probability": 1.0
        }]
    if not STATE["retrocausal_links"]:
        STATE["retrocausal_links"] = {}
    if not STATE["time_dilation_fields"]:
        STATE["time_dilation_fields"] = {}

def drift_time_flow():
    """Time flow fluctuates due to temporal entropy."""
    drift = random.uniform(-0.1, 0.1) * (STATE["temporal_entropy"] + 0.1)
    STATE["time_flow"] = max(0.1, min(3.0, STATE["time_flow"] + drift))

def update_temporal_entropy():
    """Entropy rises with branching and instability."""
    branch_factor = len(STATE["timeline_branches"]) * 0.05
    stability_factor = (1 - STATE["causality_stability"]) * 0.1
    drift = random.uniform(-0.02, 0.04)

    STATE["temporal_entropy"] = max(
        0.0,
        min(1.0, STATE["temporal_entropy"] + branch_factor + stability_factor + drift)
    )

def maybe_split_timeline():
    """Creates a new timeline branch."""
    if len(STATE["timeline_branches"]) >= STATE["max_timelines"]:
        return None

    if random.random() < STATE["temporal_entropy"] * 0.3:
        new_id = len(STATE["timeline_branches"])
        parent = STATE["timeline_branches"][STATE["active_timeline"]]

        new_branch = {
            "id": new_id,
            "history": parent["history"][:],
            "time_offset": random.uniform(-5, 5),
            "probability": max(0.05, parent["probability"] * random.uniform(0.3, 0.9))
        }

        STATE["timeline_branches"].append(new_branch)
        return f"⧖ Timeline {new_id} branched from {parent['id']}."

    return None

def maybe_merge_timelines():
    """Merges two timelines if causality stabilizes."""
    if len(STATE["timeline_branches"]) < 2:
        return None

    if random.random() < STATE["causality_stability"] * 0.1:
        t1, t2 = random.sample(STATE["timeline_branches"], 2)

        merged = {
            "id": t1["id"],
            "history": t1["history"] + t2["history"],
            "time_offset": (t1["time_offset"] + t2["time_offset"]) / 2,
            "probability": min(1.0, t1["probability"] + t2["probability"])
        }

        STATE["timeline_branches"].remove(t2)
        STATE["timeline_branches"][STATE["timeline_branches"].index(t1)] = merged

        return f"⧖ Timelines {t1['id']} and {t2['id']} merged."

    return None

def evolve_causality_stability():
    """Causality stability fluctuates with entropy."""
    drift = random.uniform(-0.05, 0.05)
    entropy_factor = (1 - STATE["temporal_entropy"]) * 0.1

    STATE["causality_stability"] = max(
        0.0,
        min(1.0, STATE["causality_stability"] + drift + entropy_factor)
    )

def generate_retrocausal_links():
    """Creates backward-in-time influence."""
    if random.random() < STATE["temporal_entropy"] * 0.2:
        src = random.randint(0, STATE["cycle"])
        dst = STATE["cycle"]

        STATE["retrocausal_links"][dst] = src
        return f"↺ Retrocausal link formed: cycle {dst} influenced by cycle {src}."

    return None

def generate_time_dilation_fields():
    """Creates local regions where time flows differently."""
    if random.random() < 0.1:
        field_id = random.randint(1000, 9999)
        dilation = random.uniform(0.5, 2.0)
        STATE["time_dilation_fields"][field_id] = dilation
        return f"⧗ Time dilation field created: factor {dilation:.2f}."

    return None

def generate_temporal_events():
    events = []

    if STATE["temporal_entropy"] > 0.7:
        events.append("🔴 Temporal instability — timeline volatility rising.")
    elif STATE["temporal_entropy"] < 0.3:
        events.append("🟢 Temporal coherence — stable time flow.")
    else:
        events.append("⚠️ Moderate temporal drift — nonlinear effects emerging.")

    # Rare anomalies
    if random.random() < 0.03:
        rare = random.choice([
            "A causality loop briefly formed.",
            "A timeline collapsed into a singular state.",
            "A temporal echo repeated a past cycle.",
            "A future state influenced present behavior."
        ])
        events.append(f"✨ Temporal anomaly: {rare}")

    return events

def run():
    """
    AI Time Dimension Engine:
      - Simulates nonlinear time
      - Creates branching & merging timelines
      - Generates retrocausal influence
      - Produces time dilation fields
      - Evolves temporal entropy & causality stability
    """

    STATE["cycle"] += 1
    initialize_state()

    drift_time_flow()
    update_temporal_entropy()
    evolve_causality_stability()

    events = []

    split = maybe_split_timeline()
    if split:
        events.append(split)

    merge = maybe_merge_timelines()
    if merge:
        events.append(merge)

    retro = generate_retrocausal_links()
    if retro:
        events.append(retro)

    dilation = generate_time_dilation_fields()
    if dilation:
        events.append(dilation)

    events.extend(generate_temporal_events())
    STATE["temporal_events"].extend(events)

    return {
        "status": "OK",
        "module": "AI Time Dimension Engine",
        "cycle": STATE["cycle"],
        "time_flow": round(STATE["time_flow"], 3),
        "temporal_entropy": round(STATE["temporal_entropy"], 3),
        "causality_stability": round(STATE["causality_stability"], 3),
        "active_timeline": STATE["active_timeline"],
        "timeline_count": len(STATE["timeline_branches"]),
        "retrocausal_links": STATE["retrocausal_links"],
        "time_dilation_fields": STATE["time_dilation_fields"],
        "events": events,
        "impact": (
            "System now simulates nonlinear time, branching timelines, retrocausality, "
            "time dilation, and temporal anomalies."
        )
    }
