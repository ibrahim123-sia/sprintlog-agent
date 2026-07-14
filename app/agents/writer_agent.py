from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.config import settings

llm = ChatGoogleGenerativeAI(
    google_api_key=settings.gemini_api_key,
    model="gemini-2.5-flash"
)

TONE_GUIDES = {
    "professional": "Formal, concise, business-appropriate tone.",
    "casual": "Friendly, relaxed tone, like messaging a teammate.",
    "concise": "Extremely brief, bullet points only, no filler sentences."
}

writer_prompt = ChatPromptTemplate.from_template("""Convert this prioritized work list into 2-5 concise bullet points
for a professional EOD report. {tone_instruction}

Rules:
- Write for a non-technical project manager audience
- Describe the outcome/feature delivered, not the technical implementation
- No file names, function names, or code-level details
- Example style: "Added SMS-capability validation to the alert sender"
  NOT "Modified alert_sender.py to check SMS field in RingCentral response"
- Output ONLY the bullet points, one per line, no greeting, no sign-off, no extra commentary

Work list:
{prioritized_text}""")

writer_chain = writer_prompt | llm


def write_summary(prioritized_text: str, tone: str = "professional") -> str:
    """Turns the prioritized list into email-ready prose in the user's chosen tone."""
    tone_instruction = TONE_GUIDES.get(tone, TONE_GUIDES["professional"])
    result = writer_chain.invoke({
        "tone_instruction": tone_instruction,
        "prioritized_text": prioritized_text
    })
    return result.content