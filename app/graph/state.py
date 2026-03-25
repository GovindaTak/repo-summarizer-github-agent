from typing import TypedDict, List, Dict, Any


class RepoState(TypedDict, total=False):
 
    github_url: str
    owner: str
    repo: str

   
    file_tree: List[str]                 
    detected_files: Dict[str, str]      
    directories: List[str]              
    is_monorepo: bool

 
    score: int
    missing_critical_files: List[str]

  
    fetched_files: Dict[str, str]     
    readme: str                        
    manifest_content: str               

  
    deep_dive_files: Dict[str, str]      

  
    structured_context: Dict[str, Any]


    summary: str
    technologies: List[str]
    structure: str