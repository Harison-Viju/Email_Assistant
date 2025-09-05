from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

NEGATIVE_WORDS = {
    "cannot", "can't", "unable", "blocked", "down", "error", "issue", "urgent",
    "critical", "immediately", "asap", "frustrated", "angry", "charged twice", "refund",
}

POSITIVE_WORDS = {"thanks", "thank you", "appreciate", "great", "awesome", "love"}

URGENT_KEYWORDS = {
    "urgent", "immediately", "critical", "asap", "cannot access", "system is down",
    "blocked", "downtime", "outage", "highly critical",
}


CONTACT_REGEXPS = [
    re.compile(r"\b(?:\+?\d[\d\s\-()]{7,}\d)\b"),  # phone-like
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),  # email
]


@dataclass
class AnalysisResult:
    sentiment: str
    priority: str
    is_urgent: bool
    extracted_contact: Optional[str]
    extracted_requirements: Optional[str]
    extracted_indicators: Optional[str]


def _detect_sentiment(text: str) -> str:
    text_l = text.lower()
    neg = sum(1 for w in NEGATIVE_WORDS if w in text_l)
    pos = sum(1 for w in POSITIVE_WORDS if w in text_l)
    if neg > pos and neg > 0:
        return "negative"
    if pos > neg and pos > 0:
        return "positive"
    return "neutral"


def _detect_priority(subject: str, body: str) -> Tuple[str, bool]:
    text = f"{subject}\n{body}".lower()
    is_urgent = any(keyword in text for keyword in URGENT_KEYWORDS)
    priority = "urgent" if is_urgent else "not_urgent"
    return priority, is_urgent


def _extract_contacts(text: str) -> Optional[str]:
    for rx in CONTACT_REGEXPS:
        m = rx.search(text)
        if m:
            return m.group(0)
    return None


def _extract_requirements(text: str) -> Optional[str]:
    # naive heuristic: capture sentences with verbs like "need", "require", "want", "looking for"
    sentences = re.split(r"(?<=[.!?])\s+", text)
    for s in sentences:
        s_l = s.lower()
        if any(k in s_l for k in ["need", "require", "want", "looking for", "cannot", "unable", "request"]):
            return s.strip()
    return None


def _extract_indicators(text: str) -> Optional[str]:
    indicators: List[str] = []
    text_l = text.lower()
    for w in NEGATIVE_WORDS.union(POSITIVE_WORDS):
        if w in text_l:
            indicators.append(w)
    if not indicators:
        return None
    return ", ".join(sorted(set(indicators)))


def analyze_email(subject: str, body: str) -> AnalysisResult:
    full_text = f"{subject}\n\n{body}"
    sentiment = _detect_sentiment(full_text)
    priority, is_urgent = _detect_priority(subject, body)
    extracted_contact = _extract_contacts(full_text)
    extracted_requirements = _extract_requirements(full_text)
    extracted_indicators = _extract_indicators(full_text)
    return AnalysisResult(
        sentiment=sentiment,
        priority=priority,
        is_urgent=is_urgent,
        extracted_contact=extracted_contact,
        extracted_requirements=extracted_requirements,
        extracted_indicators=extracted_indicators,
    )


