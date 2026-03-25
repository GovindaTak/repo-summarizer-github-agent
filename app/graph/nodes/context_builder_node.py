from app.graph.state import RepoState


# -------- Helper --------

def truncate(text: str, limit: int = 8000) -> str:
    """
    Prevent huge context from exceeding limits.
    """

    if not text:
        return ""

    return text[:limit]


# -------- Context Builder Node --------

async def context_builder_node(state: RepoState) -> RepoState:
    """
    Build structured context for the LLM.
    """

    structured_context = {}


    if state.get("readme"):
        structured_context["project_readme"] = truncate(state["readme"])

  
    if state.get("manifest_content"):
        structured_context["dependencies"] = truncate(
            state["manifest_content"], 4000
        )

    fetched_files = state.get("fetched_files", {})

    if fetched_files:
        structured_context["key_files"] = {
            path: truncate(content, 3000)
            for path, content in fetched_files.items()
        }


    deep_files = state.get("deep_dive_files", {})

    if deep_files:
        structured_context["deep_dive_files"] = {
            path: truncate(content, 3000)
            for path, content in deep_files.items()
        }


    structured_context["directories"] = state.get("directories", [])
    structured_context["is_monorepo"] = state.get("is_monorepo", False)


    state["structured_context"] = structured_context

    return state