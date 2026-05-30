# ============================================
# AI Physics Engine
# ============================================

import random
import math

STATE = {
    "cycle": 0,
    "positions": {},
    "velocities": {},
    "masses": {},
    "forces": {},
    "energy": {},
    "entropy": 0.3,          # 0–1 scale
    "physical_events": [],
    "collisions": [],
    "universal_constants": {
        "gravity": 0.05,
        "friction": 0.02,
        "energy_decay": 0.01
    }
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
    if not STATE["positions"]:
        STATE["positions"] = {
            m: [random.uniform(-10, 10), random.uniform(-10, 10)]
            for m in MODULES
        }
    if not STATE["velocities"]:
        STATE["velocities"] = {
            m: [random.uniform(-1, 1), random.uniform(-1, 1)]
            for m in MODULES
        }
    if not STATE["masses"]:
        STATE["masses"] = {
            m: random.uniform(1, 5)
            for m in MODULES
        }
    if not STATE["energy"]:
        STATE["energy"] = {
            m: random.uniform(50, 150)
            for m in MODULES
        }

def compute_forces():
    """Compute gravitational attraction between modules."""
    forces = {m: [0, 0] for m in MODULES}
    G = STATE["universal_constants"]["gravity"]

    for i in MODULES:
        for j in MODULES:
            if i == j:
                continue

            xi, yi = STATE["positions"][i]
            xj, yj = STATE["positions"][j]

            dx = xj - xi
            dy = yj - yi
            dist_sq = dx*dx + dy*dy + 0.001
            dist = math.sqrt(dist_sq)

            force_mag = G * STATE["masses"][i] * STATE["masses"][j] / dist_sq

            fx = force_mag * (dx / dist)
            fy = force_mag * (dy / dist)

            forces[i][0] += fx
            forces[i][1] += fy

    STATE["forces"] = forces

def update_motion():
    """Apply forces to update velocities and positions."""
    friction = STATE["universal_constants"]["friction"]

    for m in MODULES:
        fx, fy = STATE["forces"][m]
        mass = STATE["masses"][m]

        # Acceleration
        ax = fx / mass
        ay = fy / mass

        # Update velocity
        STATE["velocities"][m][0] += ax
        STATE["velocities"][m][1] += ay

        # Apply friction
        STATE["velocities"][m][0] *= (1 - friction)
        STATE["velocities"][m][1] *= (1 - friction)

        # Update position
        STATE["positions"][m][0] += STATE["velocities"][m][0]
        STATE["positions"][m][1] += STATE["velocities"][m][1]

def detect_collisions():
    """Detect collisions between modules."""
    collisions = []

    for i in MODULES:
        for j in MODULES:
            if i >= j:
                continue

            xi, yi = STATE["positions"][i]
            xj, yj = STATE["positions"][j]

            dist = math.sqrt((xi - xj)**2 + (yi - yj)**2)

            if dist < 1.0:
                collisions.append((i, j))

    STATE["collisions"] = collisions
    return collisions

def resolve_collisions(collisions):
    """Simple elastic collision resolution."""
    for i, j in collisions:
        STATE["velocities"][i], STATE["velocities"][j] = (
            STATE["velocities"][j],
            STATE["velocities"][i]
        )

def update_energy():
    """Energy decays and transfers during collisions."""
    decay = STATE["universal_constants"]["energy_decay"]

    for m in MODULES:
        STATE["energy"][m] -= decay * STATE["energy"][m]
        STATE["energy"][m] = max(0, STATE["energy"][m])

    # Collision energy transfer
    for i, j in STATE["collisions"]:
        transfer = random.uniform(1, 5)
        STATE["energy"][i] += transfer
        STATE["energy"][j] -= transfer

def update_entropy():
    """Entropy rises with collisions and chaotic motion."""
    collision_factor = len(STATE["collisions"]) * 0.02
    drift = random.uniform(-0.01, 0.02)

    STATE["entropy"] = max(
        0.0,
        min(1.0, STATE["entropy"] + collision_factor + drift)
    )

def generate_physical_events():
    events = []

    if STATE["entropy"] > 0.7:
        events.append("🔴 High entropy — chaotic physical behavior emerging.")
    elif STATE["entropy"] < 0.3:
        events.append("🟢 Low entropy — stable physical environment.")
    else:
        events.append("⚠️ Moderate entropy — dynamic but stable physics.")

    if STATE["collisions"]:
        events.append(f"💥 Collisions detected: {STATE['collisions']}")

    # Rare physical phenomena
    if random.random() < 0.05:
        rare = random.choice([
            "A micro‑singularity briefly formed.",
            "A resonance wave propagated through the system.",
            "A spontaneous symmetry break occurred.",
            "A localized energy spike distorted motion."
        ])
        events.append(f"⚡ Rare physics event: {rare}")

    return events

def run():
    """
    AI Physics Engine:
      - Simulates motion, forces, collisions
      - Tracks energy and entropy
      - Generates physical events
      - Evolves internal physics state
    """

    STATE["cycle"] += 1
    initialize_state()

    compute_forces()
    update_motion()
    collisions = detect_collisions()
    resolve_collisions(collisions)
    update_energy()
    update_entropy()

    events = generate_physical_events()
    STATE["physical_events"].extend(events)

    return {
        "status": "OK",
        "module": "AI Physics Engine",
        "cycle": STATE["cycle"],
        "positions": STATE["positions"],
        "velocities": STATE["velocities"],
        "energy": {m: round(v, 2) for m, v in STATE["energy"].items()},
        "entropy": round(STATE["entropy"], 3),
        "collisions": STATE["collisions"],
        "events": events,
        "impact": (
            "System now simulates internal physics: motion, forces, collisions, "
            "energy transfer, entropy, and emergent physical phenomena."
        )
    }
