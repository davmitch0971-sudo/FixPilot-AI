# solution_ai_logging.py

def log(session: dict, message: str):
    session.setdefault("logs", []).append(message)
