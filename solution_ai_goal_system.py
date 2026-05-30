# ============================================
# AI Goal System Module
# ============================================

import random
import math

STATE = {
    "cycle": 0,
    "active_goals": [],
    "completed_goals": [],
    "failed_goals": [],
    "goal_priority": {},
    "long_term_focus": 0.5,   # 0 = short-term, 1 = long-term
    "motivation": 0.5,        # influences goal pursuit intensity
    "goal_history": []
}

GOAL_POOL = [
    "reduce_system_risk",
    "improve_prediction_accuracy",
    "increase_resilience",
    "optimize_module_health",
    "stabilize_failure_patterns",
    "strengthen_memory_retention",
    "accelerate_learning_curve",
    "balance_module_strength",
    "minimize_catastrophic_events",
    "enhance_internal_cooperation"
]

def generate_goal():
    """Creates a new goal with weighted randomness."""
    goal = random.choice(GOAL_POOL)
    priority = random.uniform(0.3, 1.0)
    return goal, priority

def evaluate_goal_progress(goal):
    """Simulates progress toward a goal."""
    base = random.uniform(0.0, 1.0)
    motivation = STATE["motivation"]
    long_term = STATE["long_term_focus"]

    # Long-term goals progress slower but more steadily
    if goal in ["increase_resilience", "strengthen_memory_retention", "accelerate_learning_curve"]:
        progress = (base * 0.5) + (long_term * 0.5)
    else:
        progress = (base * 0.7) + (motivation * 0.3)

    return progress

def update_motivation():
    """Motivation drifts based on internal conditions."""
    drift = random.uniform(-0.05, 0.05)
    STATE["motivation"] = max(0.0, min(1.0, STATE["motivation"] + drift))

def update_long_term_focus():
    """Long-term focus shifts slowly over time."""
    drift = random.uniform(-0.02, 0.02)
    STATE["long_term_focus"] = max(0.0, min(1.0, STATE["long_term_focus"] + drift))

def run():
    """
    AI Goal System:
      - Generates autonomous goals
      - Tracks progress
      - Completes or fails goals
      - Adjusts priorities dynamically
      - Evolves long-term focus and motivation
    """

    STATE["cycle"] += 1
    update_motivation()
    update_long_term_focus()

    events = []

    # 1. Occasionally generate new goals
    if len(STATE["active_goals"]) < 3 and random.random() < 0.4:
        goal, priority = generate_goal()
        STATE["active_goals"].append(goal)
        STATE["goal_priority"][goal] = priority
        events.append(f"New goal generated: {goal} (priority {priority:.2f}).")

    # 2. Evaluate active goals
    completed = []
    failed = []

    for goal in STATE["active_goals"]:
        progress = evaluate_goal_progress(goal)

        if progress > 0.85:
            completed.append(goal)
            events.append(f"Goal completed: {goal}.")
        elif progress < 0.15 and random.random() < 0.2:
            failed.append(goal)
            events.append(f"Goal failed: {goal}.")
        else:
            events.append(f"Goal '{goal}' progressed by {progress:.2f}.")

    # 3. Update goal lists
    for g in completed:
        STATE["active_goals"].remove(g)
        STATE["completed_goals"].append(g)
        STATE["goal_history"].append({"goal": g, "result": "completed"})

    for g in failed:
        STATE["active_goals"].remove(g)
        STATE["failed_goals"].append(g)
        STATE["goal_history"].append({"goal": g, "result": "failed"})

    return {
        "status": "OK",
        "module": "AI Goal System",
        "cycle": STATE["cycle"],
        "active_goals": STATE["active_goals"],
        "completed_goals": STATE["completed_goals"][-10:],  # last 10
        "failed_goals": STATE["failed_goals"][-10:],        # last 10
        "motivation": round(STATE["motivation"], 3),
        "long_term_focus": round(STATE["long_term_focus"], 3),
        "goal_priority": {g: round(p, 3) for g, p in STATE["goal_priority"].items()},
        "events": events,
        "impact": (
            "AI now generates and pursues autonomous goals, evaluates progress, "
            "adapts priorities, and evolves long-term planning behavior."
        )
    }
