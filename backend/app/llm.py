from __future__ import annotations

from typing import List

from .config import OPENAI_API_KEY, MODEL_NAME
from .retrieval import get_kb


LLM_SYSTEM_PROMPT = (
    "You are a professional, empathetic customer support assistant. "
    "Write concise, friendly replies that acknowledge user sentiment, "
    "address the specific request, and outline next steps. If the tone is "
    "frustrated or urgent, apologize and reassure. Use provided context."
)


def build_prompt(subject: str, body: str, sentiment: str, priority: str) -> str:
    kb = get_kb()
    search_text = f"Subject: {subject}\nBody: {body}"
    ctx = kb.search(search_text, top_k=5)
    ctx_texts: List[str] = [p for p, _ in ctx.passages][:3]
    context_block = "\n\n".join(ctx_texts) if ctx_texts else ""
    prompt = (
        f"System:\n{LLM_SYSTEM_PROMPT}\n\n"
        f"Email:\nSubject: {subject}\nBody: {body}\nSentiment: {sentiment}\nPriority: {priority}\n\n"
        f"Knowledge Context (may include similar past tickets):\n{context_block}\n\n"
        "Task: Draft a reply. Maintain empathy and professionalism. Include any steps or links if helpful."
    )
    return prompt


def generate_draft(subject: str, body: str, sentiment: str, priority: str) -> str:
    # Use OpenAI if API key available; otherwise return a simple heuristic draft
    if OPENAI_API_KEY:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=OPENAI_API_KEY)
            prompt = build_prompt(subject, body, sentiment, priority)
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": LLM_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
            )
            return completion.choices[0].message.content.strip()
        except Exception:
            pass

    # Fallback heuristic draft
    opening = "I'm sorry to hear about the trouble" if sentiment == "negative" else "Thanks for reaching out"
    urgency = " We understand this is urgent and we're prioritizing it." if priority == "urgent" else ""
    return (
        f"Hi there,\n\n{opening}.{urgency} "
        f"Here are the next steps we recommend based on your message: \n"
        f"- We'll investigate the issue and get back to you shortly.\n"
        f"- If possible, please share any additional details (screenshots, error messages).\n\n"
        f"Best regards,\nSupport Team"
    )


