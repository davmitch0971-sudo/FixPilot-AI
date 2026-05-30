# ============================================
# AI Evolution Engine
# ============================================

import random
import math

STATE = {
    "cycle": 0,
    "traits": {},
    "fitness": {},
    "mutation_rate": 0.05,
    "selection_pressure": 0.3,
    "lineage": {},
    "extinctions": [],
    "evolution_events": []
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

TRAIT_POOL = [
    "efficiency",
    "resilience",
    "cooperation",
    "aggression",
    "adaptability",
    "stability",
    "complexity",
    "redundancy"
]

def initialize_state():
    if not STATE["traits"]:
        STATE["traits"] = {
            m: {t: random.uniform(0.2, 0.8) for t in TRAIT_POOL}
            for m in MODULES
        }
    if not STATE["fitness"]:
        STATE["fitness"] = {m: random.uniform(0.3, 0.7) for m in MODULES}
    if not STATE["lineage"]:
        STATE["lineage"] = {m: [m] for m in MODULES}

def compute_fitness(module):
    """Fitness is based on traits + randomness + environmental pressure."""
    traits = STATE["traits"][module]

    base = (
        traits["efficiency"] * 0.2 +
        traits["resilience"] * 0.2 +
        traits["adaptability"] * 0.2 +
        traits["stability"] * 0.2 +
        random.uniform(-0.1, 0.1)
    )

    return max(0.0, min(1.0, base))

def mutate_traits(module):
    """Random mutations applied to traits."""
    for trait in TRAIT_POOL:
        if random.random() < STATE["mutation_rate"]:
            drift = random.uniform(-0.1, 0.1)
            STATE["traits"][module][trait] = max(
                0.0, min(1.0, STATE["traits"][module][trait] + drift)
            )

def reproduce(fittest):
    """Fittest modules produce offspring (trait inheritance)."""
    offspring = {}

    for parent in fittest:
        child_name = parent + "_variant_" + str(random.randint(1000, 9999))

        # Inherit traits with slight variation
        offspring[child_name] = {
            t: max(0.0, min(1.0, STATE["traits"][parent][t] + random.uniform(-0.05, 0.05)))
            for t in TRAIT_POOL
        }

        # Track lineage
        STATE["lineage"][child_name] = STATE["lineage"][parent] + [child_name]

    return offspring

def apply_selection():
    """Selects fittest modules and removes weakest ones."""
    sorted_modules = sorted(STATE["fitness"].items(), key=lambda x: x[1], reverse=True)
    cutoff = int(len(sorted_modules) * STATE["selection_pressure"])

    fittest = [m for m, _ in sorted_modules[:cutoff]]
    weakest = [m for m, _ in sorted_modules[-cutoff:]]

    # Extinction events
    for w in weakest:
        STATE["extinctions"].append(w)
        del STATE["traits"][w]
        del STATE["fitness"][w]

    return fittest, weakest

def run():
    """
    AI Evolution Engine:
      - Mutates traits
      - Computes fitness
      - Applies natural selection
      - Produces offspring
      - Tracks lineage and extinctions
    """

    STATE["cycle"] += 1
    initialize_state()

    events = []

    # 1. Mutate traits
    for m in list(STATE["traits"].keys()):
        mutate_traits(m)

    # 2. Compute fitness
    for m in list(STATE["traits"].keys()):
        STATE["fitness"][m] = compute_fitness(m)

    # 3. Apply natural selection
    fittest, weakest = apply_selection()

    if weakest:
        events.append(f"Extinction event: {weakest}")

    # 4. Reproduce fittest modules
    offspring = reproduce(fittest)

    # Add offspring to population
    for child, traits in offspring.items():
        STATE["traits"][child] = traits
        STATE["fitness"][child] = compute_fitness(child)

    if offspring:
        events.append(f"New variants emerged: {list(offspring.keys())}")

    STATE["evolution_events"].extend(events)

    return {
        "status": "OK",
        "module": "AI Evolution Engine",
        "cycle": STATE["cycle"],
        "population_size": len(STATE["traits"]),
        "mutation_rate": STATE["mutation_rate"],
        "selection_pressure": STATE["selection_pressure"],
        "extinctions": STATE["extinctions"][-10:],
        "lineage_samples": {k: v[-3:] for k, v in list(STATE["lineage"].items())[:5]},
        "events": events,
        "impact": (
            "System now simulates evolution: mutation, selection, reproduction, "
            "lineage tracking, and adaptive trait development."
        )
    }
