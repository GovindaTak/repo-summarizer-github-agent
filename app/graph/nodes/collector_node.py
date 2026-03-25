from app.graph.state import RepoState
from app.providers.github_provider import GitHubProvider


async def collector_node(state: RepoState) -> RepoState:
    """
    Fetch high-signal files when context is sufficient.
    """

    owner = state["owner"]
    repo = state["repo"]
    detected_files = state.get("detected_files", {})

    fetched_files = {}

   
    readme_path = detected_files.get("readme")
    if readme_path:
        content = await GitHubProvider.fetch_file_content(owner, repo, readme_path)
        fetched_files[readme_path] = content
        state["readme"] = content

  
    manifest_path = detected_files.get("manifest")
    if manifest_path:
        content = await GitHubProvider.fetch_file_content(owner, repo, manifest_path)
        fetched_files[manifest_path] = content
        state["manifest_content"] = content

   
    entry_path = detected_files.get("entry_point")
    if entry_path:
        content = await GitHubProvider.fetch_file_content(owner, repo, entry_path)
        fetched_files[entry_path] = content

 
    state["fetched_files"] = fetched_files

    return state