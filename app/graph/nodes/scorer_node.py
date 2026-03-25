from app.graph.state import RepoState




def contains_docs_directory(directories):
    """
    Check for documentation-like folders.
    """

    keywords = ("docs", "doc", "examples", "example", "samples")

    return any(d.lower().startswith(keywords) for d in directories)




async def scorer_node(state: RepoState) -> RepoState:
    """
    Deterministic heuristic scoring to evaluate context sufficiency.
    """

    detected_files = state.get("detected_files", {})
    directories = state.get("directories", [])
    file_tree = state.get("file_tree", [])

    score = 0
    missing = []

   
    if "readme" in detected_files:
        score += 40
    else:
        missing.append("readme")

  
    if "manifest" in detected_files:
        score += 25
    else:
        missing.append("manifest")

  
    if "entry_point" in detected_files:
        score += 10


    if contains_docs_directory(directories):
        score += 5

   
    if file_tree:
        score += 20


    state.update(
        {
            "score": score,
            "missing_critical_files": missing,
        }
    )

    return state