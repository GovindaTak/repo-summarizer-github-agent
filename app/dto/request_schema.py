from pydantic import BaseModel, HttpUrl


class RepoSummarizeRequest(BaseModel):
    """
    Request schema for repository summarization.
    """

    github_url: HttpUrl