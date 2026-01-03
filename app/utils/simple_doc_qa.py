import re

def answer_from_document(
    document_text: str,
    question: str,
    context_lines: int = 3
) -> str | None:
    """
    Deterministic document QA with multi-line answers
    and highlighted matched keywords.
    """

    question = question.lower()

    KEYWORD_MAP = {
        "name": ["name"],
        "experience": ["experience", "years"],
        "email": ["email", "mail"],
        "phone": ["phone", "mobile", "contact"],
        "address": ["address", "location"],
        "skills": ["skills", "technologies"],
        "education": ["education", "degree"],
        "leave": ["leave", "vacation"],
        "policy": ["policy", "rules"]
    }

    matched_keywords = set()

    for variants in KEYWORD_MAP.values():
        for v in variants:
            if v in question:
                matched_keywords.add(v)

    if not matched_keywords:
        return None

    lines = [line.strip() for line in document_text.splitlines() if line.strip()]

    for i, line in enumerate(lines):
        if any(kw in line for kw in matched_keywords):
            start = max(i - 1, 0)
            end = min(i + context_lines + 1, len(lines))

            section = lines[start:end]
            highlighted_section = []

            for sec_line in section:
                for kw in matched_keywords:
                    # Highlight keyword (case-insensitive)
                    sec_line = re.sub(
                        rf"\b({kw})\b",
                        r"**\1**",
                        sec_line,
                        flags=re.IGNORECASE
                    )
                highlighted_section.append(sec_line)

            return "\n".join(highlighted_section)

    return None
