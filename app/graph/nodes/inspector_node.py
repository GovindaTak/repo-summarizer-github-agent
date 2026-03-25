import re

from app.graph.state import RepoState
from app.providers.github_provider import GitHubProvider
from app.exceptions.app_exception import AppException


def parse_github_url(url: str):
    """
    Extract owner and repo from GitHub URL.
    """

    pattern = r"github\.com/([^/]+)/([^/]+)"
    match = re.search(pattern, url)

    if not match:
        raise AppException("Invalid GitHub repository URL", 400)

    owner, repo = match.group(1), match.group(2).replace(".git", "")

    return owner, repo




async def inspector_node(state: RepoState) -> RepoState:
    """
    Metadata-first inspection of repository.
    """

    github_url = state.get("github_url")

    if not github_url:
        raise AppException("GitHub URL is required", 400)

  
    owner, repo = parse_github_url(github_url)

    file_tree = await GitHubProvider.fetch_repo_tree(owner, repo)

   
    detected_files = GitHubProvider.detect_high_signal_files(file_tree)

  
    directories = GitHubProvider.extract_directories(file_tree)

 
    is_monorepo = GitHubProvider.detect_monorepo(file_tree)

 
    state.update(
        {
            "owner": owner,
            "repo": repo,
            "file_tree": file_tree,
            "detected_files": detected_files,
            "directories": directories,
            "is_monorepo": is_monorepo,
        }
    )

    return state