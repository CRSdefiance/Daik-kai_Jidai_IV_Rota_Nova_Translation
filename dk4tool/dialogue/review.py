from __future__ import annotations

import re

NATURAL_DIALOGUE_POLICY = "natural-dialogue-v1"
NATURAL_DIALOGUE_POLICY_V2 = "natural-dialogue-v2"
REQUIRED_REVIEW_GATES = {
    "source",
    "context",
    "localization",
    "naturalness",
    "formatting",
}
FORBIDDEN_DRAFT_PATTERNS = (
    re.compile(r"\bsee below\b", re.IGNORECASE),
    re.compile(r"\b\d+\s+(?:cells?|shared)\b", re.IGNORECASE),
    re.compile(r"1234567890"),
)


def validate_natural_dialogue_batch(batch: dict[str, object]) -> None:
    """Reject dialogue batches that bypass the editorial/formatting workflow."""

    policy = batch.get("translation_policy")
    if policy not in {NATURAL_DIALOGUE_POLICY, NATURAL_DIALOGUE_POLICY_V2}:
        return
    encoder = batch.get("encoder")
    if encoder not in {"dialogue-fixed-v1", "dialogue-relocatable-v1"}:
        raise ValueError(
            "natural-dialogue-v1 requires a supported dialogue encoder"
        )
    if batch.get("target_locale") != "en-US":
        raise ValueError("natural-dialogue-v1 requires target_locale en-US")
    gates = batch.get("review_gates")
    if not isinstance(gates, list) or not REQUIRED_REVIEW_GATES.issubset(
        {str(value) for value in gates}
    ):
        raise ValueError(
            "natural-dialogue-v1 requires source, context, localization, "
            "naturalness, and formatting gates"
        )
    records = batch.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError("natural-dialogue-v1 batch has no records")
    for record in records:
        if not isinstance(record, dict):
            raise TypeError("natural-dialogue-v1 record must be an object")
        row_id = str(record.get("id", "<unknown>"))
        english = str(record.get("english", ""))
        if encoder == "dialogue-fixed-v1" and not english.endswith("{PAD}"):
            raise ValueError(f"{row_id}: fixed natural dialogue must end with {{PAD}}")
        if encoder == "dialogue-relocatable-v1" and "{PAD}" in english:
            raise ValueError(
                f"{row_id}: relocatable natural dialogue must not contain {{PAD}}"
            )
        if not str(record.get("speaker", "")).strip():
            raise ValueError(f"{row_id}: natural dialogue requires a mapped speaker")
        if not str(record.get("context", "")).strip():
            raise ValueError(f"{row_id}: natural dialogue requires contextual notes")
        if "{LB@" in english or "{ALIGN@" in english:
            raise ValueError(f"{row_id}: manual byte-positioned wrapping is forbidden")
        manual_breaks = english.count("{LB}")
        if manual_breaks and not str(record.get("manual_break_reason", "")).strip():
            raise ValueError(
                f"{row_id}: explicit line breaks require manual_break_reason; "
                "ordinary wrapping belongs to the formatter"
            )
        for pattern in FORBIDDEN_DRAFT_PATTERNS:
            if pattern.search(english):
                raise ValueError(f"{row_id}: draft or diagnostic placeholder text is forbidden")
        if policy == NATURAL_DIALOGUE_POLICY_V2:
            if not str(record.get("source_meaning", "")).strip():
                raise ValueError(f"{row_id}: v2 requires a faithful source_meaning gloss")
            if not str(record.get("localization_note", "")).strip():
                raise ValueError(f"{row_id}: v2 requires a localization_note")
            review = record.get("review")
            if not isinstance(review, dict) or not all(
                review.get(gate) is True for gate in REQUIRED_REVIEW_GATES
            ):
                raise ValueError(
                    f"{row_id}: v2 requires per-record source, context, localization, "
                    "naturalness, and formatting review"
                )
            if english.startswith((" ", "{LB}")) or "{LB}{LB}" in english:
                raise ValueError(
                    f"{row_id}: v2 forbids leading/consecutive layout breaks"
                )
