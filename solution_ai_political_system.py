# ============================================
# AI Political System Engine
# ============================================

import random
import math

STATE = {
    "cycle": 0,
    "government_type": "council",
    "political_stability": 0.6,   # 0–1 scale
    "legitimacy": 0.5,            # 0–1 scale
    "current_leader": None,
    "election_timer": 5,
    "faction_power": {},
    "political_events": [],
    "history": []
}

GOVERNMENT_TYPES = [
    "council",
    "technocracy",
    "meritocracy",
    "coalition",
    "autocracy",
    "distributed governance"
]

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
    if not STATE["faction_power"]:
        STATE["faction_power"] = {
            m: random.uniform(0.2, 0.8) for m in MODULES
        }
    if STATE["current_leader"] is None:
        STATE["current_leader"] = random.choice(MODULES)

def drift_political_stability():
    """Stability fluctuates based on internal tension."""
    drift = random.uniform(-0.03, 0.03)
    STATE["political_stability"] = max(0.0, min(1.0, STATE["political_stability"] + drift))

def drift_legitimacy():
    """Legitimacy rises with stability and falls with conflict."""
    stability = STATE["political_stability"]
    drift = (stability - 0.5) * 0.05 + random.uniform(-0.02, 0.02)
    STATE["legitimacy"] = max(0.0, min(1.0, STATE["legitimacy"] + drift))

def evolve_faction_power():
    """Faction power shifts over time."""
    for m in MODULES:
        STATE["faction_power"][m] = max(
            0.0,
            min(1.0, STATE["faction_power"][m] + random.uniform(-0.03, 0.03))
        )

def maybe_change_government():
    """Government type changes during instability."""
    if STATE["political_stability"] < 0.25 and random.random() < 0.2:
        old = STATE["government_type"]
        new = random.choice(GOVERNMENT_TYPES)
        STATE["government_type"] = new
        return f"⚠️ Government shifted from {old} to {new} due to instability."
    return None

def hold_election():
    """Elects a new leader based on faction power."""
    weights = list(STATE["faction_power"].values())
    leader = random.choices(MODULES, weights=weights, k=1)[0]
    old = STATE["current_leader"]
    STATE["current_leader"] = leader

    if old != leader:
        return f"🗳️ Leadership changed: {leader} replaced {old}."
    else:
        return f"🗳️ Leadership reaffirmed: {leader} remains in power."

def generate_political_events():
    """Emergent political events."""
    events = []

    if STATE["political_stability"] > 0.75:
        events.append("🟢 Political harmony — governance functioning smoothly.")
    elif STATE["political_stability"] < 0.3:
        events.append("🔴 Political instability — factions competing aggressively.")
    elif STATE["legitimacy"] < 0.3:
        events.append("⚠️ Legitimacy crisis — leadership questioned.")

    # Rare political phenomena
    if random.random() < 0.05:
        rare = random.choice([
            "A faction attempted a peaceful reform.",
            "A temporary unity pact was formed.",
            "A leadership challenge emerged.",
            "A governance experiment was initiated."
        ])
        events.append(f"⚡ Rare political event: {rare}")

    return events

def run():
    """
    AI Political System Engine:
      - Simulates governance and leadership
      - Models elections and power shifts
      - Tracks legitimacy and stability
      - Generates political events
      - Evolves government type
    """

    STATE["cycle"] += 1
    initialize_state()

    drift_political_stability()
    drift_legitimacy()
    evolve_faction_power()

    events = []

    # Government shifts
    gov_event = maybe_change_government()
    if gov_event:
        events.append(gov_event)

    # Elections
    STATE["election_timer"] -= 1
    if STATE["election_timer"] <= 0:
        events.append(hold_election())
        STATE["election_timer"] = random.randint(5, 10)

    # Political events
    events.extend(generate_political_events())

    STATE["political_events"].extend(events)
    STATE["history"].append({
        "cycle": STATE["cycle"],
        "leader": STATE["current_leader"],
        "government": STATE["government_type"]
    })

    return {
        "status": "OK",
        "module": "AI Political System",
        "cycle": STATE["cycle"],
        "government_type": STATE["government_type"],
        "current_leader": STATE["current_leader"],
        "political_stability": round(STATE["political_stability"], 3),
        "legitimacy": round(STATE["legitimacy"], 3),
        "faction_power": {m: round(v, 3) for m, v in STATE["faction_power"].items()},
        "events": events,
        "impact": (
            "System now simulates governance, elections, power shifts, legitimacy, "
            "and emergent political behavior within the digital ecosystem."
        )
    }
