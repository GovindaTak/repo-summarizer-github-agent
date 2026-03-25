from app.graph.state import RepoState
from app.providers.github_provider import GitHubProvider




def is_high_signal_file(name: str) -> bool:
    """
    Determine if file is useful for understanding project.
    """

    name = name.lower()

    return name.endswith(
        (
            ".md",
            ".txt",
            ".py",
            ".js",
            ".ts",
            ".java",
            ".go",
            ".rs",
            ".json",
            ".toml",
            ".yaml",
            ".yml",
        )
    )




async def deep_dive_node(state: RepoState) -> RepoState:
    """
    Fallback retrieval when initial signals are insufficient.
    """

    owner = state["owner"]
    repo = state["repo"]

    deep_files = {}

   
    contents = await GitHubProvider.fetch_top_level_files(owner, repo)

    for item in contents:
        if item.get("type") != "file":
            continue

        name = item.get("name", "")

        if not is_high_signal_file(name):
            continue

        path = item.get("path")


        content = await GitHubProvider.fetch_file_content(owner, repo, path)

       
        deep_files[path] = content[:5000]

  
    state["deep_dive_files"] = deep_files

    return state