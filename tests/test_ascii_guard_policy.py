from __future__ import annotations

from pathlib import Path

import pytest

from scripts.build_integrated_release import validate_ascii_guard_policy


def _batch(replacement: bytes, offsets: list[int] | None = None) -> dict[str, object]:
    return {
        "format": "dk4-ilnk-translation-batch-v1",
        "content_type": "ilnk-fixed-source-translation-v1",
        "target_locale": "en-US",
        "ascii_guard_policy": "two-byte-entry-and-line-v1",
        "records": [
            {
                "id": "TEST",
                "replacement_hex": replacement.hex(),
                "entry_offsets": [0] if offsets is None else offsets,
            }
        ],
    }


def test_two_byte_guard_policy_accepts_entries_and_continuations() -> None:
    validate_ascii_guard_policy(
        Path("valid.json"),
        _batch(b"  First\n  Second      "),
    )


@pytest.mark.parametrize(
    ("replacement", "message"),
    [
        (b" One-space entry", "entry at byte 0"),
        (b"  First\n Second", "continuation guard"),
    ],
)
def test_two_byte_guard_policy_rejects_one_space_failures(
    replacement: bytes, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        validate_ascii_guard_policy(Path("unsafe.json"), _batch(replacement))


def test_fixed_source_batches_cannot_omit_the_policy() -> None:
    batch = _batch(b"  Safe")
    del batch["ascii_guard_policy"]
    with pytest.raises(ValueError, match="requires ascii_guard_policy"):
        validate_ascii_guard_policy(Path("missing.json"), batch)


def test_raw_english_batches_must_opt_in_or_document_an_exemption() -> None:
    batch = _batch(b"  Safe")
    del batch["content_type"]
    del batch["ascii_guard_policy"]
    with pytest.raises(ValueError, match="documented ascii_guard_exemption"):
        validate_ascii_guard_policy(Path("future.json"), batch)

    batch["ascii_guard_exemption"] = "Non-dialogue binary layout; reviewed separately."
    validate_ascii_guard_policy(Path("exempt.json"), batch)


def test_packed_entry_offsets_are_independently_checked() -> None:
    with pytest.raises(ValueError, match="entry at byte 8"):
        validate_ascii_guard_policy(
            Path("packed.json"),
            _batch(b"  First One-space", offsets=[0, 8]),
        )


def test_runtime_proven_record_can_preserve_source_indentation() -> None:
    batch = _batch(b"  First  Second", offsets=[0, 7])
    batch["records"][0]["ascii_guard_exemption"] = (
        "Runtime screenshot proves that this renderer displays source indentation."
    )
    validate_ascii_guard_policy(Path("source-layout.json"), batch)
