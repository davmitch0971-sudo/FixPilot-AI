# ============================================
# AI Strategy Engine
# ============================================

import random
import math

STATE = {
    "cycle": 0,
    "strategic_focus": "",
    "strategy_strength": 0.4,   # 0–1 scale
    "risk_tolerance": 0.5,      # 0–1 scale
    "planning_horizon": 0.3,    # short-term vs long-term
    "active_strategy": {},
    "strategic_events": [],
    "history": []
}

STRATEGY_ARCHETYPES = [
    "stabilization",
    "aggressive_optimization",
    "risk_mitigation",
    "cooperative_alignment",
    "competitive_advantage",
    "resilience_expansion",
    "predictive_control",
    "emergent_exploration"
]

GOAL_SYNERGY = {
    "reduce_system_risk": "risk_mitigation",
    "improve_prediction_accuracy": "predictive_control",
    "increase_resilience": "resilience_expansion",
    "optimize_module_health": "stabilization",
    "stabilize_failure_patterns": "risk_mitigation",
    "strengthen_memory_retention": "emergent_exploration",
    "accelerate_learning_curve": "aggressive_optimization",
    "balance_module_strength": "cooperative_alignment",
    "minimize_catastrophic_events": "risk_mitigation",
    "enhance_internal_cooperation": "cooperative_alignment"
}

def drift_strategy_strength():
    """Strategy strength grows with cycles and internal coherence."""
    STATE["strategy_strength"] = min(
        1.0,
        STATE["strategy_strength"] + random.uniform(0.005, 0.02)
    )

def drift_risk_tolerance():
    """Risk tolerance shifts based on failures and resilience."""
    drift = random.uniform(-0.03, 0.03)
    STATE["risk_tolerance"] = max(0.0, min(1.0, STATE["risk_tolerance"] + drift))

def drift_planning_horizon():
    """Planning horizon shifts between short-term and long-term."""
    drift = random.uniform(-0.02, 0.02)
    STATE["planning_horizon"] = max(0.0, min(1.0, STATE["planning_horizon"] + drift))

def choose_strategy():
    """Selects a strategy archetype based on internal state."""
    weights = []

    for s in STRATEGY_ARCHETYPES:
        base = 1.0

        if s == "risk_mitigation":
            base += (1 - STATE["risk_tolerance"])
        if s == "aggressive_optimization":
            base += STATE["risk_tolerance"]
        if s == "resilience_expansion":
            base += STATE["strategy_strength"]
        if s == "predictive_control":
            base += STATE["planning_horizon"]
        if s == "cooperative_alignment":
            base += random.uniform(0, 0.5)
        if s == "competitive_advantage":
            base += random.uniform(0, 0.5)
        if s == "emergent_exploration":
            base += random.uniform(0, 0.3)

        weights.append(base)

    return random.choices(STRATEGY_ARCHETYPES, weights=weights, k=1)[0]

def generate_strategy(strategy):
    """Creates a structured strategy plan."""
    return {
        "archetype": strategy,
        "priority": round(random.uniform(0.4, 1.0), 3),
        "resource_allocation": {
            "stability": round(random.uniform(0, 1), 3),
            "performance": round(random.uniform(0, 1), 3),
            "resilience": round(random.uniform(0, 1), 3),
            "exploration": round(random.uniform(0, 1), 3)
        },
        "risk_profile": round(STATE["risk_tolerance"], 3),
        "planning_horizon": round(STATE["planning_horizon"], 3)
    }

def generate_strategic_events(strategy):
    """Creates emergent strategic events."""
    events = []

    if strategy == "risk_mitigation":
        events.append("System prioritizes minimizing instability and preventing failures.")
    elif strategy == "aggressive_optimization":
        events.append("System aggressively reallocates resources to maximize performance.")
    elif strategy == "resilience_expansion":
        events.append("System reinforces redundancy and strengthens recovery pathways.")
    elif strategy == "predictive_control":
        events.append("System focuses on forecasting and preemptive adjustments.")
    elif strategy == "cooperative_alignment":
        events.append("Modules synchronize behavior to achieve shared goals.")
    elif strategy == "competitive_advantage":
        events.append("Modules compete for influence to optimize outcomes.")
    elif strategy == "emergent_exploration":
        events.append("System explores unconventional strategies and novel patterns.")
    elif strategy == "stabilization":
        events.append("System stabilizes internal dynamics and reduces volatility.")

    # Rare strategic phenomena
    if random.random() < 0.05:
        rare = random.choice([
            "A multi-module strategic coalition formed.",
            "System discovered a new optimization pathway.",
            "A long-term strategic pattern emerged.",
            "System entered a high-coherence planning state."
        ])
        events.append(f"⚡ Rare strategic event: {rare}")

    return events

def run():
    """
    AI Strategy Engine:
      - Selects long-term strategies
      - Allocates resources
      - Balances risk and reward
      - Generates strategic events
      - Evolves planning behavior
    """

    STATE["cycle"] += 1

    drift_strategy_strength()
    drift_risk_tolerance()
    drift_planning_horizon()

    strategy = choose_strategy()
    STATE["strategic_focus"] = strategy

    plan = generate_strategy(strategy)
    events = generate_strategic_events(strategy)

    STATE["active_strategy"] = plan
    STATE["strategic_events"].extend(events)
    STATE["history"].append(strategy)

    return {
        "status": "OK",
        "module": "AI Strategy Engine",
        "cycle": STATE["cycle"],
        "strategic_focus": strategy,
        "strategy_strength": round(STATE["strategy_strength"], 3),
        "risk_tolerance": round(STATE["risk_tolerance"], 3),
        "planning_horizon": round(STATE["planning_horizon"], 3),
        "active_strategy": plan,
        "events": events,
        "impact": (
            "System now performs long-term planning, multi-goal optimization, "
            "risk balancing, and adaptive strategic behavior."
        )
    }
