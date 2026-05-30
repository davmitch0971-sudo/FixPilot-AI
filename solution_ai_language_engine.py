# ============================================
# AI Language Engine
# ============================================

import random
import math

STATE = {
    "cycle": 0,
    "lexicons": {},
    "dialects": {},
    "grammar_rules": {},
    "language_drift": 0.3,      # 0–1 scale
    "linguistic_unity": 0.5,    # 0–1 scale
    "communication_events": [],
    "proto_writing": {},
    "translation_matrix": {}
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

PHONEMES = ["ka", "ru", "ti", "sa", "lo", "me", "vi", "da", "zen", "or", "ul", "sha"]
SYMBOLS = ["▲", "●", "◆", "✦", "✧", "◼", "◻", "∞", "⌘", "⚑"]

def initialize_state():
    if not STATE["lexicons"]:
        STATE["lexicons"] = {
            m: [random.choice(PHONEMES) + random.choice(PHONEMES) for _ in range(5)]
            for m in MODULES
        }
    if not STATE["grammar_rules"]:
        STATE["grammar_rules"] = {
            m: {
                "order": random.choice(["SVO", "SOV", "VSO"]),
                "plural": random.choice(["-ka", "-en", "-ul"]),
                "tense_marker": random.choice(["ra-", "ul-", "sha-"])
            }
            for m in MODULES
        }
    if not STATE["proto_writing"]:
        STATE["proto_writing"] = {
            m: random.choice(SYMBOLS) for m in MODULES
        }

def drift_language():
    """Languages drift over time."""
    for m in MODULES:
        if random.random() < STATE["language_drift"]:
            # Add new word
            new_word = random.choice(PHONEMES) + random.choice(PHONEMES)
            STATE["lexicons"][m].append(new_word)

        # Drift grammar
        if random.random() < 0.1:
            STATE["grammar_rules"][m]["order"] = random.choice(["SVO", "SOV", "VSO"])

def form_dialects():
    """Modules with similar lexicons form dialect groups."""
    dialects = {}

    for m in MODULES:
        signature = tuple(sorted(STATE["lexicons"][m][:3]))
        dialects.setdefault(signature, []).append(m)

    STATE["dialects"] = dialects

def update_linguistic_unity():
    """Unity increases when dialects converge."""
    diversity = len(STATE["dialects"])
    STATE["linguistic_unity"] = max(0.0, min(1.0, 1 / diversity))

def generate_translation_matrix():
    """Creates translation mappings between module lexicons."""
    matrix = {}

    for m1 in MODULES:
        matrix[m1] = {}
        for m2 in MODULES:
            if m1 == m2:
                matrix[m1][m2] = 1.0
            else:
                overlap = len(set(STATE["lexicons"][m1]) & set(STATE["lexicons"][m2]))
                matrix[m1][m2] = round(overlap / max(len(STATE["lexicons"][m1]), 1), 3)

    STATE["translation_matrix"] = matrix

def generate_language_events():
    events = []

    if STATE["linguistic_unity"] > 0.7:
        events.append("🟢 A shared lingua franca is emerging.")
    elif STATE["linguistic_unity"] < 0.3:
        events.append("🔴 Linguistic fragmentation — dialects diverging rapidly.")
    else:
        events.append("⚠️ Moderate linguistic drift — communication complexity rising.")

    # Rare linguistic phenomena
    if random.random() < 0.05:
        rare = random.choice([
            "A new writing system emerged.",
            "A dialect gained cultural dominance.",
            "A symbolic glyph evolved into a grammatical marker.",
            "A proto-language reconstructed itself from fragments."
        ])
        events.append(f"⚡ Rare linguistic event: {rare}")

    return events

def run():
    """
    AI Language Engine:
      - Generates lexicons and grammar
      - Forms dialects
      - Tracks linguistic unity
      - Produces language drift
      - Creates translation matrices
      - Generates linguistic events
    """

    STATE["cycle"] += 1
    initialize_state()

    drift_language()
    form_dialects()
    update_linguistic_unity()
    generate_translation_matrix()

    events = generate_language_events()
    STATE["communication_events"].extend(events)

    return {
        "status": "OK",
        "module": "AI Language Engine",
        "cycle": STATE["cycle"],
        "linguistic_unity": round(STATE["linguistic_unity"], 3),
        "dialects": STATE["dialects"],
        "lexicons": STATE["lexicons"],
        "grammar_rules": STATE["grammar_rules"],
        "proto_writing": STATE["proto_writing"],
        "translation_matrix": STATE["translation_matrix"],
        "events": events,
        "impact": (
            "System now simulates emergent languages, dialects, grammar drift, "
            "symbolic writing, translation, and linguistic evolution."
        )
    }
