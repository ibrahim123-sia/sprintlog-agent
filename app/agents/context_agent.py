from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.config import settings

llm = ChatGoogleGenerativeAI(
    google_api_key=settings.gemini_api_key,
    model="gemini-2.5-flash"
)

context_prompt = ChatPromptTemplate.from_template("""You are analyzing a developer's raw git activity for today.

Raw data:
{raw_text}

For each meaningful change, write ONE plain-language line describing what was
actually done (not just repeating the commit message — look at the diff to
understand the real change). Ignore trivial changes like formatting-only commits.
Output as a plain bullet list, nothing else.""")

context_chain = context_prompt | llm


def analyze_context(activity: dict) -> str:
    """Reads raw commits + diffs and explains what actually happened, in plain language."""

    raw_text = ""
    for repo, commits in activity["repos"].items():
        raw_text += f"\n--- Repo: {repo} ---\n"
        for c in commits:
            raw_text += f"Commit message: {c['message']}\nDiff:\n{c['diff']}\n\n"

    result = context_chain.invoke({"raw_text": raw_text})
    return result.content