import base64
from typing import Dict, List

from app.utils.util import AIRAGUtils
from app.exceptions.app_exception import AppException


class GitHubProvider:
    BASE_API = "https://api.github.com"

   
    @staticmethod
    async def fetch_repo_tree(owner: str, repo: str) -> List[str]:
        """
        Returns list of all file paths in repo (recursive).
        """

        endpoint = f"{GitHubProvider.BASE_API}/repos/{owner}/{repo}/git/trees/HEAD"

        data = await AIRAGUtils.send_request(
            endpoint=endpoint,
            query_params={"recursive": "1"},
        )

        tree = data.get("tree", [])

        if not tree:
            raise AppException("Repository appears to be empty", 404)

        return [item["path"] for item in tree if item["type"] == "blob"]


    @staticmethod
    def detect_high_signal_files(file_tree: List[str]) -> Dict[str, str]:
        """
        Identify important files for summarization.
        """

        detected = {}

        for path in file_tree:
            name = path.lower()

            if "readme.md" in name:
                detected["readme"] = path

            elif name.endswith(("requirements.txt", "pyproject.toml", "package.json", "go.mod", "cargo.toml")):
                detected["manifest"] = path

            elif name.endswith(("main.py", "app.py", "index.js", "server.js")):
                detected["entry_point"] = path

        return detected

   
    @staticmethod
    def extract_directories(file_tree: List[str]) -> List[str]:
        dirs = set()

        for path in file_tree:
            parts = path.split("/")
            if len(parts) > 1:
                dirs.add(parts[0])

        return list(dirs)

  
    @staticmethod
    def detect_monorepo(file_tree: List[str]) -> bool:
        """
        Simple heuristic: many top-level manifests.
        """

        manifest_count = sum(
            1
            for path in file_tree
            if path.lower().endswith(("package.json", "requirements.txt", "pyproject.toml"))
        )

        return manifest_count > 1

    @staticmethod
    async def fetch_file_content(owner: str, repo: str, path: str) -> str:
        """
        Returns decoded file content from GitHub.
        """

        endpoint = f"{GitHubProvider.BASE_API}/repos/{owner}/{repo}/contents/{path}"

        data = await AIRAGUtils.send_request(endpoint=endpoint)

        content_b64 = data.get("content")

        if not content_b64:
            return ""

        return base64.b64decode(content_b64).decode("utf-8", errors="ignore")
    
      
    @staticmethod
    async def fetch_top_level_files(owner: str, repo: str):
        """
        Returns list of top-level files and directories.
        """

        endpoint = f"{GitHubProvider.BASE_API}/repos/{owner}/{repo}/contents"

        return await AIRAGUtils.send_request(endpoint=endpoint)