CASES = []

def store_case(problem, diagnosis, solution, autofix):
    CASES.append({
        "problem": problem,
        "diagnosis": diagnosis,
        "solution": solution,
        "autofix": autofix,
    })
    if len(CASES) > 1000:
        CASES.pop(0)

def recent_cases(n=5):
    return CASES[-n:]
