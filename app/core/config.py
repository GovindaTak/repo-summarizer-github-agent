from pydantic_settings import BaseSettings


class Settings(BaseSettings):

  
    LLM_PROVIDER: str = "azure_openai"

    NVIDIA_API_KEY: str = ""
    NVIDIA_MODEL: str = "meta/llama-3.1-70b-instruct"
    NVIDIA_BASE_URL: str = "https://integrate.api.nvidia.com/v1"

   
    AZURE_API_KEY: str = ""
    AZURE_ENDPOINT: str = ""
    AZURE_MODEL: str = ""
    AZURE_API_VERSION: str = "2024-02-15-preview"
    AZURE_DEPLOYMENT_NAME: str=""

  
    LLM_TEMPERATURE: float = 0.2
    GITHUB_TOKEN:str=""

    class Config:
        env_file = ".env"


settings = Settings()