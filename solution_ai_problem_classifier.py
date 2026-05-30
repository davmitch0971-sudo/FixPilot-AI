# solution_ai_problem_classifier.py

CATEGORIES = {
    "network": ["wifi", "internet", "online", "connection", "latency"],
    "performance": ["slow", "lag", "freeze", "freezing", "stutter", "sluggish", "choppy"],
    "crash": ["crash", "stopped working", "not responding", "closed", "won't open", "wont open", "force close"],
    "boot": ["won't start", "wont start", "boot", "black screen", "no display"],
}

def classify(raw_text: str):
    text = raw_text.lower()

    category = "general"
    for cat, keywords in CATEGORIES.items():
        if any(k in text for k in keywords):
            category = cat
            break

    signals = {
        "mentions_windows": any(w in text for w in ["windows", "pc", "laptop", "desktop"]),
        "mentions_android": any(w in text for w in ["android", "phone", "tablet"]),
        "mentions_ios": any(w in text for w in ["iphone", "ios", "ipad"]),
    }

    return {
        "raw_text": raw_text,
        "category": category,
        "signals": signals,
    }
