"""AI writing operations powered by OpenAI."""

from openai import OpenAI
from app.core.config import get_settings

settings = get_settings()
client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

TONES = {"professional", "casual", "friendly", "formal", "concise", "persuasive"}


def _require_client() -> OpenAI:
    if not client:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    return client


def _chat(system: str, user: str, max_tokens: int = 1000) -> str:
    c = _require_client()
    resp = c.chat.completions.create(
        model=settings.CHAT_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.4,
        max_tokens=max_tokens,
    )
    return (resp.choices[0].message.content or "").strip()


def rewrite(text: str) -> str:
    """Improve clarity and fix grammar while preserving meaning."""
    return _chat(
        "You are an expert editor. Improve the text for clarity, grammar, and flow. "
        "Preserve the original meaning and approximate length. Return only the revised text.",
        text,
    )


def change_tone(text: str, tone: str) -> str:
    """Rewrite text in the requested tone."""
    if tone not in TONES:
        raise ValueError(f"tone must be one of {sorted(TONES)}")
    return _chat(
        f"You are an expert editor. Rewrite the text in a {tone} tone. "
        "Preserve the core meaning. Return only the rewritten text.",
        text,
    )


def draft_email(intent: str, recipient: str | None = None, tone: str = "professional") -> str:
    """Draft an email from intent / bullet points."""
    if tone not in TONES:
        tone = "professional"
    recipient_line = f"Recipient: {recipient}\n" if recipient else ""
    return _chat(
        f"You are an expert email writer. Write a clear {tone} email. "
        "Include a subject line on the first line as 'Subject: ...', then a blank line, then the body. "
        "Do not include placeholders like [Your Name] unless necessary.",
        f"{recipient_line}Intent / notes:\n{intent}",
        max_tokens=800,
    )


def transform(text: str, mode: str) -> str:
    """Expand or shorten text. mode: expand | shorten"""
    if mode == "expand":
        system = (
            "Expand the text with useful detail while staying faithful to the original meaning. "
            "Return only the expanded text."
        )
    elif mode == "shorten":
        system = (
            "Make the text significantly more concise without losing key meaning. "
            "Return only the shortened text."
        )
    else:
        raise ValueError("mode must be 'expand' or 'shorten'")
    return _chat(system, text)
