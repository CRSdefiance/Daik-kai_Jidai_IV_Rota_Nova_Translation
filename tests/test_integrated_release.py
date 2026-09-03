import hashlib
import json
from pathlib import Path

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from scripts.build_integrated_release import (
    accepted_batch_paths,
    apply_arm9_fixed_batch,
    apply_arm9_fixed_batches,
    changed_segments,
    load_release_stack,
    resolve_release_batches,
    validate_natural_dialogue_qa,
    validate_playable_dialogue_header,
    validate_unchanged_segments,
)


def container(*blocks: bytes) -> bytes:
    return IlnkContainer(list(blocks)).to_bytes()


def test_changed_segments_reports_only_modified_record():
    before = container(b"one\0two\0three", b"four\0five")
    after = container(b"one\0TWO\0three", b"four\0five")

    assert changed_segments(before, after) == {(0, 1)}


def test_changed_segments_accepts_byte_identical_container():
    data = container(b"one\0two", b"three")

    assert changed_segments(data, data) == set()


def test_changed_segments_rejects_record_count_change():
    before = container(b"one\0two")
    after = container(b"one\0two\0three")

    with pytest.raises(ValueError, match="segment count changed"):
        changed_segments(before, after)


def test_reviewed_noop_segments_require_exact_declarations():
    expected = {(1, 2), (1, 3)}
    actual = {(1, 2)}

    assert validate_unchanged_segments(
        "/data/test", expected, actual, {(1, 3)}
    ) == {(1, 3)}
    with pytest.raises(ValueError, match="without an explicit declaration"):
        validate_unchanged_segments("/data/test", expected, actual, set())
    with pytest.raises(ValueError, match="declared unchanged actually changed"):
        validate_unchanged_segments(
            "/data/test", expected, actual, {(1, 2), (1, 3)}
        )


def test_arm9_fixed_batch_replaces_only_verified_slot(tmp_path):
    source = b"before\0next"
    batch = tmp_path / "arm9.json"
    batch.write_text(
        json.dumps(
            {
                "format": "dk4-arm9-fixed-text-batch-v1",
                "source_file_sha256": hashlib.sha256(source).hexdigest(),
                "records": [
                    {
                        "id": "TEST_LABEL",
                        "offset": 0,
                        "source_hex": b"before".hex(),
                        "english": "after",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    rebuilt, record_ids = apply_arm9_fixed_batch(batch, source)

    assert rebuilt == b"after\0\0next"
    assert record_ids == ["TEST_LABEL"]


def test_arm9_fixed_batches_share_one_pristine_source_lock(tmp_path):
    source = b"abcdefgh"
    digest = hashlib.sha256(source).hexdigest()
    paths = []
    for name, offset, old, new in (
        ("one", 0, b"ab", b"AB"),
        ("two", 4, b"ef", b"EF"),
    ):
        path = tmp_path / f"{name}.json"
        path.write_text(
            json.dumps(
                {
                    "format": "dk4-arm9-fixed-text-batch-v1",
                    "source_file_sha256": digest,
                    "records": [
                        {
                            "id": name,
                            "offset": offset,
                            "source_hex": old.hex(),
                            "replacement_hex": new.hex(),
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        paths.append(path)

    rebuilt, record_ids = apply_arm9_fixed_batches(paths, source)

    assert rebuilt == b"ABcdEFgh"
    assert record_ids == ["one", "two"]


def test_arm9_fixed_batches_reject_cross_batch_overlap(tmp_path):
    source = b"abcdefgh"
    digest = hashlib.sha256(source).hexdigest()
    paths = []
    for name, offset in (("one", 1), ("two", 2)):
        path = tmp_path / f"{name}.json"
        path.write_text(
            json.dumps(
                {
                    "format": "dk4-arm9-fixed-text-batch-v1",
                    "source_file_sha256": digest,
                    "records": [
                        {
                            "id": name,
                            "offset": offset,
                            "source_hex": source[offset : offset + 2].hex(),
                            "replacement_hex": b"XX".hex(),
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        paths.append(path)

    with pytest.raises(ValueError, match="overlaps"):
        apply_arm9_fixed_batches(paths, source)


def test_inline_code_batch_requires_exact_runtime_mapping(tmp_path):
    source = b"abcdefgh"
    batch = tmp_path / "inline.json"
    batch.write_text(
        json.dumps(
            {
                "format": "dk4-arm9-fixed-text-batch-v1",
                "content_type": "arm9-inline-code-v1",
                "source_file_sha256": hashlib.sha256(source).hexdigest(),
                "records": [
                    {
                        "id": "inline",
                        "offset": 2,
                        "runtime_address": 0x02000003,
                        "source_hex": b"cd".hex(),
                        "replacement_hex": b"CD".hex(),
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="runtime address does not match"):
        apply_arm9_fixed_batch(batch, source)


def test_inline_code_batch_rejects_prohibited_runtime_data_tail(tmp_path):
    offset = 0x171E48
    source = b"\0" * offset + b"abcd"
    batch = tmp_path / "inline.json"
    batch.write_text(
        json.dumps(
            {
                "format": "dk4-arm9-fixed-text-batch-v1",
                "content_type": "arm9-inline-code-v1",
                "source_file_sha256": hashlib.sha256(source).hexdigest(),
                "records": [
                    {
                        "id": "unsafe-inline",
                        "offset": offset,
                        "runtime_address": 0x02171E48,
                        "source_hex": b"abcd".hex(),
                        "replacement_hex": b"ABCD".hex(),
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="prohibited runtime-owned ARM9 data tail"):
        apply_arm9_fixed_batch(batch, source)


def test_accepted_layers_are_baked_into_promoted_baseline():
    stack = load_release_stack()
    batches = resolve_release_batches(None, [])

    assert batches == accepted_batch_paths(stack) == []
    assert all(
        layer["baked_into_baseline"] is True for layer in stack["accepted_layers"]
    )


def test_sound_profile_is_rebased_onto_promoted_baseline():
    with pytest.raises(ValueError, match="accepted-baked"):
        resolve_release_batches("sound-setup", [])


def test_revoked_relocation_profile_cannot_be_built():
    with pytest.raises(ValueError, match="profile is revoked"):
        resolve_release_batches("raphael-b44-long-dialogue-poc", [])


def test_natural_dialogue_probe_uses_live_safe_raphael_profile():
    stack = load_release_stack()
    profile = stack["profiles"]["natural-dialogue-probe"]

    for relative_path in profile["batches"]:
        batch = json.loads(Path(relative_path).read_text(encoding="utf-8"))
        assert batch["dialogue_profile"] == "raphael-story-live"


def test_full_raphael_profile_keeps_renderer_and_v2_batches_together():
    stack = load_release_stack()
    paths = [
        Path(value)
        for value in stack["profiles"]["raphael-full-natural-v2"]["batches"]
    ]

    assert paths[0] == Path("translations/dialogue_pair_phase_arm9.json")
    assert set(paths[1:]) == {
        Path("translations/raphael_natural_v2_b43_b44.json"),
        Path("translations/raphael_natural_v2_b45_b48.json"),
        Path("translations/raphael_natural_v2_b137_b141.json"),
    }
    for path in paths[1:]:
        batch = json.loads(path.read_text(encoding="utf-8"))
        assert batch["translation_policy"] == "natural-dialogue-v2"
        assert batch["dialogue_profile"] == "raphael-story-live"


def test_full_raphael_parity_profile_keeps_relocation_and_v2_batches_together():
    stack = load_release_stack()
    batches = [
        Path(value)
        for value in stack["profiles"][
            "raphael-full-natural-v2-parity-opening"
        ]["batches"]
    ]
    assert batches == [
        Path("translations/dialogue_pair_phase_arm9.json"),
        Path("translations/raphael_b44_long_dialogue_parity_poc.json"),
        Path("translations/raphael_natural_v2_b43_b44.json"),
        Path("translations/raphael_natural_v2_b45_b48.json"),
        Path("translations/raphael_natural_v2_b137_b141.json"),
    ]


def test_playable_builder_rejects_bare_newline_story_profile():
    with pytest.raises(ValueError, match="live-safe guarded profile"):
        validate_playable_dialogue_header(
            Path("translations/bad.json"),
            {
                "encoder": "dialogue-fixed-v1",
                "file_path": "/data/SC0.DK4",
                "dialogue_profile": "story-clean-revoked",
            },
        )


def test_playable_builder_rejects_unwaived_natural_dialogue_warning(monkeypatch):
    header = {
        "translation_policy": "natural-dialogue-v1",
        "dialogue_profile": "raphael-story-live",
        "records": [{"id": "TEST", "english": "Test{PAD}"}],
    }
    monkeypatch.setattr(
        "scripts.build_integrated_release.materialize_translation_batch",
        lambda batch, source: [
            {"id": "TEST", "source_hex": "00", "english": "Test{PAD}"}
        ],
    )
    monkeypatch.setattr(
        "scripts.build_integrated_release.audit_fixed_dialogue_record",
        lambda source, english, profile: {
            "issues": [{"severity": "warning", "code": "orphan-final-line"}]
        },
    )

    with pytest.raises(ValueError, match="TEST:warning:orphan-final-line"):
        validate_natural_dialogue_qa(Path("translations/test.json"), header, b"source")


def test_playable_builder_accepts_explicit_warning_waiver(monkeypatch):
    header = {
        "translation_policy": "natural-dialogue-v1",
        "dialogue_profile": "raphael-story-live",
        "records": [
            {
                "id": "TEST",
                "english": "Test{PAD}",
                "qa_waivers": ["orphan-final-line"],
                "qa_waiver_reason": "Intentional terse response.",
            }
        ],
    }
    monkeypatch.setattr(
        "scripts.build_integrated_release.materialize_translation_batch",
        lambda batch, source: [
            {"id": "TEST", "source_hex": "00", "english": "Test{PAD}"}
        ],
    )
    monkeypatch.setattr(
        "scripts.build_integrated_release.audit_fixed_dialogue_record",
        lambda source, english, profile: {
            "issues": [{"severity": "warning", "code": "orphan-final-line"}]
        },
    )

    validate_natural_dialogue_qa(Path("translations/test.json"), header, b"source")


def test_playable_builder_rejects_undocumented_warning_waiver(monkeypatch):
    header = {
        "translation_policy": "natural-dialogue-v1",
        "dialogue_profile": "raphael-story-live",
        "records": [
            {
                "id": "TEST",
                "english": "Test{PAD}",
                "qa_waivers": ["orphan-final-line"],
            }
        ],
    }
    monkeypatch.setattr(
        "scripts.build_integrated_release.materialize_translation_batch",
        lambda batch, source: [
            {"id": "TEST", "source_hex": "00", "english": "Test{PAD}"}
        ],
    )
    monkeypatch.setattr(
        "scripts.build_integrated_release.audit_fixed_dialogue_record",
        lambda source, english, profile: {"issues": []},
    )

    with pytest.raises(ValueError, match="undocumented-qa-waiver"):
        validate_natural_dialogue_qa(Path("translations/test.json"), header, b"source")


def test_release_batches_deduplicate_explicit_required_layer():
    stack = {
        "accepted_layers": [],
        "profiles": {
            "feature": {
                "status": "experimental",
                "batches": ["translations/feature.json"],
            }
        },
    }
    batches = resolve_release_batches(
        "feature", [Path("translations/feature.json")], stack
    )
    assert batches == [Path("translations/feature.json")]


def test_registered_feature_batch_requires_its_profile():
    with pytest.raises(ValueError, match="select the matching --profile"):
        resolve_release_batches(
            None, [Path("translations/sound_selector_arm9.json")]
        )


def test_unregistered_batch_is_rejected_from_playable_build():
    with pytest.raises(ValueError, match="not registered in a release profile"):
        resolve_release_batches(None, [Path("translations/new_work.json")])
