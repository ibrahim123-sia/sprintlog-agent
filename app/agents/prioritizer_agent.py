from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.config import settings

llm = ChatGoogleGenerativeAI(
    google_api_key=settings.gemini_api_key,
    model="gemini-flash-latest"
)

prioritizer_prompt = ChatPromptTemplate.from_template("""Here is a list of today's development changes:

{context_summary}

Reorder and group these into:
1. High-impact work (features, fixes, anything user-facing or architecturally important)
2. Minor/maintenance work (small tweaks, cleanup, config changes)

Drop anything truly trivial. Output as two short labeled bullet lists.""")

prioritizer_chain = prioritizer_prompt | llm


def prioritize(context_summary: str) -> str:
    """Ranks the day's changes by what a PM actually cares about."""
    result = prioritizer_chain.invoke({"context_summary": context_summary})
    return result.content