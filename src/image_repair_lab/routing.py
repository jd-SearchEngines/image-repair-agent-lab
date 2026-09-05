ROUTES = {
    "TEXT": "text_repair_local",
    "FACT": "fact_repair_local",
    "LOCAL_DEFECT": "local_inpaint",
    "COMPOSITION": "composition_reframe",
    "BACKGROUND": "background_repair",
    "GLOBAL_FAILURE": "full_regenerate_review",
}


def route(diagnosis: dict) -> dict:
    error_class = diagnosis["error_class"]
    strategy = ROUTES[error_class]
    return {
        "strategy": strategy,
        "scope": "local" if strategy != "full_regenerate_review" else "global",
        "rationale": f"{error_class} -> {strategy}; preserve constraints are explicit",
    }
