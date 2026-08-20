import pytest

from dk4tool.dialogue.review import validate_natural_dialogue_batch


def batch(english: str, **record_fields: str) -> dict[str, object]:
    return {
        "encoder": "dialogue-fixed-v1",
        "translation_policy": "natural-dialogue-v1",
        "target_locale": "en-US",
        "review_gates": [
            "source",
            "context",
            "localization",
            "naturalness",
            "formatting",
        ],
        "records": [
            {
                "id": "DK4_MES_B44_R0001",
                "english": english,
                "speaker": "Speaker",
                "context": "Opening scene",
                **record_fields,
            }
        ],
    }


def test_natural_dialogue_accepts_formatter_owned_wrapping():
    validate_natural_dialogue_batch(batch("A natural sentence.{PAD}"))


def test_natural_dialogue_requires_us_locale_and_localization_gate():
    missing_locale = batch("A natural sentence.{PAD}")
    missing_locale.pop("target_locale")
    with pytest.raises(ValueError, match="target_locale en-US"):
        validate_natural_dialogue_batch(missing_locale)

    missing_gate = batch("A natural sentence.{PAD}")
    missing_gate["review_gates"] = ["source", "context", "naturalness", "formatting"]
    with pytest.raises(ValueError, match="localization"):
        validate_natural_dialogue_batch(missing_gate)


def test_natural_dialogue_rejects_positioned_breaks():
    with pytest.raises(ValueError, match="positioned wrapping"):
        validate_natural_dialogue_batch(batch("First.{LB@20}Second.{PAD}"))


def test_natural_dialogue_requires_reason_for_explicit_break():
    with pytest.raises(ValueError, match="manual_break_reason"):
        validate_natural_dialogue_batch(batch("First.{LB}Second.{PAD}"))


def test_natural_dialogue_allows_documented_dramatic_break():
    validate_natural_dialogue_batch(
        batch("Wait...{LB}What was that?{PAD}", manual_break_reason="Dramatic pause")
    )


def test_natural_dialogue_rejects_diagnostic_placeholder():
    with pytest.raises(ValueError, match="placeholder"):
        validate_natural_dialogue_batch(batch("38 cells: 1234567890{PAD}"))


def test_v2_requires_per_record_localization_evidence():
    value = batch("A natural sentence.{PAD}")
    value["translation_policy"] = "natural-dialogue-v2"
    with pytest.raises(ValueError, match="source_meaning"):
        validate_natural_dialogue_batch(value)

    record = value["records"][0]
    record["source_meaning"] = "A faithful literal gloss."
    record["localization_note"] = "Natural American phrasing; no factual changes."
    record["review"] = {
        "source": True,
        "context": True,
        "localization": True,
        "naturalness": True,
        "formatting": True,
    }
    validate_natural_dialogue_batch(value)


def test_natural_dialogue_requires_padding_marker():
    with pytest.raises(ValueError, match="must end with"):
        validate_natural_dialogue_batch(batch("A natural sentence."))


def test_relocatable_natural_dialogue_owns_no_fixed_padding() -> None:
    value = batch("A complete sentence without padding.")
    value["encoder"] = "dialogue-relocatable-v1"
    validate_natural_dialogue_batch(value)

    value["records"][0]["english"] += "{PAD}"
    with pytest.raises(ValueError, match="must not contain"):
        validate_natural_dialogue_batch(value)
