def format_response(problem, diagnosis, solution, autofix):
    lines = []
    lines.append("Here’s what I found:\n")
    lines.append(f"Problem category: {problem['category']}")
    lines.append(f"Likely cause: {diagnosis['root_cause']} (confidence {diagnosis['confidence']:.2f})\n")

    lines.append("Recommended steps:")
    for i, step in enumerate(solution["steps"], 1):
        lines.append(f"{i}. {step}")

    if autofix:
        lines.append(f"\nAuto-fix status: {autofix['status']}")

    return "\n".join(lines)
