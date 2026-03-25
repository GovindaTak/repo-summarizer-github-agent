from app.graph.state import RepoState
from app.llm.model_factory import get_llm
from app.exceptions.app_exception import AppException
from app.dto.llm_response_schema import RepoAnalysisResponse


SYSTEM_PROMPT = """
You are an expert software analyst.

Analyze the repository context and produce:
- A concise summary
- The main technologies used
- The overall project structure
"""


async def summarize_node(state: RepoState) -> RepoState:
    """
    Final synthesis using structured LLM output.
    """

    context = state.get("structured_context")

    if not context:
        raise AppException("No context available for summarization", 500)

    llm = get_llm()

    
    structured_llm = llm.with_structured_output(RepoAnalysisResponse)

    prompt = f"""
Repository Context:
{context}
"""

    try:
     
        result: RepoAnalysisResponse = await structured_llm.ainvoke(
            [
                ("system", SYSTEM_PROMPT),
                ("human", prompt),
            ]
        )

    except Exception:
        raise AppException("LLM summarization failed", 500)

    state.update(
        {
            "summary": result.summary,
            "technologies": result.technologies,
            "structure": result.structure,
        }
    )

    return state